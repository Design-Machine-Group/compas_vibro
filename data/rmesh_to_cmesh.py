import rhinoscriptsyntax as rs
from compas.datastructures import Mesh

for i in range(50):print('')

rmesh = rs.ObjectsByLayer('comsol_mesh')

vertices = rs.MeshVertices(rmesh)
faces = rs.MeshFaceVertices(rmesh)
mesh = Mesh.from_vertices_and_faces(vertices, faces)
mesh.to_json('pringle.json')

# for fk in mesh.faces():
#     v = mesh.face_vertices(fk)
#     if len(v) == 3:
#         print(fk)
#         rs.AddPoints(v)
