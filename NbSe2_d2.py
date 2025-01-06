from src import esma

def project():
    model = esma.project(project_id="NbSe2_d2") #Define project
    model.set_cores(128) #Define number of prcessing cores
    model.get_structure(path="Structures/NbSe2-1L.poscar")
    model.set_pseudo(path="Pseudopotentials/PBE/PAW")
    model.ecutwfc(100) #Set wavefunction cutoff
    model.ecutrho(600) #Set wavefunction cutoff
    model.k_points([36,36,1]) #Set number of k points
    model.degauss(0.01) #Set degauss value
    model.conv_thr(1e-12) #Set convergence threshold
    model.ph_thr(1e-16) #Set convergence threshold
    model.smearing('fd')
    model.etot_conv_thr(10**-6)
    model.forc_conv_thr(10**-5)
    model.mixing_mode('local-TF')
    model.vdw_corr('dft-d')
    model.cell_dof('2Dxy') #Fix cell relaxation to 2D
    return model

def workflow(model,degauss):
    model.job_id=degauss
    model.degauss(degauss) #Set degauss value
    model.optimize(calculation='vc-relax',max_iter=1)
    model.optimize(calculation='relax',max_iter=1)
    model.set_q(nq1=12,nq2=12,nq3=1) #Set parameters
    model.calculate('ph')
    model.calculate('q2r') #Run calculation
    path = ['GAMMA','M',"K","GAMMA"] #define corners
    model.band_points(path,number=100) #define path
    model.calculate("matdyn") #Run calculation
    model.plot('phonon',save=True) # Plot phonon band


def run():
    sigmas = [0.006,0.005,0.004,0.003,0.002,0.001,0.0009,0.0008]
    for degauss in sigmas:
        model = project()
        workflow(model,degauss)

run()