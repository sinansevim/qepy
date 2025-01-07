#!/bin/bash 
#SBATCH --partition bansil2
#SBATCH --nodes     2
#SBATCH --ntasks    128
#SBATCH --job-name  d2
#SBATCH --output    d2.out
#SBATCH --time=30-00:00:00


export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"
source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
source .venv/bin/activate
python3 NbSe2_d2.py