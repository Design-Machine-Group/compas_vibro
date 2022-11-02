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
           'read_modal_coordinates',
           'read_harmonic_displacements_field']


def read_harmonic_displacements(structure, path, freq_list):
    # harmonic_disp = {}
    hd = {i:{} for i in range(len(freq_list))}
    for nkey in structure.nodes:
        filename  = 'node_real_{0}.txt'.format(nkey + 1)
        filename_ = 'node_imag_{0}.txt'.format(nkey + 1)

        fh = open(os.path.join(path, filename), 'r')
        dreal = fh.readlines()
        fh.close()

        fh = open(os.path.join(path, filename_), 'r')
        dimag = fh.readlines()
        fh.close()

        # harmonic_disp[nkey] = {} 
        for j in range(len(dreal)):
            
            real_string = dreal[j].split(',')
            imag_string = dimag[j].split(',')
            # frequency = float(real_string[0])
            real = list(map(float, real_string))
            imag = list(map(float, imag_string))
            nd = {'real': {'x': real[1], 'y': real[2], 'z': real[3]},
                  'imag': {'x': imag[1], 'y': imag[2], 'z': imag[3]}}
            # harmonic_disp[nkey][j] = nd
            # hd[j].update({'frequency':frequency})
            hd[j].update({nkey:nd})

    return hd


def read_harmonic_displacements_field(structure, path, freq_list):
    # harmonic_disp = {}
    hd = {i:{} for i in range(len(freq_list))}
    for fk in hd:
        path_ = os.path.join(path, 'freq_{}'.format(fk))
        fd = {}
        for nkey in structure.nodes:

            filename  = 'node_real_{0}.txt'.format(nkey + 1)
            filename_ = 'node_imag_{0}.txt'.format(nkey + 1)

            fh = open(os.path.join(path_, filename), 'r')
            dreal = fh.readlines()
            fh.close()

            fh = open(os.path.join(path_, filename_), 'r')
            dimag = fh.readlines()
            fh.close()

            real_string = dreal[0].split(',')
            imag_string = dimag[0].split(',')
            real = list(map(float, real_string))
            imag = list(map(float, imag_string))
            nd = {'real': {'x': real[1], 'y': real[2], 'z': real[3]},
                'imag': {'x': imag[1], 'y': imag[2], 'z': imag[3]}}
            fd[nkey] = nd
        hd[fk] = fd
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
    fh = open(os.path.join(out_path, '{}_{}.mcf'.format(structure.name, 0)), 'r')
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
        

def read_static_displacements(out_path):
    filename = 'static_displacements.txt'
    fh = open(os.path.join(out_path, filename))
    displacements = fh.readlines()

    sd = {'ux': {}, 'uy': {}, 'uz': {}, 'um': {}}
    for disp in displacements:
        dstring = disp.split(',')
        disp = list(map(float, dstring[1:]))
        key = int(float(dstring[0])) - 1
        sd['ux'][key] = disp[0]
        sd['uy'][key] = disp[1]
        sd['uz'][key] = disp[2]
        sd['um'][key] = length_vector([disp[0], disp[1], disp[2]])
        # print(sd['um'][key])
    return sd


def read_static_stresses(out_path):
    filename = 'static_nodal_stresses.txt'
    try:
        sfile   = open(os.path.join(out_path, filename), 'r')
    except(Exception):
        return None

    s = sfile.readlines()
    stress_dict = {'sxt': {}, 'syt': {}, 'szt': {}, 'sxb': {}, 'syb': {}, 'szb': {}}
    for i in range(len(s)):
        s_string = s[i].split(',')
        stress = list(map(float, s_string))
        key = int(stress[0]) - 1
        stress_dict['sxt'][key] = float(stress[4])
        stress_dict['syt'][key] = float(stress[5])
        stress_dict['szt'][key] = float(stress[6])
        stress_dict['sxb'][key] = float(stress[1])
        stress_dict['syb'][key] = float(stress[2])
        stress_dict['szb'][key] = float(stress[3])

    return stress_dict


def read_principal_stresses(out_path):
    filename = 'static_principal_stresses.txt'
    psfile   = open(os.path.join(out_path, filename), 'r')
    ps = psfile.readlines()

    p_stress_dict = {'ps1t': {}, 'ps2t': {}, 'ps3t': {}, 'ps1b': {}, 'ps2b': {}, 'ps3b': {}}
    for i in range(len(ps)):
        psstring = ps[i].split(',')
        p_stress = list(map(float, psstring))
        key = int(p_stress[0]) - 1
        p_stress_dict['ps1t'][key] = float(p_stress[4])
        p_stress_dict['ps2t'][key] = float(p_stress[5])
        p_stress_dict['ps3t'][key] = float(p_stress[6])
        p_stress_dict['ps1b'][key] = float(p_stress[1])
        p_stress_dict['ps2b'][key] = float(p_stress[2])
        p_stress_dict['ps3b'][key] = float(p_stress[3])

    return p_stress_dict


def read_shear_stresses(out_path):
    filename = 'static_shear_stresses.txt'
    psfile = open(os.path.join(out_path, filename), 'r')
    ss = psfile.readlines()
    ss_dict = {'sxyt': {}, 'syzt': {}, 'sxzt': {}, 'sxyb': {}, 'syzb': {}, 'sxzb': {}}
    for i in range(len(ss)):
        ss_string = ss[i].split(',')
        ss_stress = list(map(float, ss_string))
        key = int(ss_stress[0]) - 1
        ss_dict['sxyt'][key] = float(ss_stress[4])
        ss_dict['syzt'][key] = float(ss_stress[5])
        ss_dict['sxzt'][key] = float(ss_stress[6])
        ss_dict['sxyb'][key] = float(ss_stress[1])
        ss_dict['syzb'][key] = float(ss_stress[2])
        ss_dict['sxzb'][key] = float(ss_stress[3])
    return ss_dict


def read_reactions(out_path):
    filename = 'static_reactions.txt'
    rfile   = open(os.path.join(out_path, filename), 'r')
    r = rfile.readlines()
    react_dict = {'rmx': {}, 'rmy': {}, 'rmz': {}, 'rfx': {}, 'rfy': {}, 'rfz': {}, 'rfm': {}}
    for i in range(len(r)):
        r_string = r[i].split(',')
        reaction = list(map(float, r_string))
        key = int(reaction[0]) - 1
        if all(v == 0.0 for v in reaction) is False:
            react_dict['rmx'][key] = float(reaction[4])
            react_dict['rmy'][key] = float(reaction[5])
            react_dict['rmz'][key] = float(reaction[6])
            react_dict['rfx'][key] = float(reaction[1])
            react_dict['rfy'][key] = float(reaction[2])
            react_dict['rfz'][key] = float(reaction[3])
            react_dict['rfm'][key] = length_vector([reaction[1], reaction[2], reaction[3]])
    return react_dict


if __name__ == '__main__':
    pass
