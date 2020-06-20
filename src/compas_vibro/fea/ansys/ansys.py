import os
from compas_fea import structure

from compas_fea.structure import FixedDisplacement
from compas_fea.structure import PinnedDisplacement
from compas_fea.structure import ElasticIsotropic
from compas_fea.structure import ShellSection
from compas_fea.structure import ElementProperties
from compas_fea.structure import HarmonicStep
from compas_fea.structure import AcousticStep
from compas_fea.structure import ModalStep
from compas_fea.structure import PointLoad
from compas_fea.structure import HarmonicPressureLoad
from compas_fea.structure import AcousticDiffuseFieldLoad
from compas_fea.structure import SpringSection

from compas_fea.fea.ansys import load_to_results


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['shell_model',
           'modal_from_structure',
           'harmonic_from_structure',
           'harmonic_from_structure_diffuse_steps',
           'ansys_tl_from_structure',
           'add_nodal_springs',
           'extract_rst_data']


def shell_model(mesh, thickness, material, spts, path, name, node_sets=None, support_type='pin'):

    # add shell elements from mesh ---------------------------------------------
    s = structure.Structure(name=name, path=path)
    shell_keys = s.add_nodes_elements_from_mesh(mesh, element_type='ShellElement')
    s.add_set('shell', 'element', shell_keys)

    # add node sets from points ------------------------------------------------
    if node_sets:
        for k in node_sets:
            nkeys = []
            for pt in node_sets[k]:
                nkeys.append(s.check_node_exists(pt))
            s.add_set(name=k, type='NODE', selection=nkeys)

    # add supports --------------------------------------------------------------

    nkeys = []
    for pt in spts:
        nkeys.append(s.check_node_exists(pt))
    s.add_set(name='support_nodes', type='NODE', selection=nkeys)
    if support_type == 'fix':
        supports = FixedDisplacement(name='supports', nodes='support_nodes')
    else:
        supports   = PinnedDisplacement(name='supports', nodes='support_nodes')
    s.add_displacement(supports)

    # add materials and sections -----------------------------------------------
    E = material['E']
    v = material['v']
    p = material['p']
    matname = material['name']
    concrete = ElasticIsotropic(name=matname, E=E, v=v, p=p)
    s.add_material(concrete)
    section = ShellSection(name='SEC_CONCRETE', t=thickness)
    s.add_section(section)
    prop = ElementProperties(name='floor', material=matname, section='SEC_CONCRETE', elsets=['shell'])
    s.add_element_properties(prop)

    return s


def modal_from_structure(s, num_modes, fields, name):

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=name + '_modal', displacements=[s.displacements.keys()[0]], modes=num_modes)
    s.add_step(step)
    s.set_steps_order([name + '_modal'])

    # analyse ------------------------------------------------------------------
    s.write_input_file(software='ansys', fields=fields)
    s.analyse(software='ansys', cpus=4, delete=True)
    s.extract_data(software='ansys', fields=fields, steps='last')
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


def ansys_tl_from_structure(s, name, freq_range, freq_step, vmesh, damping=0.05, fields='all'):
    """
    The mesh input must be a vibro mesh with loaded faces identified.
    By default all faces in a vibro mesh are loaded.
    """

    # add acoustically loaded elements -----------------------------------------
    lfkeys = []
    for fkey in list(vmesh.faces()):
        if vmesh.get_face_attribute(fkey, 'is_loaded'):
            face = [s.check_node_exists(vmesh.vertex_coordinates(i)) for i in vmesh.face[fkey]]
            lfkeys.append(s.add_virtual_element(nodes=face, type='FaceElement'))

    # identify acoustically radiating elements --------------------------------------
    rekeys = [s.check_element_exists(vmesh.face_vertices(fk)) for fk in vmesh.face if vmesh.get_face_attribute(fk, 'is_source')]

    # add diffuse field load ---------------------------------------------------
    load = AcousticDiffuseFieldLoad('ansys_dfl', lfkeys, air_density=1.225, sound_speed=340, max_inc_angle=90)
    s.add_load(load)

    # add acoustic step --------------------------------------------------------

    step = AcousticStep(name=name + '_acoustic',
                        displacements=[s.displacements.keys()[0]],
                        loads=['ansys_dfl'],
                        freq_range=freq_range,
                        freq_step=freq_step,
                        damping=damping,
                        sources=rekeys,
                        samples=1)

    s.add_step(step)
    s.steps_order = [name + '_acoustic']

    # calculate ----------------------------------------------------------------
    s.write_input_file(software='ansys', fields=fields)
    s.analyse(software='ansys', cpus=4, delete=True)
    s.extract_data(software='ansys', fields=fields, steps='all')
    return s


