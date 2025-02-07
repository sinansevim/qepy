from src import esma

def init_model():
    model = esma.project(project_id='MnTe_HP_NONCOL')
    # model.set_pseudo(path="/scratch/s.sevim/espresso-machine/Pseudopotentials/PBE/US")
    model.set_pseudo(path="/scratch/s.sevim/espresso-machine/Pseudopotentials/PBE/US/SOC")
    model.get_structure(format="poscar",path="/scratch/s.sevim/espresso-machine/Structures/MnTe.poscar")
    model.set_cores(64)
    model.ecutwfc(100) #Set wavefunction cutoff
    model.ecutrho(1000) #Set wavefunction cutoff
    model.k_points([8,8,5]) #Set number of k points
    model.degauss(0.01) #Set degauss value
    model.conv_thr(1e-8) #Set convergence threshold
    model.smearing('mv')
    model.mixing_beta(0.2)
    model.electron_maxstep(500) #Max number of electron iteration
    model.exchange_maxstep(500) #Max number of exchange iteration
    model.mixing_mode('local-TF')
    model.etot_conv_thr(10**-4)
    model.forc_conv_thr(10**-3)
    return model

model = init_model()

model.hubbard(atom='Mn',orbital='3d',value=0.0001)
afm = model.magnetize(magnetic_atom='Mn',angle1=90,angle2=30)[1]
afm.soc()
afm.calculate('scf')
model.calculate('hp')