from src import esma
#Step 1 - Initialize model
model = esma.project(project_id="TiSe2") #Define project
model.set_cores(64) #Define number of prcessing cores
model.get_structure(format="poscar",path="/work/bansil/s.sevim/Test/espresso-machine/Structures/TiSe2.poscar")
model.set_pseudo(path="/work/bansil/s.sevim/Test/espresso-machine/Pseudopotentials/PBE/PAW")
model.ecutwfc(80) #Set wavefunction cutoff
model.ecutrho(800) #Set wavefunction cutoff
model.k_points([16,16,1]) #Set number of k points
model.degauss(0.05) #Set degauss value
model.conv_thr(1e-12) #Set convergence threshold
model.ph_thr(1e-16) #Set convergence threshold
model.smearing('fd')
model.etot_conv_thr(10**-5)
model.forc_conv_thr(10**-4)

model.cell_dof('2Dxy') #Fix cell relaxation to 2D
model.optimize(calculation='relax',max_iter=1)
model.optimize(calculation='vc-relax',max_iter=1)
model.optimize(calculation='relax',max_iter=1)

model.calculate('scf')
model.set_q(nq1=8,nq2=8,nq3=1) #Set parameters
model.calculate('ph')

model.calculate('q2r') #Run calculation
path = ['GAMMA','M',"K","GAMMA"] #define corners
model.band_points(path,number=50) #define path
model.calculate('bands')
model.plot('electron',ylim=[-3,3],save=True) #plot electron bands

num_points = 200 # Number of q points
model.calculate("matdyn") #Run calculation
model.plot('phonon',save=True) # Plot phonon band


