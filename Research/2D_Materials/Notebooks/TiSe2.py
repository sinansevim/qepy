from src import espresso_machine as esma
#Step 1 - Initialize model
model = esma.project(project_id="TiSe2") #Define project
model.set_cores(128) #Define number of prcessing cores
model.get_structure(format='poscar',name="TiSe2.poscar",path='./Research/2D_Materials/Structure/') #Load structure
model.set_pseudo(path='./Research/2D_Materials/PP/PBE/US/')
#Adjust Parameters
model.ecutwfc(100) #Set wavefunction cutoff
model.ecutrho(800) #Set wavefunction cutoff
model.k_points([24,24,1]) #Set number of k points
model.degauss(0.02) #Set degauss value
model.conv_thr(1e-12) #Set convergence threshold
model.ph_thr(1e-16) #Set convergence threshold
model.smearing('mv') #Marzari-Vanderbilt smearing
model.etot_conv_thr(10**-7) #Energy convergence threshold for optimization
model.forc_conv_thr(10**-6) #Force optimization threshold
model.electron_maxstep(500) #Max number of electron iteration
model.exchange_maxstep(500) #Max number of exchange iteration
model.mixing_beta(0.1)      #SCF cycle potential mixing value

model.stress()  #Print stress out
model.force()   #Print forces out

model.calculate('scf')
path = ['GAMMA','M',"K","GAMMA"] #define corners
num_points = 50 #Number of points
model.band_points(path,num_points) #define path
model.calculate('bands')
model.plot('electron',ylim=[-3,3],save=True) #plot electron bands
model.set_q(nq1=12,nq2=12,nq3=1) #Set parameters
model.calculate('ph')
model.calculate('q2r') #Run calculation    
model.calculate("matdyn") #Run calculation
model.plot('phonon',save=True) # Plot phonon band
