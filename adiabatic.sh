#!/bin/bash 
#SBATCH -p bansil
#SBATCH -n 64
#SBATCH -N 1
#SBATCH -J NbSe2
#SBATCH -o adiabatic.out

module load anaconda3/2022.01
source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
QE=/work/bansil/s.sevim/software/q-e/bin

# mkdir ./inputs
# mkdir ./outputs
for sigma in  0.05 0.04 0.03 0.02 0.01 0.009 0.008 0.007 0.006 0.005 0.001 0.0005 0.0001
do
# python vc-relax-generate.py $sigma
# mpirun -n 64 $QE/pw.x -inp ./inputs/$sigma-vc-relax.in > ./outputs/$sigma-vc-relax.out
# cp ./outputs/$sigma.vc-relax.out ./example_data/vc-relax.out
# python run.py -c relax -d $sigma -k 20 20 1 0 0 0
# mpirun -n 64 $QE/pw.x -inp ./inputs/$sigma-relax.in > ./outputs/$sigma-relax.out
# python run.py -c scf -d $sigma -k 30 30 1 0 0 0
# mpirun -n 64 $QE/pw.x -inp ./inputs/$sigma-scf.in > ./outputs/$sigma-scf.out
# python run.py -c bands -d $sigma
# mpirun -n 64 $QE/pw.x -inp ./inputs/$sigma-bands.in > ./outputs/$sigma-bands.out
python run.py -c bands-pp -d $sigma
mpirun -n 64 $QE/bands.x -inp ./inputs/$sigma-bands-pp.in > ./outputs/$sigma-bands-pp.out

echo "bands-pp $sigma is done"
done
