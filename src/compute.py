import subprocess

def run_pw(project_id,job_id,calculation,num_core):
    p = subprocess.Popen(f"mpirun -np {num_core} pw.x -inp ./{project_id}/{job_id}/{calculation}.in > ./{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
