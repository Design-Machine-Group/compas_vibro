
try:
    from numba import jit
    import numpy as np
    # from compas.hpc.linalg.linalg_numba import diag_complex_numba
    # from compas.hpc.linalg.linalg_numba import ew_cmatrix_cscalar_division_numba as msdc
    # from compas.hpc.linalg.linalg_numba import ew_matrix_cscalar_multiplication_numba as msxc
    # from compas.hpc.linalg.linalg_numba import ew_cmatrix_matrix_division_numba as mmdcf
    # from compas.hpc.linalg.linalg_numba import ew_cmatrix_cmatrix_multiplication_numba as mmxc
except:
    pass


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


# TODO: track down what is slowing Numba down!
# TODO: why is the R matrix producing wrong results?
# TODO: rename Z matrix to impedance matrix
# TODO: when two approaches are the same, find out the fastest.

def calculate_rayleigh_rad_power_np(s, p, v, n, sum=False):
    # both approaches to the sum W are the same (find out wich is faster)
    vH = np.conjugate(np.transpose(v))
    if sum:
        # w = float(np.sum(w))
        # w = float(w)
        area = np.sum(s)
        w = area * np.real(np.dot(vH, p)) / (2 * n)
        w = float(w)
    else:
        w = s * np.real(vH * p)
        w /= 2.0
    return w


def calculate_rayleigh_rad_power_R_np(R, v):
    # this is not correct! prodices M x M, should be M
    # Like is the case in Z, a dot product is required somewhere
    vH = np.conjugate(np.transpose(v))
    # w = vH * R * v
    # w = np.dot(vH, np.dot(R, v))
    w = np.dot(np.dot(vH, R), v)
    w = float(w)
    return w


def calculate_pressure_np(Z, v):
    p = np.dot(Z, v)
    return p


def calculate_radiation_matrix_np(k, rho, c, S, D):
    """This implementation comes from Bai and Tsao 2002 (Corrected signs)
    """
    Z = 1j * k * S / 2 / np.pi * np.exp(-1j * k * D) / D
    tempvar = k * np.sqrt(np.diag(S) / np.pi)
    d = 1.0 / 2.0 * (tempvar) ** 2.0 - 1j * 8.0 / 3.0 / np.pi * tempvar
    d_indices = np.diag_indices(np.shape(Z)[0])
    Z[d_indices] = d
    Z *= (rho * c)
    return Z


def calculate_radiation_matrix_np_fahy(k, rho, omega, S, D):
    """This implementation comes from Fahy and Gardonio 2007 (page 168)
    """
    Z = ((1j * omega * rho * S) / (2 * np.pi * D)) * np.exp(-1j * k * D)
    np.fill_diagonal(Z, 1)
    return Z


def calculate_radiation_matrix_berkhoff_np(k, rho, c, S, D):
    """This implementation comes from Berkhoff 2000 (Corrected signs)
    """
    Z = 1j * k * S / 2 / np.pi * np.exp(-1j * k * D) / D
    d = 1 - np.exp(1j * k * np.sqrt(np.diag(S) / np.pi))
    d_indices = np.diag_indices(np.shape(Z)[0])
    Z[d_indices] = d
    Z *= (rho * c)
    return Z


def calculate_resistance_matrix_np(k, omega, rho, c, s, D):
    R = np.sin(k * D) / k * D
    np.fill_diagonal(R, 1)
    R *= ((omega ** 2) * rho * (np.power(s, 2))) / (4 * np.pi * c)
    return R


def calculate_resistance_from_impedance(Z, s, n):
    # both versions of R return results equal to Z equation
    area = sum(s)
    R = area * np.real(Z) / (2. * n)
    # R = np.real(area * (Z + np.conjugate(Z.T)) / (4. * n))
    return R


def eigenvalue_decomposition(A):
    w, V = np.linalg.eig(A)
    W = np.diag(w)
    # Vi = np.linalg.inv(V)
    return W, V


# @jit(nogil=True, nopython=True, parallel=False, cache=True)
# def calculate_radiation_matrix_numba(k, rho, c, S, D):
#     A = msdc(msxc(S, k * -1j), (complex(2) * np.pi))
#     B = mmdcf(np.exp(msxc(D, 1j * k)), D)
#     Z = mmxc(A, B)
#     tempvar = k * np.sqrt(np.diag(S) / np.pi)
#     d = 1.0 / 2.0 * (tempvar) ** 2.0 - 1j * 8.0 / 3.0 / np.pi * tempvar
#     Z = diag_complex_numba(Z, d)
#     Z *= (rho * c)
#     return Z
#
#
# @jit(nopython=True)
# def calculate_rayleigh_rad_power_numba(S, p, v):
#     s = S[0].reshape(-1, 1)
#     # vH = np.conjugate(np.transpose(v))
#     vH = np.conj(v.T)
#     vH = vH.reshape(-1, 1)
#     x = p * vH
#     W = s * x.real
#     W /= 2.0
#     W = np.sum(W)
#     W = float(W)
#     return W
#
#
# @jit(nopython=True)
# def calculate_pressure_numba(Z, v):
#     p = np.dot(Z, v)
#     return p


