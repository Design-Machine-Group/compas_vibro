
import json
import math

from ast import literal_eval
import numpy as np

from compas_vibro.datastructures import VibroMesh

from compas_vibro.vibro import calculate_radiation_matrix_np
from compas_vibro.vibro import calculate_pressure_np
from compas_vibro.vibro import calculate_rayleigh_rad_power_np
from compas_vibro.vibro import make_area_matrix
from compas_vibro.vibro import calculate_distance_matrix_np
from compas_vibro.vibro import frequency_key
from compas_vibro.vibro import make_random_plane_waves
# from compas_vibro.vibro import compute_incident_power_from_wave  # probably will delete this one too...frequencies
from compas_vibro.vibro import compute_incident_power_from_field
from compas_vibro.vibro import compute_planar_wave_pressure
from compas_vibro.vibro import compute_planar_vwave_pressure  # probably will delete this one...

from compas_vibro.fea import shell_model
from compas_vibro.fea import harmonic_from_structure_diffuse_steps
from compas_vibro.fea import add_nodal_springs
from compas_vibro.fea import extract_rst_data

from compas_fea.utilities import mesh_from_shell_elements

# from compas_vibro.viewers import VibroViewer
# from compas_vibro.viewers import VibroPlotter
# from compas_vibro.viewers import VibroLoadsPlotter


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


TPL = """
================================================================================
VibroStructure summary
================================================================================

- number of frequencies : {}

- number of elements :{}

- speed of sound : {}

- air density : {}

- contains displacement data {}

- contains velocity data : {}

- contains radiation data : {}

================================================================================
"""


# TODO: Update __str__ function, what is relevant to print?

