import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection

from compas.plotters import MeshPlotter

import numpy as np

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['VibroLoadsPlotter',
           ]


class VibroLoadsPlotter(MeshPlotter):

    def __init__(self, vibro):
        super(VibroLoadsPlotter, self).__init__(vibro.mesh, figsize=(10, 6))
        self.vibro = vibro
        self.facecolor = {}
        self.mesh = vibro.mesh
        self.current_freq = 0
        self.facecolors = {k: None for k in vibro.frequencies}
        self.real = True
        self.colorbar = None

    def draw_pressure_field(self):
        patches = []
        for key in self.mesh.faces():
            points    = self.mesh.face_coordinates(key, 'xy')
            patches.append(Polygon([point[0:2] for point in points]))

        self.facecollection = PatchCollection(patches)
        self.facecollection.set_cmap('jet')
        self.axes.add_collection(self.facecollection)
        self.update_pressure_field()
        self.update_colorbar()
        self.add_freq_label()

    def update_pressure_field(self):
        loads = self.vibro.diffuse_field_loads[self.current_freq]
        if self.real:
            loads = [l.real for l in loads]
        else:
            loads = [l.imag for l in loads]
        self.facecollection.set_array(np.array(loads))
        self.facecollection.autoscale()

    def update_colorbar(self):
        if self.colorbar:
            self.colorbar.remove()
        self.colorbar = plt.colorbar(self.facecollection, ax=self._axes)
        self.colorbar.set_label('Amplitude ', rotation=90)

    def add_freq_label(self):
        freq = str(self.vibro.frequencies[self.current_freq]) + ' Hz'
        self.axes.set_xlabel(freq)

    def show(self, autoscale=True, tight=False):
        callback = FreqIndex(self)
        axprev = plt.axes([0.70, 0.03, 0.05, 0.03])
        axnext = plt.axes([0.76, 0.03, 0.05, 0.03])
        bnext = Button(axnext, '>')
        bnext.on_clicked(callback.next)
        bprev = Button(axprev, '<')
        bprev.on_clicked(callback.prev)

        self.axes.autoscale()
        if self.tight:
            plt.tight_layout()
        plt.show()


class FreqIndex(object):
    ind = 0

    def __init__(self, plotter):
        self.plotter = plotter

    def next(self, event):
        self.plotter.current_freq += 1
        self.plotter.current_freq %= len(self.plotter.vibro.frequencies)
        self.plotter.update_colorbar()
        self.plotter.update_pressure_field()
        self.plotter.axes.autoscale()
        self.plotter.add_freq_label()
        plt.draw()

    def prev(self, event):
        self.plotter.current_freq -= 1
        self.plotter.current_freq %= len(self.plotter.vibro.frequencies)
        self.plotter.update_colorbar()
        self.plotter.update_pressure_field()
        self.plotter.axes.autoscale()
        self.plotter.add_freq_label()
        plt.draw()


if __name__ == '__main__':

    import os
    import compas_vibro
    from compas_vibro.datastructures import VibroStructure

    # from json files ----------------------------------------------------------

    path = compas_vibro.DATA
    name1 = '100x100_centered'
    filepath = os.path.join(path, name1 + '.json')
    vib = VibroStructure.from_json(filepath)
    vib.plot_pressure_loads()
