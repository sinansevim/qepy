import numpy as np
import pandas as pd
from . import reads
from . import writes
from . import utils
import json


def generic(self):
    with open(self.file_path, 'w') as file:
        for i,j in self.config[self.package].items():
            if i!='hubbard':
                try:
                    if(type(j)==dict):
                            file.write(f"&{i.upper()} \n")
                    for k,l in j.items():
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
                    file.write("/ \n")
                except:
                    pass

def constructor(self):
    generic(self)
    if self.package=='pw':
        pw(self)
    if self.package=='matdyn':
        matdyn(self)
    
def pw(self):
    writes.write_atom_species(self.file_path, self.config['pw']['atomic_species'])
    writes.write_atom_positions(self.file_path,self.config['pw']['atomic_positions'])
    writes.write_cell_parameters(self.file_path, self.config['pw']['cell_parameters'])
    #Kpoint check
    if self.config['pw']["control"]['calculation']=='bands':
        writes.write_k_points_bands(self.file_path, self.config['pw']['k_points_bands'])
    else:
        writes.write_k_points(self.file_path, self.config['pw']['k_points'])
    #Hubbard Check
    if len(self.config['pw']['hubbard']['terms']) !=0:
        writes.write_hubbard(self.file_path, self.config['pw']['hubbard'])
    return

def matdyn(self):
    writes.write_k_points_matdyn(self.file_path, self.config['pw']['k_points_bands'])


def plotband(parameters):
    filedata = f"""
{parameters['prefix']}.freq
0 550
{parameters['prefix']}.xmgr
"""
    with open(f"./dyn/{parameters['prefix']}/{parameters['prefix']}-plotband.in", 'w') as file:
        file.write(filedata)
    return