import rhinoscriptsyntax as rs
from compas_vibro.structure import Mesh
import os
import compas_vibro


layers = ['structure','ex_mat', 'ex_mat_2', 'rad_mat', 'rad_mat_complete']

for lay in layers:
    print(lay)
    rmesh = rs.ObjectsByLayer(lay)[0]
    v = rs.MeshVertices(rmesh)
    f = rs.MeshFaceVertices(rmesh)
    
    mesh = Mesh.from_vertices_and_faces(v, f)
    
    fp = os.path.join(compas_vibro.DATA, 'meshes', 'glass', 'glass_{}.json'.format(lay))
    mesh.to_json(fp)