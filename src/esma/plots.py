import numpy as np
import matplotlib.pyplot as plt
import glob
from . import reads
from . import utils


def plot(self,calculation,save,xlim=False,ylim=False):
    if calculation=='electron':
        plot_electron(self,ylim=ylim,save=save)
    if calculation=='phonon':
        plot_phonon(self,save=save)
    if calculation=='dos':
        plot_dos(self,xlim=xlim,save=save)
    if calculation=='pdos':
        plot_pdos(self,xlim=xlim,save=save)
    if calculation=='kdos':
        plot_kdos(self,ylim=ylim,save=save)

def plot_electron(self,ylim=False,show=False,save=True):
    sym = reads.read_symmetries(f'./Projects/{self.project_id}/{self.job_id}/bands-pp.out')
    fermi = reads.read_efermi(f'./Projects/{self.project_id}/{self.job_id}/scf.out')
    fig = plt.figure(figsize=(8,6))
    data = np.loadtxt(f'./Projects/{self.project_id}/{self.job_id}/bands.dat.gnu')
    k = np.unique(data[:, 0])
    bands = np.reshape(data[:, 1], (-1, len(k)))
    for band in range(len(bands)):
        plt.plot(k, bands[band, :],c='black')
    plt.xticks(sym,self.path)
    for i in range(1,len(sym)-1):
        plt.axvline(sym[i],c='black')
    plt.axhline(float(fermi),c='red')
    plt.text(-0.2, float(fermi), r'$\epsilon_{Fermi}$',color='red')
    plt.ylim(ylim[0],ylim[1])
    plt.xlim(sym[0],sym[-1])
    if save==True:
        plt.savefig(f'./Projects/{self.project_id}/{self.job_id}/band.png')
    if show==True:
        return fig
    

def plot_phonon(self,save=True):
    sym = []
    point = [0]
    for k,i in enumerate(self.config['pw']['k_points_bands']):
        sym.append(i['label'].split()[1])
        if k!=len(self.config['pw']['k_points_bands'])-1:
            point.append(point[k]+int(i['number']))
    freq = np.loadtxt(f"./Projects/{self.project_id}/{self.job_id}/{self.job_id}.freq.gp")
    ph_path = freq.T[0]/max(freq.T[0])
    cm2mev = 0.124
    fig = plt.figure(figsize=(7,6))
    
    for i in range(1,len(freq.T)):
        plt.plot(ph_path,freq.T[i]*cm2mev,linewidth=2,color="blue")
    # print(point)
    tick = [ ph_path[i] for i in point ]
    for i in tick[1:-1]:
        plt.axvline(i,linestyle="--",color="black")
    plt.xticks(tick,sym,fontsize=15)
    plt.ylim(0,)
    plt.xlim(0,ph_path[-1])
    plt.ylabel("ω (meV)",fontsize=15)
    if save==True:
        plt.savefig(f'./Projects/{self.project_id}/{self.job_id}/phonon_band.png')
    plt.show()
    
def plot_dos(self,save=True,xlim=False):
    try :
        self.magnetic_order
        fermi = reads.read_efermi(f'./Projects/{self.project_id}/{self.job_id}/nscf.out')
        # load data
        energy, up, down, int_dos = np.loadtxt(f'./Projects/{self.project_id}/{self.job_id}/dos.dat', unpack=True)
        # make plot
        plt.figure(figsize = (12, 6))
        plt.plot(energy, up, linewidth=0.75, color='red')
        plt.plot(energy, -down, linewidth=0.75, color='blue')
        plt.yticks([])
        plt.xlabel('Energy (eV)')
        plt.ylabel('DOS')
        plt.axvline(x=fermi, linewidth=0.5, color='k', linestyle=(0, (8, 10)))
        plt.xlim(10, 30)
        # plt.ylim(0, )
        plt.fill_between(energy, 0, -down, where=(energy < fermi), facecolor='red', alpha=0.25)
        plt.fill_between(energy, 0, up, where=(energy < fermi), facecolor='red', alpha=0.25)
        plt.text(fermi+1, up.mean(), 'Fermi energy', rotation=90)
        plt.title(self.job_id.upper())
        if save==True:
            plt.savefig(f'./Projects/{self.project_id}/{self.job_id}/dos.png')
    except:
        fermi = reads.read_efermi(f'./Projects/{self.project_id}/{self.job_id}/nscf.out')
        # load data
        energy, dos, idos = np.loadtxt(f'./Projects/{self.project_id}/{self.job_id}/dos.dat', unpack=True)
        # make plot
        plt.figure(figsize = (12, 6))
        plt.plot(energy, dos, linewidth=0.75, color='red')
        plt.yticks([])
        plt.xlabel('Energy (eV)')
        plt.ylabel('DOS')
        plt.axvline(x=fermi, linewidth=0.5, color='k', linestyle=(0, (8, 10)))
        if xlim:
            plt.xlim(xlim)
        else:
            plt.xlim(-20, 20)
        plt.ylim(0, )
        plt.fill_between(energy, 0, dos, where=(energy < fermi), facecolor='red', alpha=0.25)
        plt.text(fermi+1, dos.mean(), 'Fermi energy', rotation=90)
        if save==True:
            plt.savefig(f'./Projects/{self.project_id}/{self.job_id}/dos.png')
    
