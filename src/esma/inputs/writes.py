import numpy as np

def add(file,text):
    with open(file, 'a') as file:
        file.write(text)


def write_atom_species(file,atomic_species):
    with open(file, "a") as file_object:
        file_object.write("ATOMIC_SPECIES \n")
        for atom in atomic_species:
            listed = list(atom.values())
            file_object.write(" ".join(listed)+'\n')


def write_atom_positions(file, positions,header=True):
    with open(file, "a") as file_object:
        if header:
            file_object.write("ATOMIC_POSITIONS (crystal) \n")
        for i in positions:
            try:
                file_object.write(" ".join(i)+'\n')
            except:
                try:
                    file_object.write(" ".join(i.astype(str))+'\n')
                except:
                    file_object.write(" ".join(str(i))+'\n')

def write_cell_parameters(file, cell,header=True):
    try:
        cell = np.array(cell,float)
    except:
        print('Something is wrong with the cell parameters. The error got caught on input file writing step.')
    with open(file, "a") as file_object:
        if header:
            file_object.write("CELL_PARAMETERS (angstrom) \n")
        for i in cell:
            for k,j in enumerate(i):
                file_object.write(f"{np.around(j,10):<.12f}  ")
            file_object.write("\n")


def write_k_grid(file,k):
    with open(file, "a") as file_object:
        file_object.write("K_POINTS crystal\n")
        file_object.write(f"{len(k)}\n")
        for i in k.round(12):
            file_object.write(f"{i[0]} {i[1]} {i[2]} {i[3]}\n")


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
            file_object.write(" ".join(listed[:-1]))
            file_object.write(f" !{listed[-1]}"+'\n')

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


