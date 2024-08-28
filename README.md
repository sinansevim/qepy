# Espresso Machine
Automation library for Quantum Espresso via python

Start discovering by checking out the Tutorials section for different calculations
It is suggested to use a virtual environment to avaoid any compatibility issues.
## Automated Calculation
Any kind of choosen calculation type will be initialized after automatically generating the input files
## Parameter Adjustment
DFT parameters can be adjusted using the functional approach to keep the bugs away
## Utility Tools
Various kind of utility tools added to make the workflow smooth

### How to use
#### 1. Prepare the python environment for avoiding compatibility issues
  > python -m venv .venv

  > source .venv/bin/activate 

  > pip install esma
#### 2. Create work script
- Initialize model and define paths
  > model = esma.project(project_id="Si") #Define project
  > model.set_cores(4) #Define number of processing cores
  > model.get_structure(format='poscar',path='./Structures/Si.poscar') 
- Pseudopotential names should be as same as the the. For example for Si atom it should be named as Si.UPF.
  > model.set_pseudo(path="./Pseudopotentials") 
- Adjust system specific parameters
  > model.ecutwfc(80) #Set wavefunction cutoff
  > model.k_points([4,4,4]) #Set number of k points
- Start calculations 
  > model.calculate('vc-relax')
  > model.calculate('scf')
- Define band path and calculate band structure 
  > path = ['L','GAMMA','X','K','GAMMA']
  > num_points = 100 
  > model.band_points(path,num_points) 
  > model.calculate('bands') 
- Plot band structure
  > model.plot('electron',ylim=[-13,12]) #plot electron bands
