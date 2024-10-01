#!/bin/bash 
#SBATCH --partition bansil2
#SBATCH --nodes     1
#SBATCH --ntasks    128
#SBATCH --job-name  xy_z
#SBATCH --output    xy_z.out


export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"
source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
source .venv/bin/activate
python3 MnTe_xy_z.py
