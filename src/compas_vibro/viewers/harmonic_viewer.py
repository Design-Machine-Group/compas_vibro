from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

import plotly.graph_objects as go

from compas.datastructures import Mesh

from compas_vibro.viewers import PlotlyViewer

class HarmonicViewer(PlotlyViewer):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, structure):
        super().__init__(structure)
        self.scale      = 1e7
        self.make_layout('harmonic')
        self.plot_shape('harmonic')

    def show(self):
        self._show('harmonic')


if __name__ == "__main__":
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    for i in range(60): print()

    filepath = os.path.join(compas_vibro.TEMP, 'opensees_mesh_flat_20x20_harmonic.obj')
    s = Structure.from_obj(filepath)
    v = HarmonicViewer(s)
    v.show()


