import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def make_monolayer(atoms):
    df = pd.DataFrame()
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