def harmonic_from_structure_diffuse_steps(s, name, freq_list, dif_list, vmesh, damping=0.05, fields='all'):
    """
    The mesh input must be a vibro mesh with loaded faces identified.
    By default all faces in a vibro mesh are loaded.
    """
    lfkeys = []
    for fkey in list(vmesh.faces()):
        if vmesh.get_face_attribute(fkey, 'is_loaded'):
            face = [s.check_node_exists(vmesh.vertex_coordinates(i)) for i in vmesh.face[fkey]]
            lfkeys.append(s.add_virtual_element(nodes=face, type='FaceElement'))

    for j, diffuse in enumerate(dif_list):
        freq = freq_list[j]

        loads = []
        for lkey in diffuse:
            load = HarmonicPressureLoad(name='diffuse_{0}_{1}'.format(j, lkey),
                                        elements=lfkeys[lkey],
                                        pressure=diffuse[lkey].real,
                                        phase=diffuse[lkey].imag)
            s.add_load(load)
            loads.append('diffuse_{0}_{1}'.format(j, lkey))

        step = HarmonicStep(name='{0}_harmonic_{1}Hz'.format(name, freq),
                            displacements=[s.displacements.keys()[0]],
                            loads=loads,
                            freq_list=[freq],
                            damping=damping)
        s.add_step(step)
        s.steps_order.append('{0}_harmonic_{1}Hz'.format(name, freq))

    # calculate ----------------------------------------------------------------
    s.write_input_file(software='ansys', fields=fields)
    s.analyse(software='ansys', cpus=4, delete=True)
    s.extract_data(software='ansys', fields=fields, steps='all')
    return s


def add_nodal_springs(s, spring_dict):

    for skey in spring_dict:
        nkeys = spring_dict[skey]['nkeys']
        spring_keys = []
        for nkey in nkeys:
            spring_keys.append(s.add_nodal_element(nkey, 'SpringElement', virtual_node=True))
        s.add_set('springs_' + str(skey), 'element', spring_keys)
        spr_sec = SpringSection('spring_section_' + str(skey), stiffness=spring_dict[skey]['stiffness'])
        prop = ElementProperties(name='springs_' + str(skey), material=None, section=spr_sec, elsets=['springs_' + str(skey)])
        s.add_element_properties(prop)

    disp = FixedDisplacement('spring_disp', 'virtual_nodes')
    # disp = PinnedDisplacement('spring_disp', 'virtual_nodes')
    s.add_displacement(disp)
    return s


def extract_rst_data(path, name):
    filepath = os.path.join(path, name + '.obj')
    s = structure.Structure.load_from_obj(filepath)
    fields = 'all'
    steps = 'all'
    s.path = path
    load_to_results(s, fields, steps)
    return s


if __name__ == '__main__':
    for i in range(60):
        print()
    import compas_vibro
    import json
    import numpy as np
    from compas_vibro.datastructures import VibroMesh
    # from compas_vibro.fea import make_random_plane_wave
    # from compas_vibro.fea import compute_incident_power_from_wave
    # from compas_vibro.fea import compute_planar_wave_pressure

    path = compas_vibro.TEMP
    name = 'harmonic_flat20x20'

    with open(compas_vibro.get('flat20x20.json'), 'r') as fp:
        data = json.load(fp)
    mesh = VibroMesh()
    mesh.data = data['mesh']
    xyz = [mesh.face_center(fk) for fk in mesh.face]
    xyz = np.array(xyz)
    area = sum([mesh.face_area(fk) for fk in mesh.face])

    spts = data['pts']
    lpts = None  # data['fpts']

    set_pts = data['set_pts']
    node_sets = {'radiating_pts': set_pts}

    thickness = 0.02
    material = {'E': 44.8 * 10 ** 9, 'v': .02, 'p': 2406.8, 'name': 'leuven_conncrete'}

    s = shell_model(mesh, thickness, material, spts, path, name, node_sets=None)

    kt = 1
    kn  = 1
    kz = 1
    krt = 1
    krn = 1
    kmax = max([kt, kn])
    krmax = max([krt, krn])

    nkeys0 = [key for key in mesh.vertices_where({'x': 0, 'y': (.001, 4.999)})]
    nkeys0.extend([key for key in mesh.vertices_where({'x': 5, 'y': (.001, 4.999)})])

    nkeys1 = [key for key in mesh.vertices_where({'y': 0, 'x': (.001, 4.999)})]
    nkeys1.extend([key for key in mesh.vertices_where({'y': 5, 'x': (.001, 4.999)})])

    nkeys2 = [key for key in mesh.vertices_where({'x': 0, 'y': 0})]
    nkeys2.extend(mesh.vertices_where({'x': 5, 'y': 0}))
    nkeys2.extend(mesh.vertices_where({'x': 5, 'y': 5}))
    nkeys2.extend(mesh.vertices_where({'x': 0, 'y': 5}))

    spring_dict = {0: {'nkeys': nkeys0, 'stiffness': {'x': kt, 'y': kn, 'z': kz, 'xx': krt, 'yy': krn}},
                   1: {'nkeys': nkeys1, 'stiffness': {'x': kn, 'y': kt, 'z': kz, 'xx': krn, 'yy': krt}},
                   2: {'nkeys': nkeys2, 'stiffness': {'x': kmax, 'y': kmax, 'z': kz, 'xx': krmax, 'yy': krmax}}}

    s = add_nodal_springs(s, spring_dict)
    print(s)
    k = nkeys0
    from compas.plotters import MeshPlotter
    plotter = MeshPlotter(mesh, figsize=(10, 7))

    plotter.draw_vertices(text={key: key for key in k},
                          radius={key: 0.2 for key in k},
                          facecolor={key: (255, 0, 0) for key in k}
                          )

    k = nkeys1
    plotter.draw_vertices(text={key: key for key in k},
                          radius={key: 0.2 for key in k},
                          facecolor={key: (0, 255, 0) for key in k}
                          )

    k = nkeys2
    plotter.draw_vertices(text={key: key for key in k},
                          radius={key: 0.2 for key in k},
                          facecolor={key: (0, 0, 255) for key in k}
                          )

    plotter.draw_edges()
    plotter.draw_faces()

    plotter.show()