if __name__ == '__main__':

    import os
    import json
    import compas_vibro
    from compas.datastructures import Mesh
    from compas_vibro.vibro import get_mesh_data
    from compas_vibro.vibro import make_area_matrix
    from compas_vibro.vibro import make_velocities_pattern_mesh
    from compas_vibro.vibro import from_W_to_dB
    from compas_vibro.vibro import calculate_distance_matrix_np

    import time

    # from mesh ----------------------------------------------------------------

    numiter = 1
    f = 50.0
    c = 340.0
    rho = 1.225
    wlen = c / f
    k = (2. * np.pi) / wlen
    omega = k * c

    with open(compas_vibro.get('flat10x10.json'), 'r') as fp:
        data = json.load(fp)
    mesh = Mesh()
    mesh.data = data['mesh']
    mdata = get_mesh_data(mesh)
    faces = sorted(mesh.face, key=int)
    s = [mesh.face_area(fkey) for fkey in faces]
    face_centers = [mesh.face_center(fkey) for fkey in faces]

    S = make_area_matrix(s)
    D = calculate_distance_matrix_np(face_centers)
    n = int(np.sqrt(np.shape(S)[0]))
    v = make_velocities_pattern_mesh(mesh, .1, 3, complex=True)
    vr = np.real(v)
    I = np.eye(np.shape(D)[0])
    Ii = 1 - I

    # from vibro structure -----------------------------------------------------

    # from compas_vibro.datastructures import VibroStructure

    # path = compas_vibro.TEMP
    # # name = 'testing_0'
    # # name = 'testing2x2_0'
    # name = 'testing20x20wide0'
    # # name = 'testing100x100'
    # filepath = os.path.join(path, name + '.json')
    # vib = VibroStructure.from_json(filepath)

    # numiter = 1

    # f_index = 8  # key of the frequencies dict in the VibroStructure
    # f = vib.frequencies[f_index]
    # c = 340.0
    # rho = 1.225
    # wlen = c / f
    # k = (2. * np.pi) / wlen
    # omega = k * c
    # print 'f', f, 'k', k

    # mesh = vib.mesh
    # faces = sorted(mesh.face, key=int)
    # s = [mesh.face_area(fkey) for fkey in faces]
    # face_centers = [mesh.face_center(fkey) for fkey in faces]

    # S = make_area_matrix(s)
    # D = calculate_distance_matrix_np(face_centers)
    # n = len(mesh.face)
    # v = [vib.face_v[fkey][f_index] for fkey in faces]
    # vr = np.real(v)

    # # # numpy via Z matrix ---------------------------------------------------

    t0 = time.time()
    for i in range(numiter):
        Z = calculate_radiation_matrix_np(k, rho, c, S, D)
        p = calculate_pressure_np(Z, v)
        W = calculate_rayleigh_rad_power_np(s, p, v, n, sum=True)
        lw = from_W_to_dB(W)
    t1 = time.time()

    print('-' * 50)
    print('numpy')
    print('W   ', W)
    print('lw    ', lw)
    print('calculation time = ', t1 - t0)
    print('-' * 50)

    # # # numpy via fahy Z matrix ---------------------------------------------------

    t0 = time.time()
    for i in range(numiter):
        Z = calculate_radiation_matrix_np_fahy(k, rho, omega, S, D)
        p = calculate_pressure_np(Z, v)
        W = calculate_rayleigh_rad_power_np(s, p, v, n, sum=True)
        lw = from_W_to_dB(W)
    t1 = time.time()

    print('-' * 50)
    print('numpy Fahy')
    print('W   ', W)
    print('lw    ', lw)
    print('calculation time = ', t1 - t0)
    print('-' * 50)
    # # # numpy via Berkhoff Z matrix ---------------------------------------------------

    t0 = time.time()
    for i in range(numiter):
        Z = calculate_radiation_matrix_berkhoff_np(k, rho, c, S, D)
        p = calculate_pressure_np(Z, v)
        W = calculate_rayleigh_rad_power_np(s, p, v, n, sum=True)
        lw = from_W_to_dB(W)
    t1 = time.time()

    print('-' * 50)
    print('numpy Berkhoff')
    print('W   ', W)
    print('lw    ', lw)
    print('calculation time = ', t1 - t0)
    print('-' * 50)

    # # # numpy via R matrix -----------------------------------------------------

    t0 = time.time()
    for i in range(numiter):
        R = calculate_resistance_matrix_np(k, omega, rho, c, s, D)
        # R = calculate_resistance_from_impedance(Z, s, n)
        W_ = calculate_rayleigh_rad_power_R_np(R, vr)
        lw_ = from_W_to_dB(W_)
    t1 = time.time()

    print('-' * 50)
    print('numpy via R matrix')
    print('W_   ', W_)
    print('lw_    ', lw_)
    print('calculation time = ', t1 - t0)
    print('-' * 50)
    print(lw_.shape)

    print('the R matrix')
    print('is possitive definite', np.all(np.linalg.eigvals(R) > 0))
    # print('eigenvalues' , np.linalg.eigvals(R))
    print('is symmetric', np.allclose(R, R.T))
    print('is complex', np.iscomplexobj(R))
    print('shape', R.shape)
    # np.linalg.cholesky(R)



    # # ------------------------------------------------------------------------

    # # numba ------------------------------------------------------------------

    # t2 = time.time()
    # for i in range(numiter):
    #     Z_ = calculate_radiation_matrix_numba(k, rho, c, S, D)
    #     p_ = calculate_pressure_numba(Z_, v)
    #     W_ = calculate_rayleigh_rad_power_numba(S, p_, v)
    #     lw_ = from_W_to_dB(W_)
    # t3 = time.time()

    # print '-' * 50
    # print 'numba'
    # print 'W_   ', W_
    # print 'lw_    ', lw_
    # print 'calculation time = ', t3 - t2
    # print '-' * 50
    # # --------------------------------------------------------------------------
    # print np.allclose(Z, Z_)


