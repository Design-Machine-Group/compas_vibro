from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_vibro.structure import material


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go

from compas.datastructures import Mesh

from compas.geometry import length_vector

# TODO: Plot elements per property (colors, hover data with properties)
# TODO: hoverdata for nodes should show node key

class PlotlyStructureViewer(object):
    def __init__(self, structure):
        self.structure = structure
        self.data       = []
        self.layout     = None


    def make_layout(self):
        name = self.structure.name

        title = '{0} - Structure'.format(name)

        
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

    def plot_shape(self):

        vertices = []
        nodes = sorted(self.structure.nodes.keys(), key=int)
        vertices = [self.structure.nodes[vk].xyz() for vk in nodes]

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


        attrs = ['elset', 'is_rad', 'material', 'thickess']
        intensity_ = []
        text = []
        for ek in self.structure.elements:
            ep = self.structure.elements[ek].element_property
            ep = self.structure.element_properties[ep]
            intensity_.append(int(ep.is_rad) + .1)
            string = 'ekey:{}<br>'.format(ek)
            for att in attrs:
                if att == 'elset':
                    val = ep.elset
                elif att == 'is_rad':
                    val = ep.is_rad
                elif att == 'material':
                    val = ep.material
                elif att == 'thickess':
                    val = self.structure.sections[ep.section].geometry['t']
                string += '{}: {}<br>'.format(att, val)
            text.append(string)
            if len(self.structure.elements[ek].nodes) == 4:
                intensity_.append(int(ep.is_rad) + .1)
                text.append(string)

        faces = [go.Mesh3d(x=x,
                            y=y,
                            z=z,
                            i=i,
                            j=j,
                            k=k,
                            opacity=1.,
                            colorbar_title='is_rad',
                            colorbar_thickness=10,
                            colorscale='Emrld_r',
                            intensity=intensity_,
                            intensitymode='cell',
                            text=text,
                            hoverinfo='text',
                            showscale=False,
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

    def plot_point_loads(self):
        dots = []
        for lk in self.structure.loads:
            load = self.structure.loads[lk]
            if load.__name__ == 'PointLoad':
                nodes = load.nodes
                x = [self.structure.nodes[nk].x for nk in nodes]
                y = [self.structure.nodes[nk].y for nk in nodes]
                z = [self.structure.nodes[nk].z for nk in nodes]
                dots.append(go.Scatter3d(x=x, y=y, z=z, mode='markers'))
        self.data.extend(dots)

    def show(self):
        self.make_layout()
        self.plot_shape()
        self.plot_supports()
        self.plot_point_loads()
        fig = go.Figure(data=self.data, layout=self.layout)
        fig.show()



if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    fp = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20_radiation_t10.obj')
    s = Structure.from_obj(fp)

    # for ek in s.elements:
    #     pass
    # ek = s.elements[ek].element_property
    # print(dir(s.element_properties[ek]))

    v = PlotlyStructureViewer(s)
    v.show()

    