from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_vibro.structure import Structure
from compas_vibro.structure import FixedDisplacement
from compas_vibro.structure import PointLoad
from compas_vibro.structure import ShellSection
from compas_vibro.structure import ISection
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties
from compas_vibro.viewers import StructureViewer

import compas_vibro
from compas_vibro.structure import Mesh
from compas_vibro.vibro import from_W_to_dB

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
name = 'shell_beams_harmonic'
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

beam_section = ISection('beam_sec', b=.2, h=.2, tw=.01, tf=.01)
s.add(beam_section)

# ## Add materials -----------------------------------------------------------------------

clt_material = ElasticIsotropic('clt', E=7e9, v=.42, p=500)
s.add(clt_material)

beam_material = ElasticIsotropic('steel', E=210e9, v=.3, p=7500)
s.add(beam_material)

## Add loads -----------------------------------------------------------------------------
cpt = mesh.identify_center_point()
load_pts = [cpt]

load = PointLoad(name='pload', nodes=load_pts, x=0, y=0, z=1, xx=0, yy=0, zz=0)
s.add(load)

## Add sets ------------------------------------------------------------------------------

fins = list(mesh.faces_where({'is_fin':True}))
no_fins = list(mesh.faces_where({'is_fin':False}))
s.add_set('fins', 'element', fins)
s.add_set('no_fins', 'element', no_fins)

# ## Add element properties --------------------------------------------------------------

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

# ## Visualize structure------------------------------------------------------------------

v = StructureViewer(s)
v.show()

# # Analyze model -------------------------------------------------------------------------

freq_list = list(range(20, 300, 5))
num_modes = 25
damping=.02

s.analyze_harmonic_super(num_modes, freq_list, fields=['u'], backend='ansys', damping=damping)
s.compute_rad_power()

s.to_obj(path=os.path.join(compas_vibro.DATA, 'structures'), name=name)

## Plot results --------------------------------------------------------------------------

print(' N |  Hz | Rad.Pow.(W)  | Rad.Pow.(dB)')
for k in s.results['radiation']:
    f = s.results['radiation'][k].frequency
    p = s.results['radiation'][k].radiated_p
    db = from_W_to_dB(p)
    print('{:2d} | {:3d} | {:e} | {:7.3F}'.format(k, f, p, db))


