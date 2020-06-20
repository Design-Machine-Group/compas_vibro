from compas.plotters import MeshPlotter
from compas.utilities import i_to_rgb
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
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

    def compute_pressure_facecolors(self, real=True):
        fk = self.current_freq
        if not self.facecolors[fk]:
            loads = self.vibro.diffuse_field_loads[fk]
            if real:
                loads = [l.real for l in loads]
            else:
                loads = [l.imag for l in loads]
            maxl = max(loads)
            minl = min(loads)
            sloads = [(l - minl) / (maxl - minl) for l in loads]
            facecolor = {i: i_to_rgb(l) for i, l in enumerate(sloads)}
            self.facecolors[fk] = facecolor

    def show_with_buttons(self, collection):
        callback = FreqIndex(self)
        axprev = plt.axes([0.70, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, '>')
        bnext.on_clicked(callback.next)
        bprev = Button(axprev, '<')
        bprev.on_clicked(callback.prev)

        # plt.colorbar(collection, ax=self.axes)

        self.axes.autoscale()
        self.add_freq_label()
        plt.show()

    def add_freq_label(self):
        freq = str(self.vibro.frequencies[self.current_freq]) + ' Hz'
        self.axes.set_xlabel(freq)


class FreqIndex(object):
    ind = 0

    def __init__(self, plotter):
        self.plotter = plotter

    def next(self, event):
        self.plotter.current_freq += 1
        self.plotter.current_freq %= len(self.plotter.vibro.frequencies)
        self.plotter.compute_pressure_facecolors()
        self.plotter.update_faces(facecolor=self.plotter.facecolors[self.plotter.current_freq])
        self.plotter.axes.autoscale()
        self.plotter.add_freq_label()
        plt.draw()

    def prev(self, event):
        self.plotter.current_freq -= 1
        self.plotter.current_freq %= len(self.plotter.vibro.frequencies)
        self.plotter.update_faces(facecolor=self.plotter.facecolors[self.plotter.current_freq])
        self.plotter.axes.autoscale()
        self.plotter.add_freq_label()
        plt.draw()


if __name__ == '__main__':
    # import compas_vibro
    # import json
    # from compas_vibro.datastructures import VibroMesh
    # from compas_vibro.datastructures import VibroStructure

    # # model = 'shell_leuven.json'
    # # model = 'flat20x20.json'
    # # model = 'flat10x10.json'
    # model = 'flat100x100.json'
    # # model = 'face_areas16x16.json'
    # frequencies = [62, 125, 250, 500, 1000]
    # num_waves = 1000

    # with open(compas_vibro.get(model), 'r') as fp:
    #     data = json.load(fp)
    # mesh = VibroMesh.from_data(data['mesh'])

    # vib = VibroStructure.from_mesh(mesh, frequencies=frequencies, tol='4f')
    # vib.compute_diffuse_field_loads(num_waves)
    # vib.plot_pressure_loads()

    # from json files ----------------------------------------------------------

    import os
    import compas_vibro
    from compas_vibro.datastructures import VibroStructure

    path = compas_vibro.TEMP
    name1 = 'Model C'
    filepath = os.path.join(path, name1 + '.json')
    vib = VibroStructure.from_json(filepath)
    vib.plot_pressure_loads()
