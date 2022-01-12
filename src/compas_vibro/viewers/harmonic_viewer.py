from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go

from compas.geometry import length_vector

from compas.datastructures import Mesh

from compas_vibro.viewers import PlotlyViewer


class HarmonicViewer(PlotlyViewer):
    """
    Plotly based viewer for harmonic analysis.
    """
    def __init__(self, structure):
        super().__init__(structure)
        self.scale      = 1e6

    def show(self):
        self.make_layout('harmonic')
        self.plot_shape('harmonic')
        self._show('harmonic')

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
                    # dx = self.structure.results[plot_type][mode].displacements['ux'][vk]
                    # dy = self.structure.results[plot_type][mode].displacements['uy'][vk]
                    # dz = self.structure.results[plot_type][mode].displacements['uz'][vk]
                    dx = self.structure.results[plot_type][mode].displacements[vk]['real']['x']
                    dy = self.structure.results[plot_type][mode].displacements[vk]['real']['y']
                    dz = self.structure.results[plot_type][mode].displacements[vk]['real']['z']

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


if __name__ == "__main__":
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    for i in range(60): print()

    filepath = os.path.join(compas_vibro.TEMP, 'ansys_mesh_flat_20x20_harmonic.obj')
    s = Structure.from_obj(filepath)
    v = HarmonicViewer(s)
    v.scale = 1e8
    v.show()