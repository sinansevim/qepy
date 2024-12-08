from src import esma
import copy
import numpy as np

def init_model():
    model = esma.project(project_id="NbSe2_strain_disorder_2sq3_x_2sq3")
    model.set_cores(256) #Define number of prcessing cores
    model.get_structure(format="poscar",path="./Structures/NbSe2_2sq2_x_2sq2.poscar")
    model.set_pseudo(path="./Pseudopotentials/PBE/PAW")
    model.ecutwfc(100) #Set wavefunction cutoff
    model.ecutrho(600) #Set wavefunction cutoff
    model.k_points([12,12,1]) #Set number of k points
    model.degauss(0.01) #Set degauss value
    model.conv_thr(1e-8) #Set convergence threshold
    model.smearing('fd')
    model.etot_conv_thr(10**-5)
    model.forc_conv_thr(10**-4)
    model.config['pw']['system']['nosym']=True
    return model




def workflow():
    model = init_model()

    models = []
    strain = np.arange(0.96,1.05,0.01)
    for i in strain:
        temp_model = copy.deepcopy(model)
        temp_model.strain(axis=['x','y'],value=i)
        models.append(temp_model)

    for j,i in enumerate(models):
        disordered_models = i.disorder(number_of_states=5)
        for k,model in enumerate(disordered_models):
            model.job_id=f"strain_{strain[j]}_state_{k}"
            model.optimize(calculation='relax',max_iter=1)
            model.calculate('scf')
    # energy = model.get_total_energy()
    # print(f"{model.job_id} {energy}")

workflow()



