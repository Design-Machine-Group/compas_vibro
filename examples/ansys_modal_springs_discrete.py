from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas.datastructures import Mesh
from compas.utilities import geometric_key

import compas_vibro

from compas_vibro.fea import remesh_face_by_face

from compas_vibro.structure import Structure
from compas_vibro.structure import FixedDisplacement
from compas_vibro.structure import PointLoad
from compas_vibro.structure import ShellSection
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties
from compas_vibro.structure import SpringElement
from compas_vibro.structure import SpringSection

from compas_vibro.viewers import StructureViewer

from compas_vibro.viewers import MeshViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


for i in range(60): print('')

path = compas_vibro.TEMP
geometry = 'folded'
name = '{0}_modal_springs'.format(geometry)

# remesh mesh faces to create separate meshes - - - - - - -
mesh = Mesh.from_json(os.path.join(compas_vibro.DATA, 'meshes', '{}.json'.format(geometry)))

meshes = remesh_face_by_face(mesh, .1, weld=False)

# create scructure with all meshes - - - - - - 
s = Structure(path, name)

section = ShellSection('shell_sec', t=.1)
s.add(section)

material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(material)

s.add_nodes_elements_from_meshes(meshes, 'ShellElement', elset='shells')

el_prop = ElementProperties('concrete_shell',
                            material='concrete',
                            section='shell_sec',
                            elset='shells')
s.add(el_prop)

# v = StructureViewer(s)
# v.show_node_labels = True
# v.show()

# # add springs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

# # add a line spring connecting shell boundary to supports - - - - - - -

vks_list = []
for mesh in meshes:
    vks_list.append(list(mesh.vertices_where({'z': (-.01, .01)}))) 

lines = []
supports = []
h = .01
for i, vks in enumerate(vks_list):
    for vk in vks:
        vk = s.check_node_exists(meshes[i].vertex_coordinates(vk))
        x, y, z = s.node_xyz(vk)
        xyz_ = [x, y , z - h]
        sk = s.add_node(xyz_)
        supports.append(sk)
        lines.append([vk, sk])

d = FixedDisplacement('boundary', supports)
s.add(d)

springs = []
for nodes in lines:
    ek = s.add_element(nodes, 'SpringElement', axes={}, check=True)
    springs.append(ek)
s.add_set('springs', 'element', springs)

kx  = 1e12
ky  = 1e12
kz  = 1e12
kxx = 1e12
kyy = 1e12
kzz = 1e12
stiffness = {'x':kx, 'y':ky, 'z':kz, 'xx':kxx, 'yy': kyy, 'zz': kzz}
spring_section = SpringSection('spring_section', stiffness=stiffness)
s.add(spring_section)

prop = ElementProperties(name='springs', 
                         material=None,
                         section='spring_section',
                         elset='springs')
s.add(prop)


# # # add spring between discrete elements - - - - - - - 

# find pairs  - - - - - - - - - 

nk_dict ={}
pairs = []
for nk in s.nodes:
    gk = geometric_key(s.node_xyz(nk))
    if gk in nk_dict:
        pairs.append((nk, nk_dict[gk]))
    else:
        nk_dict[gk] = nk

springs = []
for nodes in pairs:
    ek = s.add_element(nodes, 'SpringElement', axes={}, check=True)
    springs.append(ek)
s.add_set('springs_joints', 'element', springs)

kx  = 1e10
ky  = 1e10
kz  = 1e10
kxx = 1e3
kyy = 1e3
kzz = 1e3
stiffness = {'x':kx, 'y':ky, 'z':kz, 'xx':kxx, 'yy': kyy, 'zz': kzz}
spring_section = SpringSection('spring_section_joints', stiffness=stiffness)
s.add(spring_section)

prop = ElementProperties(name='spring_joints', 
                         material=None,
                         section='spring_section_joints',
                         elset='springs_joints')
s.add(prop)


# # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# # v = StructureViewer(s)
# # # v.show_node_labels = True
# # v.show()


s.analyze_modal(backend='ansys', fields=['f', 'u'], num_modes=20)
# s.to_obj()
v = StructureViewer(s)
v.modal_scale = 1e1
# v.show_legend = False
v.show('modal')

# modes = s.results['modal'].keys()
# for mode in modes:
#     f = s.results['modal'][mode].frequency
#     pf = s.results['modal'][mode].pfact['z']
#     em = s.results['modal'][mode].efmass['z']
#     print(mode, f, pf, em)
