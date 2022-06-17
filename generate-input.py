from qepy import *
import argparse
import json

with open('./example_data/input_parameter.json') as f:
    data = f.read()
input_parameters = json.loads(data)

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-c", "--calculation", required=True,
   help="Type of calculation")
ap.add_argument("-d", "--degauss", required=True,
   help="Degauss value")
args = vars(ap.parse_args())

#Type of calculation
calculation = args['calculation']
#Degauss parameter
degauss = args['degauss']

#Set parameters from input
input_parameters["file_name"] = f"./inputs/{degauss}-{calculation}.in"
input_parameters["degauss"] = degauss

if args['calculation'] == 'vc-relax':
#Import initial cell and atom parameters
    cell, atoms = read_vc_relax('./example_data/vc-relax.out')

elif args['calculation'] == 'relax':
    cell, atoms = read_vc_relax(f"./outputs/{degauss}-vc-relax.out")
    atoms = make_monolayer(atoms)

else:
    cell, temp = read_vc_relax(f"./outputs/{degauss}-vc-relax.out")
    atoms = read_relax(f"./outputs/{degauss}-relax.out")
    


input_parameters['nat']=len(atoms)
input_parameters['atomic_positions']=atoms
input_parameters['cell_parameters']=cell
 
generate_input(input_parameters)
