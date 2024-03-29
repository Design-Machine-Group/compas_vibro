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

from compas_vibro.vibro import from_W_to_dB

from compas_vibro.viewers import StructureViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


path = compas_vibro.TEMP
geometry = 'flat_mesh_20x20'
name = '{0}_radiation'.format(geometry)



mesh = Mesh.from_json(os.path.join(compas_vibro.DATA, 'meshes', '{}.json'.format(geometry)))

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
section = ShellSection('sec', t=.3)
s.add(section)

# add material - - - - - - 
material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(material)

# add element properties - - - - - - - - -
prop = ElementProperties('concrete_shell',
                          material='concrete',
                          section='sec',
                          elset='shell',
                          is_rad=True)
s.add(prop)

# add analysis frequencies - - - - - - - -
freq_list = range(20, 350, 2)

num_modes = 25
# analyze - - - - 
s.analyze_harmonic_super(num_modes, freq_list, fields=['u'], backend='ansys')
s.compute_rad_power()
# s.to_obj()
for k in s.results['radiation']:
    f = s.results['radiation'][k].frequency
    p = s.results['radiation'][k].radiated_p
    db = from_W_to_dB(p)
    print(k, f, p, db)