class VibroStructure(object):
    def __init__(self, name='VibroStructure', mesh=None, frequencies=None, tol='3f'):
        self.name = name
        self.structure = None
        self.mesh = mesh
        self.rho = 1.225
        self.c = 340.0
        self.frequencies = frequencies
        self.freq_index = {}
        self.tol = tol
        self.update_freq_data()
        self.node_v = {}
        self.face_v = {}
        self.node_disp = {}
        self.face_w = {}
        self.face_lw = {}
        self.diffuse_field_loads = {}
        self.diffuse_incident_power = {}
        self.total_radiation_w = {}
        self.total_radiation_lw = {}
        self.transmission_loss = {}
        self.str_attrs = {}
        self.waves = {}

    # --------------------------------------------------------------------------
    # customisation
    # --------------------------------------------------------------------------

    def __str__(self):
        """Compile a summary of the VibroStructure."""
        try:
            numf = len(self.frequencies)
        except:
            numf = 0
        try:
            numfac = self.number_of_faces()
        except:
            numfac = 0

        return TPL.format(numf,
                          numfac,
                          self.c,
                          self.rho,
                          contains_data(self.node_disp),
                          contains_data(self.node_v) or contains_data(self.face_v),
                          contains_data(self.face_w))

    # --------------------------------------------------------------------------
    # special properties
    # --------------------------------------------------------------------------

    @property
    def data(self):
        data = {'name'                      : self.name,
                'rho'                       : self.rho,
                'c'                         : self.c,
                'tol'                       : self.tol,
                'frequencies'               : {},
                'freq_index'                : self.freq_index,
                'node_disp'                 : {},
                'face_v'                    : {},
                'face_w'                    : {},
                'face_lw'                   : {},
                'diffuse_field_loads'       : {},
                'diffuse_incident_power'    : {},
                'total_radiation_w'         : {},
                'total_radiation_lw'        : {},
                'transmission_loss'         : {},
                'mesh'                      : {},
                'str_attrs'                 : {}}

        for key in self.frequencies:
            rkey = repr(key)
            data['frequencies'][rkey] = self.frequencies[key]

        for key in self.node_disp:
            rkey = repr(key)
            data['node_disp'][rkey] = {repr(fk): self.node_disp[key][fk] for fk in self.node_disp[key]}

        for key in self.face_v:
            rkey = repr(key)
            data['face_v'][rkey] = {repr(fk): self.face_v[key][fk] for fk in self.face_v[key]}

        for key in self.diffuse_field_loads:
            rkey = repr(key)
            data['diffuse_field_loads'][rkey] = self.diffuse_field_loads[key]

        for key in self.diffuse_incident_power:
            rkey = repr(key)
            data['diffuse_incident_power'][rkey] = self.diffuse_incident_power[key]

        for key in self.total_radiation_w:
            rkey = repr(key)
            data['total_radiation_w'][rkey] = self.total_radiation_w[key]

        for key in self.transmission_loss:
            rkey = repr(key)
            data['transmission_loss'][rkey] = self.transmission_loss[key]

        for key in self.str_attrs:
            rkey = repr(key)
            data['str_attrs'][rkey] = self.str_attrs[key]

        data['mesh'] = self.mesh.to_data()

        return data

    @data.setter
    def data(self, data):

        self.clear()

        self.name               = data['name']
        self.rho                = data['rho']
        self.c                  = data['c']
        self.tol                = data['tol']
        self.freq_index         = data['freq_index']

        frequencies             = data['frequencies']
        face_v                  = data['face_v']
        node_disp               = data['node_disp']
        diffuse_field_loads     = data['diffuse_field_loads']
        diffuse_incident_power  = data['diffuse_incident_power']
        total_radiation_w       = data['total_radiation_w']
        transmission_loss       = data['transmission_loss']
        str_attrs               = data['str_attrs']

        for key in frequencies:
            k = literal_eval(key)
            self.frequencies[k] = frequencies[key]

        for key in face_v:
            k = literal_eval(key)
            self.face_v[k] = {literal_eval(fk): face_v[key][fk] for fk in face_v[key]}

        for key in node_disp:
            k = literal_eval(key)
            self.node_disp[k] = {literal_eval(fk): node_disp[key][fk] for fk in node_disp[key]}

        for key in diffuse_field_loads:
            k = literal_eval(key)
            self.diffuse_field_loads[k] = diffuse_field_loads[key]

        for key in diffuse_incident_power:
            k = literal_eval(key)
            self.diffuse_incident_power[k] = diffuse_incident_power[key]

        for key in total_radiation_w:
            k = literal_eval(key)
            self.total_radiation_w[k] = total_radiation_w[key]

        for key in transmission_loss:
            k = literal_eval(key)
            self.transmission_loss[k] = transmission_loss[key]

        for key in str_attrs:
            k = literal_eval(key)
            self.str_attrs[k] = str_attrs[key]

        self.mesh = VibroMesh.from_data(data['mesh'])

    # --------------------------------------------------------------------------
    # constructors
    # --------------------------------------------------------------------------

    @classmethod
    def from_mesh(cls, name, mesh, frequencies=None, tol='3f'):
        vibro = cls(name=name, mesh=mesh, frequencies=frequencies, tol=tol)
        return vibro

    @classmethod
    def from_fe_structure(cls, name, structure, frequencies=None):
        vibro = cls(name=name, mesh=None, frequencies=frequencies)
        vibro.structure = structure
        vibro.extract_mesh_from_structure()
        if structure.results:
            vibro.extract_frequencies_from_structure()
            vibro.extract_displacements_from_structure()
            # vibro.compute_face_velocities_from_displacements()
            vibro.compute_velocities_from_displacements()

        return vibro

    @classmethod
    def from_data(cls, data):
        vibro = cls()
        vibro.data = data
        return vibro

    @classmethod
    def from_json(cls, filepath):
        with open(filepath, 'r') as fp:
            data = json.load(fp, object_hook=decode_complex)
        vibro = cls()
        vibro.data = data
        return vibro

    @classmethod
    def from_ansys_rst(cls, path, name):

        structure = extract_rst_data(path, name)
        frequencies = []
        for skey in structure.steps_order:
            step = structure.steps[skey]
            frequencies.extend(step.freq_list)
        mesh  = mesh_from_shell_elements(structure)
        vibro = cls(name=name, frequencies=frequencies)
        vibro.structure = structure
        vibro.mesh = mesh
        return vibro

    # --------------------------------------------------------------------------
    # converters
    # --------------------------------------------------------------------------

    def to_json(self, filepath=None):
        if not filepath:
            return json.dumps(self.data, default=encode_complex)
        else:
            with open(filepath, 'w+') as fp:
                json.dump(self.data, fp, default=encode_complex)

    # --------------------------------------------------------------------------
    # attributes
    # --------------------------------------------------------------------------

    def set_node_velocities(self, frequency, velocities):
        for i, nkey in enumerate(self.mesh.vertex):
            self.node_v.setdefault(nkey, {})
            self.node_v[nkey].setdefault(frequency, velocities[i])

    def get_node_velocity(self, frequency, nkey):
        return self.node_v[nkey][frequency]

    # --------------------------------------------------------------------------
    # acoustic computation
    # --------------------------------------------------------------------------

    def compute_face_velocities(self, frequency):

        faces = self.mesh.faces()
        velocities = []
        for fkey in faces:
            nkeys = self.mesh.face_vertices(fkey)

            vr = [self.node_v[nkey][frequency].real for nkey in nkeys]
            vi = [self.node_v[nkey][frequency].imag for nkey in nkeys]

            real = np.average(vr, axis=0)
            imag = np.average(vi, axis=0)
            velocities.append(complex(real, imag))

        return velocities

    def compute_face_velocities_from_displacements(self):
        lfaces = [fk for fk in self.mesh.face if self.mesh.get_face_attributes(fk, 'is_loaded')]
        lfaces = sorted(lfaces, key=int)
        for fkey in lfaces:
            nkeys = self.mesh.face_vertices(fkey)
            self.face_v[fkey] = {}
            for f in self.frequencies:
                vr = [self.node_disp[nkey][f]['real'] for nkey in nkeys]
                vi = [self.node_disp[nkey][f]['imag'] for nkey in nkeys]

                vr = [[d['x'], d['y'], d['z']] for d in vr]
                vi = [[d['x'], d['y'], d['z']] for d in vi]

                real = np.average(vr, axis=0)
                imag = np.average(vi, axis=0)

                real_l = (real[0] ** 2 + real[1] ** 2 + real[2] ** 2) ** 0.5
                imag_l = (imag[0] ** 2 + imag[1] ** 2 + imag[2] ** 2) ** 0.5
                x = real_l + (imag_l * 1j)
                v = 2 * np.pi * float(self.frequencies[f]) * x * 1j
                self.face_v[fkey][f] = v

    def compute_velocities_from_displacements(self):
        velocities = {}
        for nkey in self.mesh.vertex:
            velocities[nkey] = {}
            for f in self.frequencies:
                vr = self.node_disp[nkey][f]['real']
                vi = self.node_disp[nkey][f]['imag']

                vr = [vr['x'], vr['y'], vr['z']]
                vi = [vi['x'], vi['y'], vi['z']]

                real_l = (vr[0] ** 2 + vr[1] ** 2 + vr[2] ** 2) ** 0.5
                imag_l = (vi[0] ** 2 + vi[1] ** 2 + vi[2] ** 2) ** 0.5
                x = real_l + (imag_l * 1j)
                v = 2 * np.pi * float(self.frequencies[f]) * x * 1j
                velocities[nkey][f] = v

        self.node_v = velocities

    def compute_radiation(self):
        lfaces = [fk for fk in self.mesh.face if self.mesh.get_face_attributes(fk, 'is_loaded')]
        lfaces = sorted(lfaces, key=int)
        face_areas = [self.mesh.face_area(fkey) for fkey in lfaces]
        face_centers = [self.mesh.face_center(fkey) for fkey in lfaces]

        S = make_area_matrix(face_areas)
        s = face_areas
        D = calculate_distance_matrix_np(face_centers)
        n = len(lfaces)

        for f in self.frequencies:
            v = [self.face_v[fkey][f] for fkey in lfaces]
            k = self.k[f]
            Z = calculate_radiation_matrix_np(k, self.rho, self.c, S, D)
            p = calculate_pressure_np(Z, v)
            # w = calculate_rayleigh_rad_power_np(S, p, v).tolist()
            w = calculate_rayleigh_rad_power_np(s, p, v, n).tolist()
            self.face_w[f] = {fk: w[i] for i, fk in enumerate(lfaces)}
            self.total_radiation_w[f] = sum(self.face_w[f].values())

    def compute_diffuse_field_loads(self, num_waves=1000, waves=None):
        lfaces = [fk for fk in self.mesh.face if self.mesh.get_face_attributes(fk, 'is_loaded')]
        xyz = [self.mesh.face_center(fk) for fk in lfaces]
        xyz = np.array(xyz)
        area = sum([self.mesh.face_area(fk) for fk in lfaces])
        if not waves:
            waves = make_random_plane_waves(num_waves)
        for f in self.frequencies:
            I = 0
            P = np.zeros(self.mesh.number_of_faces(), dtype=np.complex_)
            for wave in waves:
                # I += compute_incident_power_from_wave(wave, area, self.c, self.rho)
                P += compute_planar_wave_pressure(wave, xyz, self.k[f])
            I = compute_incident_power_from_field(P, area, self.c, self.rho)
            self.diffuse_incident_power[f] = I
            P = P.tolist()
            self.diffuse_field_loads[f] = {fk: P[i] for i, fk in enumerate(lfaces)}
        self.waves = waves

    def compute_diffuse_field_loads_vector(self, waves=None):

        xyz_list = [self.mesh.face_center(fk) for fk in self.mesh.face]

        for f in self.frequencies:
            P = np.zeros(self.mesh.number_of_faces(), dtype=np.complex_)
            for wave in waves:
                for i, xyz in enumerate(xyz_list):
                    xyz = np.array(xyz)
                    wlen = self.wlen[f]
                    P[i] += compute_planar_vwave_pressure(wave, xyz, wlen)
            self.diffuse_field_loads[f] = P.tolist()

    def compute_transmission_loss(self):
        for f in self.frequencies:
            tl = 10 * math.log10(self.diffuse_incident_power[f] / self.total_radiation_w[f])
            self.transmission_loss[f] = tl

    def save_waves(self, filepath):
        wavedata = {}
        for i, wave in enumerate(self.waves):
            wavedata[i] = wave

        if not filepath:
            return json.dumps(wavedata)
        else:
            with open(filepath, 'w+') as fp:
                json.dump(wavedata, fp)

    # --------------------------------------------------------------------------
    # fea structure
    # --------------------------------------------------------------------------

    def compute_radiation_from_diffuse_loads(self, path, fields='all'):
        frequencies = [self.frequencies[f] for f in self.frequencies]
        diffuse = [self.diffuse_field_loads[f] for f in self.diffuse_field_loads]

        thickness = self.str_attrs['thickness']
        material = self.str_attrs['material']
        damping = self.str_attrs['damping']
        spts = self.str_attrs['spts']
        suptyp = self.str_attrs['support_type']

        self.structure = shell_model(self.mesh,
                                     thickness,
                                     material,
                                     spts,
                                     path,
                                     self.name,
                                     support_type=suptyp)

        if 'springs' in self.str_attrs:
            spring_dict = self.str_attrs['springs']
            self.structure = add_nodal_springs(self.structure, spring_dict)

        self.structure = harmonic_from_structure_diffuse_steps(self.structure,
                                                               self.name,
                                                               frequencies,
                                                               diffuse,
                                                               self.mesh,
                                                               damping=damping,
                                                               fields=fields)

        self.extract_displacements_from_structure()
        self.compute_face_velocities_from_displacements()
        self.compute_radiation()

    def extract_mesh_from_structure(self):
        snodes = self.structure.nodes
        nodes = [[snodes[n]['x'], snodes[n]['y'], snodes[n]['z']] for n in snodes]
        faces = [self.structure.elements[e].nodes for e in self.structure.elements]
        self.mesh = VibroMesh.from_vertices_and_faces(nodes, faces)

    def extract_displacements_from_structure(self):
        steps = self.structure.results.keys()
        if steps:
            for step in steps:
                nks = self.structure.results[step]['nodal'].keys()
                for nk in nks:
                    self.node_disp.setdefault(nk, {})
                    fks = self.structure.results[step]['nodal'][nk].keys()
                    for fk in fks:
                        freq_key = self.freq_index[frequency_key(fk, self.tol)]
                        self.node_disp[nk][freq_key] = self.structure.results[step]['nodal'][nk][fk]

    def extract_frequencies_from_structure(self):
        steps = self.structure.results.keys()
        if steps:
            step = steps[0]
            self.frequencies = [float(f) for f in self.structure.results[step]['frequencies']]
            self.update_freq_data()

    def set_structure_variables(self, attrs):
        for attr in attrs:
            self.str_attrs[attr] = attrs[attr]

    # --------------------------------------------------------------------------
    # viewers / plotters
    # --------------------------------------------------------------------------

    def plot_radiation(self, frequency):

        viewer = VibroViewer(self, 0, velocities=False)
        viewer.axes_on = False
        viewer.grid_on = False
        for i in range(20):
            viewer.camera.zoom_in()
        viewer.setup()
        viewer.show()

    def plot_radiation_vtk(self, frequency):
        viewer = VtkVibroViewer(self, frequency)
        viewer.settings['draw_axes'] = 1
        viewer.settings['draw_vertices'] = 0
        viewer.settings['draw_faces'] = 1
        # viewer.keycallbacks['s'] = func
        viewer.start()

    def plot_radiation_curve(self):
        plotter = VibroPlotter(self, log_freq=False)
        plotter.plot_radiation_curve()

    def plot_transmission_loss(self):
        plotter = VibroPlotter(self, log_freq=False)
        plotter.plot_transmission_loss()

    def plot_radiation_vs_tl(self):
        plotter = VibroPlotter(self, log_freq=False)
        plotter.plot_rad_vs_tl()

    def plot_harmonic_displacements(self, frequency):
        viewer = VtkVibroViewer(self, frequency)
        viewer.settings['draw_axes'] = 1
        viewer.settings['draw_vertices'] = 0
        viewer.settings['draw_faces'] = 1
        # viewer.keycallbacks['s'] = func
        viewer.start()

    def plot_pressure_loads(self,):
        plotter = VibroLoadsPlotter(self)
        plotter.title = 'Diffuse field Pressure loads'
        # plotter.compute_pressure_facecolors()
        plotter.draw_pressure_field()
        plotter.show()
        # plotter.show()

    # --------------------------------------------------------------------------
    # helpers
    # --------------------------------------------------------------------------

    def clear(self):

        self.structure = None
        self.mesh = None
        self.rho = 1.225
        self.c = 340.0
        self.frequencies = {}
        self.freq_index = {}
        self.tol = '3f'
        self.node_v = {}
        self.face_v = {}
        self.node_disp = {}
        self.face_w = {}
        self.face_lw = {}
        self.diffuse_field_loads = {}
        self.diffuse_incident_power = {}
        self.total_radiation_w = {}
        self.total_radiation_lw = {}
        self.transmission_loss = {}

    def update_freq_data(self):
        if self.frequencies:
            self.frequencies = {i: f for i, f in enumerate(self.frequencies)}
            self.wlen = {i: self.c / self.frequencies[f] for i, f in enumerate(self.frequencies)}
            self.k = {i: (2 * math.pi) / self.wlen[l] for i, l in enumerate(self.wlen)}
            self.make_freq_index_dic()

    def make_freq_index_dic(self):
        for fkey in self.frequencies:
            fk = frequency_key(self.frequencies[fkey], self.tol)
            self.freq_index[fk] = fkey


