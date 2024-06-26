import numpy as np
def write_atom_species(file,atomic_species):
    with open(file, "a") as file_object:
        file_object.write("ATOMIC_SPECIES \n")
        for atom in atomic_species:
            listed = list(atom.values())
            file_object.write(" ".join(listed)+'\n')


def write_atom_positions(file, positions):
    with open(file, "a") as file_object:
        file_object.write("ATOMIC_POSITIONS (crystal) \n")
        for i in positions:
            try:
                file_object.write(" ".join(i)+'\n')
            except:
                try:
                    file_object.write(" ".join(i.astype(str))+'\n')
                except:
                    file_object.write(" ".join(str(i))+'\n')

def write_cell_parameters(file, cell):
    try:
        cell = np.array(cell,float)
    except:
        print('Something is wrong with the cell parameters. The error got caught on input file writing step.')
    with open(file, "a") as file_object:
        file_object.write("CELL_PARAMETERS (angstrom) \n")
        for i in cell:
            for k,j in enumerate(i):
                file_object.write(f"{np.around(j,8):<.10f}  ")
            file_object.write("\n")


def write_k_points(file, k):
    with open(file, "a") as file_object:
        file_object.write("K_POINTS automatic \n")
        file_object.write(k+'\n')

def write_k_points_bands(file,k):
    with open(file, "a") as file_object:
        file_object.write("K_POINTS crystal_b \n")
        file_object.write(str(len(k))+'\n')
        for point in k:
            listed = list(point.values())
            file_object.write(" ".join(listed)+'\n')

def write_k_points_matdyn(file,k):
    with open(file, "a") as file_object:
        file_object.write(str(len(k))+'\n')
        for point in k:
            listed = list(point.values())
            file_object.write(" ".join(listed)+'\n')


def write_hubbard(file,parameter):
    with open(file, "a") as file_object:
        file_object.write(f"HUBBARD {parameter['projection']} \n")
        for term in parameter['terms']:
            file_object.write(f"{term['interaction']} {term['atom']}-{term['orbital']} {term['value']}\n")


def write_poscar(structure_name,atom,cell,file_name='POSCAR',file_path='./'):
    full_path = file_path+"/"+file_name+".poscar"
    atom_name  = np.array(atom).T[0].tolist()
    atom_type = {} 
    for i in atom_name:
        if i in atom_type:
            atom_type[i]+=1
        else:
            atom_type[i]=1
    with open(full_path, "w") as file_object:
        file_object.write(f"{structure_name} \n")
        file_object.write("1.0 \n")
        for i in cell:
            for k,j in enumerate(i):
                file_object.write(f"{np.around(float(j),10):<.12f}  ")
            file_object.write("\n")
        for i in atom_type:
            file_object.write(f"{i}  ")
        file_object.write("\n")
        for i in atom_type:
            file_object.write(f"{atom_type[i]}  ")
        file_object.write("\n")
        file_object.write("direct")
        file_object.write("\n")
        for i in atom:
            for k,j in enumerate(i[1:]):
                file_object.write(f"{np.around(float(j),8):<.10f}  ")
            file_object.write(f"{i[0]}  ")
            file_object.write("\n")