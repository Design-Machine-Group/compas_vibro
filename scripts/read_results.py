import os
import compas_vibro
from compas_vibro.structure import Structure

for i in range(50): print('')

name = 'mesh_flat_20x20_radiation.obj'
s = Structure.from_obj(os.path.join(compas_vibro.DATA, name))

print(s.results['modal'][0].frequency)