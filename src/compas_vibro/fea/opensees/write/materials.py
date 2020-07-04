from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['write_materials']

def write_materials(structure, path, filename):
    materials = structure.materials
    for key in materials:
        material = materials[key]
        if material.__name__ == 'ElasticIsotropic':
            write_elastic_isotropic(structure, path, filename, key)

def write_elastic_isotropic(structure, path, filename, key):

    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Materials\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')

    i = structure.materials[key].index
    e = structure.materials[key].E['E']
    v = structure.materials[key].v['v']
    p = structure.materials[key].p

    # TODO: Are both lines needed? Why the uniaxial instead of just elastic isotropic?
    # fh.write('uniaxialMaterial Elastic {0} {1}\n'.format(i + 1, e))
    fh.write('nDMaterial ElasticIsotropic {0} {1} {2} {3}\n'.format(i + 1, e, v, p))
    fh.close()