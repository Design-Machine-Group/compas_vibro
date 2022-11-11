from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['write_heading']

def write_heading(structure, path, filename):
    fh = open(os.path.join(path, filename), 'w')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Heading\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    fh.write('wipe\n')
    fh.write('model basic -ndm 3 -ndf {}\n'.format(structure.num_dof))
    fh.write('#\n')
    fh.write('logFile error.txt\n')
    fh.write('#\n')
    fh.write('#\n')
    fh.close()
