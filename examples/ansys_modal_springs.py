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
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties
from compas_vibro.structure import SpringElement
from compas_vibro.structure import SpringSection

from compas_vibro.viewers import StructureViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


for i in range(60): print('')

path = compas_vibro.TEMP
geometry = 'flat_mesh_20x20'
name = 'ansys_{0}_modal'.format(geometry)

mesh = Mesh.from_json(os.path.join(compas_vibro.DATA, 'meshes', '{}.json'.format(geometry)))
s = Structure(path, name)

s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

# add springs - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

nkeys = [220]
skeys = []
for nkey in nkeys:
    skey = s.add_nodal_element(nkey, 'SpringElement', virtual_node=True)
    skeys.append(skey)
s.add_set('springs', 'element', skeys)

kx = 1e10
ky = 1e10
kz = 1e10
kxx = 1e10
stiffness = {'x':kx, 'y':ky, 'z':kz, 'xx':kxx}
spring_section = SpringSection('spring_section', stiffness=stiffness)
s.add(spring_section)

prop = ElementProperties(name='springs', 
                         material=None,
                         section='spring_section',
                         elset='springs')
s.add(prop)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

d = FixedDisplacement('boundary', mesh.vertices_on_boundary())
s.add(d)

section = ShellSection('shell_sec', t=.1)
s.add(section)

material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(material)

el_prop = ElementProperties('concrete_shell',
                            material='concrete',
                            section='shell_sec',
                            elset='shell')
s.add(el_prop)


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

v = StructureViewer(s)
# v.show_node_labels = True
v.show()


# s.analyze_modal(backend='ansys', fields=['f', 'u'], num_modes=20)
# s.to_obj()
# v = StructureViewer(s)
# v.show('modal')

# modes = s.results['modal'].keys()
# for mode in modes:
#     f = s.results['modal'][mode].frequency
#     pf = s.results['modal'][mode].pfact['z']
#     em = s.results['modal'][mode].efmass['z']
#     print(mode, f, pf, em)

# TODO: Add spring elements/sections, figure out how many types are needed
# TODO: Fix overlap in modal viewer, by getting rid of color bar