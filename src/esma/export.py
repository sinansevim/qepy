import numpy as np


def exportPoscar(structure_name,atom,cell,file_name='POSCAR',file_path='./'):
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
                file_object.write(f"{np.around(float(j),10):<.12f}  ")
            file_object.write(f"{i[0]}  ")
            file_object.write("\n")