import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import subprocess
import json
import qcelemental as qcel
import untangle
import copy
import math
import glob
from . import compute
from .configs.config import defaultConfig
import qmsa


def check_relax(path):
    lines = open(path, 'r').readlines()
    for i in lines:
        if "bfgs failed after" in i:
            return False
        if "bfgs converged" in i:
            return True

def k_grid(num_points, factor=1,spacing=True):
    if type(num_points)==list:
        if len(num_points)==3:
            x = np.linspace(0, 1, num_points[0], endpoint=False)
            y = np.linspace(0, 1, num_points[1], endpoint=False)
            z = np.linspace(0, 1, num_points[2], endpoint=False)
        elif len(num_points)==1:
            x = np.linspace(0, 1, num_points[0], endpoint=False)
            y = np.linspace(0, 1, num_points[0], endpoint=False)
            z = np.linspace(0, 1, num_points[0], endpoint=False)

    elif type(num_points)==int:
        x = np.linspace(0, 1, num_points, endpoint=False)
        y = np.linspace(0, 1, num_points, endpoint=False)
        z = np.linspace(0, 1, num_points, endpoint=False)
    if spacing!=False:
        spacing = round(1/(len(x)*len(y)*len(z)),12)
        three_dim = np.array([[i, j,k,spacing] for i in x for j in y for k in z])
    else:
        three_dim = np.array([[i, j,k] for i in x for j in y for k in z])
    return (three_dim*factor)

def shift_cell(atom,cell,direction,vector):
    vacuum_atom = np.dot(atom,cell)+vector
    directions = ['x','y','z']
    shift_matrix = np.zeros(shape=(3,3))
    for i,j in enumerate(directions):
        if direction==j:
            shift_matrix[i]=np.array(vector)*2
    cell_vacuum = cell+shift_matrix
    frac_vacuum = np.dot(vacuum_atom,np.linalg.inv(cell_vacuum))

    return frac_vacuum,cell_vacuum



def shift_frac(atoms,vector):
    return np.mod(atoms+vector,1)

def make_monolayer(atoms,direction='z'):
    direction = direction.lower()
    if direction not in ['x','y','z']:
        raise Exception("Direction should be x y or z")
    df = pd.DataFrame()
    atoms=np.array(atoms)
    df['Atoms'] = atoms.T[0]
    df['x'] = atoms.T[1].astype(float)
    df['y'] = atoms.T[2].astype(float)
    df['z'] = atoms.T[3].astype(float)
    df = df.query(f'{direction}<0.5')
    df_shifted = pd.DataFrame()
    df_shifted["Atoms"] = df['Atoms'].values
    for i in ['x','y','z']:
        if direction==i:
            df_shifted[i] = df[i].values+0.25
        else:
            df_shifted[i] = df[i].values
    return df_shifted.values


def plot_sigma_energy(path):
    out_files = os.listdir(path)
    total_energy = []
    e_fermi = []
    for file in out_files:
        temp_file = open(f'{path}/{file}', 'r').readlines()
        for i in range(len(temp_file)):
            if len(temp_file[i].split())>2:
                if temp_file[i].split()[0]=='!':
                    temp_en=temp_file[i].split()[4]
                # if temp_file[i].split()[0]=='the':
                #     temp_fermi=temp_file[i].split()[-2]
        total_energy.append([float(temp_en),float(file[:-13])])
        # e_fermi.append([float(temp_fermi),float(file[:-13])])
        
    tot_en = np.array(total_energy)
    tot_en = tot_en[tot_en[:, 1].argsort()]
    
    
    # e_f = np.array(e_fermi)
    # e_f = e_f[e_f[:, 1].argsort()]
    
    fig = plt.figure(figsize=(8,6))
    plt.plot(tot_en.T[1],tot_en.T[0])
    plt.ylabel('Total Energy [Ry]',fontsize=20)
    plt.xlabel('Smearing Value [Ry]',fontsize=20)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.savefig('total_sigma.png')

def get_total_energy(self):
    # path = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.save/data-file-schema.xml'
    # obj = untangle.parse(path)
    path = f'./Projects/{self.project_id}/{self.job_id}/scf.out'
    temp_file = open(f'{path}', 'r').readlines()
    for i in range(len(temp_file)):
        if len(temp_file[i].split())>2:
            if temp_file[i].split()[0]=='!':
                en=temp_file[i].split()[4]
    # en = float(obj.qes_espresso.output.total_energy.etot.cdata)*2
    # p = subprocess.Popen(f"grep '!' {path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # line = p.stdout.readlines()[0].decode()
    # en = float(re.findall(r"[-+]?(?:\d*\.*\d+)", line)[0])
    return(en)

