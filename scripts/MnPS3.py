from src import esma

def init_model():
    model = esma.project(project_id='MnPS3')
    model.set_pseudo(path="/scratch/s.sevim/espresso-machine/Pseudopotentials/PBE/US")
    model.get_structure(format="poscar",path="/scratch/s.sevim/espresso-machine/Structures/MnPS3.poscar")
    model.set_cores(64)
    model.ecutwfc(100) #Set wavefunction cutoff
    model.ecutrho(1000) #Set wavefunction cutoff
    model.k_points([6,3,5]) #Set number of k points
    model.degauss(0.02) #Set degauss value
    model.conv_thr(1e-6) #Set convergence threshold
    model.smearing('mv')
    # model.mixing_beta(0.2)
    model.electron_maxstep(500) #Max number of electron iteration
    model.exchange_maxstep(500) #Max number of exchange iteration
    model.hubbard(atom='Mn',orbital='3d',value=4)
    model.mixing_mode('local-TF')
    return model

def run_model():
    energies={}
    for theta in [0,90]:
        for phi in [0,90,180]:
            model=init_model()
            models = model.magnetize(magnetic_atom='Mn',angle1=theta,angle2=phi)
            for j,state in enumerate(models):
                state.job_id=f"state_{j}_{theta}_{phi}"
                try:
                    sta
                    energies[f"theta_pi_te.calculate('scf')j"] = state.energy()
                except:
                    print(theta,phi,state,"error")


run_model()