import os

# from compas_vibro.structure import FixedDisplacement
# from compas_vibro.structure import PinnedDisplacement
# from compas_vibro.structure import ElasticIsotropic
# from compas_vibro.structure import ShellSection
# from compas_vibro.structure import ElementProperties
# from compas_vibro.structure import HarmonicStep
# from compas_vibro.structure import AcousticStep
from compas_vibro.structure.step import ModalStep
# from compas_vibro.structure import PointLoad
# from compas_vibro.structure import HarmonicPressureLoad
# from compas_vibro.structure import AcousticDiffuseFieldLoad
# from compas_vibro.structure import SpringSection

# from compas_vibro.fea.ansys import load_to_results


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['modal_from_structure',
           'harmonic_from_structure']




def modal_from_structure(s, num_modes=5):

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=s.name + '_modal', 
                     displacements=[list(s.displacements.keys())[0]],
                     modes=num_modes)
    s.add(step)

    # analyse ------------------------------------------------------------------
    s.write_input_file(software='ansys', fields='u')
    s.analyse(software='ansys', cpus=4, delete=True)
    s.extract_data(software='ansys', fields='u', steps='last')
    return s


def harmonic_from_structure(s, name, freq_list, lpts=None, diffuse_pressure=None, diffuse_mesh=None, damping=0.05, fields='all', sets=None):

    # add loads ----------------------------------------------------------------
    loads = []
    if lpts:
        nodes = [s.check_node_exists(pt) for pt in lpts]
        s.add_set(name='load_nodes', type='NODE', selection=nodes)
        load = PointLoad(name='hload', nodes='load_nodes', x=0, y=0, z=1, xx=0, yy=0, zz=0)
        s.add_load(load)
        loads.append('hload')

    if diffuse_pressure:
        for fkey in list(diffuse_mesh.faces()):
            face = [s.check_node_exists(diffuse_mesh.vertex_coordinates(i)) for i in diffuse_mesh.face[fkey]]
            s.add_virtual_element(nodes=face, type='FaceElement')

        for i in range(len(diffuse_pressure)):
            load = HarmonicPressureLoad(name='diffuse' + str(i),
                                        elements=s.element_count() + i,
                                        pressure=diffuse_pressure[i].real,
                                        phase=diffuse_pressure[i].imag)
            s.add_load(load)
            loads.append('diffuse' + str(i))

    # add harmonic step --------------------------------------------------------
    step = HarmonicStep(name=name + '_harmonic', displacements=[s.displacements.keys()[0]], loads=loads,
                        freq_list=freq_list, damping=damping)
    s.add_step(step)
    s.steps_order = [name + '_harmonic']

    # calculate ----------------------------------------------------------------
    s.write_input_file(software='ansys', fields=fields)
    s.analyse(software='ansys', cpus=4, delete=True)
    s.extract_data(software='ansys', fields=fields, steps='last', sets=sets)
    return s



if __name__ == '__main__':
    pass