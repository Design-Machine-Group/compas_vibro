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


for i in range(60):
    print()

path = compas_vibro.TEMP
geometry = 'mesh_flat_20x20'
name = 'ansys_{0}_harmonic_s'.format(geometry)

mesh = Mesh.from_json(compas_vibro.get('{0}.json'.format(geometry)))

# make an instance of the stucture object - - - - - - - - - - - - - - - - - - - 
s = Structure(path, name) 

# add nodes and elements from mesh - - - - - - - - - - - - - - - - - - - - - - - 
s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

# add displacements - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
d = FixedDisplacement('boundary', mesh.vertices_on_boundary())
s.add(d)

# add loads - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
load = PointLoad(name='pload', nodes=[100], x=0, y=0, z=1, xx=0, yy=0, zz=0)
s.add(load)

# add sections - - - - - - - - - - - - 
section = ShellSection('shell_sec', t=.1)
s.add(section)

# add material - - - - - - 
material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)

s.add(material)
# add element properties - - - - - - - - -
el_prop = ElementProperties('concrete_shell',
                            material='concrete',
                            section='shell_sec',
                            elset='shell')
s.add(el_prop)

# add analysis frequencies - - - - - - - -
freq_list = range(20, 50, 2)

num_modes = 20

# analyze - - - - 
s.analyze_harmonic_super(num_modes, freq_list, fields=['u'], backend='ansys')

# # save results - - - - - - 
s.to_obj()

v = HarmonicViewer(s)
v.show()

# for k in s.results['harmonic']:
#     print(s.results['harmonic'][k].frequency)
#     print(s.results['harmonic'][k].modal_coordinates['f'])
#     print(s.results['harmonic'][k].modal_coordinates)
#     print('')

