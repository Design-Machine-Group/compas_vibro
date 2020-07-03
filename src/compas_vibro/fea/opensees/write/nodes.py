from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

def write_nodes(structure, path, filename):
   
   fh = open(os.path.join(path, filename), 'w')
   fh.write('#\n')
   fh.write('#-{} \n'.format('-'*80))
   fh.write('# Nodes\n')
   fh.write('#-{} \n'.format('-'*80))
   fh.write('#\n')

   for nk in structure.nodes:
      x, y, z = structure.node_xyz(nk)
      fh.write('node {0} {1} {2} {3}\n'.format(nk, x, y, z))
   fh.write('#\n')
   fh.close()
