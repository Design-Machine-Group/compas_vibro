
try:
    import numpy as np
except:
    pass
import random
import json

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

# TODO: Must implement loading for non-planar geometry, az and pl angles must be recomputed per planar wave!

__all__ = ['make_random_plane_waves',
           'compute_incident_power_from_wave',
           'compute_planar_wave_pressure',
           'make_uniform_plane_waves',
           'compute_planar_vwave_pressure',
           'compute_incident_power_from_field',
           'waves_from_json']


def remap_to_domain(value, old, new):
    old = [float(i) for i in old]
    new = [float(i) for i in new]
    return (((value - old[0]) * (new[1] - new[0])) / (old[1] - old[0])) + new[0]


def make_random_plane_waves(num_waves, fixed_pressure=True):
    waves = []
    for i in range(num_waves):
        pl_angle = random.uniform(0, np.pi / 2.)            # must be from 0 to pi
        az_angle = random.uniform(0, 2 * np.pi)        # must be from 0 to 2 pi
        phase    = random.uniform(0, 2 * np.pi)           # must be from 0 to 2 pi

        if fixed_pressure:
            pressure = 1
        else:
            pressure = random.uniform(0, 1)                     # must be from 0 to 1

        waves.append({'pl_angle': pl_angle, 'az_angle': az_angle, 'pressure': pressure, 'phase': phase})
    return waves


def make_uniform_plane_waves(numpolar, numazimut, numpressures, numphases):

    # numvar = num_waves + 1  # = int(num_waves ** (1 / 4.)) + 1
    pl_angles   = [(i / float(numpolar + 1)) * np.pi / 2. for i in range(1, numpolar + 1)]
    # pl_angles   = [remap_to_domain(i / float(numpolar), (0,1), (-np.pi/2., np.pi/2.)) for i in range(1, numpolar + 1)]
    az_angles   = [(i / float(numazimut + 1)) * 2 * np.pi for i in range(1, numazimut + 1)]
    pressures   = [(i / float(numpressures + 1)) for i in range(1, numpressures + 1)]
    phases      = [(i / float(numphases + 1)) * 2 * np.pi for i in range(1, numphases + 1)]

    waves = []
    for pl in pl_angles:
        for az in az_angles:
            for p in pressures:
                for ph in phases:
                    waves.append({'pl_angle': pl, 'az_angle': az, 'pressure': p, 'phase': ph})
    return waves


def compute_incident_power_from_wave(wave, area, c, rho):
    pl = wave['pl_angle']
    p = wave['pressure']
    # I = area * np.cos(pl) * (((p * np.cos(pl)) ** 2) / (rho * c))
    I = area * (((p * np.cos(pl)) ** 2) / (rho * c))
    return I


def compute_incident_power_from_field(field, area, c, rho):
    I = (np.average(np.power(np.abs(field), 2))) / (4 * rho * c)
    I *= area
    return I


def compute_planar_wave_pressure(wave, xyz, k):
    pl = wave['pl_angle']
    p = wave['pressure']
    az = wave['az_angle']
    phase = wave['phase']

    kx = k * np.sin(pl) * np.cos(az)
    ky = k * np.sin(pl) * np.sin(az)
    kz = k * np.cos(pl)

    temp = 1j * (phase + kx * xyz[:, 0] + ky * xyz[:, 1] + kz * xyz[:, 2])
    # P = 2 * p * np.cos(pl) * np.exp(temp)
    P = 2 * p * np.exp(temp)
    return P


def compute_planar_vwave_pressure(wave, xyz, wlen):  # TODO: this function must be vectorised
    v = wave['direction']
    phase = wave['phase']
    p = wave['pressure']
    temp = 1j * ((np.pi / wlen) * np.dot(np.transpose(xyz), v) - phase)
    P = p * np.exp(temp)
    return P


def waves_from_json(filepath):
    with open(filepath, 'r') as fp:
        wdict = json.load(fp)
    keys = sorted(wdict.keys(), key=int)
    waves = []
    for key in keys:
        waves.append(wdict[key])
    return waves

if __name__ == '__main__':

    import json
    import compas_vibro
    from compas_vibro.datastructures import VibroMesh

    # get geometry ------------------------------------------------------------
    model = 'flat20x20.json'
    with open(compas_vibro.get(model), 'r') as fp:
        data = json.load(fp)

    vmesh = VibroMesh.from_data(data['mesh'])
    xyz = [vmesh.face_center(fk) for fk in vmesh.face]
    xyz = np.array(xyz)
    area = sum([vmesh.face_area(fk) for fk in vmesh.face])

    filepath = compas_vibro.get('2k_waves.json')
    waves = waves_from_json(filepath)



    # # acoustic input ----------------------------------------------------------
    # f = 500
    # c = 340.0
    # rho = 1.225
    # lambda_ = c / f
    # k = (2 * np.pi) / lambda_
    # num_waves = 1300

    # # compute pressure field and incident power (random)------------------------
    # I = 0
    # P = np.zeros(vmesh.number_of_faces(), dtype=np.complex_)
    # waves = make_random_plane_waves(num_waves)
    # for wave in waves:
    #     I += compute_incident_power_from_wave(wave, area, c, rho)
    #     P += compute_planar_wave_pressure(wave, xyz, k)
    # I_ = compute_incident_power_from_field(P, area, c, rho)
    # print 'I', I
    # print 'I_', I_
    # # print P

    # compute pressure field and incident power (uniform)-----------------------
    # numwaves = 10

    # waves = make_uniform_plane_waves(10, 1, 1, 1)
    # for w in waves: print w['pl_angle'], np.cos(w['pl_angle'])
    # I = 0
    # P = np.zeros(vmesh.number_of_faces(), dtype=np.complex_)
    # for wave in waves:
    #     I += compute_incident_power_from_wave(wave, area, c, rho)
    #     P += compute_planar_wave_pressure(wave, xyz, k)
    # print I
    # print P

