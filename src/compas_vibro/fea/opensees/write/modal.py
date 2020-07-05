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

s = """
#------------------------------------------------------------------
# Steps
#------------------------------------------------------------------
#
# step_load
#----------
#
timeSeries Constant 1 -factor 1.0
pattern Plain 1 1 -fact 1 {
#
# load_weights
#-------------
#
load 16 0.0 0.0 -100.0 0.0 0.0 0.0
load 15 0.0 0.0 -100.0 0.0 0.0 0.0
#
#
#
# Output
#-------
#
}  
#
#  
recorder Node -file /Users/tmendeze/Documents/UW/04_code/compas_vibro/temp/step_load_u.out -time -nodeRange 1 117 -dof 1 2 3 disp
#
#
# Element recorders
#------------------
#
#
# Solver
#-------
#
#
constraints Transformation
numberer RCM
system ProfileSPD
test NormUnbalance 0.01 100 5
algorithm NewtonLineSearch
integrator LoadControl 0.01
analysis Static
analyze 100
"""

def write_command_file_modal(structure, path):
    path = structure.path
    filename = structure.name + '.tcl'
    
    write_heading(path, filename)
    write_nodes(structure, path, filename)
    write_displacements(structure, path, filename)
    write_materials(structure, path, filename)
    write_sections(structure, path, filename)
    write_elements(structure, path, filename)


    write_modal_solve(structure, path, filename)
    # write_constraints(structure, path, filename)
    # write_loadstep(structure, path, filename)
    # write_solve_step(structure, path, filename)
    # write_modal_results(structure, fields, path, filename)

def write_modal_solve(structure, path, filename):
    # num_modes = structure.step.modes
    fh = open(os.path.join(path, filename), 'a')
    fh.write(s)
    fh.close()
