from src import espresso_machine as esma

 #Step 1 - Initialize model
model = esma.project(project_id="TiSe2") #Define project
model.set_cores(64) #Define number of prcessing cores
model.get_structure(format='poscar',path='./Research',name='/TiSe2/TiSe2.poscar') #Load structure
model.set_pseudo(path='./Research/TiSe2')
model.ecutwfc(100) #Set wavefunction cutoff
model.ecutrho(700) #Set wavefunction cutoff
model.k_points(16) #Set number of k points
model.conv_thr(1e-8) #Set convergence threshold
model.smearing('fd')
model.shift_atoms([0,0,0.5]) #Shift Te atom to the middle
model.config['pw']['control']['etot_conv_thr'] = 10**-5
model.config['pw']['control']['forc_conv_thr'] = 10**-4
model.nbnd(40)

def pipeline(model):
     #Step 1 - Crystal optimization
    model.calculate('vc-relax')

     #Step 2 - Atomic optimization
    model.get_structure('vc-relax') #Get vc-relaxed strucutre
    model.add_vacuum('z',[0,0,5]) #Add vacuum on z direction
    model.k_points([16,16,1])
    model.calculate('relax')

     #Step 3 - Scf calculation
    model.get_structure('relax') #Get relaxed strucutre
    model.calculate('scf')

     #Step 4 - Bands calculation
    path = ['GAMMA','M',"K","GAMMA"] #define corners
    model.band_points(path,number=50) #define path
    model.calculate('bands')

     #Step 5 - Electron Plotting
    model.plot('electron',ylim=[-3,3],save=True) #plot electron bands

     # Step 6 - Run ph.x
    model.set_q(nq1=8,nq2=8,nq3=1) #Set parameters
    model.calculate('ph')

     #Step- 7 - Run q2r.x
    model.calculate('q2r') #Run calculation

     #Step 8 - Run matdyn.x
    num_points = 200 # Number of q points
    model.calculate("matdyn") #Run calculation

     #Step 9 - Phonon Plotting
    model.plot('phonon',save=True) # Plot phonon band

sigmas = [0.05,0.04,0.03,0.02,0.01]

import copy 
models = [copy.deepcopy(model) for i in range(len(sigmas))] 


for i,sigma in enumerate(sigmas):
    models[i].job_id = sigma
    models[i].degauss(sigma)
    pipeline(models[i])

    