#### Local testing variables ####
#Path to quantum-espresso
QE=/path/to/quantum/espresso
#Number of cores
SLURM_NTASKS=number_of_cores

#Initial degauss value (0 for POSCAR initialization)
initial=0
#POSCAR file
POSCAR=C.poscar

#vc-relax k points
vc_relax_k=('4 4 2 0 0 0')
relax_k=('4 4 1 0 0 0')
scf_k=('4 4 1 0 0 0')


echo "Espresso Machine is starting"
#Smearing parameters
for sigma in 0.05 
do
echo "Adiabatic automation for $sigma is started"

#Crystal relaxation
if [ $initial -eq 0 ]
then 
    echo "Generating crystal relaxation input from POSCAR for $sigma"
    python run.py -c vc-relax -d $sigma -p $POSCAR -k ${vc_relax_k[@]}
else 
    echo "Generating crystal relaxation input from output for $sigma"
    python run.py -c vc-relax -d $sigma -i ./results/$initial/vc-relax.out -k ${vc_relax_k[@]}
fi

echo "Calculating crystal relaxation for $sigma"
mpirun -np $SLURM_NTASKS $QE/pw.x -inp ./results/$sigma/vc-relax.in > ./results/$sigma/vc-relax.out
echo "Crystal relaxation for $sigma is finished"

#Atom Relaxation
echo "Generating relaxation input for $sigma"
python run.py -c relax -d $sigma -k ${relax_k[@]}
echo "Starting relaxation for $sigma"
mpirun -n $SLURM_NTASKS $QE/pw.x -inp ./results/$sigma/relax.in > ./results/$sigma/relax.out
echo "Atom relaxation for $sigma is finished"

#Scf calculation
echo "Scf input for $sigma is generated"
python run.py -c scf -d $sigma -k ${scf_k[@]}
echo "Scf calculation for $sigma is started"
mpirun -n $SLURM_NTASKS $QE/pw.x -inp ./results/$sigma/scf.in > ./results/$sigma/scf.out
echo "Scf calculation for $sigma is finished"

#Band calculation
echo "Band calculation input for $sigma is generated"
python run.py -c bands -d $sigma
echo "Band calculation for $sigma is started"
mpirun -n $SLURM_NTASKS $QE/pw.x -inp ./results/$sigma/bands.in > ./results/$sigma/bands.out
echo "Band-pp for $sigma is generated"
python run.py -c bands-pp -d $sigma
echo "Band-pp calculation $sigma is started"
mpirun -n $SLURM_NTASKS $QE/bands.x -inp ./results/$sigma/bands-pp.in > ./results/$sigma/bands-pp.out
python ./src/plot_band.py -d $sigma

echo "Adiabatic automation for $sigma is completed"
##Memorize the last calculation
initial=$sigma
done 

echo "Adiabatic automation is completed"
echo "vc-relax > relax > scf > band"

# # mkdir dyn
# # mkdir dyn/$sigma/
# # python run.py -c ph -d $sigma
# # mpirun -n 256 $QE/ph.x -npool 256 -inp ./inputs/$sigma-ph.in > ./outputs/$sigma-ph.out
# # python run.py -c q2r -d $sigma
# # $QE/q2r.x  < ./inputs/$sigma-q2r.in > ./outputs/$sigma-q2r.out
# # python run.py -c matdyn -d $sigma
# # $QE/matdyn.x  < ./inputs/$sigma-matdyn.in > ./outputs/$sigma-matdyn.out
# # python run.py -c plotband -d $sigma
# # cd ./dyn/$sigma/
# # $QE/plotband.x  < $sigma-plotband.in > $sigma-plotband.out
# # cd ../..
# # bash ph.sh $QE $sigma
# python ph_plot.py -d $sigma
