from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go

from compas.datastructures import Mesh

import plotly.io as pio
pio.renderers.default = "firefox"


class ModalViewer(object):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, structure, mode):
        self.structure  = structure
        self.data       = []
        self.mode       = mode
        self.layout     = None
        self.scale      = 20
        self.make_layout()

    def make_layout(self):
        f = round(self.structure.results['modal'][self.mode].frequency, 4)
        title = 'Modal Analysis - mode {0} - {1}Hz'.format(self.mode, f)
        layout = go.Layout(title=title,
                          scene=dict(aspectmode='data',
                                    xaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    yaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    zaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)')
                                    ),
                          showlegend=False,
                            )
        self.layout = layout

    def show(self):
        fig = go.Figure(data=self.data, layout=self.layout)

        # fig.data[-2].visible = False

        fig.show()

    def plot_modal_shape(self):
        mode = self.mode
        s = self.scale
        vertices = []
        nodes = sorted(self.structure.nodes.keys(), key=int)
        for vk in nodes:
            x, y, z = self.structure.nodes[vk].xyz()
            dx = self.structure.results['modal'][mode].displacements['ux'][vk]
            dy = self.structure.results['modal'][mode].displacements['uy'][vk]
            dz = self.structure.results['modal'][mode].displacements['uz'][vk]
            xyz = [x + dx * s, y + dy * s, z + dz * s]
            vertices.append(xyz)

        faces = [self.structure.elements[ek].nodes for ek in self.structure.elements]
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,200)', width=1)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])
        lines = [go.Scatter3d(x=x, y=y, z=z, mode='lines', line=line_marker)]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        faces = [go.Mesh3d(x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           alphahull=1,
                           opacity=0.4,
                           color='cyan')]
        self.data.extend(lines)
        self.data.extend(faces)


    def plot_supports(self):
        dots = []
        for dk in self.structure.displacements:
            nodes = self.structure.displacements[dk].nodes
            x = [self.structure.nodes[nk].x for nk in nodes]
            y = [self.structure.nodes[nk].y for nk in nodes]
            z = [self.structure.nodes[nk].z for nk in nodes]
            dots.append(go.Scatter3d(x=x, y=y, z=z, mode='markers'))
        self.data.extend(dots)



if __name__ == "__main__":
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    for i in range(60): print()

    filepath = os.path.join(compas_vibro.TEMP, 'mesh_flat_100x100_modal.obj')
    s = Structure.from_obj(filepath)
    mode = 19

    v = ModalViewer(s, mode)
    v.plot_modal_shape()
    v.plot_supports()
    v.show()


