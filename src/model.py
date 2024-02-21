from . import utils
from . import reads
from . import generate
from . import compute

class pw:
    def __init__(self,project_id):
        self.project_id = project_id
        self.config = utils.configure()
        self.atom = False
        self.lattice = False
        self.calculation=False
        self.job_id = False

    def from_poscar(self,directory):
        self.poscar=directory
        lattice, atom = reads.read_poscar(directory)
        self.config['atomic_positions'] = atom
        self.config['cell_parameters'] = lattice
    
    def set_calculation(self,calculation_type):
        self.calculation = calculation_type
        self.config['control']['calculation'] = calculation_type


    def create_input(self,job_id='default',layer="False"):
        self.job_id = job_id
        generate.input(project_id=self.project_id,calculation=self.calculation,job_id=self.job_id, config=self.config,layer=layer)
    
    def calculate(self,num_core):
        compute.run_pw(self.project_id,self.job_id,self.calculation,num_core)