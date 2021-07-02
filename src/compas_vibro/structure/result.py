from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from compas.geometry import length_vector


TPL = """
################################################################################
compas_vibro Result
################################################################################

Frequency
---------
{0}

Type
----
{1}
"""


class Result(object):

    def __init__(self, frequency, name='VibroResult', type=None):

        self.displacements          = {}
        self.frequency              = frequency
        self.name                   = name
        self.tol                    = '3'
        self.type                   = type
        self.pfact                  = {}
        self.efmass                 = {}
        self.efmass_r               = {}

    def __str__(self):
        return TPL.format(self.frequency, self.type)

    def compute_max_displacement(self):
        d = []
        nodes = list(self.displacements['ux'].keys())
        for vk in nodes:
            dx = self.displacements['ux'][vk]
            dy = self.displacements['uy'][vk]
            dz = self.displacements['uz'][vk]
            d.append(length_vector([dx, dy, dz]))
        return max(d)


if __name__ == '__main__':
    pass
