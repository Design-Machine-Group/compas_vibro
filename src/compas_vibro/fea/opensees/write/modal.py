from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from compas_vibro.fea.opensees.write.process import write_heading
from compas_vibro.fea.opensees.write.nodes import write_nodes
from compas_vibro.fea.opensees.write.nodes import write_displacements
from compas_vibro.fea.opensees.write.materials import write_materials
from compas_vibro.fea.opensees.write.sections import write_sections
from compas_vibro.fea.opensees.write.elements import write_elements


def write_command_file_modal(structure, fields):
    path = structure.path
    filename = structure.name + '.tcl'

    
    write_heading(path, filename)
    write_nodes(structure, path, filename)
    write_displacements(structure, path, filename)
    write_materials(structure, path, filename)
    write_sections(structure, path, filename)
    write_elements(structure, path, filename)
    if 'u' or 'all' in fields:
        write_modal_shape(structure, path, filename)
    write_modal_solve(structure, path, filename)


def write_modal_solve(structure, path, filename):
    modes = structure.step.modes

    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Eigen Analysis\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    fh.write('eigen  {}\n'.format(modes))
    fh.write('#\n')
    fh.write('record\n')
    fh.write('#\n')
    fh.close()

def write_modal_shape(structure, path, filename):
    modes = structure.step.modes
    num_nodes = len(structure.nodes)
    outpath = os.path.join(path, '{}_output'.format(structure.name))

    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Modal shape recorders\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    string = 'recorder Node -file \"{0}/mode{1}.out\" -nodeRange 1 {2} -dof 1 2 3 "eigen {1}"\n'
    for i in range(modes):
        fh.write(string.format(outpath, i + 1, num_nodes))
    fh.write('#\n')
    fh.write('#\n')
    fh.close()

    