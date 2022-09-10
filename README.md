# Espresso Machine
Automation library for Quantum Espresso via python

# Execute run.py with the following input set 
## Input parameter
input.json file is supported in Example foldeer
## Calculation type
vc-relax, relax, scf, band
## Degauss parameter
Fermi-Dirac smearing width in Ry
## K points
nx ny nz type mesh grid or k space path
## Initial guess or poscar
Read from vc-relax or poscar file

# Input Example
python run.py -c vc-relax -d 0.001 -i ./vc-relax.out
python run.py -c vc-relax -d 0.2 -i ./NbSe2.poscar
python run.py -c scf -d 0.05 -k 30 30 1 0 0 0
