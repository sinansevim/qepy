import src as esma #Import library
model = esma.project(project_id='UTe2')
model.gpu=True
model.get_structure(format='poscar')
model.set_pseudo("US")
model.ecutwfc(120) #Set wavefunction cutoff
model.ecutrho(750)  
model.degauss(0.02) #Set degauss value
model.conv_thr(1e-6) #Set convergence threshold
model.k_points(8) #Set number of k points
model.hubbard(atom='U',orbital='5f',value=4)
model.smearing('mv')
model.config['pw']['electrons']['mixing_mode']='local-TF'
model.debug=True
models = model.magnetise(magnetic_atom='U')

for i,state in enumerate(models):
    #Run vc-relax
    # state.config['pw']['electrons']['mixing_beta'] = 0.1
    state.calculate('vc-relax')
for i,state in enumerate(models):
    #Get structures and start scf
    state.get_structure('vc-relax') #Get vc-relaxed strucutre
    state.calculate('scf')
ground_state = esma.minimum_energy(models)
ground_state.debug=False
path = ['GAMMA','X',"L_0","T","W","R"] #define corners
num_points = 50 #number of points
ground_state.band_points(path,num_points) #define path
ground_state.calculate('bands')
ground_state.plot('electron',ylim=[-20,30]) #plot electron bands