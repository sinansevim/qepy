import subprocess

def run_pw(project_id,job_id,calculation,num_core):
    if calculation == 'bands-pp':
        p = subprocess.Popen(f"mpirun -np {num_core} bands.x -inp ./{project_id}/{job_id}/{calculation}.in > ./{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
    else:
        p = subprocess.Popen(f"mpirun -np {num_core} pw.x -inp ./{project_id}/{job_id}/{calculation}.in > ./{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
