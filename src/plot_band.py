import argparse
import numpy as np
import matplotlib.pyplot as plt


ap = argparse.ArgumentParser()
ap.add_argument("-d", "--degauss", required=True, help="Degauss value")
args = vars(ap.parse_args())
degauss = args['degauss']


def read_efermi(path):
    lines = open(path, 'r').readlines()
    e_fermi = 0
    for i in lines:
        if "the Fermi energy is" in i:
            e_fermi = float(i.split()[-2])
            return e_fermi
        
def Symmetries(fstring):
    f = open(fstring, 'r')
    x = np.zeros(0)
    for i in f:
        if "high-symmetry" in i:
            x = np.append(x, float(i.split()[-1]))
    f.close()
    return x

sym = Symmetries(f'./results/{degauss}/bands-pp.out')


temp_file = open(f'./results/{degauss}/scf.out', 'r').readlines()
for i in range(len(temp_file)):
    if len(temp_file[i].split())>2:
        if temp_file[i].split()[0]=='the':
            fermi=temp_file[i].split()[-2]

fig = plt.figure(figsize=(8,6))
temp_data = np.loadtxt(f'./results/{degauss}/bands.dat.gnu')
plt.scatter(temp_data.T[0],temp_data.T[1]-float(fermi))
plt.xticks(sym,['G','M','K','G'])
plt.axvline(sym[1],c='black')
plt.axvline(sym[2],c='black')
plt.axhline(0,c='red')
plt.ylim(-10,10)
plt.xlim(sym[0],sym[-1])
plt.savefig(f'band_{degauss}.png')
# plt.show()
                