from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2021, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go
# import plotly.io as pio
from compas.datastructures import Mesh



all = ['PressureFieldViewer']


class PressureFieldViewer(object):
    """Plotly based viewer for acoustic pressure fields.
    """
    def __init__(self, mesh, fields):
        self.name = 'Pressure fields'
        self.mesh = mesh
        self.fields = fields
        self.data       = []
        self.layout     = None

    def make_layout(self):
        name = self.name
        f = round(list(self.fields.keys())[0], 4)
        title = '{0} - {1}Hz'.format(name, f)

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
        # modes = self.structure.step.modes
        # modes = list(self.fields.keys())
        modes = len(self.fields)
        for i in range(2, modes * 2):
            fig.data[i].visible = False
        freqs = list(self.fields.keys())
        # Create and add slider
        steps = []
        for i in range(modes):
            name = self.name

            prefix = 'Freq. '
            f = freqs[i]
            title = '{0} - {1}Hz'.format(name, f)
            step_label = '{} Hz'.format(f)

            step = dict(
                method="update",
                args=[{"visible": [False] * len(fig.data)},
                    {"title": title}],
                label=step_label)
            step["args"][0]["visible"][i * 2] = True
            step["args"][0]["visible"][i * 2 + 1] = True
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": prefix},
            pad={"t": 50},
            steps=steps
        )]

        fig.update_layout(sliders=sliders)

        fig.show()

    def show(self):
        self.make_layout()
        self.plot_shape()
        self._show()

    def plot_shape(self):

        modes = list(self.fields.keys())
        mesh = self.mesh

        # vertices, faces = mesh.to_vertices_and_faces()
        vertices = [mesh.vertex_coordinates(vk) for vk in mesh.vertex]
        faces = [mesh.face_vertices(fk) for fk in mesh.faces()]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])


        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)

        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        lines = [go.Scatter3d(x=x, y=y, z=z, mode='lines', line=line_marker)]
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        for mode in modes:
            intensity = [self.fields[mode][vk].real for vk in mesh.vertex]
            faces_ = [go.Mesh3d(x=x,
                            y=y,
                            z=z,
                            i=i,
                            j=j,
                            k=k,
                            opacity=1.,
                            # contour={'show':True},
                            # vertexcolor=vcolor,
                            colorbar_title='Amplitude',
                            colorscale= 'jet', # 'jet', # 'viridis'
                            intensity=intensity
                    )]
            self.data.extend(lines)
            self.data.extend(faces_)





