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
           'read_modal_freq',
           'read_modal_coordinates']


def read_harmonic_displacements(structure, path):
    harmonic_disp = {}
    hd = {i:{} for i in range(len(structure.step['harmonic'].freq_list))}
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


def read_participation_factor(out_path):
    p_dict = {}
    fh = open(os.path.join(out_path, 'modal_pfact.txt'), 'r')
    mode = fh.readlines()
    fh.close()
    for j in range(len(mode)):
        p_dict[j] = {'x': {}, 'y': {}, 'z': {}, 'rx': {}, 'ry': {}, 'rz': {}}
        string = mode[j].split(',')
        a = list(map(float, string))
        nkey = int(a[0]) - 1
        p_dict[j]['x']  = a[1]
        p_dict[j]['y']  = a[2]
        p_dict[j]['z']  = a[3]
        p_dict[j]['rx'] = a[4]
        p_dict[j]['ry'] = a[5]
        p_dict[j]['rz'] = a[6]
    return p_dict


def read_effective_mass(out_path):
    m_dict = {}
    fh = open(os.path.join(out_path, 'modal_efmass.txt'), 'r')
    mode = fh.readlines()
    fh.close()
    for j in range(len(mode)):
        m_dict[j] = {'x': {}, 'y': {}, 'z': {}, 'rx': {}, 'ry': {}, 'rz': {}}
        string = mode[j].split(',')
        a = list(map(float, string))
        nkey = int(a[0]) - 1
        m_dict[j]['x']  = a[1]
        m_dict[j]['y']  = a[2]
        m_dict[j]['z']  = a[3]
        m_dict[j]['rx'] = a[4]
        m_dict[j]['ry'] = a[5]
        m_dict[j]['rz'] = a[6]
    return m_dict


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


def read_modal_coordinates(structure, out_path):
    fh = open(os.path.join(out_path, '{}{}.mcf'.format(structure.name, 0)), 'r')
    print(os.path.join(out_path, '{}{}.mcf'.format(structure.name, 0)))
    num_modes = structure.step['modal'].modes
    coo = fh.readlines()[8:]
    ncd = {}
    for i, c in enumerate(coo):
        ncd[i] = {}
        data = c.split()
        ncd[i]['f'] = float(data[0])
        tot = [abs(float(real)) for real in data[1::2]]
        tot = sum(tot)
        cd = {j: {'real':float(data[(j * 2) + 1]), 'imag':float(data[(j * 2) + 2]), 'norm':abs(float(data[(j * 2) + 1])) / tot} for j in range(num_modes)}
        ncd[i].update(cd)
    return ncd
        


if __name__ == '__main__':
    pass
