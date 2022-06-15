from qepy import *
import sys
arg = sys.argv[-1]
cell, atoms = read_vc_relax('./example_data/vc_relax.out')

input_parameters = {
    # &CONTROL
    "file_name": "./inputs/pw.in",
    "prefix": 'pw',
    "calculation": "vc-relax",
    "etot_conv_thr": "1d-07",
    "forc_conv_thr": "1d-06",
    "outdir": './outdir',
    "pseudo_dir": '../pseudos/',
    "tprnfor": "true",
    "tstress": "true",
    # &SYSTEM
    "degauss": "0.03",
    "ecutwfc": "80",
    "ecutrho": "600",
    "ibrav": "0",
    "nat": "6",
    "ntyp": "2",
    "occupations": 'smearing',
    "smearing": 'fd',
    # &ELECTRONS
    "conv_thr": "1d-10",
    "mixing_mode": "local-TF",
    # ATOMIC_SPECIES
    'atomic_species': [["Nb", "92.90", "Nb.pbe-mt_fhi.UPF"], ["Se", "78.96", "Se.pbe-mt_fhi.UPF"]],
    # ATOMIC_SPECIES
    'atomic_positions': atoms,
    # CELL_PARAMETERS
    'cell_parameters': cell,
    # K_POINTS
    'k_points': '60 60 30 0 0 0'
}


input_parameters["file_name"] = f"./inputs/{arg}.in"
input_parameters["degauss"] = arg
generate_input(input_parameters)
