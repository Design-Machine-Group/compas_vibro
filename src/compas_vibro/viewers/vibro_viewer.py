from compas.viewers import MeshViewer
from compas.viewers.core.drawing import xdraw_lines
from compas.viewers.core.drawing import xdraw_polygons
from compas.utilities import i_to_rgb


__author__     = ['Tomas Mendez Echenagucia <mendez@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'mendez@arch.ethz.ch'


class VibroViewer(MeshViewer):

    def __init__(self, vibro, frequency, width=600, height=600, velocities=False):
        super(VibroViewer, self).__init__(vibro.mesh, width=width, height=height)
        self.frequency = frequency
        self.velocities = velocities
        self.mesh = vibro.mesh
        self.vibro = vibro
        self.update_face_colors(frequency)

    def update_face_colors(self, frequency):
        wmin = min(self.vibro.face_w[frequency].values())
        wmax = max(self.vibro.face_w[frequency].values())
        for fk in self.mesh.faces():
            w = self.vibro.face_w[frequency][fk]
            w = (w - wmin) / (wmax - wmin)
            color = i_to_rgb(w)
            color = [c / 255. for c in color]
            color.append(1)
            self.mesh.set_face_attribute(fk, 'color', color)

    def display(self):
        polygons = []
        for fkey in self.mesh.faces():
            points = self.mesh.face_coordinates(fkey)
            color_front = self.mesh.get_face_attribute(fkey, 'color', (0.8, 0.8, 0.8, 1.0))
            # color_back  = (0.2, 0.2, 0.2, 1.0)
            polygons.append({'points': points,
                             'color.front': color_front,
                             'color.back' : color_front})
        xdraw_polygons(polygons)

        if self.velocities:
            vel = []
            for vk in self.mesh.vertex:
                xyz = self.mesh.vertex_coordinates(vk)
                v = self.vibro.get_node_velocity(self.frequency, vk).real
                vel.append({'start': xyz,
                            'end'  : (xyz[0], xyz[1], xyz[2] + v),
                            'color': (1, 1, 1),
                            'width': 2.})
            xdraw_lines(vel)


# if __name__ == '__main__':
#     import compas_vibro
#     import json
#     from compas_vibro.datastructures import VibroMesh
#     from compas_vibro.datastructures import VibroStructure
#     from compas_vibro.vibro import make_velocities_pattern_mesh

#     with open(compas_vibro.get('flat20x20.json'), 'r') as fp:
#         data = json.load(fp)
#     vmesh = VibroMesh.from_data(data['mesh'])

#     frequencies = [50, 60, 70]
#     vib = VibroStructure.from_mesh(mesh=vmesh, frequencies=frequencies)

#     for frkey in vib.frequencies:
#         v = make_velocities_pattern_mesh(vmesh, 3, 2, complex=True)
#         vib.set_node_velocities(frkey, v)

#     # viewer -------------------------------------------------------------------
#     viewer = VibroViewer(vib, 0, velocities=True)

#     viewer.axes_on = False
#     viewer.grid_on = False

#     for i in range(10):
#         viewer.camera.zoom_in()

#     viewer.setup()
#     viewer.show()
