from . import scaffold
from . import reads
from . import utils
import os
import sys


def input(project_name,input_parameters, calculation,degauss=None, file_name=None, initial_guess=None, k_points=None, poscar=None, layer=None):

    
    
    if (not file_name):
        if (degauss):
            file_name = degauss
        else:
            sys.stdout.writelines("No file name \n")
            print("No file name")


    try:
        os.makedirs(f'./{project_name}')
        os.makedirs(f'./{project_name}/{file_name}')
    except:
        try:
            os.makedirs(f'./{project_name}/{file_name}')
        except:
            pass

    
    # Set parameters from input
    input_parameters["file_path"] = f"./{project_name}/{file_name}/{calculation}.in"
    if(degauss!=None):
        input_parameters["system"]["degauss"] = degauss
    input_parameters["control"]["outdir"] = f"./{project_name}/{file_name}/"
    nat = int(input_parameters["system"]['nat'])


    if calculation == 'vc-relax':
        # Import initial cell and atom parameters
        if initial_guess != None:
            cell, atoms = reads.read_vc_relax(f"{initial_guess}",nat)
        if poscar != None:
            cell, atoms = reads.read_poscar(f'{poscar}')

    elif calculation == 'relax':
        cell, atoms = reads.read_vc_relax(f"./{project_name}/{file_name}/vc-relax.out",nat)


    else:
        if poscar != None:
            cell, atoms = reads.read_poscar(f'{poscar}')
        else:
            cell, temp = reads.read_vc_relax(f"./{project_name}/{file_name}/vc-relax.out",nat)
            atoms = reads.read_relax(f"./{project_name}/{file_name}/relax.out")
    if(layer=='mono'):
            atoms = utils.make_monolayer(atoms)

    if k_points != None:
        input_parameters['k_points'] = k_points

    input_parameters["control"]['prefix'] = file_name
    input_parameters["system"]['nat'] = len(atoms)
    input_parameters['atomic_positions'] = atoms
    input_parameters['cell_parameters'] = cell
    input_parameters["control"]['calculation'] = calculation

    if calculation == 'bands-pp':
        scaffold.bands_pp(input_parameters)
    elif calculation == 'ph':
        scaffold.ph(input_parameters)
    elif calculation == 'q2r':
        scaffold.q2r(input_parameters)
    elif calculation == 'matdyn':
        scaffold.matdyn(input_parameters)
    elif calculation == 'plotband':
        scaffold.plotband(input_parameters)
    elif calculation == "ph_plot":
        scaffold.ph_plot(input_parameters)
    else:
        scaffold.pw(input_parameters)


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