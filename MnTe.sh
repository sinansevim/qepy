#!/bin/bash 
#SBATCH -N 1 
#SBATCH -n 64
#SBATCH -J python
#SBATCH -p bansil
#SBATCH --output=MnTe.out
#SBATCH --time=7-00:00:00
#SBATCH --mem=0
#module load anaconda3/2022.01

module load git

export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"

source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
source /home/s.sevim/miniforge3/etc/profile.d/conda.sh
source /home/s.sevim/miniforge3/etc/profile.d/mamba.sh
conda activate esma
# conda info --envs
jupyter-lab --no-browser  --ip "*" --notebook-dir ./





# source ~/miniconda/bin/mamba
# export PATH="/work/bansil/s.sevim/software/qe-7.3/q-e/bin/:$PATH"
# source /shared/centos7/intel/oneapi/2022.1.0/setvars.sh
# source .venv/bin/activate

#source /work/bansil/s.sevim/Work/typy/.venv/bin/activate
# jupyter-lab --no-browser  --ip "*" --notebook-dir /scratch/s.sevim/espresso-machine
#ssh -L 8888:d3040:8888 s.sevim@login.discovery.neu.edu
