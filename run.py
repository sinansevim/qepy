parameter = './example_data/input_parameter.json'


from scripts.generate import *
import argparse

# Construct the argument parser
ap = argparse.ArgumentParser()

# Add the arguments to the parser
ap.add_argument("-c", "--calculation", required=True,
   help="Type of calculation")
ap.add_argument("-d", "--degauss", required=True,
   help="Degauss value")
ap.add_argument("-k", "--kpoints", nargs='+',required=False,
   help="K points")
   
args = vars(ap.parse_args())


#Type of calculation
calculation = args['calculation']
#Degauss parameter
degauss = args['degauss']

#K points

if args['kpoints']!=None:
    k_points = ' '.join(args['kpoints'])
else:
    k_points=None


generate(parameter,calculation,degauss,k_points=k_points)