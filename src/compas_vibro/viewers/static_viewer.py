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

class StaticViewer(PlotlyViewer):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, structure):
        super().__init__(structure)
        self.scale      = 1e5


    def show(self):
        self.make_layout('static')
        self.plot_shape('static')
        self._show('static')


if __name__ == "__main__":
    pass