def plot_pdos(self,xlim=False,save=False):
    files = glob.glob(f'./Projects/{self.project_id}/{self.job_id}/sumpdos*')
    files.append(f'./Projects/{self.project_id}/{self.job_id}/projwfc.dat.pdos_tot')
    fermi = reads.read_efermi(f'./Projects/{self.project_id}/{self.job_id}/nscf.out')
    plt.figure(figsize = (8, 4))
    for i in files:
        parts = i.split("_")
        if len(parts)==2:
            label='Total'
        else:
            atom = parts[1]
            orbital = parts[2].split('.')[0]
            label=atom+'-'+orbital
        energy, pdos = utils.pdos_loader(i)
        plt.plot(energy, pdos, linewidth=0.75,label=label)
        plt.yticks([])
        plt.xlabel('Energy (eV)')
        plt.ylabel('DOS')
        plt.axvline(x= fermi, linewidth=0.5, color='k', linestyle=(0, (8, 10)))
        if xlim:
            plt.xlim(xlim)
        else:
            plt.xlim(-20, 20)
        if label=='Total':
            plt.ylim(0, max(pdos)*1.2)
        plt.fill_between(energy, 0, pdos, where=(energy < fermi), alpha=0.25)
    plt.text(fermi+1, pdos.mean(), 'Fermi energy', rotation=90)
    plt.legend(frameon=False)
    plt.savefig(f'./Projects/{self.project_id}/{self.job_id}/pdos.png')

def plot_kdos(self,ylim=False,save=False):
    files = glob.glob(f'./Projects/{self.project_id}/{self.job_id}/sumkdos*')
    files.append(f'./Projects/{self.project_id}/{self.job_id}/dos.k.pdos_tot')
    fermi = reads.read_efermi(f'./Projects/{self.project_id}/{self.job_id}/scf.out')
    for i in files:
        parts = i.split("_")
        if len(parts)==2:
            label='Total'
        else:
            atom = parts[1]
            orbital = parts[2].split('.')[0]
            label=atom+'-'+orbital
        # print(label)
        data = np.loadtxt(i)

        k = np.unique(data[:, 0])  # k values
        e = np.unique(data[:, 1])  # dos energy values

        dos = np.zeros([len(k), len(e)])

        for i in range(len(data)):
            e_index = int(i % len(e))
            k_index = int(data[i][0] - 1)
            dos[k_index, e_index] = data[i][2]
        sym = reads.read_symmetries(f'./Projects/{self.project_id}/{self.job_id}/bands-pp.out')
        sym =sym/max(sym)*max(k)
        fermi = reads.read_efermi(f'./Projects/{self.project_id}/{self.job_id}/scf.out')
        plt.pcolormesh(k, e, dos.T, cmap='magma', shading='auto')
        plt.xticks(sym,self.path)
        for i in range(1,len(sym)-1):
            plt.axvline(sym[i],c='white')
        plt.axhline(float(fermi),c='white')
        if ylim:
            plt.ylim(ylim)
        plt.ylabel('Energy (eV)')
        plt.title(label)
        plt.savefig(f'./Projects/{self.project_id}/{self.job_id}/kdos_{label}.png')