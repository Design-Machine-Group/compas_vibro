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

from compas_vibro.viewers import ModalViewer

__author__ = ["Tomas Mendez Echenagucia"]
__copyright__ = "Copyright 2020, Design Machine Group - University of Washington"
__license__ = "MIT License"
__email__ = "tmendeze@uw.edu"
__version__ = "0.1.0"


for i in range(60):
    print()

path = compas_vibro.TEMP
geometry = 'mesh_flat_20x20'
name = '{0}_modal'.format(geometry)

mesh = Mesh.from_json(compas_vibro.get('{0}.json'.format(geometry)))
s = Structure(path, name)
s.add_nodes_elements_from_mesh(mesh, 'ShellElement', elset='shell')

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


# s.analyze_modal(backend='opensees', fields=['f', 'u'], num_modes=20)
# s.to_obj()

s = Structure.from_obj(os.path.join(path, name + '.obj'))
mode = 1
v = ModalViewer(s, mode)
v.plot_modal_shape()
v.plot_supports()
v.show()
