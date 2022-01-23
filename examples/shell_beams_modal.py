from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import compas_vibro

from compas_vibro.structure import Structure
from compas_vibro.structure import FixedDisplacement
from compas_vibro.structure import PointLoad
from compas_vibro.structure import ShellSection
from compas_vibro.structure import ISection, BoxSection, RectangularSection
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties
from compas_vibro.structure import Mesh

from compas_vibro.viewers import StructureViewer

from compas.geometry import is_point_on_polyline_xy
from compas.geometry import is_point_on_line_xy
from compas.geometry import distance_point_point

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


for i in range(60): print('')

path = os.path.join(compas_vibro.TEMP)
name = 'shell_recbeams_modal'


mesh = Mesh.from_json(os.path.join(compas_vibro.DATA, 'meshes', 'pattern1_fins.json'))

## Add shell geometry from mesh-----------------------------------------------------------

s = Structure(path, name)

s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='floor')

## Add beam elements ---------------------------------------------------------------------

pl = mesh.bounding_box_xy()
pl.append(pl[0])

vks = []
for vk in mesh.vertices():
    pt = mesh.vertex_coordinates(vk)
    if is_point_on_polyline_xy(pt, pl):
        if pt[2] == 0:
            vks.append(vk)

skeys = []
for i in range(len(pl) - 1):
    vks_line = [vk for vk in vks if is_point_on_line_xy(mesh.vertex_coordinates(vk), [pl[i], pl[i + 1]])]
    dist = [(vk, distance_point_point(mesh.vertex_coordinates(vk), pl[i])) for vk in vks_line]
    sdist = sorted(dist, key = lambda x: x[1]) 
    skeys_ = [j[0] for j in sdist if j[0] not in skeys]
    skeys.extend(skeys_) 
skeys.append(skeys[0])

lines = [[skeys[i], skeys[i+1]] for i in range(len(skeys) - 1)]
lines = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u, v in lines]
beam_k = s.add_nodes_elements_from_lines(lines, 'BeamElement', elset='beams', normal=[0, 0, 1])


## Add fixed nodes from mesh boundary and beams ----------------------------------------

fixed = [s.check_node_exists(pt) for pt in pl[:-1]]
# fixed = skeys
d = FixedDisplacement('corners', fixed)
s.add(d)

# ## Add sections ------------------------------------------------------------------------

shell_section = ShellSection('shell_sec', t=.1)
s.add(shell_section)

# beam_section = ISection('beam_sec', b=.2, h=.2, tw=.01, tf=.01)
beam_section = BoxSection('beam_sec',  b=.15, h=.25, tw=.03, tf=.01)
# beam_section = RectangularSection('beam_sec', b=.15, h=.25)
s.add(beam_section)

# ## Add materials -----------------------------------------------------------------------

clt_material = ElasticIsotropic('clt', E=7e9, v=.42, p=500)
s.add(clt_material)

beam_material = ElasticIsotropic('steel', E=210e9, v=.3, p=7500)
s.add(beam_material)

## Add sets ------------------------------------------------------------------------------

fins = list(mesh.faces_where({'is_fin':True}))
no_fins = list(mesh.faces_where({'is_fin':False}))
s.add_set('fins', 'element', fins)
s.add_set('no_fins', 'element', no_fins)

# ## Add element properties ----------------------------------------------------------------

el_prop1 = ElementProperties('fins_elset',
                            material='clt',
                            section='shell_sec',
                            elset='fins',
                            is_rad=False)
s.add(el_prop1)


el_prop2 = ElementProperties('no_fins_elset',
                            material='clt',
                            section='shell_sec',
                            elset='no_fins',
                            is_rad=True)
s.add(el_prop2)


el_prop_beams = ElementProperties('steel_beams',
                                  material='steel',
                                  section='beam_sec',
                                  elset='beams',
                                  is_rad=False)
s.add(el_prop_beams)

# ## Visualize structure--------------------------------------------------------------------

v = StructureViewer(s)
v.show()

# # Analyze model -------------------------------------------------------------------------

s.analyze_modal(backend='ansys', fields=['f', 'u'], num_modes=20)

# s.to_obj(path=os.path.join(compas_vibro.DATA, 'structures'), name=name)
# s.to_obj(path=compas_vibro.TEMP, name=name)

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


