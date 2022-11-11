from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['write_nodes',
           'write_displacements']

def write_nodes(structure, path, filename):

   fh = open(os.path.join(path, filename), 'a')
   fh.write('#\n')
   fh.write('#-{} \n'.format('-'*80))
   fh.write('# Nodes\n')
   fh.write('#-{} \n'.format('-'*80))
   fh.write('#\n')

   for nk in structure.nodes:
      x, y, z = structure.node_xyz(nk)
      fh.write('node {0} {1} {2} {3}\n'.format(nk + 1, x, y, z))
   fh.write('#\n')
   fh.close()

def write_displacements(structure, path, filename):
   
   fh = open(os.path.join(path, filename), 'a')
   fh.write('#\n')
   fh.write('#-{} \n'.format('-'*80))
   fh.write('# Displacements\n')
   fh.write('#-{} \n'.format('-'*80))
   fh.write('#\n')

   if structure.num_dof == 3:
      f_string = 'fix {} 1 1 1\n'
      p_string = 'fix {} 1 1 1\n'
   else:
      f_string = 'fix {} 1 1 1 1 1 1\n'
      p_string = 'fix {} 1 1 1 0 0 0\n'

   for dk in structure.displacements:
      d = structure.displacements[dk]
      if d.__name__== 'FixedDisplacement':
         string = f_string
      elif d.__name__ == 'PinnedDisplacement':
         string = p_string
      for nk in d.nodes:
         fh.write(string.format(nk + 1))
   fh.write('#\n')
   fh.close()