import src as esma #Import library
model = esma.project(project_id='UTe3')
model.set_cores(128)
model.get_structure(format='poscar')
model.set_pseudo("US")
model.ecutwfc(120) #Set wavefunction cutoff
model.ecutrho(750)  
model.degauss(0.02) #Set degauss value
model.conv_thr(1e-6) #Set convergence threshold
model.smearing('mv')
model.k_points(8) #Set number of k points
model.hubbard(atom='U',orbital='5f',value=4)
model.config['pw']['electrons']['mixing_mode']='local-TF'
models = model.magnetise(magnetic_atom='U')
for i,state in enumerate(models):
    #Adjust parameters
    state.calculate('vc-relax')
for i,state in enumerate(models):
    state.get_structure('vc-relax') #Get vc-relaxed strucutre
    state.calculate('scf')
ground_state = esma.minimum_energy(models)
# ground_state.job_id='soc'
# ground_state.config['pw']['electrons']['mixing_beta'] = 0.1
# ground_state.config['pw']['system']['noncolin']=True
# ground_state.config['pw']['system']['lspinorb']=True
# ground_state.config['pw']['electrons']['diagonalization']='cg'

# del ground_state.config['pw']['system']['nspin']
# ground_state.set_pseudo("US/REL")
# ground_state.debug=False
# ground_state.calculate('scf')
path = ['GAMMA','X',"L_0","T","W","R"] #define corners
num_points = 50 #number of points
ground_state.band_points(path,num_points) #define path
ground_state.calculate('bands')
ground_state.plot('electron',ylim=[-20,30]) #plot electron bands