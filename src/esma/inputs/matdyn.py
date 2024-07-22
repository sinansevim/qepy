from . import writes


def matdyn(self):
    writes.write_k_points_matdyn(self.file_path, self.config['pw']['k_points_bands'])