from . import writes
import json 

def wannier90(self):
    self.file_path = self.file_path = f"./Projects/{self.project_id}/{self.job_id}/{self.job_id}.win"
    write_control(self)
    write_crystal(self)
    write_kpoints(self)
    write_grid(self)

def write_control(self):
    with open(self.file_path, 'w') as file:
        for k,l in self.config[self.package].items():
            try:
                float(l)
                file.write(f"{k} = {l} \n")
            except:
                try:
                    json.loads(l)
                    file.write(f"{k} = .{l}. \n")
                except:
                    if(bool(l)):
                        file.write(f"{k} = '{l}' \n")


def write_crystal(self):
    # Lattice
    writes.add(self.file_path,"begin unit_cell_cart \n")
    writes.write_cell_parameters(self.file_path,self.config['pw']['cell_parameters'],header=False)
    writes.add(self.file_path,"end unit_cell_cart \n")
    #Atom
    writes.add(self.file_path,"begin atoms_frac\n")
    writes.write_atom_positions(self.file_path,self.atoms(),header=False)
    writes.add(self.file_path,"end atoms_frac\n")

def write_kpoints(self):
    writes.add(self.file_path,"begin kpoint_path \n")
    points = self.config['pw']['k_points_bands']
    with open(self.file_path, "a") as file_object:
        for i in range(1,len(points)) :
            listed = list(points[i-1].values())
            file_object.write(f" {listed[-1]} ")
            file_object.write(" ".join(listed[:3]))
            listed = list(points[i].values())
            file_object.write(f" {listed[-1]} ")
            file_object.write(" ".join(listed[:3])+"\n")
    writes.add(self.file_path,"end kpoint_path \n")

def write_grid(self):
    writes.add(self.file_path,f"mp_grid {self.grid[0]} {self.grid[1]}  {self.grid[2]}\n")
    writes.add(self.file_path,"begin kpoints \n")
    k = self.config['pw']['k_points']
    with open(self.file_path, "a") as file_object:
        for i in k.round(8):
            file_object.write(f"{i[0]} {i[1]} {i[2]} \n")
    writes.add(self.file_path,"end kpoints \n")
    