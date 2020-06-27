from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go

from compas.datastructures import Mesh

def plot_mesh_lines(structure):
    vertices = [structure.nodes[vk].xyz() for vk in structure.nodes]
    faces = [structure.elements[ek].nodes for ek in structure.elements]
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
    line_marker = dict(color='#0066FF', width=2)
    lines = []
    for u, v in edges:
        lines.append(go.Scatter3d(x=(u[0], v[0]), y=(u[1], v[1]), z=(u[2], v[2]), mode='lines', line=line_marker))
    fig = go.Figure(data=lines)
    fig.show()

if __name__ == "__main__":
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    for i in range(60): print()

    filepath = os.path.join(compas_vibro.DATA, 'vibro_test.obj')
    s = Structure.from_obj(filepath)
    plot_modal(s)


