import numpy as np
import pandas as pd
from . import reads
from . import writes
from . import utils


def pw(parameters):
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
  nosym    = .{parameters['nosym']}.
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
    writes.write_atom_species(parameters['file_name'], parameters['atomic_species'])
    writes.write_atom_positions(parameters['file_name'],parameters['atomic_positions'])
    writes.write_cell_parameters(parameters['file_name'], parameters['cell_parameters'])
    if parameters['calculation']=='bands':
        writes.write_k_points_bands(parameters['file_name'], parameters['k_points_bands'])
    else:
        writes.write_k_points(parameters['file_name'], parameters['k_points'])
    return


def bands_pp(parameters):
    filedata = f"""
&bands
outdir = '{parameters['outdir']}'
prefix = '{parameters['prefix']}'
filband = '{parameters['outdir']}bands.dat'
/
"""
    with open(parameters['file_name'], 'w') as file:
        file.write(filedata)
    return


def ph(parameters):
    filedata = f"""
&inputph
  prefix = '{parameters['prefix']}'
  fildyn = './dyn/{parameters['prefix']}/{parameters['prefix']}.dyn',
  outdir = '{parameters['outdir']}'
  ldisp  = {parameters['ldisp']},
  trans  = {parameters['trans']},
  fildvscf = 'dvscf',
  nq1    = {parameters['nq1']},
  nq2    = {parameters['nq2']},
  nq3    = {parameters['nq3']},
  tr2_ph = {parameters['tr2_ph']},
  /
"""
    with open(parameters['file_name'], 'w') as file:
        file.write(filedata)
    return

def q2r(parameters):
    filedata = f"""
&input
  fildyn = './dyn/{parameters['prefix']}/{parameters['prefix']}.dyn',
  zasr = 'simple'
  flfrc = './dyn/{parameters['prefix']}/{parameters['prefix']}.fc'
/
"""
    with open(parameters['file_name'], 'w') as file:
        file.write(filedata)
    return

def matdyn(parameters):
    filedata = f"""
&input
  asr = 'simple'
  flfrc = './dyn/{parameters['prefix']}/{parameters['prefix']}.fc'
  flfrq = './dyn/{parameters['prefix']}/{parameters['prefix']}.freq'
  q_in_band_form=.true.
  q_in_cryst_coord=.true.
/
"""
    with open(parameters['file_name'], 'w') as file:
        file.write(filedata)
    writes.write_k_points_matdyn(parameters['file_name'], parameters['k_points_bands'])
    return

def plotband(parameters):
    filedata = f"""
{parameters['prefix']}.freq
0 550
{parameters['prefix']}.xmgr
"""
    with open(f"./dyn/{parameters['prefix']}/{parameters['prefix']}-plotband.in", 'w') as file:
        file.write(filedata)
    return