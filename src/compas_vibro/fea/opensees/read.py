from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

for i in range(60): print()


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['read_modal_displacements']


def read_modal_displacements(outpath, mode):
    disp_dict = {'ux': {}, 'uy': {}, 'uz': {}}
    filepath = os.path.join(outpath, 'mode{}.out'.format(mode + 1))
    fh = open(filepath, 'r')
    line = fh.readline()
    line = line.split(' ')
    nkey = 0
    for i in range(0, len(line), 3):
        a = list(map(float, line[i:i+3]))
        disp_dict['ux'][nkey] = a[0]
        disp_dict['uy'][nkey] = a[1]
        disp_dict['uz'][nkey] = a[2]
        nkey += 1
    return disp_dict

if __name__ == "__main__":
    pass