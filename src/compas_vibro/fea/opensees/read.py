from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

for i in range(60): print()


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['read_modal_displacements',
           'read_modal_frequencies',
           'read_harmonic_displacements']


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

def read_modal_frequencies(outpath):
    filepath = os.path.join(outpath, 'modal_frequencies.out')
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()
    return  {i: float(line) for i, line in enumerate(lines)}

def read_harmonic_displacements(outpath):
    filepath = os.path.join(outpath, 'harmonic_disp.out')
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()
    hd = {}
    for j, line in enumerate(lines):
        line = line.split(' ')
        time = line.pop(0)
        nkey = 0
        hd[j] = {'ux':{}, 'uy': {}, 'uz': {}}
        for i in range(0, len(line), 3):
            a = list(map(float, line[i: i + 3]))
            hd[j]['ux'][nkey] = a[0]
            hd[j]['uy'][nkey] = a[1]
            hd[j]['uz'][nkey] = a[2]
            nkey += 1
    return hd

if __name__ == "__main__":
    pass