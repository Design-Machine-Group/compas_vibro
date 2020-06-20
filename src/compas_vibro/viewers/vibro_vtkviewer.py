from compas.viewers import VtkViewer
from compas.viewers.vtkviewer import EdgeWidthCallback
from compas.utilities import i_to_rgb
import vtk

__author__     = ['Tomas Mendez Echenagucia <mendez@arch.ethz.ch>']
__copyright__  = 'Copyright 2017, BLOCK Research Group - ETH Zurich'
__license__    = 'MIT License'
__email__      = 'mendez@arch.ethz.ch'


class VtkVibroViewer(VtkViewer):
    def __init__(self, vibro, frequency, width=1000, height=700, velocities=False):
        # super(VtkViewer, self).__init__()
        super(VtkVibroViewer, self).__init__(name='Vibro Viewer', width=1000, height=700, data={})

        self.settings = {'draw_axes': False,
                         'draw_vertices': False,
                         'draw_edges': False,
                         'draw_faces': True,
                         'draw_blocks': False,
                         'draw_velocities': False,
                         'draw_displacements': True,
                         'vertex_size': 0.01,
                         'edge_width': .1,
                         'vel_width': .3,
                         'disp_amp': 1.,
                         'camera_pos': [10, -1, 10],
                         'camera_focus': [0, 0, 0],
                         'camera_azi': 30,
                         'camera_ele': 0}

        self.frequency = frequency
        self.velocities = velocities
        self.mesh = vibro.mesh
        self.vibro = vibro
        self.faces = {}
        self.vertices = {}
        self.vel_dict = {}
        self.make_vertex_dict(frequency)
        self.make_face_dict(frequency)
        self.original_v = [self.mesh.vertex_coordinates(vk) for vk in self.mesh.vertex]
        self.data = {'vertices': self.vertices, 'faces': self.faces}

    def make_vertex_dict(self, frequency):

        self.vertices = {vk: self.mesh.vertex_coordinates(vk) for vk in self.mesh.vertex}
        if self.vibro.node_disp:
            for vk in self.mesh.vertex:
                disp = self.vibro.node_disp[vk][self.vibro.frequencies[frequency]]['real']
                self.vertices[vk][0] += disp['x'] * self.settings['disp_amp'] * 1e6
                self.vertices[vk][1] += disp['y'] * self.settings['disp_amp'] * 1e6
                self.vertices[vk][2] += disp['z'] * self.settings['disp_amp'] * 1e6

    def make_face_dict(self, frequency):
        if self.vibro.face_w:
            wmin = min(self.vibro.face_w[frequency].values())
            wmax = max(self.vibro.face_w[frequency].values())
        faces = {}
        for fk in self.mesh.faces():
            if self.vibro.face_w:
                w = self.vibro.face_w[frequency][fk]
                w = (w - wmin) / (wmax - wmin)
                color = i_to_rgb(w)
            else:
                color = (30, 50, 255)
            faces[fk] = {'vertices': self.mesh.face_vertices(fk), 'color': color}

        self.faces = faces

    # def make_velocities_dict(self, frequency):
    #     vel_dict = {}
    #     for vk in self.mesh.vertex:
    #         xyz = self.mesh.vertex_coordinates(vk)
    #         v = self.vibro.get_node_velocity(self.frequency, vk).real

    #     self.vel_dict = vel_dict

    def gui(self):

        w = 0.005
        h = 0.015
        l = 0.015
        y = 0.90
        a = 0.01
        b = 0.10

        disp_amp  = self.settings['disp_amp']
        frequency = self.vibro.frequencies[self.frequency]
        minf = self.vibro.frequencies[0]
        maxf = self.vibro.frequencies[len(self.vibro.frequencies) - 1]

        if self.settings['draw_displacements']:
            self.slider_freq = self.slider(w, h, l, [a, y], [b, y], minf, maxf, frequency, 'Frequency ')

            disp = self.vibro.node_disp
            original_v = self.original_v
            self.slider_freq.AddObserver(vtk.vtkCommand.InteractionEvent,
                                         Frequencycallback(frequency,
                                                          self.vertices,
                                                          disp,
                                                          original_v))

            y -= 0.12
            self.slider_disp = self.slider(w, h, l, [a, y], [b, y], .0, 10.0, disp_amp, 'Disp Amp')
            self.slider_disp.AddObserver(vtk.vtkCommand.InteractionEvent,
                                         DisplacementAmpCallback(frequency,
                                                                 self.vertices,
                                                                 disp,
                                                                 original_v))


class Frequencycallback():
    def __init__(self, frequency, vertices, disp, original_v):
        self.frequency = frequency
        self.vertices = vertices
        self. disp = disp
        self.original_v = original_v

    def __call__(self, caller, ev):
        value = int(caller.GetRepresentation().GetValue())
        vtkpts = self.vertices
        for id in range(vtkpts.GetNumberOfPoints()):
            vertex = self.original_v[id]
            vtkpts.SetPoint(id, [vertex[0] + self.disp[id][value]['real']['x'] * 1e6,
                                 vertex[1] + self.disp[id][value]['real']['y'] * 1e6,
                                 vertex[2] + self.disp[id][value]['real']['z'] * 1e6])

        vtkpts.Modified()


class DisplacementAmpCallback():
    def __init__(self, frequency, vertices, disp, original_v):
        self.frequency = frequency
        self.vertices = vertices
        self. disp = disp
        self.original_v = original_v

    def __call__(self, caller, ev):
        value = caller.GetRepresentation().GetValue()
        vtkpts = self.vertices
        for id in range(vtkpts.GetNumberOfPoints()):
            vertex = self.original_v[id]
            vtkpts.SetPoint(id, [vertex[0] + self.disp[id][self.frequency]['real']['x'] * value * 1e6,
                                 vertex[1] + self.disp[id][self.frequency]['real']['y'] * value * 1e6,
                                 vertex[2] + self.disp[id][self.frequency]['real']['z'] * value * 1e6])

        vtkpts.Modified()