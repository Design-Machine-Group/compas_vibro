from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go
from compas.utilities import i_to_rgb
from compas.datastructures import Mesh
from compas.geometry import length_vector

import plotly.io as pio

all = ['PlotlyViewer']


class PlotlyViewer(object):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, structure):
        self.structure  = structure
        self.data       = []
        self.layout     = None
        self.scale      = None

    def make_layout(self, plot_type):
        name = self.structure.name
        if plot_type == 'modal':
            f = round(self.structure.results[plot_type][0].frequency, 4)
            title = '{0} - Modal Analysis - mode {1} - {2}Hz'.format(name,0, f)
        elif plot_type == 'harmonic':
            f = round(self.structure.results[plot_type][0].frequency, 4)
            title = '{0} - Analysis - {1}Hz'.format(name, f)
        elif plot_type == 'static':
            title = '{0} - Analysis'.format(name)
        else:
            raise NameError('PLot type {} does not exist yet'.format(plot_type))
        
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

    def _show(self, plot_type):
        fig = go.Figure(data=self.data, layout=self.layout)
        # modes = self.structure.step.modes
        modes = len(self.structure.results[plot_type])
        for i in range(2, modes * 2):
            fig.data[i].visible = False

        # Create and add slider
        steps = []
        for i in range(modes):
            name = self.structure.name
            if plot_type == 'modal':
                prefix = 'Mode: '
                f = round(self.structure.results[plot_type][i].frequency, 4)
                title = '{0} - Modal Analysis - mode {1} - {2}Hz'.format(name, i, f)
                step_label = str(i)
            if plot_type == 'harmonic':
                prefix = 'Frequency: '
                f = round(self.structure.results[plot_type][i].frequency, 4)
                title = '{0} - Analysis - {1}Hz'.format(name, f)
                step_label = str(f)
            # else:
            #     title = '{0} - Analysis'.format(name)
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

    def plot_shape(self, plot_type):
        if plot_type == 'harmonic':
            modes = len(self.structure.results[plot_type])
        elif plot_type == 'modal':
            modes = self.structure.step.modes
        elif plot_type == 'static':
            modes = 1
        else:
            raise NameError('Plot type {} has not yet been implemented'.format(plot_type))
        for i in range(modes):
            mode = i
            s = self.scale
            vertices = []
            dm = []
            nodes = sorted(self.structure.nodes.keys(), key=int)
            for vk in nodes:
                x, y, z = self.structure.nodes[vk].xyz()
                dx = self.structure.results[plot_type][mode].displacements['ux'][vk]
                dy = self.structure.results[plot_type][mode].displacements['uy'][vk]
                dz = self.structure.results[plot_type][mode].displacements['uz'][vk]
                # dx = self.structure.results[plot_type][mode].displacements[vk]['real']['x']
                # dy = self.structure.results[plot_type][mode].displacements[vk]['real']['y']
                # dz = self.structure.results[plot_type][mode].displacements[vk]['real']['z']

                xyz = [x + dx * s, y + dy * s, z + dz * s]
                dm.append(length_vector([dx, dy, dz]))
                vertices.append(xyz)

            faces = [self.structure.elements[ek].nodes for ek in self.structure.elements]
            
            mesh = Mesh.from_vertices_and_faces(vertices, faces)
            edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
            line_marker = dict(color='rgb(0,0,0)', width=1.5)
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
                if len(face) == 4:
                    triangles.append([face[2], face[3], face[0]])
            
            i = [v[0] for v in triangles]
            j = [v[1] for v in triangles]
            k = [v[2] for v in triangles]

            x = [v[0] for v in vertices]
            y = [v[1] for v in vertices]
            z = [v[2] for v in vertices]

            intensity = [d * 1e3 for d in dm]

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
                            colorscale= 'viridis', # 'jet', # 'viridis'
                            intensity=intensity
                    )]
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





