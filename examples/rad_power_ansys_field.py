from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from compas.datastructures import Mesh

import compas_vibro

from compas_vibro.structure import Structure
from compas_vibro.structure import FixedDisplacement
from compas_vibro.structure import HarmonicPressureFieldsLoad
from compas_vibro.structure import ShellSection
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties

from compas_vibro.vibro import generate_uniform_waves_numpy
from compas_vibro.vibro import compute_pressure_fields_structure

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


path = compas_vibro.TEMP
geometry = 'clt_1_remeshed'
name = '{0}_field'.format(geometry)

mesh = Mesh.from_json(compas_vibro.get('{0}.json'.format(geometry)))

# make an instance of the stucture object - - - - - - - - - - - - - - - - - - - 
s = Structure(path, name) 

# add nodes and elements from mesh - - - - - - - - - - - - - - - - - - - - - - - 
s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

# add displacements - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# d = FixedDisplacement('boundary', mesh.vertices_on_boundary())
# s.add(d)

bv = {vk for fk in mesh.faces_where({'is_boundary': True}) for vk in mesh.face_vertices(fk)}
d = FixedDisplacement('boundary', list(bv))
s.add(d)

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


# add loads - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

freq_list = range(20, 350, 2)
waves = generate_uniform_waves_numpy()
fields = compute_pressure_fields_structure(waves, s, freq_list, center=True)

load = HarmonicPressureFieldsLoad('uniform_field', fields=fields)
s.add(load)

# analyze - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
num_modes = 20
s.analyze_harmonic_field(num_modes, freq_list, fields=['u'], damping=.02, backend='ansys')
# s.compute_rad_power()
# s.to_obj()
