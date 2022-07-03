import numpy as np

def read_poscar(path):
    data = open("./example_data/NbSe2.poscar", 'r').readlines()
    cell =[]
    for i in data[2:5]:
        line=i.split()
        cell.append(line)
    atoms= []
    for i in data[8:]:
        line=(i.split())
        position=line[:3] 
        atom = [line[-1][:-2]]
        atoms.append(atom+position)
    return(cell,atoms)
    
        
def read_vc_relax(path):
    vc_relax = open(path, 'r').readlines()
    begin = 0
    end = 0
    for i in range(len(vc_relax)):
        if vc_relax[i] == 'Begin final coordinates\n':
            begin = i
        if vc_relax[i] == 'End final coordinates\n':
            end = i
    cell = np.array([i.split()
                    for i in vc_relax[begin+5:begin+8]]).astype(float)
    atoms = np.array([i.split() for i in vc_relax[end-6:end]])
    return(cell, atoms)

def read_relax(path):
    data = open(path, 'r').readlines()
    begin = 0
    end = 0
    for i in range(len(data)):
        if data[i] == 'Begin final coordinates\n':
            begin = i
        if data[i] == 'End final coordinates\n':
            end = i
    atoms = np.array([i.split() for i in data[begin+3:end]])
    return atoms