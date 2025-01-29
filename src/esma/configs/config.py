import json

def defaultConfig():
  config = {
  "metadata":{

    },
  "pw": {
    "control": { "pseudo_dir": "./pseudos/NC" },
    "system": { "degauss": "0.1", "ecutwfc": "20", "occupations": "smearing" },
    "electrons": { "conv_thr": "1e-6" },
    "ions": {},
    "cell": {},
    "k_points": "1 1 1 0 0 0",
    "hubbard": { "projection": "atomic", "terms": [] }
  },
  "dos": { "dos": { "emin": "-20.0", "emax": "20.0" } },
  "bands": { "bands": {"lsym":"false"} },
  "projwfc": { "projwfc": {} },
  "ph": { "inputph": { "ldisp": "true", "nq1": "1", "nq2": "1", "nq3": "1" } },
  "q2r": { "input": { "zasr": "simple" } },
  "matdyn": {
    "input": {
      "asr": "simple",
      "q_in_band_form": "true",
      "q_in_cryst_coord": "true"
    }
  },
  "pw2wannier90": {
    "inputpp": {
      "write_amn": "true",
      "write_mmn": "true",
      "write_unk": "true",
      "scdm_proj": "true",
      "scdm_entanglement": "erfc",
      "scdm_mu": "10",
      "scdm_sigma": "4"
    }
  },
  "wannier90": {
    "num_iter": "0",
    "dis_num_iter": "0",
    "num_print_cycles": "10",
    "geninterp": "true",
    "auto_projections": "true",
    "write_xyz": "true",
    "write_hr": "true",
    "bands_plot": "true",
    "bands_num_points" : "200"
  },
  "hp":{
    "inputhp":{
      "conv_thr_chi":"1e-6",
      "nq1" :"2", "nq2" : "2", "nq3" :"2",
    }
  },
  "d3hess":{
    "input":{
      "step":"1e-3"
    }
  }
}
  return config