from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas_vibro.structure import Mesh

import compas_vibro

from compas_vibro.structure import Structure
from compas_vibro.structure import FixedDisplacement
# from compas_vibro.structure import PointLoad
from compas_vibro.structure import ShellSection
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties

from compas_vibro.viewers import StructureViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


path = compas_vibro.TEMP
geometry = 'flat_mesh_10x10'
name = '{}'.format(geometry)


fp = os.path.join(compas_vibro.DATA, 'meshes', '{}.json'.format(geometry))

mesh = Mesh.from_json(fp)

print(mesh.summary())

# make an instance of the stucture object - - - - - - - - - - - - - - - - - - - 
s = Structure(path, name) 

# add nodes and elements from mesh - - - - - - - - - - - - - - - - - - - - - - - 
s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

# add displacements - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
d = FixedDisplacement('boundary', mesh.vertices_on_boundary())
s.add(d)

# bv = {vk for fk in mesh.faces_where({'is_boundary': True}) for vk in mesh.face_vertices(fk)}
# d = FixedDisplacement('boundary', list(bv))
# s.add(d)


# add loads - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# load = PointLoad(name='pload', nodes=[100], x=0, y=0, z=1, xx=0, yy=0, zz=0)
# s.add(load)


# add sections - - - - - - - - - - - - 
section = ShellSection('sec', t=.05)
s.add(section)

# add material - - - - - - 
material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(material)

# add element properties - - - - - - - - -
el_prop1 = ElementProperties('concrete_shell_thin',
                             material='concrete',
                             section='sec',
                             elset='shell',
                             is_rad=True,
                             is_incident=True)
s.add(el_prop1)



path = os.path.join(compas_vibro.DATA, 'structures')
s.to_obj(path=path, name='flat_10x10')

v = StructureViewer(s)
v.show()


