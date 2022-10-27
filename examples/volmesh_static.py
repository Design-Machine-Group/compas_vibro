import os
import compas_vibro

from compas_vibro.structure import Structure
from compas_vibro.structure import FixedDisplacement
from compas_vibro.structure import PointLoad
from compas_vibro.structure import SolidSection
from compas_vibro.structure import ElasticIsotropic
from compas_vibro.structure import ElementProperties


from compas.datastructures import VolMesh

for i in range(50): print('')

fp = os.path.join(compas_vibro.DATA, 'meshes', 'volmesh.json')
vmesh = VolMesh.from_json(fp)

path = compas_vibro.TEMP
s = Structure(path, 'volmesh')
s.add_nodes_elements_from_volmesh(vmesh, elset='tetra')

nodes = list(vmesh.vertices_where({'z': (1, 10)}))
load = PointLoad(name='pload', nodes=nodes, x=0, y=0, z=1000, xx=0, yy=0, zz=0)
s.add(load)

d = FixedDisplacement('boundary', vmesh.vertices_where({'z':(-1, 0.001)}))
s.add(d)

section = SolidSection('solid_sec')
s.add(section)

material = ElasticIsotropic('concrete', E=30e9, v=.2, p=2400)
s.add(material)


el_prop = ElementProperties('concrete_tetra',
                            material='concrete',
                            section='solid_sec',
                            elset='tetra')
s.add(el_prop)

s.analyze_static(backend='ansys', fields=['u'])
print(s)
