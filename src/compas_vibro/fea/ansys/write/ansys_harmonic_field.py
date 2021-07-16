from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from .ansys_nodes import write_constraints
from .ansys_nodes import write_nodes
from .ansys_elements import write_elements
from .ansys_materials import write_materials
from .ansys_process import write_preprocess
from .ansys_loads import write_loads
from .ansys_modal import write_modal_results

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['write_command_file_harmonic_super']


def write_command_file_harmonic_field(structure, fields):
    path = structure.path
    filename = structure.name + '.txt'
    
    write_preprocess(path, filename)
    write_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    # write_modalsuper_solve(structure, path, filename)
    # write_constraints(structure, 'modal', path, filename)
    # write_super_solve_step(structure, path, filename)
    # write_harmonicsuper_solve(structure, path, filename)
    # write_loads(structure, 'harmonic', path, filename)
    # write_super_solve_step(structure, path, filename)
    # # write_loadstep(structure, path, filename)
    # # write_solve_step(structure, path, filename)

    # write_harmonic_results(structure, fields, path, filename)
    # write_modal_results(structure, fields, path, filename)