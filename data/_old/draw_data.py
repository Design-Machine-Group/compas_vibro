import os
import json
from compas_rhino.helpers import mesh_draw

from compas.datastructures import Mesh
path = '/Users/mtomas/Documents/compas/packages/compas_vibro/data/'
model = 'shell_leuven.json'
filepath = os.path.join(path, model)


with open(filepath, 'r') as fp:
    data = json.load(fp)
mesh = Mesh.from_data(data['mesh'])
mesh_draw(mesh)
