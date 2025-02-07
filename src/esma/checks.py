from . import utils
import os 

def generic_check(self):
    if self.config['metadata']['outdir']==False:
        self.config[self.package][self.package]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    else:
        self.config[self.package][self.package]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/{self.config['metadata']['outdir']}"
    self.config[self.package][self.package]["prefix"] = self.job_id
    self.config[self.package][self.package][f"fil{self.package}"]  = f'./Projects/{self.project_id}/{self.job_id}/{self.package}.dat'

def d3hess_checks(self):
    if self.config['metadata']['outdir']==False:
        self.config[self.package]["input"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    else:
        self.config[self.package]["input"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/{self.config['metadata']['outdir']}"
    self.config[self.package]["input"]["prefix"] = self.job_id
    self.config[self.package]["input"][f"filhess"]  = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.hess'
    self.config['ph']['inputph']['dftd3_hess'] = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.hess'


def hp_checks(self):
    self.config[self.package]["inputhp"]["prefix"] = self.job_id
    if self.config['metadata']['outdir']==False:
        self.config[self.package]["inputhp"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    else:
        self.config[self.package]["inputhp"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/{self.config['metadata']['outdir']}"


def pw2wannier90_checks(self):
    if self.config['metadata']['outdir']==False:
        self.config[self.package]["inputpp"]["outdir"] = f"./"
    else:
        self.config[self.package]["inputpp"]["outdir"] = f"./{self.config['metadata']['outdir']}"
    self.config[self.package]["inputpp"]["prefix"]    = self.job_id
    self.config[self.package]["inputpp"]["seedname"]  = self.job_id
    try:
        if self.config['metadata']['scdm']==True:
            self.config[self.package]['inputpp']["scdm_proj"]='true'
            try:
                self.config[self.package]['inputpp']["scdm_entanglement"]
            except:
                self.config[self.package]['inputpp']["scdm_entanglement"]="erfc"
    except:
        pass

def wannier90_checks(self):
    try:
        if self.config['metadata']['scdm']==True:
            self.config[self.package]["num_wann"]  = self.get_nbnd()
            self.config[self.package]["num_iter"]  = 0
            self.config[self.package]["dis_num_iter"]  = 0
            self.config[self.package]["auto_projections"]  = "true"
        else:
            self.config[self.package]["num_bands"]  = self.get_nbnd()
    except:
            self.config[self.package]["num_bands"]  = self.get_nbnd()
        
    try:
        if self.config['pw']['system']['lspinorb'] == True:
            self.config[self.package]["spinors"]  = 'true'
    except:
       pass


def check_project_id(project_id):
    if (project_id==False):
        raise Exception("Define a project_id")
    
def check_job_id(job_id):
    if (job_id==False):
        raise Exception("Define a job_id")
    
def check_config(config):
    if config==False:
        raise Exception("Define a configuration")




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
    check_project_id(project_id)
    check_job_id(job_id)
    check_config(config)
    config['control']['calculation'] = self.calculation
    # Set outfolders
    create_folders(project_id=project_id,job_id=job_id)
    if self.config['metadata']['outdir']==False:
        config["control"]["outdir"] = f"./Projects/{project_id}/{job_id}/"
    else:
        config["control"]["outdir"] = f"./Projects/{project_id}/{job_id}/{self.config['metadata']['outdir']}"
    

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

def projwfc_checks(self):
    if self.calculation=='pdos':
        self.config[self.package][self.package][f"filpdos"]  = f'./Projects/{self.project_id}/{self.job_id}/{self.package}.dat'
    elif self.calculation=='kdos':
        self.config[self.package][self.package]["filpdos"]  = f'./Projects/{self.project_id}/{self.job_id}/dos.k'
        self.config[self.package][self.package]["kresolveddos"]  = 'true'
        self.config[self.package][self.package]["degauss"]  =  self.config['pw']['system']['degauss']
    if self.config['metadata']['outdir']==False:
        self.config[self.package][self.package]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    else:
        self.config[self.package][self.package]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/{self.config['metadata']['outdir']}"
    self.config[self.package][self.package]["prefix"] = self.job_id


def bands_checks(self):
    if self.config['metadata']['outdir']==False:
        self.config[self.package][self.package]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    else:
        self.config[self.package][self.package]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/{self.config['metadata']['outdir']}"
    
    self.config[self.package][self.package]["prefix"] = self.job_id
    self.config[self.package][self.package][f"filband"]  = f'./Projects/{self.project_id}/{self.job_id}/{self.package}.dat'



def ph_checks(self):
    if self.config['metadata']['outdir']==False:
        self.config['ph']["inputph"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/"
    else:
        self.config['ph']["inputph"]["outdir"] = f"./Projects/{self.project_id}/{self.job_id}/{self.config['metadata']['outdir']}"
    
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


