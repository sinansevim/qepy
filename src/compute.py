import subprocess

def run_pw(project_id,job_id,calculation,num_core):
    if calculation == 'bands-pp':
        p = subprocess.Popen(f"mpirun -np {num_core}  -allow-run-as-root bands.x -inp ./Projects/{project_id}/{job_id}/{calculation}.in > ./Projects/{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
    else:
        p = subprocess.Popen(f"mpirun -np {num_core}  -allow-run-as-root pw.x -inp ./Projects/{project_id}/{job_id}/{calculation}.in > ./Projects/{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

def run_ph(project_id,job_id,calculation,num_core):
    if calculation == 'ph':
        p = subprocess.Popen(f"mpirun -np {num_core}  -allow-run-as-root ph.x -inp ./Projects/{project_id}/{job_id}/{calculation}.in > ./Projects/{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
    if calculation == 'q2r':
        p = subprocess.Popen(f"mpirun -np {num_core}  -allow-run-as-root q2r.x -inp ./Projects/{project_id}/{job_id}/{calculation}.in > ./Projects/{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
    if calculation == 'matdyn':
        p = subprocess.Popen(f"mpirun -np {num_core}  -allow-run-as-root matdyn.x -inp ./Projects/{project_id}/{job_id}/{calculation}.in > ./Projects/{project_id}/{job_id}/{calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()