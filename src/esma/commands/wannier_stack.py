import subprocess


def wannier_pp(self):
        p = subprocess.Popen(f"cd ./Projects/{self.project_id}/{self.job_id}/ ; wannier90.x -pp {self.job_id} ; cd $OLDPWD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()
def pw2wannier90(self):
        p = subprocess.Popen(f"cd ./Projects/{self.project_id}/{self.job_id}/ ; mpirun -np {self.num_core} pw2wannier90.x -inp pw2wannier90.in > pw2wannier90.out ; cd $OLDPWD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

def wannier90(self):
        p = subprocess.Popen(f"cd ./Projects/{self.project_id}/{self.job_id}/ ; wannier90.x {self.job_id}; cd $OLDPWD", shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        p.wait()

def full_stack(self):
        wannier_pp(self)
        pw2wannier90(self)
        wannier90(self)