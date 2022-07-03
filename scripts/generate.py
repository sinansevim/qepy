from . import scaffold
from . import reads
from . import utils
import argparse
import json
import os

def generate(parameter_path,calculation,degauss,k_points=None,prev=None,poscar=False):
    try:
        os.makedirs('./inputs')
    except:
        pass
        
    with open(f'{parameter_path}') as f:
        data = f.read()
    input_parameters = json.loads(data)
    
    
    #Set parameters from input
    input_parameters["file_name"] = f"./inputs/{degauss}-{calculation}.in"
    input_parameters["degauss"] = degauss
    
    if calculation == 'vc-relax':
    #Import initial cell and atom parameters
        if poscar!=False:
            cell, atoms = reads.read_poscar(f'{poscar}')
        else:
            cell, atoms = reads.read_vc_relax(f"./outputs/{prev}-vc-relax.out")
    
    elif calculation == 'relax':
        cell, atoms = reads.read_vc_relax(f"./outputs/{degauss}-vc-relax.out")
        atoms = utils.make_monolayer(atoms)
    
    else:
        cell, temp = reads.read_vc_relax(f"./outputs/{degauss}-vc-relax.out")
        atoms = reads.read_relax(f"./outputs/{degauss}-relax.out")
        
    if k_points!=None:
        input_parameters['k_points'] = k_points

    input_parameters['prefix'] = degauss
    input_parameters['nat']=len(atoms)
    input_parameters['atomic_positions']=atoms
    input_parameters['cell_parameters']=cell
    input_parameters['calculation']=calculation
    
    if calculation=='bands-pp':
        scaffold.bands_pp(input_parameters)
    else:
        scaffold.pw(input_parameters)
    