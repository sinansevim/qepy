QE=/usr/bin/
SLURM_NTASKS=1
project_name=Graphene_ecutwfc
    
echo Starting ecutwfc calculation
for file_name in ecutwfc_10 ecutwfc_20 ecutwfc_30 ecutwfc_40 ecutwfc_50 ecutwfc_60 ecutwfc_70 ecutwfc_80 ecutwfc_90 ecutwfc_100
do
echo $file_name is started
mpirun -n $SLURM_NTASKS $QE/pw.x -inp ./$project_name/$file_name/scf.in > ./$project_name/$file_name/scf.out
echo $file_name is done
done
echo All ecutwfc calculations are completed
    