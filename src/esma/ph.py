from . import utils
from . import reads
from . import generate
from . import compute
from . import kpoints
from . import plots
from . import structure
from .project import project


class ph:
    def __init__(self,project_id):
        self.project_id = project_id
        self.config = utils.configure('ph')
        self.job_id = 'results'
        self.calculation = False
    def create_input(self,job_id='results'):
        # self.set_calculation(self.calculation)
        generate.ph_input(project_id=self.project_id,calculation=self.calculation,job_id=self.job_id, config=self.config)
    def set_calculation(self,calculation):
        self.calculation=calculation
        self.config = utils.configure(calculation)
    def calculate(self, num_core=1):
        compute.run_ph(self.project_id,self.job_id,self.calculation,num_core)
    def set_q(self,nq1=2,nq2=2,nq3=2):
        self.config['inputph']['nq1']=nq1
        self.config['inputph']['nq2']=nq2
        self.config['inputph']['nq3']=nq3
    def set_path(self, path,number,poscar=True):
        model = pw(project_id=self.project_id )
        if (poscar):
            model.get_structure(format='poscar')
        model.band_points(path,number)
        kpt = model.config['k_points_bands']
        self.config['k_points_bands']=kpt
    def plot(self):
        plots.plot_phonon(self)