def configure(path):
    if not path:
        config = defaultConfig()
    else:
        with open(path) as f:
            data = f.read()
            config = json.loads(data)
    return config


def fm_maker(self,magnetic_atom,mag_start=1,angle1=False,angle2=False):
    model = copy.deepcopy(self)
    model.job_id = 'fm'
    model.magnetism=True
    model.magnetic_atom=magnetic_atom
    model.magnetic_order='fm'
    for j,i in enumerate(model.config['pw']['atomic_species']): #for each atom
        if  i['atom']==magnetic_atom: # choose magnetic atom
            model.config['pw']['system'][f'starting_magnetization({j+1})']=mag_start
            if (angle1):
                model.config['pw']['system'][f'angle1({j+1})']=angle1
                self.angle1=angle1
            if (angle2):
                model.config['pw']['system'][f'angle2({j+1})']=angle2
                self.angle2=angle2
            if angle1 or angle2:
                model.config['pw']['system']['noncolin']='true'
            else:
                model.config['pw']['system']['nspin']=2
    ntyp = len(model.config['pw']['atomic_species'])
    model.config['pw']['system']['ntyp']=ntyp
    return model #send it back


def afm_maker(self,magnetic_atom,mag_start=[1,-1],angle1=False,angle2=False):
    #1 - Give initial model
    #2 - Define magnetic atom
    #3 - Return magnetic states
    #4 - FM and AFM
    model = copy.deepcopy(self)
    model.magnetic_atom=magnetic_atom
    model.magnetic_order='afm'
    model.magnetism=True
    """
    FM is easier to do. Only starting magnetization parameter should be added for the relevant atom
    Number of AFM states can be changing depending on the number of magnetic atoms. 
    The number of magnetic atoms should be divided into two for spin up and down. 
    Total magnetism is going to be zero but the order of spins are going to be change.
    """
    models=[] #initialize models
    atom_index=[] #initialize atom index
    for j,i in enumerate(model.config['pw']['atomic_positions']): #iterate over atomic positions
        if i[0]==magnetic_atom: #select magnetic atoms
            atom_index.append(j) #add magnetic atoms index to the array
    number = len(atom_index) # check for magnetic atom number
    if number ==2: #if there are 2
        spin_matrix = [[1,0]] #use this one
    else: #otherwise
        num_config = int(math.factorial(number)/(math.factorial(number-int(number/2))*math.factorial(int(number/2)))/2) #choose N/2 of N divide by 2
        one = np.ones(num_config).T.reshape(num_config,1) #keep the first atom up
        id = np.identity(num_config) #create other atom combinations
        spin_matrix = np.concatenate((one,id), axis=1) #combine them
    for j,i in enumerate(model.config['pw']['atomic_species']): #for each atom
        if  i['atom']==magnetic_atom: # choose magnetic atom
            i['atom']=i['atom']+str(int(1)) #change the name atom atom1
            model.config['pw']['system'][f'starting_magnetization({j+1})']=mag_start[0]
            if (angle1):
                model.config['pw']['system'][f'angle1({j+1})']=angle1
            if (angle2):
                model.config['pw']['system'][f'angle2({j+1})']=angle2
            if angle1 or angle2:
                model.config['pw']['system']['noncolin']='true'
            else:
                model.config['pw']['system']['nspin']=2            
            model.config['pw']['atomic_species'].append(copy.deepcopy(i)) #create the same atom
    model.config['pw']['atomic_species'][-1]['atom']=magnetic_atom+str(int(0)) #change name to atom0
    ntyp = len(model.config['pw']['atomic_species'])
    model.config['pw']['system']['ntyp']=ntyp
    
    for i in model.config['pw']['hubbard']['terms']:
        if i['atom'].lower()==magnetic_atom.lower():
            model.config['pw']['hubbard']['terms'].append(copy.deepcopy(i))
            i['atom']=magnetic_atom+str(int(1))
            model.config['pw']['hubbard']['terms'][-1]['atom']=magnetic_atom+str(int(0))
        
    
    if (angle1):
        model.config['pw']['system'][f'angle1({ntyp})']=angle1
    if (angle2):
        model.config['pw']['system'][f'angle2({ntyp})']=angle2
    model.config['pw']['system'][f'starting_magnetization({ntyp})']=mag_start[1]
    for i,spin_config in enumerate(spin_matrix): #for each configuration of spin matirx
        temp_model = copy.deepcopy(model) #create a model
        temp_model.job_id = f'afm{i+1}'
        for j,i in enumerate(atom_index): #for each magnetic atom
            temp_model.config['pw']['atomic_positions'][i][0]=temp_model.config['pw']['atomic_positions'][i][0]+str(int(spin_config[j])) #change name with the spin matrix
        models.append(temp_model) #add to models array
    return models #send it back

