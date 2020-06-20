from compas_rhino.helpers import mesh_draw
from compas_vibro.vibro import frequency_key
from compas.utilities import i_to_rgb

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


def plot_diffuse_loads(vibro, real=True):
    mesh = vibro.mesh
    for fk in vibro.frequencies:
        freq = 'loads' + str(vibro.frequencies[fk]) + 'Hz'
        loads = vibro.diffuse_field_loads[fk]
        if real:
            loads = [l.real for l in loads]
        else:
            loads = [l.imag for l in loads]
        maxl = max(loads)
        minl = min(loads)
        sloads = [(l - minl) / (maxl - minl) for l in loads]
        color = {i:i_to_rgb(l) for i, l in enumerate(sloads)}
        mesh_draw(mesh, facecolor=color, layer=freq, clear_layer=True)


if __name__ == '__main__':
    import rhinoscriptsyntax as rs
    import compas_vibro
    from compas_vibro.cad import rhino_plotter
    from compas_vibro.datastructures import VibroStructure

    for i in range(30): print ''
    rs.DeleteObjects(rs.ObjectsByLayer('Default'))

    model = 'diffuse_field_example.json'
    filepath = compas_vibro.get(model)

    vibro = VibroStructure.from_json(filepath)
    plot_diffuse_loads(vibro, real=True)
