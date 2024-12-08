#!/bin/bash 
#SBATCH --partition bansil2
#SBATCH --nodes     4
#SBATCH --ntasks    256
#SBATCH --job-name  ph_us
#SBATCH --output    ph_us.out
#SBATCH --time=30-00:00:00


export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"
source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
source .venv/bin/activate
python3 PbTe_us.py