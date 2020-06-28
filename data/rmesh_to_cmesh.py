import rhinoscriptsyntax as rs
from compas.datastructures import Mesh

rmesh = rs.ObjectsByLayer('mesh')

vertices = rs.MeshVertices(rmesh)
faces = rs.MeshFaceVertices(rmesh)

mesh = Mesh.from_vertices_and_faces(vertices, faces)
mesh.to_json('mesh_flat_100x100.json')
