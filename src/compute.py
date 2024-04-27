import subprocess

def run(self):
    p = subprocess.Popen(f"mpirun -np {self.num_core} {self.package}.x -inp ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.in > ./Projects/{self.project_id}/{self.job_id}/{self.calculation}.out ", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    print(f'{self.calculation} is finished')
