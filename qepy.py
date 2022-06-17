import numpy as np
import pandas as pd


def generate_input(parameters):
    filedata = f"""
&CONTROL
etot_conv_thr =  {parameters['etot_conv_thr']}
forc_conv_thr =  {parameters['forc_conv_thr']}
prefix        = '{parameters['prefix']}'
calculation   = '{parameters['calculation']}'
outdir        = '{parameters['outdir']}'
pseudo_dir    = '{parameters['pseudo_dir']}'
tprnfor       = .{parameters['tprnfor']}.
tstress       = .{parameters['tstress']}.
/
&SYSTEM
  degauss     = {parameters['degauss']}
  ecutwfc     = {parameters['ecutwfc']}
  ecutrho     = {parameters["ecutrho"]}
  ibrav       = {parameters['ibrav']}
  nat         = {parameters['nat']}
  ntyp        = {parameters['ntyp']}
  occupations = '{parameters['occupations']}'
  smearing    = '{parameters['smearing']}'
/
&ELECTRONS
  conv_thr    =  {parameters['conv_thr']}
  mixing_mode = '{parameters['mixing_mode']}'
/
&IONS
/
&CELL
/   
"""
    with open(parameters['file_name'], 'w') as file:
        file.write(filedata)
    write_atom_species(parameters['file_name'], parameters['atomic_species'])
    write_atom_positions(parameters['file_name'],parameters['atomic_positions'])
    write_cell_parameters(parameters['file_name'], parameters['cell_parameters'])
    write_k_points(parameters['file_name'], parameters['k_points'])
    return


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
            file_object.write(" ".join(i.astype(str))+'\n')


def write_cell_parameters(file, cell):
    with open(file, "a") as file_object:
        file_object.write("CELL_PARAMETERS (angstrom) \n")
        for i in cell:
            file_object.write(" ".join(i.astype(str))+'\n')


def write_k_points(file, k):
    with open(file, "a") as file_object:
        file_object.write("K_POINTS automatic \n")
        file_object.write(k+'\n')


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