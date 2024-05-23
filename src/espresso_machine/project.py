from . import utils
from . import reads
from . import generate
from . import compute
from . import kpoints
from . import plots
from . import structure
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

    def band_points(self,path,number):
        self.path=path
        points = self.get_points()
        k_path = kpoints.band_input(path,points,number)
        self.config['pw']['k_points_bands'] = k_path
    def occupations(self,occupation):
        self.config['pw']['system']['occupations'] = occupation
    def ecutwfc(self,number):
        self.config['pw']['system']['ecutwfc'] = number
    def ecutrho(self,number):
        self.config['pw']['system']['ecutrho'] = number
    def conv_thr(self,number):
        self.config['pw']['electrons']['conv_thr']=number
    def make_layer(self,layer_type='mono',direction='z'):
        if layer_type=='mono':
            self.config['pw']['atomic_positions'] = utils.make_monolayer(self.config['pw']['atomic_positions'],direction)
    def k_points(self,number):
        if type(number) == int :
            self.config['pw']['k_points']=f'{number} {number} {number} 0 0 0'
        elif len(number) == 3:
            self.config['pw']['k_points']=f'{number[0]} {number[1]} {number[2]} 0 0 0'
        else:
            raise Exception("K points can be either a number or an array with 3 enteries")


    def shift_atoms(self,vector):
        atoms = np.array(self.config['pw']['atomic_positions']).T[1:].T.astype(float)
        shifted = utils.shift_frac(atoms=atoms,vector=vector)
        for i,atom in enumerate(shifted):
            for j in range(3):
                self.config['pw']['atomic_positions'][i][1+j]=atom[j].astype(str)



        self.config['pw']['atomic_positions']


    def plot(self,calculation,save=False,xlim=False,ylim=False):
        plots.plot(self,calculation,save,xlim,ylim)

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
        
    def get_points(self,file_path=False,file_format=False):
        if file_format==False:
            file_format='qeinp-qetools'
        if file_path==False:
            file_path=f'./Projects/{self.project_id}/{self.job_id}/scf.in'
        k_points = structure.get_k(file_path,file_format)
        self.points=k_points
        return k_points
    def get_structure(self,format,name=False,path=False,project_id=False,job_id=False,config=False):
        # self.poscar=f'./Structures/{self.project_id}.poscar'
        reads.read_structure(self,format,name=name,path=path)

    def calculate(self,calculation):
        self.set_calculation(calculation_type=calculation) #set calculation
        generate.input(self) #create input
        compute.run(self) #run calculation
        if calculation=='bands':
            self.set_calculation('bands-pp') #set calculaion
            generate.input(self) #create input
            compute.run(self) #run calculation
        elif calculation=='pdos':
            utils.sumpdos(self)
        elif calculation=='kdos':
            utils.sumkdos(self)

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
    def test(self,parameter_name,start,end,step,conv_thr=False,num_core=1,debug=False,out=False):
        result = utils.test_parameter(self=self,parameter_name=parameter_name,conv_thr=conv_thr,start=start,end=end,step=step,num_core=num_core,debug=debug,out=out)
        # if parameter=='ecutwfc':
        #     result = utils.test_ecutwfc(self=self,start=start,end=end,step=step,num_core=num_core,debug=debug)
        # elif parameter=='kpoints':
        #     result = utils.test_k(self=self,start=start,end=end,step=step,num_core=num_core,debug=debug)
        return result
    
    def set_q(self,nq1=2,nq2=2,nq3=2):
        self.config['ph']['inputph']['nq1']=nq1
        self.config['ph']['inputph']['nq2']=nq2
        self.config['ph']['inputph']['nq3']=nq3
    def set_path(self, path,number,poscar=True):
        self.get_structure(format='poscar')
        self.band_points(path,number)
        kpt = self.config['pw']['k_points_bands']
        self.config['pw']['k_points_bands']=kpt
