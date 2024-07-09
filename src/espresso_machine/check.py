def project_id(project_id):
    if (project_id==False):
        raise Exception("Define a project_id")
    
def job_id(job_id):
    if (job_id==False):
        raise Exception("Define a job_id")
    
def config(config):
    if config==False:
        raise Exception("Define a configuration")

def check_relax(path):
    lines = open(path, 'r').readlines()
    for i in lines:
        if "bfgs failed after" in i:
            return False
        if "bfgs converged" in i:
            return True