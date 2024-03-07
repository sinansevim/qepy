from . import utils
from . import reads
from . import generate
from . import compute
from . import kpoints
from . import plots
from . import structure
class pw:
    def __init__(self,project_id):
        self.project_id = project_id
        self.config = utils.configure_pw()
        self.atom = False
        self.lattice = False
        self.calculation=False
        self.job_id = 'results'
        self.path = False
        self.poscar= False


    def from_poscar(self,directory):
        self.poscar=directory
        lattice, atom = reads.read_poscar(directory)
        self.config['atomic_positions'] = atom
        self.config['cell_parameters'] = lattice
    
    def set_calculation(self,calculation_type):
        self.calculation = calculation_type
        self.config['control']['calculation'] = calculation_type


    def create_input(self,job_id='results',layer="False"):
        self.job_id = job_id
        generate.pw_input(project_id=self.project_id,calculation=self.calculation,job_id=self.job_id, config=self.config,layer=layer)
    
    def calculate(self,num_core=1):
        compute.run_pw(self.project_id,self.job_id,self.calculation,num_core)
    def band_points(self,path,number):
        self.path=path
        points = self.get_points()
        k_path = kpoints.band_input(path,points,number)
        self.config['k_points_bands'] = k_path

    def ecutwfc(self,number):
        self.config['system']['ecutwfc'] = number
    def conv_thr(self,number):
        self.config['electrons']['conv_thr']=number

    def k_points(self,number):
        if type(number) == int :
            self.config['k_points']=f'{number} {number} {number} 0 0 0'
        elif len(number) == 3:
            self.config['k_points']=f'{number[0]} {number[1]} {number[2]} 0 0 0'
        else:
            raise Exception("K points can be either a number or an array with 3 enteries")
    
    def plot_electron(self,ylim=False,show=False,save=False):
        plots.plot_electron(self,ylim,show,save)

    def nbnd(self,number):
        self.config['system']['nbnd']=number
    
    def get_nbnd(self):
        return int(reads.read_num_bands(self))
    
    def mixing_mode(self,value):
        self.config['electrons']['mixing_mode']=value
    def smearing(self,value):
        self.config['system']['smearing'] = value
    def degauss(self,value):
        self.config['system']['degauss'] = value

    def get_primitive(self,file='vasp-ase'):
        lattice,atoms,kpoints = structure.primitive(self.poscar,file)
        self.config['atomic_positions'] = atoms
        self.config['cell_parameters']=lattice
        
    def get_points(self,file='vasp-ase'):
        lattice,atoms,kpoints = structure.primitive(self.poscar,file)
        self.points=kpoints
        return kpoints
    
class ph:
    def __init__(self,project_id):
        self.project_id = project_id
        self.config = utils.configure_ph()
        self.job_id = 'results'
        self.calculation = False
    def create_input(self,job_id='results'):
        # self.set_calculation(self.calculation)
        generate.ph_input(project_id=self.project_id,calculation=self.calculation,job_id=self.job_id, config=self.config)
    def set_calculation(self,calculation):
        self.calculation=calculation
        self.config = utils.configure_ph(calculation)
    def calculate(self,num_core=1):
        compute.run_ph(self.project_id,self.job_id,self.calculation,num_core)
    def set_q(self,nq1=2,nq2=2,nq3=2):
        self.config['inputph']['nq1']=nq1
        self.config['inputph']['nq2']=nq2
        self.config['inputph']['nq3']=nq3
    def set_path(self, path,number,poscar=True):
        model = pw(project_id=self.project_id )
        if (poscar):
            model.from_poscar(directory=f"{self.project_id}.poscar")
        model.band_points(path,number)
        kpt = model.config['k_points_bands']
        self.config['k_points_bands']=kpt
    def plot(self):
        plots.plot_phonon(self)

