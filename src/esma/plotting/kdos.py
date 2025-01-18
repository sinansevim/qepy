import numpy as np
import matplotlib.pyplot as plt
import glob
import os

# Function to read k-resolved PDOS files and sum over s, p, or d orbitals
def read_pdos_files(directory, atom, orbital):
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' not found.")
        return {}

    # Find all files corresponding to the selected atom and orbital group (s, p, d)
    file_pattern = os.path.join(directory, f"dos.k.pdos_atm*({atom})_wfc#*({orbital}_*)")
    files = sorted(glob.glob(file_pattern))  # Get all matching files

    if not files:
        print(f"No PDOS files found for atom '{atom}' and orbital '{orbital}' in {directory}.")
        return {}

    summed_pdos = None
    ik_values, energy_values = None, None

    for file in files:
        try:
            data = np.loadtxt(file, comments="#")

            if data.size == 0:
                print(f"Warning: {file} is empty.")
                continue

            ik = data[:, 0]  # k-point index
            E = data[:, 1]   # Energy values
            pdos_values = np.sum(data[:, 3:], axis=1)  # Sum over all components of the orbital

            if summed_pdos is None:
                summed_pdos = pdos_values
                ik_values, energy_values = ik, E
            else:
                summed_pdos += pdos_values  # Sum over all matching orbital components

        except Exception as e:
            print(f"Error reading {file}: {e}")

    if summed_pdos is None:
        return {}

    return {"ik": ik_values, "E": energy_values, "pdos": summed_pdos}

# Function to plot k-resolved PDOS using plt.pcolormesh()
def plot_k_resolved_pdos(directory, atom, orbital, fermi=0, sym=None, labels=None, ylim=None, cmap="Reds"):
    pdos_data = read_pdos_files(directory, atom, orbital)

    if not pdos_data:
        print("No PDOS data available. Exiting plot function.")
        return

    k = np.unique(pdos_data["ik"])  # Unique k-points
    e = np.unique(pdos_data["E"])   # Unique energy levels

    # Create a 2D PDOS matrix initialized to zeros
    dos = np.zeros((len(e), len(k)))

    # Fill the PDOS matrix
    for i in range(len(pdos_data["ik"])):
        k_idx = np.where(k == pdos_data["ik"][i])[0][0]
        e_idx = np.where(e == pdos_data["E"][i])[0][0]
        dos[e_idx, k_idx] = pdos_data["pdos"][i]

    # Ensure correct dimensions for pcolormesh
    k_grid, e_grid = np.meshgrid(k, e)
    
    plt.figure(figsize=(8, 6))
    plt.pcolormesh(k_grid, e_grid-float(fermi), dos, cmap=cmap, shading='auto')
    sym =sym/max(sym)*max(k)
    # Add symmetry points if provided
    plt.xticks(sym, labels)
    for i in range(1, len(sym) - 1):
        plt.axvline(sym[i], color='black')

    # Add Fermi level
    plt.axhline(0, color='black', linestyle='--', label="Fermi Level")

    # Set energy limits
    if ylim:
        plt.ylim(ylim)

    plt.ylabel("Energy (eV)")
    plt.title(f"k-Resolved PDOS for {atom}, Orbital: {orbital}")
    plt.colorbar(label="PDOS Intensity")
    plt.savefig(f'{directory}/kdos_{atom}_{orbital}.png')
    plt.show()
