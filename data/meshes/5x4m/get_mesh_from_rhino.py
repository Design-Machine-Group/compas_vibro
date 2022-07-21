import rhinoscriptsyntax as rs
from compas_vibro.structure import Mesh
import os
import compas_vibro


types = ['structure', 'quarter']
subds  = ['6x6', '20x20', '50x50']

for mt in types:
    for subd in subds:
        layer  = '{}_{}'.format(subd, mt)
        print(layer, subd)
        rmesh = rs.ObjectsByLayer(layer)[0]
        v = rs.MeshVertices(rmesh)
        f = rs.MeshFaceVertices(rmesh)
        
        mesh = Mesh.from_vertices_and_faces(v, f)
        
        fp = os.path.join(compas_vibro.DATA, 'meshes', '5x4m', '{}_{}.json'.format(subd, mt))
        mesh.to_json(fp)