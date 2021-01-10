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
from compas_vibro.fea.opensees.write.materials import write_material
from compas_vibro.fea.opensees.write.sections import write_section
from compas_vibro.fea.opensees.write.elements import write_elements

def write_command_file_static(structure, fields):
    path = structure.path
    filename = structure.name + '.tcl'

    write_heading(path, filename)
    write_nodes(structure, path, filename)
    write_displacements(structure, path, filename)

    eps = structure.element_properties
    for ep in eps:
        material = structure.materials[eps[ep].material]
        section = structure.sections[eps[ep].section]

        write_material(structure, path, filename, material)
        write_section(structure, path, filename, section, ep)
    
    write_elements(structure, path, filename)
    write_static_loads(structure, path, filename)

    write_static_solve(structure, path, filename)

    if 'u' or 'all' in fields:
        write_static_shape(structure, path, filename)
    write_static_analyze(structure, path, filename)    


def write_static_loads(structure, path, filename):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('pattern Plain 1 "Linear" {\n')
    fh.write('load 200 0 0 -50 0 0 0\n')
    fh.write('}\n')
    fh.write('#\n')
    fh.close()

def write_static_solve(structure, path, filename):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('system BandSPD\n')
    fh.write('numberer RCM\n')
    fh.write('constraints Plain\n')
    fh.write('integrator LoadControl 1.0\n')
    fh.write('algorithm Linear\n')
    fh.write('analysis Static\n')
    fh.write('#\n')
    fh.close()

def write_static_shape(structure, path, filename):
    num_nodes = len(structure.nodes)
    outpath = os.path.join(path, '{}_output'.format(structure.name))

    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Static shape recorders\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    string = 'recorder Node -file \"{0}/displacements.out\" -load -nodeRange 1 {1} -dof 1 2 3 disp\n'
    # 'recorder Node -file example.out -load -node 4 -dof 1 2 disp'
    fh.write(string.format(outpath, num_nodes))
    fh.write('#\n')
    fh.write('#\n')
    fh.close()

def write_static_analyze(structure, path, filename):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('analyze 1\n')
    fh.write('#\n')
    fh.close()



"""

# # Create ModelBuilder (with two-dimensions and 2 DOF/node)
# 'model BasicBuilder -ndm 2 -ndf 2'

# Create nodes & add to Domain - command: node nodeId xCrd yCrd
'node 1 0.0 0.0'
'node 2 144.0 0.0'
'node 3 168.0 0.0'
'node 4 72.0 96.0'

# Set the boundary conditions - command: fix nodeID xResrnt? yRestrnt?
'fix 1 1 1'
'fix 2 1 1'
'fix 3 1 1'



# Define materials for truss elements
# Create Elastic material prototype - command: uniaxialMaterial Elastic matID E
'uniaxialMaterial Elastic 1 3000'

# Define elements
# Create truss elements - command: element truss trussID node1 node2 A matID
'element truss 1 1 4 10.0 1'
'element truss 2 2 4 5.0 1'
'element truss 3 3 4 5.0 1'


# Define loads
# Create a Plain load pattern with a linear TimeSeries
# Create the nodal load - command: load nodeID xForce yForce
'pattern Plain 1 "Linear" {'
'load 4 100 -50'
'}'
# End of model generation


# ------------------------------
# Start of analysis generation
# ------------------------------

# Create the system of equation, a SPD using a band storage scheme
'system BandSPD'

# Create the DOF numberer, the reverse Cuthill-McKee algorithm
'numberer RCM'

# Create the constraint handler, a Plain handler is used as homo constraints
'constraints Plain'

# Create the integration scheme, the LoadControl scheme using steps of 1.0
'integrator LoadControl 1.0'

# Create the solution algorithm, a Linear algorithm is created
'algorithm Linear'

# create the analysis object
'analysis Static'
# End of analysis generation


# ------------------------------
# Start of recorder generation
# ------------------------------

# create a Recorder object for the nodal displacements at node 4
'recorder Node -file example.out -load -node 4 -dof 1 2 disp'
# End of recorder generation


# ------------------------------
# Finally perform the analysis
# ------------------------------

# Perform the analysis
'analyze 1'
"""