def default_pseudo(atom):
    atom_type = list(set([a[0] for a in atom]))
    atom_array = []
    for i in atom_type:
        for j in i:
            try:
                int(j)
                k=i[:-1]
            except:
                k=i
        temp_atom = {"atom":i,'mass':str(qcel.periodictable.to_mass(k)),'pseudopotential':f"{k}.UPF"}
        atom_array.append(temp_atom)
        # print(temp_atom)
    # print(atom_array)  
    return atom_array  

def atom_type(atom):
    num_type = len(list(set([a[0] for a in atom])))
    return num_type


def test_parameter(self,parameter_name,start,end,step,conv_thr=False,num_core=1,debug=False,out=False,dual=4):
    parameter = np.arange(start,end,step)
    result = np.zeros(shape=(3,len(parameter)))
    end=0
    for j,i in enumerate(parameter):
        if parameter_name=="ecutwfc":
            self.ecutwfc(i)
            self.ecutrho(dual*i)
            self.job_id=f"ecutwfc_{i}"
        if parameter_name=="kpoints":
            self.k_points(int(i))
            self.job_id=f"kpoints_{i}"
        if parameter_name=="num_core":
            self.job_id=f"num_core_{i}"
            self.num_core
        if debug==False:
            self.calculate('scf')
        temp_en = get_total_energy(self)
        temp_time = get_time(self)
        result[0][j]=i #parameters
        result[1][j]=temp_en #energy
        result[2][j]=temp_time #time
        end+=1
        if j!=0:
            if out==True:
                if parameter_name=="num_core":
                    print(f"{parameter_name}: {result[0][j]}     DeltaT :{(result[2][j]-result[2][j-1])} seconds    Time: {result[2][j]} seconds")
                else:
                    print(f"{parameter_name}: {result[0][j]}     DeltaE :{(result[1][j]-result[1][j-1])} seconds    Time: {result[2][j]} seconds")
            if conv_thr!=False:
                if abs(result[1][j-1] - result[1][j]) < conv_thr:
                    end=j
                    break
        else:
            print(f"{parameter_name}: {result[0][j]}      Time: {result[2][j]} seconds")

    # print(result.T[:end+1].T)
    return result.T[:end+1].T


def get_time(self):
    path = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.save/data-file-schema.xml'
    obj = untangle.parse(path)
    time = float(obj.qes_espresso.timing_info.total.wall.cdata)
    return time
def pdos_loader(fname):
    import numpy as np

    data = np.loadtxt(fname)
    energy = data[:, 0]
    pdos = data[:, 1]  # ldos col, total contribution for a given orbital

    return energy, pdos


def sumpdos(self):
    files = glob.glob(f'./Projects/{self.project_id}/{self.job_id}/projwfc.dat*')
    for i in files:
        parts = i.split("_")
        if len(parts)==2:
            label='Total'
        else:
            atom = parts[1].split('(')[-1].split(')')[0]
            orbital = parts[2].split('(')[-1].split(')')[0]
            # print(atom,orbital)
            compute.sumpdos(self,atom,orbital)


def sumkdos(self):
    files = glob.glob(f'./Projects/{self.project_id}/{self.job_id}/dos.k*')
    for i in files:
        parts = i.split("_")
        if len(parts)==2:
            label='Total'
        else:
            atom = parts[1].split('(')[-1].split(')')[0]
            orbital = parts[2].split('(')[-1].split(')')[0]
            compute.sumkdos(self,atom,orbital)


def minimum_energy(models):
    energies = []
    labels =[]
    index =[]
    for i,state in enumerate(models):
        energy = get_total_energy(state)
        energies.append(float(energy))
        labels.append(state.job_id.upper())
        index.append(i)
    min_state= np.argmin(energies)
    print(labels[min_state])
    return models[min_state]



def strain(initial_cell,axis,value):
    final_cell = copy.deepcopy(initial_cell)
    if 'x' in axis:
        final_cell[0] *= value
    if 'y' in axis:
        final_cell[1] *= value
    if 'z' in axis:
        final_cell[2] *= value
    return final_cell