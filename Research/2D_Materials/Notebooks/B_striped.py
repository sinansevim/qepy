from . import src as src
#Initialize model
model = src.project(project_id="B_striped") #Define project
model.set_cores(64) #Define number of prcessing cores
model.get_structure(format='poscar',path='Research/2D_Materials/Structure/',name='B_striped.poscar') #Load structure
model.set_pseudo(path='./Research/2D_Materials/PP/PBE/US')

#Define model parameters
model.ecutwfc(100) #Set wavefunction cutoff
model.ecutrho(800) #Set wavefunction cutoff
model.k_points([40,30,1]) #Set number of k points
model.degauss(0.02) #Set degauss value
model.conv_thr(1e-12) #Set convergence threshold
model.ph_thr(1e-16) #Set convergence threshold
model.smearing('mv')
model.etot_conv_thr(10**-7) 
model.forc_conv_thr(10**-6)
model.config['pw']['electrons']['electron_maxstep'] = 500
model.config['pw']['electrons']['exx_maxstep'] = 500
model.config['pw']['electrons']['mixing_beta'] = 0.1
model.stress()
model.force()

#PW
model.relax_iteration(calculation='relax',max_iter=20) #Relax structure iteratively
model.calculate('scf') #scf calculation

#PH
model.set_q(nq1=13,nq2=11,nq3=1) #Set parameters
model.calculate('ph') #run ph calculations
model.calculate('q2r') #run q2r
path = ['S','X',"GAMMA","Y","S","GAMMA"] #define corners
num_points = 200 # Number of q points
model.band_points(path,num_points) #define path
model.calculate("matdyn") #run matdyn
model.plot('phonon',save=True) # Plot phonon band