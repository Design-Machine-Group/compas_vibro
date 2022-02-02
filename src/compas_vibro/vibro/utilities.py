
from compas.geometry import area_polygon
from compas.geometry import centroid_points


try:
    import numpy as np
    import scipy.spatial.distance as sp
except:
    pass

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


all = ['calculate_distance_matrix_np',
       'make_velocities_pattern_mesh',
       'get_mesh_data',
       'from_W_to_dB',
       'make_area_matrix',
       'frequency_key',
       'structure_face_surfaces',
       'structure_face_centers',
       ]


def calculate_distance_matrix_np(face_centers):
    XY = [[pt[0], pt[1]] for pt in face_centers]
    np.array(XY, dtype=np.float64)
    D = sp.squareform(sp.pdist(XY, metric='euclidean'))
    np.fill_diagonal(D, 1)
    return D.astype(np.float64)


def make_velocities_pattern_mesh(mesh, f, amp, complex=False):
    faces = sorted(mesh.face, key=int)
    x = [mesh.face_center(fkey)[0] for fkey in faces]
    y = [mesh.face_center(fkey)[1] for fkey in faces]

    x = (x - np.min(x)) / np.ptp(x)
    y = (y - np.min(y)) / np.ptp(y)

    if complex:
        x = np.array(x, dtype=np.complex_)
        y = np.array(y, dtype=np.complex_)
    else:
        x = np.array(x, dtype=np.float64)
        y = np.array(y, dtype=np.float64)

    y = y.conjugate().transpose()
    v = amp * (np.sin(np.pi * x * f) * np.sin(np.pi * y * f))
    # v = v.tolist()
    return v


def get_mesh_data(mesh):
    data = {}
    faces = sorted(mesh.face, key=int)
    face_centers = [mesh.face_center(fkey) for fkey in faces]
    face_areas = [mesh.face_area(fkey) for fkey in faces]
    data['face_centers'] = face_centers
    data['face_areas'] = face_areas
    return data


def from_W_to_dB(W):
    if type(W) == list:
        lw = []
        for w in W:
            lw.append((10 * np.log10(w)) + 120)
        return lw
    else:
        return (10 * np.log10(W)) + 120


def make_area_matrix(face_areas):
    s = np.array(face_areas, dtype=np.float64)
    n = np.shape(s)[0]
    S = s * np.ones((n, n))
    return S


def frequency_key(frequency, tol='3f'):
    return '{0:.{1}}'.format(float(frequency), tol)


def structure_face_surfaces(structure):
    eks = radiating_faces(structure)
    areas = []
    for ek in eks:
        pl = [structure.nodes[nk].xyz() for nk in structure.elements[ek].nodes]
        areas.append(area_polygon(pl))
    return areas


def structure_face_centers(structure):
    eks = radiating_faces(structure)
    centers = []
    for ek in eks:
        pl = [structure.nodes[nk].xyz() for nk in structure.elements[ek].nodes]
        centers.append(centroid_points(pl))
    return centers


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    for i in range(50): print('')

    # name = 'ansys_mesh_flat_20x20_harmonic.obj'
    # s = Structure.from_obj(os.path.join(compas_vibro.DATA, name))
    
    # # areas = structure_face_surfaces(s)
    # # print(areas)
    
    # centers = structure_face_centers(s)
    # print(centers)