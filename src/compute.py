import subprocess

def run(self):
    if self.debug == False:
        p = subprocess.Popen(f"mpirun -np {self.num_core} {self.package}.x -inp ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.in > ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
        print(f'{self.calculation} is finished')

def sumpdos(self,atom,orbital):
        p = subprocess.Popen(f"sumpdos.x ./Projects/{self.project_id}/{self.job_id}/*\({atom}\)*\({orbital}\) > ./Projects/{self.project_id}/{self.job_id}/sumpdos_{atom}_{orbital}.dat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

def sumkdos(self,atom,orbital):
        p = subprocess.Popen(f"sumpdos.x ./Projects/{self.project_id}/{self.job_id}/dos.k*\({atom}\)*\({orbital}\) > ./Projects/{self.project_id}/{self.job_id}/sumkdos_{atom}_{orbital}.dat", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()