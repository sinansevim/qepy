#!/bin/bash 
#SBATCH --partition bansil-gpu
#SBATCH --nodes     1
#SBATCH --job-name  T-gpu
#SBATCH --output    T-gpu.out
#SBATCH --gres=gpu:1           # number of gpus per node
#SBATCH --ntasks-per-node=1      # number of tasks per node
#SBATCH --cpus-per-gpu=16      # cpu-cores per task 
#SBATCH --mem=0              # total memory per node



module load singularity
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
# export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"
# source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
# source .venv/bin/activate
python3 TiSe2_gpu.py
