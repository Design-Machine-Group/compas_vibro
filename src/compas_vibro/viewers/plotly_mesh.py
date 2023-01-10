from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

for i in range(50): print('')

from compas.utilities import i_to_rgb
from compas.geometry import length_vector

import plotly.graph_objects as go
import plotly.io as pio

all = ['PlotlyMeshViewer']

class PlotlyMeshViewer(object):
    """Plotly based viewer for meshes.
    """
    def __init__(self, mesh):
        self.mesh               = mesh
        self.data               = []
        self.layout             = None
        self.scale              = None
        self.show_vertex_labels = False

    def make_layout(self):
        name = self.mesh.name
        title = '{0}'.format(name)
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

    def _show(self):
        fig = go.Figure(data=self.data, layout=self.layout)
        fig.show()

    def plot_shape(self):
        # s = self.scale
        # vertices = []
        # dm = []
        
        edges = [[self.mesh.vertex_coordinates(u), self.mesh.vertex_coordinates(v)] for u,v in self.mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        lines = [go.Scatter3d(x=x, y=y, z=z, mode='lines', line=line_marker)]

        self.mesh.quads_to_triangles()
        fks = []
        for fk in self.mesh.faces():
            nv = len(self.mesh.face_vertices(fk))
            if nv >= 4:
                fks.append(fk)
        for fk in fks:
            self.mesh.insert_vertex(fk)

        vertices, triangles = self.mesh.to_vertices_and_faces()
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        intensity = None  #[d * 1e3 for d in dm]

        faces = [go.Mesh3d(x=x,
                        y=y,
                        z=z,
                        i=i,
                        j=j,
                        k=k,
                        opacity=1.,
                        # contour={'show':True},
                        # vertexcolor=vcolor,
                        colorbar_title='Displacements',
                        colorscale='jet', # 'viridis'
                        intensity=intensity
                )]
        self.data.extend(lines)
        self.data.extend(faces)

        if self.show_vertex_labels:
            vertices = list(self.mesh.vertices())
            x = [self.mesh.vertex_coordinates(nk)[0] for nk in vertices]
            y = [self.mesh.vertex_coordinates(nk)[1] for nk in vertices]
            z = [self.mesh.vertex_coordinates(nk)[2] for nk in vertices]
            text = [nk for nk in vertices]
            dots = [go.Scatter3d(x=x, y=y, z=z, text=text, mode='markers+text')]
            self.data.extend(dots)


    def show(self):
        self.make_layout()
        self.plot_shape()
        self._show()


if __name__ == '__main__':
    import os
    from compas.datastructures import Mesh
    import compas_vibro

    for i in range(50): print('')
    
    # name = 'clt_1_remeshed'
    # filepath = os.path.join(timber_vibro.DATA, 'other', '{}.json'.format(name))
    
    filepath = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20.json')
    mesh = Mesh.from_json(filepath)
    pl = PlotlyMeshViewer(mesh)
    pl.show()

