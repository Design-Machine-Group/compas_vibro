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
geometry = '6x6_sym_structure'
inc_geometry = '6x6_sym_quarter'
name = '{}'.format(geometry)

fp_mesh = os.path.join(compas_vibro.DATA, 'meshes', '6x6_sym', '{}.json'.format(geometry))
fp_inc_mesh = os.path.join(compas_vibro.DATA, 'meshes', '6x6_sym', '{}.json'.format(inc_geometry))

mesh = Mesh.from_json(fp_mesh)
inc_mesh = Mesh.from_json(fp_inc_mesh)


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
section = ShellSection('sec', t=.012)
s.add(section)

# add material - - - - - - 
material = ElasticIsotropic('glass', E=70e9, v=.22, p=2500)
s.add(material)

# add element properties - - - - - - - - -
el_prop1 = ElementProperties('concrete_shell_thin',
                             material='glass',
                             section='sec',
                             elset='shell',
                             is_rad=True,
                             is_incident=False)
s.add(el_prop1)

s.add_incident_elements_from_mesh(inc_mesh)

path = os.path.join(compas_vibro.DATA, 'structures')
s.to_obj(path=path, name=geometry)


print(s.sets)
print(s.element_properties)
# v = StructureViewer(s)
# v.show_rad_nodes = True
# v.show_incident_nodes = True
# v.show()


