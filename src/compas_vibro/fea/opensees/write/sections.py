from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['write_section']


def write_section(structure, path, filename, section, ep_key):
    sec_type = section.__name__
    if  sec_type == 'ShellSection':
        write_shell_section(structure, path, filename, section, ep_key)
    else:
        raise NameError('The \'{}\' section type is not yet implmenented'.format(sec_type))


def write_shell_section(structure, path, filename, section, ep_key):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Shell sections\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    i = section.index
    t = section.geometry['t']
    e = structure.materials[structure.element_properties[ep_key].material].E['E']
    v = structure.materials[structure.element_properties[ep_key].material].v['v']
    p = structure.materials[structure.element_properties[ep_key].material].p
    string = 'section ElasticMembranePlateSection {0} {1} {2} {3} {4}\n'
    fh.write(string.format(i + 1,  e, v, t, p))
    fh.write('#\n')
    # fh.write('set EleType ShellMITC4\n')  # Is this required?
    fh.close()
