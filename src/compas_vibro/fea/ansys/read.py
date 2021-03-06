from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
from compas.geometry import length_vector


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['read_harmonic_displacements',
           'read_modal_displacements',
           'read_modal_freq']

def read_harmonic_displacements(structure, path):
    harmonic_disp = {}
    hd = {i:{} for i in range(len(structure.step.freq_list))}
    for nkey in structure.nodes:
        filename  = 'node_real_{0}.txt'.format(nkey + 1)
        filename_ = 'node_imag_{0}.txt'.format(nkey + 1)

        fh = open(os.path.join(path, filename), 'r')
        dreal = fh.readlines()
        fh.close()

        fh = open(os.path.join(path, filename_), 'r')
        dimag = fh.readlines()
        fh.close()

        harmonic_disp[nkey] = {} 
        for j in range(len(dreal)):
            
            real_string = dreal[j].split(',')
            imag_string = dimag[j].split(',')
            # frequency = float(real_string[0])
            real = list(map(float, real_string))
            imag = list(map(float, imag_string))
            nd = {'real': {'x': real[1], 'y': real[2], 'z': real[3]},
                  'imag': {'x': imag[1], 'y': imag[2], 'z': imag[3]}}
            harmonic_disp[nkey][j] = nd
            # hd[j].update({'frequency':frequency})
            hd[j].update({nkey:nd})

    return hd


def read_modal_displacements(out_path, mode):
    disp_dict = {'ux': {}, 'uy': {}, 'uz': {}}

    fh = open(os.path.join(out_path, 'modal_shape_{}.txt'.format(str(mode))), 'r')
    mode = fh.readlines()
    fh.close()
    for j in range(len(mode)):
        string = mode[j].split(',')
        a = list(map(float, string))
        nkey = int(a[0]) - 1
        disp_dict['ux'][nkey] = a[1]
        disp_dict['uy'][nkey] = a[2]
        disp_dict['uz'][nkey] = a[3]
    return disp_dict


def read_modal_freq(out_path):
    modal_freq_file = open(os.path.join(out_path, 'modal_freq.txt'), 'r')
    if modal_freq_file:
        modal_freqs = {}
        freqs = modal_freq_file.readlines()
        for freq in freqs:
            string = freq.split(',')
            modal_freqs[int(float(string[0])) - 1] = float(string[1])
    else:
        modal_freqs = None

    return modal_freqs


if __name__ == '__main__':
    pass
