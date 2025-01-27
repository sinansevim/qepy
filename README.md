# Espresso Machine

**Espresso Machine** (`esma`) is a Python library designed to simplify and automate workflows for [Quantum ESPRESSO](https://www.quantum-espresso.org/). By providing a functional interface for setting up calculations, it significantly reduces the time spent writing and debugging input files. Whether you’re a beginner in density functional theory (DFT) or an advanced researcher needing efficient high-throughput computations, Espresso Machine aims to streamline your process.

---

## Table of Contents
- [Espresso Machine](#espresso-machine)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Example Workflows](#example-workflows)
  - [Contributing](#contributing)
  - [License](#license)

---

## Features

- **Automated Input Generation**  
  Generate `pw.x`, `ph.x`, `projwfc.x`, and `wannier90.x` input files with minimal boilerplate for SCF, NSCF, DOS, PDOS, band structure, phonon, and Wannier calculations.

- **High-Throughput Workflows**  
  Easily set up parametric studies (strain, doping, etc.) with minimal code duplication.

- **DFT+U, Spin-Orbit and Magnetization**  
  Native support for Hubbard +U, spin-orbit coupling, and various magnetic configurations (FM, AFM, custom angles).

- **Plotting Utilities**  
  Quick plotting of band structures, phonon dispersions, DOS/PDOS, and Wannier-interpolated bands—all in Python.

- **User-Friendly API**  
  Provides a clean, Pythonic interface via the `project` class.

---

## Installation

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/susyexists/espresso-machine.git
   cd espresso-machine
   ```

2. **Create a Virtual Environment (Recommended)**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Linux/Mac
   # or
   .venv\Scripts\activate     # On Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```


4. **(Optional) Install Quantum ESPRESSO**  
   Make sure `pw.x`, `ph.x`, `projwfc.x`, and other required QE executables are in your `PATH` or otherwise accessible.

---

## Getting Started

Here’s a quick example showing how you might set up a simple SCF calculation on silicon:

```python
import esma

# 1) Create a project
model = esma.project(project_id="Si_bulk")

# 2) Load a structure from a POSCAR file
model.get_structure(format='poscar', path='./Structures/Si.poscar')

# 3) Define the pseudopotential directory
model.set_pseudo(path="./Pseudopotentials")

# 4) Basic DFT parameters
model.ecutwfc(60)           # Wavefunction cutoff
model.ecutrho(480)          # Charge density cutoff
model.k_points([6,6,6])     # K-point mesh
model.degauss(0.01)         # Smearing
model.smearing('mv')        # Marzari-Vanderbilt smearing
model.set_cores(8)          # Use 8 CPU cores

# 5) Perform SCF calculation
model.calculate('scf')
```

After running, you’ll find the generated input and output in `./Projects/Si_bulk/results/`.

---

## Example Workflows

In this repository, you’ll find **advanced workflow scripts** demonstrating:

- **Strain Sweeps**: Apply a range of strain values to a 2D material and perform relaxation + SCF steps.  
- **Phonon Calculations**: Set up `ph.x`, run phonon dispersions, and plot phonon band structures.  
- **Spin-Orbit Coupling + Hubbard U**: Configure FM or AFM states, enable spin-orbit coupling, and specify `hubbard()` corrections.  
- **Wannier90**: Conduct non-SCF runs on dense k-meshes, generate Wannier functions, and plot the Wannier-interpolated band structure.

Explore the `examples/` or `workflows/` folder (as applicable) to see these scripts in action.

---


## Contributing

We welcome contributions from the community! To contribute:

1. **Fork** the repo and **clone** it locally.  
2. Create a **feature branch** (e.g., `git checkout -b feature-new-workflow`).  
3. **Commit** your changes (`git commit -m "Add new workflow ..."`).  
4. **Push** your branch to GitHub.  
5. Open a **Pull Request** with a description of your changes.

Please ensure that you’ve tested your changes.

---

## License


```
MIT License

Copyright (c) [2023] ...

Permission is hereby granted, free of charge, to any person ...
```

See the [LICENSE](LICENSE) file for details.

---


**Happy Computing!** If you have any questions or suggestions, open an issue or pull request. We appreciate your feedback and contributions.
