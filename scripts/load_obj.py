import os
import compas_vibro
from compas_vibro.structure import Structure
from compas_vibro.viewers import HarmonicViewer
from compas_vibro.viewers import ModalViewer



filepath = os.path.join(compas_vibro.TEMP, 'ansys_mesh_flat_20x20_harmonic_s.obj')

s = Structure.from_obj(filepath)
print(s.results.keys())

v = HarmonicViewer(s)
v.show()

v = ModalViewer(s)
v.show()