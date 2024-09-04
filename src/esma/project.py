from . import utils
from . import reads
from . import generate
from . import compute
from . import kpoints
from . import plots
from . import structure
from . import export
from . import checks
import numpy as np 

class project:
    def __init__(self,project_id,config=False):
        self.project_id = project_id
        self.config = utils.configure(config)
        self.atom = False
        self.lattice = False
        self.calculation=False
        self.job_id = 'results'
        self.path = False
        self.poscar= False
        self.debug = False
        self.magnetism=False
        self.gpu = False
        self.num_core=1

    def set_cores(self,value):
        self.num_core=value

    def energy(self):
        return utils.get_total_energy(self)
    
    def from_poscar(self,directory=False):
        if directory==False:
            self.poscar=f'./Structures/{self.project_id}.poscar'
            lattice, atom = reads.read_poscar(self.poscar)
        else:
            self.poscar=directory
            lattice, atom = reads.read_poscar(directory)
        self.config['pw']['atomic_positions'] = atom
        self.config['pw']['cell_parameters'] = lattice
    
    def from_json(self,data=False,path=False):
        lattice, atom = reads.read_json(data=data,path=path)
        self.config['pw']['atomic_positions'] = atom
        self.config['pw']['cell_parameters'] = lattice
    
    def set_calculation(self,calculation_type):
        self.calculation = calculation_type
        if calculation_type in ['vc-relax','relax','scf','nscf','bands']:
            self.package='pw'
        elif calculation_type == 'bands-pp':
            self.package='bands'
        elif calculation_type in ['pdos','kdos']:
            self.package='projwfc'
        elif calculation_type == 'wannier90':
            self.package='wannier90'
        elif calculation_type =='pw2wannier90':
            self.package='pw2wannier90'
        else:
            self.package=calculation_type

        self.file_path = f"./Projects/{self.project_id}/{self.job_id}/{self.calculation}.in"

    def hubbard(self,atom,orbital,value,interaction='U',projection="atomic"):
        self.config['pw']['hubbard']['projection']=projection
        self.config['pw']['hubbard']['terms'].append({"interaction":interaction,'atom':atom,'orbital':orbital,'value':value})
    

    def set_pseudo(self,pseudo_type=False,path=False):
        if path is not False:
            self.config['pw']['control']['pseudo_dir']=f'{path}'
        elif pseudo_type is not False:
            self.config['pw']['control']['pseudo_dir']='./pseudos/'+pseudo_type.upper()+'/'
    
    def make_afm(self,magnetic_atom,angle1=False,angle2=False):
        afm_models = utils.afm_maker(self,magnetic_atom,angle1=angle1,angle2=angle2)
        return afm_models
    def make_fm(self,magnetic_atom,angle1=False,angle2=False):
        fm = utils.fm_maker(self,magnetic_atom,angle1=angle1,angle2=angle2)
        return fm
    def magnetize(self,magnetic_atom,angle1=False,angle2=False):
        fm = utils.fm_maker(self,magnetic_atom,angle1=angle1,angle2=angle2)
        afm = utils.afm_maker(self,magnetic_atom,angle1=angle1,angle2=angle2)
        models = [fm,*afm]
        return models


    def press_conv_thr(self,value):
        self.config['pw']['cell']['press_conv_thr'] = value



    def band_points(self,path,number,file_path=False,file_name=False,points=False):
        self.path=path
        if points==False:
            file_path = f'./Projects/{self.project_id}/{self.job_id}'
            file_name = f"{self.project_id}_{self.job_id}"
            self.export_structure(file_path=file_path,file_name=file_name)
            points = self.get_points()
        
        k_path = kpoints.band_input(path,points,number)
        self.config['pw']['k_points_bands'] = k_path


    def pw(self):
        return self.config['pw']
    def system(self):
        return self.config['system']
    def control(self):
        return self.config['control']
    def electrons(self):
        return self.config['electrons']


    def occupations(self,occupation):
        self.config['pw']['system']['occupations'] = occupation
    def ecutwfc(self,number):
        self.config['pw']['system']['ecutwfc'] = number
    def ecutrho(self,number):
        self.config['pw']['system']['ecutrho'] = number
    def conv_thr(self,number):
        self.config['pw']['electrons']['conv_thr']=number
    def ph_thr(self,number):
        self.config['ph']['inputph']['tr2_ph']=number
    def force(self,value=True):
        self.config['pw']['control']['tprnfor'] = value
    def stress(self,value=True):
        self.config['pw']['control']['tstress'] = value
    def etot_conv_thr(self,value):
        self.config['pw']['control']['etot_conv_thr'] = value
    def forc_conv_thr(self,value):
        self.config['pw']['control']['forc_conv_thr'] = value
    def make_layer(self,layer_type='mono',direction='z'):
        if layer_type=='mono':
            self.config['pw']['atomic_positions'] = utils.make_monolayer(self.config['pw']['atomic_positions'],direction)
    
    def k_points(self,number,grid=False):
        if type(number) == int :
            self.config['pw']['k_points']=f'{number} {number} {number} 0 0 0'
        elif len(number) == 3:
            self.config['pw']['k_points']=f'{number[0]} {number[1]} {number[2]} 0 0 0'
        else:
            raise Exception("K points can be either a number or an array with 3 enteries")
        if grid!=False:
            self.config['pw']['k_points']=utils.k_grid(num_points=number)
            self.grid=number

        
    def atoms(self):
        return self.config['pw']['atomic_positions']
    
    def positions(self):
        atom =  np.array(self.config['pw']['atomic_positions']).T[1:].T.astype(float)
        return atom
    def cell(self):
        return self.config['pw']['cell_parameters']
    
    def add_vacuum(self,direction,vector):
            cell = np.array(self.config['pw']["cell_parameters"],dtype=float)
            atom =  self.positions()
            vacuum_atom, vacuum_cell =  utils.shift_cell(atom,cell,direction,vector)
            for i,atom in enumerate(vacuum_atom):
                for j in range(3):
                    self.config['pw']['atomic_positions'][i][1+j]=atom[j].astype(str)
            self.config['pw']["cell_parameters"] = vacuum_cell


    def shift_atoms(self,vector):
        atoms = np.array(self.config['pw']['atomic_positions']).T[1:].T.astype(float)
        shifted = utils.shift_frac(atoms=atoms,vector=vector)
        for i,atom in enumerate(shifted):
            for j in range(3):
                self.config['pw']['atomic_positions'][i][1+j]=atom[j].astype(str)
        self.config['pw']['atomic_positions']

    def strain(self,axis,value):
        initial_cell = np.array(self.cell()).astype(float)
        final_cell = utils.strain(initial_cell,axis,value)
        self.config['pw']['cell_parameters'] = final_cell

    def plot(self,calculation,save=False,xlim=False,ylim=False,figsize=False,save_name=False,title=False):
        plots.plot(self,calculation=calculation,save=save,xlim=xlim,ylim=ylim,figsize=figsize,save_name=save_name,title=title)

    def nbnd(self,number):
        self.config['pw']['system']['nbnd']=number
    
    def get_nbnd(self):
        return int(reads.read_num_bands(self))
    
    def mixing_mode(self,value):
        self.config['pw']['electrons']['mixing_mode']=value
    def smearing(self,value):
        self.config['pw']['system']['smearing'] = value
    def degauss(self,value):
        self.config['pw']['system']['degauss'] = value
    def nosym(self,value):
        self.config['pw']['system']['nosym'] = value
    def get_primitive(self,file='vasp-ase'):
        lattice,atoms,k_points = structure.primitive(self.poscar,file)
        self.config['pw']['atomic_positions'] = atoms
        self.config['pw']['cell_parameters']=lattice
    def soc(self,pseudo_path=False):
        if pseudo_path==False:
            pseudo_path = f"Research/{self.project_id}/REL"
        try:
            del self.config['pw']['system']['nspin']
        except:
            pass
        self.config['pw']['system']['noncolin']= True
        self.config['pw']['system']['lspinorb']= True
    def starting_potential(self,potential='file'):
        self.config['pw']['electrons']['startingpot']= potential
        if self.magnetism==True:
            self.config['pw']['system']['lforcet'] = True
    def magnetic_angle(self,angle1=[0,0],angle2=[0,0]):
        ntype = len(self.config['pw']['atomic_species']) #check number of atom types
        magnetic_atoms = [] #create magnetic atom index array
        for j,i in enumerate(self.config['pw']['atomic_species']): #for each atom
            if  i['atom']==self.magnetic_atom: # choose magnetic atom
                magnetic_atoms.append(j) #add atom magnetic atom list
            for k in range(ntype): #this for is necessary for AFM due to naming convention
                if  i['atom']==self.magnetic_atom+str(k): # choose magnetic atom
                    magnetic_atoms.append(j) #add atom magnetic atom list
        for j,i in enumerate(magnetic_atoms): #for all magnetic atoms
            self.config['pw']['system'][f'angle1({i+1})']=angle1[j] #define angle1 for atoms
            self.config['pw']['system'][f'angle2({j+1})']=angle2[j]#define angle2 for atoms
        
    def get_points(self,file_path=False,file_format=False):
        if file_format==False:
            file_format='qeinp-qetools'
        if file_path==False:
            file_path=f'./Projects/{self.project_id}/{self.job_id}/scf.in'
        try:
            k_points = structure.get_k(file_path,file_format)
        except:
            file_path=f'./Projects/{self.project_id}/{self.job_id}/vc-relax.in'
            k_points = structure.get_k(file_path,file_format)
        self.points=k_points
        return k_points
    
    def electron_maxstep(self,value):
        self.config['pw']['electrons']['electron_maxstep'] = value

    def exchange_maxstep(self,value):
        self.config['pw']['electrons']['exx_maxstep'] = value

    def mixing_beta(self,value):
        self.config['pw']['electrons']['mixing_beta'] = value

    def cell_dof(self,value):
        self.config['pw']['cell']['cell_dofree'] = value
        
    def get_structure(self,format,name=False,path=False,project_id=False,job_id=False,config=False):
        if format == 'input':
            reads.read_input(self,path)
        else:
            reads.read_structure(self,format,name=name,path=path)

    def calculate(self,calculation,pp_core=1):
        self.set_calculation(calculation_type=calculation) #set calculation
        if calculation=='wannier90':
            self.run_wannier()
        else:
            generate.input(self) #create input
            compute.run(self) #run calculation
        if calculation=='bands':
            self.set_calculation('bands-pp') #set calculation
            generate.input(self) #create input
            compute.run(self,num_core=pp_core) #run calculation
        elif calculation=='pdos':
            utils.sumpdos(self)
        elif calculation=='kdos':
            utils.sumkdos(self)

    def run_wannier(self):
        self.set_calculation(calculation_type='pw2wannier90') #set calculation
        generate.input(self) #create input
        self.set_calculation(calculation_type='wannier90') #set calculation
        generate.input(self) #create input
        compute.run(self)

    def check_convergence(self,calculation=False,job_id=False):
        if calculation==False:
            calculation=self.calculation
        if job_id == False:
            job_id = self.job_id
        path = f'./Projects/{self.project_id}/{job_id}/{calculation}.out'
        if calculation in ['relax','vc-relax']:
            try:
                isConverged = utils.check_relax(path=path)
            except:
                isConverged=False
        return isConverged

    def fermi_energy(self,calculation=False):
        if calculation==False:
            calculation='scf'
        path = f'./Projects/{self.project_id}/{self.job_id}/{calculation}.out'
        self.fermi = reads.read_efermi(path)
        return self.fermi
        


    def optimize(self,max_iter = 10,calculation=False):
        if calculation==False:
            calculation=self.calculation
        for i in range(max_iter):
            print(f'Starting {calculation} iteration {i+1} ')
            self.calculate(calculation)
            self.get_structure(calculation)
            isConverged = self.check_convergence(calculation)
            if isConverged:
                print(f'{calculation} is converged after {i+1} steps')
                break
        if i==max_iter-1 and not isConverged:
            print(f'{calculation} did not converged please increace number of steps steps')
                
    def dos(self,emin=False,emax=False,deltaE=False):
        if emin:
            self.config['dos']['dos']['emin']=emin
        if emax:
            self.config['dos']['dos']['emax']=emax
        if deltaE:
            self.config['dos']['dos']['deltaE']=deltaE
    def pdos(self,emin=False,emax=False,deltaE=False):
        if emin:
            self.config['projwfc']['projwfc']['emin']=emin
        if emax:
            self.config['projwfc']['projwfc']['emax']=emax
        if deltaE:
            self.config['projwfc']['projwfc']['deltaE']=deltaE
    def kdos(self,deltaE=0.005,ngauss=0,degauss=0.01):
            self.config['projwfc']['projwfc']['degauss']=degauss
            self.config['projwfc']['projwfc']['deltaE']=deltaE
            self.config['projwfc']['projwfc']['ngauss']=ngauss
    def test(self,parameter_name,start,end,step,conv_thr=False,num_core=1,debug=False,out=False,dual=4):
        result = utils.test_parameter(self=self,parameter_name=parameter_name,conv_thr=conv_thr,start=start,end=end,step=step,num_core=num_core,debug=debug,out=out,dual=dual)
        # if parameter=='ecutwfc':
        #     result = utils.test_ecutwfc(self=self,start=start,end=end,step=step,num_core=num_core,debug=debug)
        # elif parameter=='kpoints':
        #     result = utils.test_k(self=self,start=start,end=end,step=step,num_core=num_core,debug=debug)
        return result

    # def screen(self,parameter_name,begin,end,steps):
    #     if parameter_name==U:



    def set_q(self,nq1=2,nq2=2,nq3=2):
        self.config['ph']['inputph']['nq1']=nq1
        self.config['ph']['inputph']['nq2']=nq2
        self.config['ph']['inputph']['nq3']=nq3
    def set_path(self, path,number,poscar=True):
        self.get_structure(format='poscar')
        self.band_points(path,number)
        kpt = self.config['pw']['k_points_bands']
        self.config['pw']['k_points_bands']=kpt

    def export_structure(self,format='poscar',file_path=False,file_name=False,structure_name=False):
        atom = self.atoms() #Get atomic positions
        cell = self.cell()
        if  file_path == False:
            file_path = f'./Projects/{self.project_id}/{self.job_id}'
        if structure_name==False:
            if self.job_id=='results':
                structure_name = self.project_id
            else:
                structure_name = str(self.project_id)+str(self.job_id)
        if file_name==False:
            file_name=structure_name
        if format.lower()=='poscar':
            export.exportPoscar(structure_name=structure_name,atom=atom,cell=cell,file_name=file_name,file_path=file_path)
