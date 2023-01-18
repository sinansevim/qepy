# Espresso Machine
Automation library for Quantum Espresso via python

# Start by executing adiabatic.sh
Edit parameters in the file for local environment. Such as HPC parameters, python, MPI, Quantum Espresso directories
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
