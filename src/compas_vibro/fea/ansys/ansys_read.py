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


def get_modal_shapes_from_result_files(out_path):
    try:
        filenames = [f in os.listdir(out_path) if f.startswith('modal_shape_')]
    except(Exception):
        print ('Result files not found')
        return None, None
        
    modal_files = []
    for i in range(len(filenames)):
        f = 'modal_shape_' + str(i + 1) + '.txt'
        modal_files.append(open(os.path.join(out_path, f), 'r'))

    modes_dict = {}
    for i, f in enumerate(modal_files):
        modes_dict['ux' + str(i)] = {}
        modes_dict['uy' + str(i)] = {}
        modes_dict['uz' + str(i)] = {}
        modes_dict['um' + str(i)] = {}
        mode = f.readlines()
        for j in range(len(mode)):
            string = mode[j].split(',')
            a = map(float, string[1:])
            nkey = int(a[0]) - 1
            modes_dict['ux' + str(i)][nkey] = a[1]
            modes_dict['uy' + str(i)][nkey] = a[2]
            modes_dict['uz' + str(i)][nkey] = a[3]
            modes_dict['um' + str(i)][nkey] = a[4]
        f.close()

    return modes_dict


def get_modal_freq_from_result_files(out_path):
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
