from src import esma
import copy
import numpy as np

def init_model():
    model = esma.project(project_id="NbSe2_strain_disorder_2r3x2r3")
    model.set_cores(256) #Define number of prcessing cores
    model.get_structure(path="Structures/NbSe2-1L.poscar")
    model.set_pseudo(path="./Pseudopotentials/PBE/PAW")
    model.ecutwfc(100) #Set wavefunction cutoff
    model.ecutrho(600) #Set wavefunction cutoff
    model.k_points([8,8,1]) #Set number of k points
    model.degauss(0.01) #Set degauss value
    model.conv_thr(1e-8) #Set convergence threshold
    model.smearing('fd')
    model.etot_conv_thr(10**-5)
    model.forc_conv_thr(10**-4)
    model.nosym(True)
    model.mixing_mode('local-TF')
    return model




def workflow():
    model = init_model()
    models = []
    strain = np.arange(1,1.10,0.01)
    for i in strain:
        temp_model = copy.deepcopy(model)
        temp_model.strain(axis=['x','y'],value=i)
        models.append(temp_model)

    for j,model in enumerate(models):
        model.job_id=f"strain_{strain[j]}_state_pristine"
        model.optimize(calculation='relax',max_iter=1)
        model.calculate('scf')
        model.supercell(scaling_matrix=[[4,2,0],[2,4,0],[0,0,1]])
        model.job_id=f"strain_{strain[j]}_state_supercell"
        model.calculate('scf')
        disordered_models = model.disorder(number_of_states=3,scale=0.1)
        for k,state in enumerate(disordered_models):
            state.job_id=f"strain_{strain[j]}_state_{k+1}"
            state.optimize(calculation='relax',max_iter=1)
            state.calculate('scf')
    # energy = model.get_total_energy()
    # print(f"{model.job_id} {energy}")

workflow()



