from . import scaffold
from . import reads
from . import utils
from . import check
import os
import sys


def create_folders(project_id,job_id):
    #Create directory for input files
    try:
        os.makedirs(f'./Projects/')
    except:
        pass
    try:
        os.makedirs(f'./Projects/{project_id}')
        os.makedirs(f'./Projects/{project_id}/{job_id}')
    except:
        try:
            os.makedirs(f'./Projects/{project_id}/{job_id}')
        except:
            pass

def pw_checks(self):
    project_id = self.project_id
    job_id = self.job_id
    config=self.config['pw']
    calculation=self.calculation
    check.project_id(project_id)
    check.job_id(job_id)
    check.config(config)
    
    # Set outfolders
    create_folders(project_id=project_id,job_id=job_id)
    config["control"]["outdir"] = f"./Projects/{project_id}/{job_id}/"
    
    cell, atoms = config['cell_parameters'], config['atomic_positions']


    config["control"]['prefix'] = job_id
    config["system"]['nat'] = len(atoms)
    #check types of atoms
    try:
        config["system"]['ntyp']
    except:
        config["system"]['ntyp'] = utils.atom_type(atoms)
    
    #check ibrav
    try:
        config["system"]['ibrav']
    except:
        config["system"]['ibrav'] = 0
    config["control"]['calculation'] = calculation

    

def input(self):
    if self.package=='pw':
        pw_checks(self)
    if self.package=='ph':
        ph_checks(self)
    if self.package=='q2r':
        q2r_checks(self)
    if self.package=='matdyn':
        matdyn_checks(self)
    if self.package=='bands':
        bands_chekcs(self)
    if self.package=='dos':
        dos_chekcs(self)
    scaffold.constructor(self)

def ph_checks(self):
    self.config['ph']["inputph"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    self.config['ph']["inputph"]['prefix'] = self.job_id
    self.config['ph']["inputph"]["fildyn"]= f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.dyn'
def q2r_checks(self):
        self.config['q2r']['input']['fildyn'] = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.dyn'
        self.config['q2r']['input']['flfrc']  = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.fc'
def matdyn_checks(self):
        self.config['matdyn']['input']['fildyn'] = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.dyn'
        self.config['matdyn']['input']['flfrc']  = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.fc'
        self.config['matdyn']['input']['flfrq']  = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.freq'
        self.config['matdyn']['input']['flvec']  = f'./Projects/{self.project_id}/{self.job_id}/matdyn.modes'
def bands_chekcs(self):
    self.config['bands']["bands"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    self.config['bands']["bands"]["prefix"] = self.job_id
    self.config['bands']["bands"]["filband"]  = f'./Projects/{self.project_id}/{self.job_id}/bands.dat'

def dos_chekcs(self):
    self.config['dos']["dos"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    self.config['dos']["dos"]["prefix"] = self.job_id
    self.config['dos']["dos"]["fildos"]  = f'./Projects/{self.project_id}/{self.job_id}/dos.dat'

def runner(project_name,iteration,file_names,calculation,qe_path,ncore):
    pre = f'''QE={qe_path}
SLURM_NTASKS={ncore}
project_name={project_name}
    '''
    # print(pre)
    post =f'''
echo Starting {iteration} calculation
for file_name in {" ".join(file_names)}
do
echo $file_name is started
mpirun -n $SLURM_NTASKS $QE/pw.x -inp ./$project_name/$file_name/{calculation}.in > ./$project_name/$file_name/{calculation}.out
echo $file_name is done
done
echo All {iteration} calculations are completed
    '''
    # print(post)
    with open(f"./{iteration}.sh", 'w') as file:
        file.write(pre)
        file.write(post)
    return