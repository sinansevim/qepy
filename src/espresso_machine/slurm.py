from dotenv import dotenv_values

config = dotenv_values(".env")

QE_PATH=config['QE_PATH']
COMPILER=config['COMPILER']
SLURM_JOB_NUM_NODES=config['SLURM_JOB_NUM_NODES']             
SLURM_NTASKS=config['SLURM_NTASKS']
SLURM_PARTITION=config['SLURM_PARTITION']
SLURM_JOB_NAME=config['SLURM_JOB_NAME']
WORK_DIR=config['WORK_DIR']
PYTHON_ENV=config['PYTHON_ENV']


def generate(file_name="run.sh",num_core=SLURM_NTASKS,num_node=SLURM_JOB_NUM_NODES,job_name=SLURM_JOB_NAME,partition=SLURM_PARTITION,qe_path=QE_PATH,compiler_path=COMPILER,PYTHON_ENV=PYTHON_ENV):
    text=f"""{sbatch(num_core,num_node,job_name,partition)}
{qe(qe_path)}
{compiler(compiler_path)}
{python(PYTHON_ENV)}
cd {WORK_DIR}
python3 job.py
"""
    with open(file_name, 'w') as file:
        file.write(text)
    return text


def sbatch(num_core,num_node,job_name,partition):
    text = f"""#!/bin/bash 
#SBATCH --partition {partition}
#SBATCH --nodes     {num_node}
#SBATCH --ntasks    {num_core}
#SBATCH --job-name  {job_name}
#SBATCH --output    {job_name}.out
"""
    return text

def qe(path):
    text = f"""
export PATH="{path}/bin/:$PATH"
"""
    return text
def python(path):
    text=f"""
{path}
""" 
    return text

def compiler(path):
    text = f"""
{path}
"""
    return text
