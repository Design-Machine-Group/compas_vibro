__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


try:
    import numpy as np
except:
    pass

from compas_vibro.structure.load import PointLoad
from compas_vibro.vibro.rayleigh import calculate_radiation_matrix_np
from compas_vibro.vibro.utilities import calculate_distance_matrix_np
from compas_vibro.vibro.utilities import make_area_matrix
from compas_vibro.vibro.utilities import make_diagonal_area_matrix
from compas.geometry import length_vector


def compute_mobility_matrices(structure, freq_list, fx, fy, fz, damping=.02, backend='ansys'):

    rad_nks = structure.radiating_nodes()
    inc_nks = structure.incident_nodes()

    mm = [[] for _ in range(len(freq_list))]

    fvl = length_vector([fx, fy, fz])

    for ink in inc_nks:
        load = PointLoad(name='pload', nodes=[ink], x=fx, y=fy, z=fz, xx=0, yy=0, zz=0)
        structure.add(load)
        structure.analyze_harmonic(freq_list,
                                   fields=['u'],
                                   backend=backend, 
                                   damping=damping)
        fkeys = structure.results['harmonic']
        for fkey in fkeys:
            structure.results['harmonic'][fkey].compute_node_velocities()
            vr = [structure.results['harmonic'][fkey].velocities[nkey].real for nkey in rad_nks]
            vi = [structure.results['harmonic'][fkey].velocities[nkey].imag for nkey in rad_nks]
            v = [complex(vr[i], vi[i]) for i in range(len(vr))]
            v = [vi / fvl for vi in v]
            
            mm[fkey].append(v)

    mob_mats = []
    for a in mm:
        mob_mats.append(np.array(a))
    return mob_mats


def compute_radiation_matrices(structure):
    mesh = structure.radiating_mesh()
    rad_nks = structure.radiating_nodes()
    areas = [mesh.vertex_area(nk) for nk in rad_nks]
    S = make_area_matrix(areas)
    node_xyz = [structure.node_xyz(nk) for nk in rad_nks]
    D = calculate_distance_matrix_np(node_xyz)
    fkeys = structure.results['harmonic']
    rms = []
    for fkey in fkeys:
        f = structure.results['harmonic'][fkey].frequency
        wlen = structure.c / f
        k = (2. * np.pi) / wlen
        Z = calculate_radiation_matrix_np(k, structure.rho, structure.c, S, D)
        rms.append(Z)
    return rms

def compute_mobility_based_r(structure, freq_list, damping, fx, fy, fz):
    # mob_mats = compute_mobility_matrices(structure, freq_list, fx, fy, fz, damping=damping)
    # rad_mats = compute_radiation_matrices(structure)
    mesh = structure.radiating_mesh()
    rad_nks = structure.radiating_nodes()
    areas = [mesh.vertex_area(nk) for nk in rad_nks]
    dS = make_diagonal_area_matrix(areas)
    print(np.trace(dS))
    # for i, fkey in enumerate(structure.results['harmonic']):
    #     f = structure.results['harmonic'][fkey].frequency
    #     H = mob_mats[i]
    #     Z = rad_mats[i]


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    s = Structure.from_obj(os.path.join(compas_vibro.DATA, 'structures', 'flat_5x5.obj'))
    print(s)
    freq_list = list(range(20, 200, 5))
    damping=.02
    fx = 0
    fy = 0
    fz = 1
    compute_mobility_based_r(s, freq_list, damping, fx, fy, fz)

