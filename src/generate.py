from . import scaffold
from . import reads
from . import utils
import argparse
import json
import os


def generate(project_name,parameter, calculation, degauss=None, initial_guess=None, k_points=None, poscar=None, layer=None):

    with open(f'{parameter}') as f:
        data = f.read()
    input_parameters = json.loads(data)

    try:
        os.makedirs(f'./{project_name}')
        os.makedirs(f'./{project_name}/{degauss}')
    except:
        try:
            os.makedirs(f'./{project_name}/{degauss}')
        except:
            pass


    # Set parameters from input
    input_parameters["file_name"] = f"./{project_name}/{degauss}/{calculation}.in"
    input_parameters["system"]["degauss"] = degauss
    input_parameters["control"]["outdir"] = f"./{project_name}/{degauss}/"
    nat = int(input_parameters["system"]['nat'])


    if calculation == 'vc-relax':
        # Import initial cell and atom parameters
        if initial_guess != None:
            cell, atoms = reads.read_vc_relax(f"{initial_guess}",nat)
        if poscar != None:
            cell, atoms = reads.read_poscar(f'{poscar}')

    elif calculation == 'relax':
        cell, atoms = reads.read_vc_relax(f"./{project_name}/{degauss}/vc-relax.out",nat)
        if(layer=='mono'):
            atoms = utils.make_monolayer(atoms)

    else:
        cell, temp = reads.read_vc_relax(f"./{project_name}/{degauss}/vc-relax.out",nat)
        atoms = reads.read_relax(f"./{project_name}/{degauss}/relax.out")

    if k_points != None:
        input_parameters['k_points'] = k_points

    input_parameters["control"]['prefix'] = degauss
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
