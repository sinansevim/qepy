from src import esma

def init_model():
    model = esma.project(project_id='PbTe_US_hess')
    model.set_pseudo(path="/scratch/s.sevim/espresso-machine/Pseudopotentials/PBE/US")
    model.get_structure(format="poscar",path="/scratch/s.sevim/espresso-machine/Structures/PbTe.poscar")
    model.set_cores(256)
    model.ecutwfc(200) #Set wavefunction cutoff
    model.ecutrho(800) #Set wavefunction cutoff
    model.k_points([16,16,1]) #Set number of k points
    model.degauss(0.03) #Set degauss value
    model.conv_thr(1e-12) #Set convergence threshold
    model.ph_thr(1e-16) #Set convergence threshold
    model.smearing('fd')
    model.electron_maxstep(500) #Max number of electron iteration
    model.exchange_maxstep(500) #Max number of exchange iteration
    model.etot_conv_thr(10**-5)
    model.forc_conv_thr(10**-4)
    model.mixing_mode('local-TF')
    model.config['pw']['system']['vdw_corr']='dft-d'
    model.config['pw']['system']['dftd3_threebody']=False
    # model.nbnd(26)
    # model.mixing_beta(0.2)
    return model
model = init_model()

model.cell_dof('2Dxy') #Fix cell relaxation to 2D
model.optimize('relax')
model.optimize('vc-relax')
model.optimize('relax')

model.calculate('scf')
# model.calculate("d3hess")

model.set_q(nq1=8,nq2=8,nq3=1) #Set parameters
model.calculate('ph')

model.calculate('q2r') #Run calculation
path = ['GAMMA','M',"K","GAMMA"] #define corners
model.band_points(path,number=50) #define path
# model.calculate('bands')
# model.plot('electron',ylim=[-3,3],save=True) #plot electron bands

num_points = 200 # Number of q points
model.calculate("matdyn") #Run calculation
model.plot('phonon',save=True) # Plot phonon band


