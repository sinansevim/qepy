from . import writes


import numpy as np


def pw(self):
    writes.write_atom_species(self.file_path, self.config['pw']['atomic_species'])
    writes.write_atom_positions(self.file_path,self.config['pw']['atomic_positions'])
    writes.write_cell_parameters(self.file_path, self.config['pw']['cell_parameters'])
    #Kpoint check
    if self.config['pw']["control"]['calculation']=='bands':
        writes.write_k_points_bands(self.file_path, self.config['pw']['k_points_bands'])
    elif type(self.config['pw']['k_points'])== np.ndarray:
        writes.write_k_grid(self.file_path, self.config['pw']['k_points'])
    else:
        writes.write_k_points(self.file_path, self.config['pw']['k_points'])
    #Hubbard Check
    if len(self.config['pw']['hubbard']['terms']) !=0:
        writes.write_hubbard(self.file_path, self.config['pw']['hubbard'])
    return