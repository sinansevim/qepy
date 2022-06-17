#!/bin/zsh

mkdir ./inputs
mkdir ./outputs
for sigma in 0.04 0.03 0.02 0.01 0.009 0.008 0.007 0.006 0.005 0.001 0.0005 0.0001
do
python vc-relax-generate.py $sigma
mpirun -n 64 $QE/pw.x -inp ./inputs/$sigma.vc-relax.in > ./outputs/$sigma.vc-relax.out
cp ./outputs/$sigma.vc-relax.out ./example_data/vc-relax.out
echo "$sigma is done"
done
