from .inputs.generic import generic
from .inputs.matdyn import matdyn
from .inputs.pw import pw
from .inputs.wannier90 import wannier90
from .inputs.pw2wannier90 import pw2wannier90


def constructor(self):
    generic(self)
    if self.package=='pw':
        pw(self)
    elif self.package=='matdyn':
        matdyn(self)
    elif self.package=='wannier90':
        wannier90(self)
    elif self.package=='pw2wannier90':
        pw2wannier90(self)