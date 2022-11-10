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

from compas_vibro.viewers import StructureViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


for i in range(60): print('')

path = compas_vibro.TEMP
# geometry = 'pringle'
geometry = 'flat_mesh_20x20'
name = 'opensees_{0}_modal'.format(geometry)

mesh = Mesh.from_json(os.path.join(compas_vibro.DATA, 'meshes', '{}.json'.format(geometry)))
s = Structure(path, name)

s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

d = FixedDisplacement('boundary', mesh.vertices_on_boundary())
s.add(d)

section = ShellSection('shell_sec', t=.2)
s.add(section)

material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(material)


el_prop = ElementProperties('concrete_shell',
                            material='concrete',
                            section='shell_sec',
                            elset='shell')
s.add(el_prop)

exe = '/Applications/OpenSees3.3.0/bin/OpenSees'
s.analyze_modal(backend='opensees', fields=['f', 'u', 'm'], num_modes=12, exe=exe)
# s.analyze_modal(backend='opensees', fields=['m'], num_modes=12)

s.to_obj(path=os.path.join(compas_vibro.DATA, 'structures'))
v = StructureViewer(s)
v.modal_scale = 40
v.show('modal')

modes = s.results['modal'].keys()
for mode in modes:
    f = s.results['modal'][mode].frequency
    m = s.results['modal'][mode].efmass['z']
    mr = s.results['modal'][mode].efmass_r['z']
    print(mode, f, m, mr)