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

#TODO: Both plotters should inherit some basics from a BasePLotter

class HarmonicViewer(object):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, structure, frequency):
        self.structure  = structure
        self.data       = []
        self.frequency  = frequency
        self.layout     = None
        self.scale      = 1e8
        self.make_layout()

    def make_layout(self):
        f = round(self.structure.results['harmonic'][self.frequency].frequency, 4)
        title = 'Modal Analysis - mode {0} - {1}Hz'.format(self.frequency, f)
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
        fig.show()

    def plot_harmonic_shape(self):
        frequency = self.frequency
        s = self.scale
        vertices = []
        nodes = sorted(self.structure.nodes.keys(), key=int)
        for vk in nodes:
            x, y, z = self.structure.nodes[vk].xyz()
            dx = self.structure.results['harmonic'][frequency].displacements[vk]['real']['x']
            dy = self.structure.results['harmonic'][frequency].displacements[vk]['real']['y']
            dz = self.structure.results['harmonic'][frequency].displacements[vk]['real']['z']
            xyz = [x + dx * s, y + dy * s, z + dz * s]
            vertices.append(xyz)

        faces = [self.structure.elements[ek].nodes for ek in self.structure.elements]
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='#0066FF', width=2)
        lines = []
        for u, v in edges:
            lines.append(go.Scatter3d(x=(u[0], v[0]), y=(u[1], v[1]), z=(u[2], v[2]), mode='lines', line=line_marker))
        
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

        faces = [go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, alphahull=1, opacity=0.4,color='cyan')]
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

    filepath = os.path.join(compas_vibro.DATA, 'mesh_flat_10x10_harmonic.obj')
    s = Structure.from_obj(filepath)
    mode = 3
    # print(s.results['harmonic'][0].displacements[0])
    v = HarmonicViewer(s, mode)
    v.plot_harmonic_shape()
    v.plot_supports()
    v.show()

