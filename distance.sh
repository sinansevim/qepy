QE=/usr/bin/
SLURM_NTASKS=1
project_name=Graphene_distance
    
echo Starting distance calculation
for file_name in distance_0.05 distance_0.06 distance_0.08 distance_0.1 distance_0.11 distance_0.12 distance_0.14 distance_0.16 distance_0.17 distance_0.19 distance_0.2
do
echo $file_name is started
mpirun -n $SLURM_NTASKS $QE/pw.x -inp ./$project_name/$file_name/scf.in > ./$project_name/$file_name/scf.out
echo $file_name is done
done
echo All distance calculations are completed
    