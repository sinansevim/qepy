from src import esma

def init_model():
    model = esma.project(project_id='IrSbSe')
    model.set_pseudo(path="/scratch/s.sevim/espresso-machine/Pseudopotentials/PBE/US")
    model.get_structure(format="poscar",path="/scratch/s.sevim/espresso-machine/Structures/IrSbSe.poscar")
    model.set_cores(256)
    model.ecutwfc(200) #Set wavefunction cutoff
    model.ecutrho(800) #Set wavefunction cutoff
    model.k_points([12,12,12]) #Set number of k points
    model.degauss(0.03) #Set degauss value
    model.conv_thr(1e-8) #Set convergence threshold
    model.smearing('fd')
    model.electron_maxstep(500) #Max number of electron iteration
    model.exchange_maxstep(500) #Max number of exchange iteration
    model.etot_conv_thr(10**-6)
    model.forc_conv_thr(10**-5)
    model.mixing_mode('local-TF')
    return model
model = init_model()

# model.cell_dof('2Dxy') #Fix cell relaxation to 2D

model.optimize('vc-relax')
# model.optimize('relax')

model.k_points([4,4,4]) #Set number of k points
model.conv_thr(1e-10) #Set convergence threshold
model.ph_thr(1e-14) #Set convergence threshold

model.calculate('scf')
model.set_q(nq1=2,nq2=2,nq3=2) #Set parameters
model.calculate('ph')

model.calculate('q2r') #Run calculation
path = ['GAMMA','M',"K","GAMMA"] #define corners
model.band_points(path,number=50) #define path
model.calculate('bands')
model.plot('electron',ylim=[-3,3],save=True) #plot electron bands

num_points = 200 # Number of q points
model.calculate("matdyn") #Run calculation
model.plot('phonon',save=True) # Plot phonon band


