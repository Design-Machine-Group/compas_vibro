from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import re
from compas.geometry import length_vector


# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)



def get_harmonic_data_from_result_files(structure, path, step):

    freq = structure.steps[step].freq_list[0]
    harmonic_path = os.path.join(path, 'harmonic_out')
    filename  = 'harmonic_disp_real_{0}_Hz.txt'.format(freq)
    filename_ = 'harmonic_disp_imag_{0}_Hz.txt'.format(freq)

    fh = open(os.path.join(harmonic_path, filename), 'r')
    dreal = fh.readlines()
    fh.close()

    fh = open(os.path.join(harmonic_path, filename_), 'r')
    dimag = fh.readlines()
    fh.close()

    harmonic_disp = {}
    for j in range(len(dreal)):
        real_string = dreal[j].split(',')
        imag_string = dimag[j].split(',')
        nkey = int(float(real_string[0]) - 1)
        del real_string[0]
        del imag_string[0]
        harmonic_disp[nkey] = {}
        real = map(float, real_string)
        imag = map(float, imag_string)
        harmonic_disp[nkey][freq] = {'real': {'x': real[0], 'y': real[1], 'z': real[2]},
                                     'imag': {'x': imag[0], 'y': imag[1], 'z': imag[2]}}

    return harmonic_disp, structure.steps[step].freq_list


def read_modal_displacements(out_path, mode):
    disp_dict = {'ux': {}, 'uy': {}, 'uz': {}}

    fh = open(os.path.join(out_path, 'modal_shape_{}.txt'.format(str(mode))), 'r')
    mode = fh.readlines()
    fh.close()
    for j in range(len(mode)):
        string = mode[j].split(',')
        a = list(map(float, string))
        nkey = int(a[0]) - 1
        disp_dict['ux'][nkey] = a[0]
        disp_dict['uy'][nkey] = a[1]
        disp_dict['uz'][nkey] = a[2]
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
