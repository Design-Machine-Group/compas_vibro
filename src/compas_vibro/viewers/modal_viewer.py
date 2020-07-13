from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from compas_vibro.viewers import PlotlyViewer


class ModalViewer(PlotlyViewer):
    """Plotly based viewer for modal analysis.
    """
    def __init__(self, structure):
        super().__init__(structure)
        self.scale = 20
        self.make_layout('modal')
        self.plot_shape('modal')
    
    def show(self):
        self._show('modal')


if __name__ == "__main__":
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    for i in range(60): print()

    filepath = os.path.join(compas_vibro.DATA, 'ansys_mesh_flat_20x20_modal.obj')
    s = Structure.from_obj(filepath)

    v = ModalViewer(s)
    v.show()

