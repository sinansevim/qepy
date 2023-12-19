#!/bin/zsh

#### Local testing variables ####
#Path to quantum-espresso
QE=/usr/bin
#Number of cores
SLURM_NTASKS=4

#Initial degauss value (0 for POSCAR initialization)
initial=0
#POSCAR file
POSCAR=C.poscar
project_name=Graphene
pw_json=pw.json
#vc-relax k points
vc_relax_k=('1 1 1 0 0 0')
relax_k=('1 1 1 0 0 0')
scf_k=('1 1 1 0 0 0')


echo "Espresso Machine is starting"
#Smearing parameters
for sigma in 0.05 
do
echo "Automation for $sigma is started"

#Scf calculation
echo "Scf input for $sigma is generated"
python run.py -n $project_name -c scf -j $pw_json  -d $sigma -k ${scf_k[@]} -p $POSCAR -l mono
echo "Scf calculation for $sigma is started"
mpirun -n $SLURM_NTASKS $QE/pw.x -inp ./$project_name/$sigma/scf.in > ./$project_name/$sigma/scf.out
echo "Scf calculation for $sigma is finished"


echo "Automation for $sigma is completed"
done 
echo "Automation is completed"