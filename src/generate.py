from . import scaffold
from . import reads
from . import utils
import argparse
import json
import os


def generate(parameter, calculation, degauss, initial_guess=None, k_points=None, poscar=None):

    with open(f'{parameter}') as f:
        data = f.read()
    input_parameters = json.loads(data)

    project_name = input_parameters["project_name"]

    try:
        os.makedirs('./results')
        os.makedirs(f'./results/{degauss}')
        os.makedirs(f'./results/{degauss}')
    except:
        try:
            os.makedirs(f'./results/{degauss}')
        except:
            pass


    # Set parameters from input
    input_parameters["file_name"] = f"./results/{degauss}/{calculation}.in"
    input_parameters["pw"]["system"]["degauss"] = degauss
    input_parameters["outdir"] = f"./results/{degauss}/"
    nat = int(input_parameters["pw"]["system"]['nat'])


    if calculation == 'vc-relax':
        # Import initial cell and atom parameters
        if initial_guess != None:
            cell, atoms = reads.read_vc_relax(f"{initial_guess}",nat)
        if poscar != None:
            cell, atoms = reads.read_poscar(f'{poscar}')

    elif calculation == 'relax':
        cell, atoms = reads.read_vc_relax(f"./results/{degauss}/vc-relax.out",nat)
        atoms = utils.make_monolayer(atoms)

    else:
        cell, temp = reads.read_vc_relax(f"./results/{degauss}/vc-relax.out",nat)
        atoms = reads.read_relax(f"./results/{degauss}/relax.out")

    if k_points != None:
        input_parameters['k_points'] = k_points

    input_parameters['prefix'] = degauss
    input_parameters["pw"]["system"]['nat'] = len(atoms)
    input_parameters["pw"]['atomic_positions'] = atoms
    input_parameters["pw"]['cell_parameters'] = cell
    input_parameters["pw"]["control"]['calculation'] = calculation

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
