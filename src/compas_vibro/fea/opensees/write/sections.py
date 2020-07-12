from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['write_sections']


def write_sections(structure, path, filename):
    for sk in structure.sections:
        sec_type = structure.sections[sk].__name__
        if  sec_type == 'ShellSection':
            write_shell_sections(structure, path, filename, sk)
        else:
            raise NameError('The \'{}\' section type is not yet implmenented'.format(sec_type))


def write_shell_sections(structure, path, filename, key):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Shell sections\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    i = structure.sections[key].index
    t = structure.sections[key].geometry['t']
    e = 30e9
    v = .2
    p = 2400
    string = 'section ElasticMembranePlateSection {0} {1} {2} {3} {4}\n'
    fh.write(string.format(i + 1,  e, v, t, p))
    fh.write('#\n')
    # fh.write('set EleType ShellMITC4\n')  # Is this required?
    fh.close()
