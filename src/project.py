from . import utils
from . import reads
from . import generate
from . import compute
from . import kpoints
from . import plots
from . import structure



class project:
    def __init__(self,project_id):
        self.project_id = project_id
        self.config = utils.configure()
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
            self.config['pw']['control']['calculation'] = calculation_type
        if calculation_type == 'bands-pp':
            self.package='bands'
        if calculation_type == 'dos':
            self.package='dos'
        if calculation_type == 'ph':
            self.package='ph'
        if calculation_type == 'q2r':
            self.package='q2r'
        if calculation_type == 'matdyn':
            self.package='matdyn'
        self.file_path = f"./Projects/{self.project_id}/{self.job_id}/{self.calculation}.in"

    def set_pseudo(self,pseudo_type):
        self.config['pw']['control']['pseudo_dir']='./pseudos/'+pseudo_type.upper()+'/'
    
    def make_afm(self,magnetic_atom,angle1=False,angle2=False):
        afm_models = utils.afm_maker(self,magnetic_atom,angle1=angle1,angle2=angle2)
        return afm_models

    def create_input(self):
            generate.input(self)
    
    def calculate(self, num_core=False):
        if num_core==False:
            num_core=self.num_core
        if self.debug == False:
            compute.run(self)
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
    def make_layer(self,layer_type):
        if layer_type=='mono':
            self.config['pw']['atomic_positions'] = utils.make_monolayer(self.config['pw']['atomic_positions'])
    def k_points(self,number):
        if type(number) == int :
            self.config['pw']['k_points']=f'{number} {number} {number} 0 0 0'
        elif len(number) == 3:
            self.config['pw']['k_points']=f'{number[0]} {number[1]} {number[2]} 0 0 0'
        else:
            raise Exception("K points can be either a number or an array with 3 enteries")

    def plot_electron(self,ylim=False,show=False,save=False):
        plots.plot_electron(self,ylim,show,save)

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
        lattice,atoms,kpoints = structure.primitive(self.poscar,file)
        self.config['pw']['atomic_positions'] = atoms
        self.config['pw']['cell_parameters']=lattice
        
    def get_points(self,file='vasp-ase'):
        lattice,atoms,kpoints = structure.primitive(self.poscar,file)
        self.points=kpoints
        return kpoints
    def get_structure(self,format,name=False,project_id=False,job_id=False,config=False):
        if format=="poscar" and not name:
            self.poscar=f'./Structures/{self.project_id}.poscar'
        reads.read_structure(self,format,name=name)

    def vc_relax(self,num_core=False): #Crystal optimization
        self.set_calculation(calculation_type='vc-relax') #set calculation
        self.create_input() #create input
        self.calculate(num_core) #run calculation
    
    def relax(self,num_core=False): #Atomic optimization
        self.set_calculation(calculation_type='relax') #set calculation
        self.create_input() #create mono-layer input
        self.calculate(num_core) #run calculation

    def scf(self,num_core=False): #Scf calculation
        self.set_calculation(calculation_type='scf') #set calculation
        self.create_input() #create input
        self.calculate(num_core) #run calculation
    def nscf(self,num_core=False): #Scf calculation
        self.set_calculation(calculation_type='nscf') #set calculation
        self.create_input() #create input
        self.calculate(num_core) #run calculation
    def bands(self,path,num_points,num_core=False): #Band calculation
        self.band_points(path,num_points) #define path
        self.set_calculation(calculation_type='bands') #set calculation
        self.create_input() #create input
        self.calculate(num_core) #run calculations
        self.set_calculation('bands-pp') #set calculaion
        self.create_input() #create input
        self.calculate(num_core) #run calculation
    def dos(self,e_min=False,e_max=False,deltaE=False,num_core=False):
        if e_min:
            self.config['dos']['dos']['emin']=e_min
        if e_max:
            self.config['dos']['dos']['emax']=e_max
        if deltaE:
            self.config['dos']['dos']['DeltaE']=deltaE
        self.set_calculation(calculation_type='dos') #set calculation
        self.create_input() #create input
        self.calculate(num_core) #run calculation
    

    def plot_dos(self,xlim=False):
        plots.plot_dos(self,xlim=xlim)

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
    def plot_phonon(self):
        plots.plot_phonon(self)

