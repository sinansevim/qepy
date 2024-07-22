from .generic import generic


def pw2wannier90(self):
    self.file_path = self.file_path = f"./Projects/{self.project_id}/{self.job_id}/pw2wannier90.in"
    generic(self)