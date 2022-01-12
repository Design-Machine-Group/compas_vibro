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

from compas_vibro.viewers import HarmonicViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


path = compas_vibro.TEMP
geometry = 'flat_mesh_20x20'
name = '{0}_radiation'.format(geometry)



mesh = Mesh.from_json(compas_vibro.get('{0}.json'.format(geometry)))

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
load = PointLoad(name='pload', nodes=[100], x=0, y=0, z=1, xx=0, yy=0, zz=0)
s.add(load)


# add sections - - - - - - - - - - - - 
section = ShellSection('thin_sec', t=.1)
s.add(section)
section = ShellSection('thick_sec', t=.2)
s.add(section)

# add sets - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
fins = list(mesh.faces_where({'is_fin':True}))
no_fins = list(mesh.faces_where({'is_fin':False}))
s.add_set('fins', 'element', fins)
s.add_set('no_fins', 'element', no_fins)

# add material - - - - - - 
material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(material)

# add element properties - - - - - - - - -
el_prop1 = ElementProperties('concrete_shell_thin',
                             material='concrete',
                             section='thin_sec',
                             elset='fins',
                             is_rad=False)
s.add(el_prop1)

el_prop2 = ElementProperties('concrete_shell_thick',
                             material='concrete',
                             section='thick_sec',
                             elset='no_fins',
                             is_rad=True)
s.add(el_prop2)


# add analysis frequencies - - - - - - - -
freq_list = range(20, 350, 2)

num_modes = 25
# analyze - - - - 
s.analyze_harmonic_super(num_modes, freq_list, fields=['u'], backend='ansys')
s.compute_rad_power()
# s.to_obj()

print(s.results.keys())

