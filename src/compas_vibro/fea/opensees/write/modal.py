from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from compas_vibro.fea.opensees.write.process import write_heading
from compas_vibro.fea.opensees.write.nodes import write_nodes
from compas_vibro.fea.opensees.write.nodes import write_displacements
from compas_vibro.fea.opensees.write.materials import write_materials


def write_command_file_modal(structure, path):
    path = structure.path
    filename = structure.name + '.tcl'
    
    write_heading(path, filename)
    write_nodes(structure, path, filename)
    write_displacements(structure, path, filename)
    write_materials(structure, path, filename)

    # write_nodes(structure, path, filename)
    # write_elements(structure, path, filename)
    # write_modal_solve(structure, path, filename)
    # write_constraints(structure, path, filename)
    # write_loadstep(structure, path, filename)
    # write_solve_step(structure, path, filename)
    # write_modal_results(structure, fields, path, filename)