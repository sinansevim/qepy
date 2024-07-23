from .checks import bands_checks, generic_check, matdyn_checks, ph_checks, projwfc_checks, pw_checks, q2r_checks, pw2wannier90_checks, wannier90_checks
from . import scaffold
from . import reads
import os

def input(self):
    if self.package=='pw':
        pw_checks(self)
    elif self.package=='ph':
        ph_checks(self)
    elif self.package=='q2r':
        q2r_checks(self)
    elif self.package=='matdyn':
        matdyn_checks(self)
    elif self.package=='projwfc':
        projwfc_checks(self)
    elif self.package=='bands':
        bands_checks(self)
    elif self.package=='wannier90':
        wannier90_checks(self)
    elif self.package=='pw2wannier90':
        pw2wannier90_checks(self)
    else:
        generic_check(self)
    scaffold.constructor(self)

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