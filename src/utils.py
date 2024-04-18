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


def make_monolayer(atoms):
    df = pd.DataFrame()
    atoms=np.array(atoms)
    df['Atoms'] = atoms.T[0]
    df['x'] = atoms.T[1].astype(float)
    df['y'] = atoms.T[2].astype(float)
    df['z'] = atoms.T[3].astype(float)
    df = df.query('z<0.5')
    df_shifted = pd.DataFrame()
    df_shifted["Atoms"] = df['Atoms'].values
    df_shifted["x"] = df['x'].values
    df_shifted["y"] = df['y'].values
    df_shifted["z"] = df['z'].values+0.25
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
    path = f'./Projects/{self.project_id}/{self.job_id}/{self.job_id}.save/data-file-schema.xml'
    obj = untangle.parse(path)
    en = float(obj.qes_espresso.output.total_energy.etot.cdata)*2
    # p = subprocess.Popen(f"grep '!' {path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # line = p.stdout.readlines()[0].decode()
    # en = float(re.findall(r"[-+]?(?:\d*\.*\d+)", line)[0])
    return(en)

def configure(calculation,path="./config.json"):
    with open(path) as f:
        data = f.read()
        config = json.loads(data)
    return config[calculation]

def afm_maker(model,magnetic_atom,mag_start=[1,-1],angle1=False,angle2=False):
    #1 - Give initial model
    #2 - Define magnetic atom
    #3 - Return magnetic states
    #4 - FM and AFM

    """
    FM is easier to do. Only starting magnetization parameter should be added for the relevent atom
    Number of AFM states can be changing depending on the number of magnetic atoms. 
    The number of magnetic atoms should be divided into two for spin up and down. 
    Total magnetism is going to be zero but the order of spins are going to be change.
    """
    models=[] #initialize models
    atom_index=[] #intialize atom index
    for j,i in enumerate(model.config['atomic_positions']): #iterate over atomic positions
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
    for j,i in enumerate(model.config['atomic_species']): #for each atom
        if  i['atom']==magnetic_atom: # choose magnetic atom
            i['atom']=i['atom']+str(int(1)) #change the name atom atom1
            model.config['system'][f'starting_magnetization({j+1})']=mag_start[0]
            if (angle1):
                model.config['system'][f'angle1({j+1})']=angle1
            if (angle2):
                model.config['system'][f'angle2({j+1})']=angle2
            if angle1 or angle2:
                model.config['system']['noncolin']='true'
            model.config['atomic_species'].append(copy.deepcopy(i)) #create the same atom
    model.config['atomic_species'][-1]['atom']=magnetic_atom+str(int(0)) #change name to atom0
    model.config['system']['nspin']=2
    ntype = len(model.config['atomic_species'])
    if (angle1):
        model.config['system'][f'angle1({ntype})']=angle1
    if (angle2):
        model.config['system'][f'angle2({ntype})']=angle2
    model.config['system'][f'starting_magnetization({ntype})']=mag_start[1]
    for spin_config in spin_matrix: #for each configuration of spin matirx
        temp_model = copy.deepcopy(model) #create a model
        for j,i in enumerate(atom_index): #for each magnetic atom
            temp_model.config['atomic_positions'][i][0]=temp_model.config['atomic_positions'][i][0]+str(int(spin_config[j])) #change name with the spin matrix
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


def test_parameter(self,parameter_name,start,end,step,conv_thr=False,num_core=1,debug=False,out=False):
    parameter = np.arange(start,end,step)
    result = np.zeros(shape=(3,len(parameter)))
    end=0
    for j,i in enumerate(parameter):
        if parameter_name=="ecutwfc":
            self.ecutwfc(i)
            self.job_id=f"ecutwfc_{i}"
        if parameter_name=="kpoints":
            self.k_points(int(i))
            self.job_id=f"kpoints_{i}"
        if parameter_name=="num_core":
            self.job_id=f"num_core_{i}"
            num_core = i
        if debug==False:
            self.scf(num_core)
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
    # with open(path, 'r') as data:
    #  data = data.read().split()
    #  counter = 0 
    #  for j,i in enumerate(data):
    #     # if i == "PWSCF":
    #     #     counter += 1 
    #     #     if counter ==3:
    #     #                         # print(f"CPU: {data[j+2]}, WALL: {data[j+4]}")
    #     #                         return (data[j+4])
    #     if i=='End':
    #        return(data[j-2])