def contains_data(var):
    if var:
        return True
    else:
        return False


def encode_complex(x):
    if isinstance(x, complex):
        return {'__complex__': True, 'real': x.real, 'imag': x.imag}
    else:
        type_name = x.__class__.__name__
        raise TypeError('Object of type {0} is not JSON serializable'.format(type_name))


def decode_complex(dic):
    if '__complex__' in dic:
        return complex(dic['real'], dic['imag'])
    return dic


if __name__ == '__main__':

    for i in range(60): print()
    import compas_vibro

    # # ------------------------------------------------------------------------

    # # model = 'shell_leuven.json'
    # # model = 'flat20x20.json'
    # # model = 'flat10x10.json'
    # model = 'flat100x100.json'
    # # model = 'face_areas16x16.json'
    # # frequencies = [50, 100, 1000]
    # frequencies = range(1, 1000, 50)
    # num_waves = 1000

    # with open(compas_vibro.get(model), 'r') as fp:
    #     data = json.load(fp)
    # mesh = VibroMesh.from_data(data['mesh'])

    # vib = VibroStructure.from_mesh(model, mesh, frequencies=frequencies, tol='4f')
    # vib.compute_diffuse_field_loads(num_waves, uniform=False)
    # vib.plot_pressure_loads()

    # # from mesh --------------------------------------------------------------

    import json
    from compas_vibro.datastructures import VibroMesh
    from compas_vibro.vibro import make_velocities_pattern_mesh

    # model = 'shell_leuven.json'
    model = 'flat20x20.json'
    # model = 'flat10x10.json'
    # model = 'face_areas16x16.json'

    with open(compas_vibro.get(model), 'r') as fp:
        data = json.load(fp)
    vmesh = VibroMesh.from_data(data['mesh'])

    frequencies = [50]
    vib = VibroStructure.from_mesh(mesh=vmesh, frequencies=frequencies)

    for frkey in vib.frequencies:
        v = make_velocities_pattern_mesh(vmesh, 3, .5, complex=True)
        vib.set_node_velocities(frkey, v)

    vib.compute_radiation()
    # vib.plot_radiation(0)
    vib.plot_radiation_vtk(0)

    print(vib)

    # from FEA structure -------------------------------------------------------

    # filepath = compas_vibro.get('harmonic_flat20x20.obj')
    # structure = Structure.load_from_obj(filepath)
    # vib = VibroStructure.from_fe_structure(structure)
    # vib.compute_radiation()
    # # print vib.face_w[1]
    # vib.plot_harmonic_displacements(1)
    # print vib


