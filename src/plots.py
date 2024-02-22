import numpy as np
import matplotlib.pyplot as plt
from . import reads

def plot_electron(self,ylim=False,show=False,save=False):
    sym = reads.read_symmetries(f'./{self.project_id}/{self.job_id}/bands-pp.out')
    fermi = reads.read_efermi(f'./{self.project_id}/{self.job_id}/scf.out')
    fig = plt.figure(figsize=(8,6))
    data = np.loadtxt(f'./{self.project_id}/{self.job_id}/bands.dat.gnu')
    k = np.unique(data[:, 0])
    bands = np.reshape(data[:, 1], (-1, len(k)))
    for band in range(len(bands)):
        plt.plot(k, bands[band, :]-float(fermi),c='black')
    plt.xticks(sym,self.path)
    for i in range(1,len(sym)-1):
        plt.axvline(sym[i],c='black')
    plt.axhline(0,c='red')
    plt.ylim(ylim[0],ylim[1])
    plt.xlim(sym[0],sym[-1])
    if save==True:
        plt.savefig(f'./{self.project_id}/{self.job_id}/band.png')
    if show==True:
        return fig