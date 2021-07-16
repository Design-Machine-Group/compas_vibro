
try:
    import numpy as np
except:
    pass


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2021, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

def generate_random_waves_numpy(num_waves):
    polar       = np.random.uniform(low=0., high=np.pi / 2., size=num_waves)
    azimuth     = np.random.uniform(low=0., high=2 * np.pi, size=num_waves)
    phase       = np.random.uniform(low=0., high=2 * np.pi, size=num_waves)
    amplitude   = np.random.uniform(low=0., high= 1, size=num_waves)
    return {'polar': polar, 'azimuth': azimuth, 'phase': phase, 'amplitude': amplitude}


def generate_uniform_waves_numpy(num_waves=4):
    # polar       = np.linspace(0., np.pi / 2., num_waves)
    polar   = np.ones(num_waves) * np.pi / 4.
    azimuth     = np.linspace(0., 2 * np.pi, num_waves + 1)
    # phase       = np.linspace(0., 2 * np.pi, num_waves)
    phase       = np.ones(num_waves)
    # amplitude   = np.linspace(0., 1, num_waves)
    amplitude   = np.ones(num_waves)
    return {'polar': polar, 'azimuth': azimuth, 'phase': phase, 'amplitude': amplitude}


def compute_pressure_fields_mesh(waves, mesh, frequencies, c, center=False):
    # TODO: Vectorize pressure field calculation

    xyz = [mesh.face_center(fk) for fk in mesh.faces()]
    xyz = np.array(xyz)

    if center:
        cx, cy, cz = mesh.centroid()
        xyz[:, 0] -= cx
        xyz[:, 1] -= cy
        xyz[:, 2] -= cz 

    fields = {}
    for f in frequencies:
        lambda_ = c / float(f)
        k = (2 * np.pi) / lambda_
        P = np.zeros(shape=len(xyz), dtype=np.complex128)
        for i in range(len(waves['polar'])):
            pl      = waves['polar'][i]
            az      = waves['azimuth'][i]
            phase   = waves['phase'][i]
            p       = waves['amplitude'][i]

            kx = k * np.sin(pl) * np.cos(az)
            ky = k * np.sin(pl) * np.sin(az)
            kz = k * np.cos(pl)

            temp = 1j * (phase + kx * xyz[:, 0] + ky * xyz[:, 1] + kz * xyz[:, 2])
            # P = 2 * p * np.cos(pl) * np.exp(temp)
            P += 2 * p * np.exp(temp)
        fields[f] = P
    return fields


def compute_pressure_fields_structure(waves, structure, frequencies, center=False):
    # TODO: Vectorize pressure field calculation

    eks = structure.radiating_faces()
    xyz = structure.radiating_face_centers()
    xyz = np.array(xyz)

    if center:
        cx, cy, cz = structure.radiating_center()
        xyz[:, 0] -= cx
        xyz[:, 1] -= cy
        xyz[:, 2] -= cz 

    fields = {}
    for f in frequencies:
        lambda_ = structure.c / float(f)
        k = (2 * np.pi) / lambda_
        P = np.zeros(shape=len(xyz), dtype=np.complex128)
        for i in range(len(waves['polar'])):
            pl      = waves['polar'][i]
            az      = waves['azimuth'][i]
            phase   = waves['phase'][i]
            p       = waves['amplitude'][i]

            kx = k * np.sin(pl) * np.cos(az)
            ky = k * np.sin(pl) * np.sin(az)
            kz = k * np.cos(pl)

            temp = 1j * (phase + kx * xyz[:, 0] + ky * xyz[:, 1] + kz * xyz[:, 2])
            # P = 2 * p * np.cos(pl) * np.exp(temp)
            P += 2 * p * np.exp(temp)
        P = P.tolist()
        fields[f] = {ek: P[i] for i, ek in enumerate(eks)}
    return fields


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas.datastructures import Mesh
    from compas_vibro.viewers import PressureFieldViewer
    from compas_vibro.structure import Structure

    for i in range(50): print('')


    filepath = os.path.join(compas_vibro.DATA, 'clt_1_remeshed_radiation.obj')
    s = Structure.from_obj(filepath)
    frequencies = range(20, 500, 10)
    waves = generate_uniform_waves_numpy()
    fields = compute_pressure_fields_structure(waves, s, frequencies, center=True)

    v = PressureFieldViewer(fields, structure=s)
    v.real = True
    v.show()


    num_waves = 500

    model = 'flat_mesh_20x20.json'
    # model = 'clt_2.json'
    mesh = Mesh.from_json(compas_vibro.get(model))
    # waves = generate_random_waves_numpy(num_waves)
    waves = generate_uniform_waves_numpy()
    frequencies = range(20, 500, 10)
    c = 340.0
    fields = compute_pressure_fields_mesh(waves, mesh, frequencies, c, center=True)
    v = PressureFieldViewer(fields, mesh=mesh)
    v.real = True
    v.show()