#!/bin/bash
#SBATCH --partition bansil-gpu
#SBATCH --job-name  remote-gpu
#SBATCH --output    remote-gpu.out
#SBATCH --nodes=1                # node count
#SBATCH --ntasks-per-node=4      # number of tasks per node
#SBATCH --cpus-per-gpu=1      # cpu-cores per task 
#SBATCH --mem=0              # total memory per node
#SBATCH --gres=gpu:4           # number of gpus per node
#SBATCH --nodelist  d3227


module load singularity
source /work/bansil/s.sevim/remote-deploy/espresso-machine/.venv/bin/activate
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
python job_gpu.py

# QE=/work/bansil/s.sevim/software/qe-gpu/qe-7.1-gpu.sif
# PROJECT_ID=UTe2
# CALCULATION=vc-relax
# JOB_ID=afm3
# # for JOB_ID in fm afm1 afm2 afm3
# # do
# srun --mpi=pmi2 singularity run --nv $QE pw.x -inp ./Projects/$PROJECT_ID/$JOB_ID/$CALCULATION.in >  ./Projects/$PROJECT_ID/$JOB_ID/$CALCULATION.out
# # done
