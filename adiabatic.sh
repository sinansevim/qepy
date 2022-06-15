#!/bin/zsh

mkdir ./inputs
for sigma in 0.05 0.04 0.03 0.02 0.01 0.009 0.008 0.007 0.006 0.005 0.001 0.0005 0.0001
do
python generate.py $sigma
# mpirun -n 64 $QE/pw.x -inp $sigma.in > $sigma.out
cp ./inputs/$sigma.in ./example_data/vc_relax.out
done
