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

## Add beam elements ---------------------------------------------------------------------

sp = s.node_xyz(266)
ep = [sp[0], sp[1], sp[2] - 3]
lines =[[sp, ep]]
beam_k = s.add_nodes_elements_from_lines(lines, 'BeamElement', elset='beams', normal=[0,1,0])[0]

## Add fixed nodes from mesh boundary and beams ------------------------------------------

d = FixedDisplacement('boundary', mesh.vertices_on_boundary())
s.add(d)

beam_end = s.elements[beam_k].nodes[-1]
d = FixedDisplacement('beam_ends', [beam_end])
s.add(d)


## Add sections --------------------------------------------------------------------------

shell_section = ShellSection('shell_sec', t=.1)
s.add(shell_section)

beam_section = ISection('beam_sec', b=.2, h=.2, tw=.01, tf=.01)
s.add(beam_section)

## Add materials -------------------------------------------------------------------------

shell_material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(shell_material)

beam_material = ElasticIsotropic('steel', E=210e9, v=.3, p=7500)
s.add(beam_material)

## Add element properties ----------------------------------------------------------------

el_prop_shell = ElementProperties('concrete_shell',
                                  material='concrete',
                                  section='shell_sec',
                                  elset='shell',
                                  is_rad=True)
s.add(el_prop_shell)

el_prop_beams = ElementProperties('steel_beams',
                                  material='steel',
                                  section='beam_sec',
                                  elset='beams',
                                  is_rad=False)
s.add(el_prop_beams)

## Visualize structure--------------------------------------------------------------------

# v = PlotlyStructureViewer(s)
# # v.show_node_labels = True
# v.show()

## Analyze model -------------------------------------------------------------------------

s.analyze_modal(backend='ansys', fields=['f', 'u'], num_modes=20)


## Plot results --------------------------------------------------------------------------


print(' N | Freq.   | P.fac   | Eff.mass | Eff.M.R  | Cum EMR')
modes = s.results['modal'].keys()
cemr = 0
for mode in modes:
    f = s.results['modal'][mode].frequency
    pf = s.results['modal'][mode].pfact['z']
    em = s.results['modal'][mode].efmass['z']
    emr = s.results['modal'][mode].efmass_r['z']
    cemr += emr
    print('{:2d} | {:7.3F} | {:7.3F} | {:8.3F} | {:8.3F} | {:8.3F}'.format(mode, f, pf, em, emr, cemr))


# v = ModalViewer(s)
# v.show()

# TODO: Modal viewer with beams, how to display beam orientation?