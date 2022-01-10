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
        _ = line.pop(0)
        nkey = 0
        hd[j] = {'ux':{}, 'uy': {}, 'uz': {}}
        for i in range(0, len(line), 3):
            a = list(map(float, line[i: i + 3]))
            hd[j]['ux'][nkey] = a[0]
            hd[j]['uy'][nkey] = a[1]
            hd[j]['uz'][nkey] = a[2]
            nkey += 1
    return hd

def read_static_displacements(outpath):
    filepath = os.path.join(outpath, 'displacements.out')
    fh = open(filepath, 'r')
    line = fh.readline()
    fh.close()
    line = line.split(' ')
    _ = line.pop(0)
    nkey = 0
    sd = {'ux':{}, 'uy': {}, 'uz': {}}
    for i in range(0, len(line), 3):
        a = list(map(float, line[i: i + 3]))
        sd['ux'][nkey] = a[0]
        sd['uy'][nkey] = a[1]
        sd['uz'][nkey] = a[2]
        nkey += 1
    return sd

def read_modal_masses(outpath, num_modes):
    filepath = os.path.join(outpath, 'modal_masses.txt')
    fh = open(filepath, 'r')
    lines = fh.readlines()
    fh.close()
    s1 = '* 9. MODAL PARTICIPATION MASS RATIOS (%):\n'
    n1 = lines.index(s1) + 4
    s2 = '* 7. MODAL PARTICIPATION MASSES:\n'
    n2 = lines.index(s2) + 4
    mod_mass = {}
    mod_mass_r = {}
    for i in range(num_modes):
        line = lines[n1 + i]
        line = " ".join(line.split())
        m = line.split(' ')
        m = [float(_) / 100. for _ in m]
        mod_mass_r[i] = {'x': m[1], 'y':m[2], 'z':m[3],
                        'xx':m[4], 'yy':m[5], 'zz':m[6]}
        
        line = lines[n2 + i]
        line = " ".join(line.split())
        m = line.split(' ')
        mod_mass[i] = {'x': m[1], 'y':m[2], 'z':m[3],
                        'xx':m[4], 'yy':m[5], 'zz':m[6]}

    return mod_mass, mod_mass_r


if __name__ == "__main__":
    pass