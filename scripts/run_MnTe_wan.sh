#!/bin/bash 
#SBATCH --partition bansil2
#SBATCH --nodes     1
#SBATCH --ntasks    128
#SBATCH --job-name  MnTe_wan
#SBATCH --output    MnTe_wan.out


export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"
source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
source .venv/bin/activate
python3 MnTe_wannier.py > MnTe_wan.py.out
