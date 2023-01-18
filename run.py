import argparse
from src.generate import *
parameter = './input.json'


# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-c", "--calculation", required=True,
                help="Type of calculation")
ap.add_argument("-d", "--degauss", required=True,
                help="Degauss value")
ap.add_argument("-k", "--kpoints", nargs='+', required=False,
                help="K points")
ap.add_argument("-i", "--initial",  required=False,
                help="Initial guess path")
ap.add_argument("-p", "--poscar",  required=False,
                help="Poscar path")

args = vars(ap.parse_args())


# Type of calculation
calculation = args['calculation']
# Degauss parameter
degauss = args['degauss']

# K points

if args['kpoints'] != None:
    k_points = ' '.join(args['kpoints'])
else:
    k_points = None


initial = args['initial']
poscar = args['poscar']
# print(f"Initial path: {initial}")
# print(f"Initial path: {poscar}")


generate(parameter, calculation, degauss, k_points=k_points,
         initial_guess=initial, poscar=poscar)
