import sys
import argparse
from src.generate import *
parameter = './input.json'


# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-n", "--name", required=True,
                help="Project name")
ap.add_argument("-c", "--calculation", required=True,
                help="Type of calculation")
ap.add_argument("-j", "--json",  required=True,
                help="JSON file")
ap.add_argument("-d", "--degauss", required=False,
                help="Degauss value")
ap.add_argument("-k", "--kpoints", nargs='+', required=False,
                help="K points")
ap.add_argument("-i", "--initial",  required=False,
                help="Initial guess path")
ap.add_argument("-p", "--poscar",  required=False,
                help="Poscar path")
ap.add_argument("-l", "--layer",  required=False,
                help="Layered materials")



args = vars(ap.parse_args())

project_name = args['name']
# Type of calculation
calculation = args['calculation']
# Degauss parameter
degauss = args['degauss']
parameter = args['json']
# K points

if args['kpoints'] != None:
    k_points = ' '.join(args['kpoints'])
else:
    k_points = None

layer = args["layer"]


initial = args['initial']
poscar = args['poscar']
# print(f"Initial path: {initial}")
# print(f"Initial path: {poscar}")


generate(project_name,parameter, calculation, degauss, k_points=k_points,
         initial_guess=initial, poscar=poscar,layer=layer)
