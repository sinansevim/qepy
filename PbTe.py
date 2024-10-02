from src import esma

def init_model():
    model = esma.project(project_id='PbTe')
    model.set_pseudo(path="/scratch/s.sevim/espresso-machine/Pseudopotentials/PBE/PAW")
    model.get_structure(format="poscar",path="/scratch/s.sevim/espresso-machine/Structures/PbTe.poscar")
    model.set_cores(64)
    model.ecutwfc(100) #Set wavefunction cutoff
    model.ecutrho(600) #Set wavefunction cutoff
    model.k_points([12,12,1]) #Set number of k points
    model.degauss(0.01) #Set degauss value
    model.conv_thr(1e-8) #Set convergence threshold
    model.smearing('fd')
    model.electron_maxstep(500) #Max number of electron iteration
    model.exchange_maxstep(500) #Max number of exchange iteration
    model.etot_conv_thr(10**-6)
    model.forc_conv_thr(10**-5)
    model.mixing_mode('local-TF')
    return model
model = init_model()

model.cell_dof('2Dxy') #Fix cell relaxation to 2D

model.optimize('relax')
model.optimize('vc-relax')
model.optimize('relax')

model.k_points([36,36,1]) #Set number of k points
model.conv_thr(1e-12) #Set convergence threshold
model.ph_thr(1e-16) #Set convergence threshold

model.calculate('scf')
model.set_q(nq1=12,nq2=12,nq3=1) #Set parameters
model.calculate('ph')

model.calculate('q2r') #Run calculation
path = ['GAMMA','M',"K","GAMMA"] #define corners
model.band_points(path,number=50) #define path
model.calculate('bands')
model.plot('electron',ylim=[-3,3],save=True) #plot electron bands

num_points = 200 # Number of q points
model.calculate("matdyn") #Run calculation
model.plot('phonon',save=True) # Plot phonon band


