from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas.datastructures import Mesh

import compas_vibro


from compas_vibro.structure import Structure
from compas_vibro.structure import FixedDisplacement
from compas_vibro.structure import PointLoad
from compas_vibro.structure import ShellSection
from compas_vibro.structure import ISection
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties

from compas_vibro.viewers import ModalViewer, PlotlyStructureViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


for i in range(60): print('')

path = compas_vibro.TEMP
geometry = 'flat_mesh_20x20'
name = 'ansys_{0}_modal'.format(geometry)


## Add shell geometry from mesh-----------------------------------------------------------
mesh = Mesh.from_json(compas_vibro.get('{0}.json'.format(geometry)))
s = Structure(path, name)

s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

## Add fixed nodes from mesh boundary ----------------------------------------------------

d = FixedDisplacement('boundary', mesh.vertices_on_boundary())
s.add(d)

## Add beam elements ---------------------------------------------------------------------

sp = s.node_xyz(266)
ep = [sp[0], sp[1], sp[2] - 3]
lines =[[sp, ep]]
s.add_nodes_elements_from_lines(lines, 'BeamElement', elset='beams')


## Add sections --------------------------------------------------------------------------

shell_section = ShellSection('shell_sec', t=.1)
s.add(shell_section)

# beam_section = ISection('beam_sec', b=.2, h=.2, tw=.01, tf=.01)
# s.add(beam_section)

## Add materials -------------------------------------------------------------------------

shell_material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(shell_material)

# beam_material = ElasticIsotropic('steel', E=210e9, v=.3, p=7500)
# s.add(beam_material)

## Add element properties ----------------------------------------------------------------

el_prop_shell = ElementProperties('concrete_shell',
                                  material='concrete',
                                  section='shell_sec',
                                  elset='shell')
s.add(el_prop_shell)

# el_prop_beams = ElementProperties('steel_beams',
#                                   material='steel',
#                                   section='beam_sec',
#                                   elset='beams')
# s.add(el_prop_beams)

## Visualize structure--------------------------------------------------------------------

v = PlotlyStructureViewer(s)
# v.show_node_labels = True
v.show()


## Analyze model -------------------------------------------------------------------------

# s.analyze_modal(backend='ansys', fields=['f', 'u'], num_modes=20)


## Plot results --------------------------------------------------------------------------
# v = ModalViewer(s)
# v.show()

# modes = s.results['modal'].keys()
# for mode in modes:
#     f = s.results['modal'][mode].frequency
#     pf = s.results['modal'][mode].pfact['z']
#     em = s.results['modal'][mode].efmass['z']
#     print(mode, f, pf, em)