import subprocess
from .commands import wannier_stack

def run(self,num_core=False):
    if num_core==False:
           num_core=self.num_core
    if self.debug == False:
        print(f'{self.calculation} for {self.job_id} is started')
        if self.gpu==True:
                p = subprocess.Popen(f"srun --mpi=pmi2 singularity run --nv  /work/bansil/s.sevim/software/qe-gpu/qe-7.1-gpu.sif {self.package}.x -npool {self.num_gpu} -inp ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.in > ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p.wait()
        else:
                if self.package == "wannier90":
                        wannier_stack.full_stack(self)
                else:
                        p = subprocess.Popen(f"mpirun -np {num_core} {self.package}.x -inp ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.in > ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                        p.wait()
        print(f'{self.calculation} for {self.job_id} is finished')




def sumpdos(self,atom,orbital):
        p = subprocess.Popen(f"sumpdos.x ./Projects/{self.project_id}/{self.job_id}/*\({atom}\)*\({orbital}\) > ./Projects/{self.project_id}/{self.job_id}/sumpdos_{atom}_{orbital}.dat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

def sumkdos(self,atom,orbital):
        p = subprocess.Popen(f"sumpdos.x ./Projects/{self.project_id}/{self.job_id}/dos.k*\({atom}\)*\({orbital}\) > ./Projects/{self.project_id}/{self.job_id}/sumkdos_{atom}_{orbital}.dat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()