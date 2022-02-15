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

    for i, ink in enumerate(inc_nks):
        print('Computing H matrix {}/{}'.format(i + 1, len(inc_nks)))
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


def compute_cross_spectral_matrices(structure):
    rad_nks = structure.radiating_nodes()
    node_xyz = [structure.node_xyz(nk) for nk in rad_nks]
    D = calculate_distance_matrix_np(node_xyz)
    fkeys = structure.results['harmonic']
    csm = []
    for fkey in fkeys:
        f = structure.results['harmonic'][fkey].frequency
        wlen = structure.c / f
        k = (2. * np.pi) / wlen
        Gd = np.sin(k * np.abs(D)) / k * np.abs(D)
        np.fill_diagonal(Gd, 1)
        csm.append(Gd)
    return csm


def compute_mobility_based_r(structure, freq_list, damping, fx, fy, fz, backend='ansys', num_modes=20):
    structure.analyze_modal(['u'], backend=backend, num_modes=num_modes)

    mob_mats = compute_mobility_matrices(structure, freq_list, fx, fy, fz, damping=damping)
    rad_mats = compute_radiation_matrices(structure)
    spec_mats = compute_cross_spectral_matrices(structure)
    mesh = structure.radiating_mesh()
    rad_nks = structure.radiating_nodes()
    areas = [mesh.vertex_area(nk) for nk in rad_nks]
    dS = make_diagonal_area_matrix(areas)
    S = np.trace(dS)
    N = len(rad_nks)
    rho = structure.rho
    c = structure.c
    
    freqs = []
    rs = []
    rs_ = []
    rs__ = []
    structure.results['mob_radiation'] = {}
    for i, fkey in enumerate(structure.results['harmonic']):
        f = structure.results['harmonic'][fkey].frequency
        H = mob_mats[i]
        H_ = np.conjugate(np.transpose(H))
        Z = rad_mats[i]
        Gd = spec_mats[i]

        A = np.dot(np.dot(H, Z), dS)
        B = np.dot(np.dot(Gd, H_), dS)
        C = np.dot(np.real(np.dot(A, B)), dS)
        D = np.trace(C) * ((8 * rho * c ) / S)
        R = -10 * np.log10(D)

        R_ = -10 * np.log10(((8 * rho * c * np.square(S)) / N **3) * np.trace(np.real(np.dot(np.dot(np.dot(Z, H), Gd), H_))))
        R__ = -10 * np.log10(((8 * rho * c * np.square(S)) / N **3) * np.trace(np.real(np.dot(np.dot(np.dot(Gd, H_), H), Z))))

        # A = np.dot(Z, H)
        # B = np.dot(Gd, H_)
        # C = np.trace(np.real(np.dot(A, B))) * ((8 * rho * c * np.square(S)) / N ** 3)
        # R_ = -10 * np.log10(C) 
        
        # print(R, R_)
        # print(np.allclose(R, R_))
        # print('')

        freqs.append(f)
        rs.append(R)
        rs_.append(R_)
        rs__.append(R__)

        structure.results['mob_radiation'][fkey] = compas_vibro.structure.result.Result(f) 
        structure.results['mob_radiation'][fkey].radiated_p = R


    import plotly.graph_objects as go
    l1 = go.Scatter(x=freqs, y=rs, mode='lines', name='R')
    l2 = go.Scatter(x=freqs, y=rs_, mode='lines', name = 'R_')
    l3 = go.Scatter(x=freqs, y=rs__, mode='lines', name = 'R__')
    fig = go.Figure(data=[l1, l2, l3])
    fig.show()


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    geometry = 'glass_5x5'

    s = Structure.from_obj(os.path.join(compas_vibro.DATA, 'structures', '{}.obj'.format(geometry)))
    print(s)
    freq_list = list(range(20, 300, 2))
    damping=.02
    fx = 0
    fy = 0
    fz = 1
    compute_mobility_based_r(s, freq_list, damping, fx, fy, fz)
    # path = os.path.join(compas_vibro.DATA, 'structures')
    # name = '{}_mobility'.format(geometry)
    # s.to_obj(path=path, name=name)

