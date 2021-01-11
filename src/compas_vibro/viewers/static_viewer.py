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
from compas_vibro.viewers import PlotlyViewer
from compas.geometry import length_vector

class StaticViewer(PlotlyViewer):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, structure):
        super().__init__(structure)
        self.scale      = 1e3
        self.num_steps  = 10

    def show(self):
        self.make_layout('static')
        self.plot_shape()
        self._show()

    def plot_shape(self):
        nodes = sorted(self.structure.nodes.keys(), key=int)
        for i in range(self.num_steps):
            s = self.scale * 1 * i
            vertices = []
            dm = []
            for vk in nodes:
                x, y, z = self.structure.nodes[vk].xyz()
                dx = self.structure.results['static'][0].displacements['ux'][vk]
                dy = self.structure.results['static'][0].displacements['uy'][vk]
                dz = self.structure.results['static'][0].displacements['uz'][vk]
                xyz = [x + dx * s, y + dy * s, z + dz * s]
                dm.append(length_vector([dx, dy, dz]))
                vertices.append(xyz)

            faces = [self.structure.elements[ek].nodes for ek in self.structure.elements]
            
            mesh = Mesh.from_vertices_and_faces(vertices, faces)
            edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
            line_marker = dict(color='rgb(0,0,0)', width=2.5)
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
                            colorbar_title='Displacements (mm)',
                            colorscale='viridis',
                            intensity=intensity
                    )]
            self.data.extend(lines)
            self.data.extend(faces)

    def _show(self):
        fig = go.Figure(data=self.data, layout=self.layout)
        for i in range(2, self.num_steps * 2):
            fig.data[i].visible = False

        # Create and add slider
        steps = []
        for i in range(self.num_steps):
            name = self.structure.name
            title = '{0} - Analysis'.format(name)
            step = dict(
                method="update",
                args=[{"visible": [False] * len(fig.data)},
                    {"title": title}],
                label=str(i))
            step["args"][0]["visible"][i * 2] = True
            step["args"][0]["visible"][i * 2 + 1] = True
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "Scale: "},
            pad={"t": 50},
            steps=steps
        )]

        fig.update_layout(sliders=sliders)

        fig.show()

if __name__ == "__main__":
    pass


