from src import esma
model = esma.project(project_id='MnTe_SOC')
model.set_pseudo(path="/work/bansil/s.sevim/Test/espresso-machine/Pseudopotentials/PBE/US/SOC")
model.get_structure(format="poscar",path="/work/bansil/s.sevim/Test/espresso-machine/Structures/MnTe.poscar")
model.set_cores(128)
model.ecutwfc(100) #Set wavefunction cutoff
model.ecutrho(1000) #Set wavefunction cutoff
model.k_points([8,8,5]) #Set number of k points
model.degauss(0.01) #Set degauss value
model.conv_thr(1e-6) #Set convergence threshold
model.smearing('mv')
model.electron_maxstep(500) #Max number of electron iteration
model.exchange_maxstep(500) #Max number of exchange iteration
model.mixing_beta(0.2)
model.hubbard(atom='Mn',orbital='3d',value=3)

points = [
            ['GAMMA',0,0,0],
            ['M',0.5,0,0],
            ["M'",0.5,0,0.35],
            ["GAMMA'",0,0,0.35],
            ["K",0.33333,0.3333,0]
            ]

import copy
import numpy as np

models = []
strain = np.arange(0.96,1.042,0.002)
strains = [[i,j] for i in strain for j in strain]
for i in strains:
    temp_model = copy.deepcopy(model)
    temp_model.strain(axis=['x','y'],value=i[0])
    temp_model.strain(axis=['z'],value=i[1])
    models.append(temp_model)

def workflow(model,id):
    afm = model.magnetize(magnetic_atom='Mn',angle1=90,angle2=30)[1]    
    afm.soc()
    afm.job_id = f"strain_xy_{id[0]}_z_{id[1]}"
    afm.calculate('scf')
    path = ['K','GAMMA','K'] #choose corners
    afm.band_points(path,number=50,points=points) #define path
    afm.calculate('bands',pp_core=8)
    a = round(float(model.cell()[0][0]),3)
    ac = round(float(model.cell()[2][2])/float(model.cell()[0][0]),3)
    epsilon_xy = round(id[0]-1,3)
    epsilon_z = round(id[1]-1,3)
    afm.plot('electron',ylim=[9,13],save=True,figsize=(4,6),save_name='plot_KGK',title=fr"$\epsilon xy$={epsilon_xy} $\epsilon z$={epsilon_z} a={a} c/a={ac}") #plot electron bands
    path = ['M','GAMMA','M'] #choose corners
    afm.band_points(path,number=50,points=points) #define path
    afm.calculate('bands',pp_core=8)
    afm.plot('electron',ylim=[9,13],save=True,figsize=(4,6),save_name='plot_MGM',title=fr"$\epsilon xy$={epsilon_xy} $\epsilon z$={epsilon_z} a={a} c/a={ac}") #plot electron bands
    # path = ["M'","GAMMA'","M'"] #choose corners
    # afm.band_points(path,number=100,points=points,save_name='plot_MGM') #define path
    # afm.calculate('bands',pp_core=32)
try:
    for i,model in enumerate(models):
        workflow(model,strains[i])
except:
    pass
