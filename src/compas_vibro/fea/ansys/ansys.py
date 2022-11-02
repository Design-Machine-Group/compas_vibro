from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import subprocess

from compas_vibro.structure.result import Result

from compas_vibro.structure.step import StaticStep
from compas_vibro.structure.step import ModalStep
from compas_vibro.structure.step import HarmonicStep
from compas_vibro.structure.step import HarmonicFieldStep

from compas_vibro.fea.ansys.write import write_command_file_static
from compas_vibro.fea.ansys.write import write_command_file_modal
from compas_vibro.fea.ansys.write import write_command_file_modal_prestressed
from compas_vibro.fea.ansys.write import write_command_file_harmonic
from compas_vibro.fea.ansys.write import write_command_file_harmonic_super
from compas_vibro.fea.ansys.write import write_command_file_harmonic_field

from compas_vibro.fea.ansys.read import read_modal_freq
from compas_vibro.fea.ansys.read import read_participation_factor
from compas_vibro.fea.ansys.read import read_effective_mass
from compas_vibro.fea.ansys.read import read_modal_displacements
from compas_vibro.fea.ansys.read import read_harmonic_displacements
from compas_vibro.fea.ansys.read import read_harmonic_displacements_field
from compas_vibro.fea.ansys.read import read_modal_coordinates
from compas_vibro.fea.ansys.read import read_static_displacements
from compas_vibro.fea.ansys.read import read_static_stresses
from compas_vibro.fea.ansys.read import read_principal_stresses
from compas_vibro.fea.ansys.read import read_shear_stresses
from compas_vibro.fea.ansys.read import read_reactions

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['ansys_static',
           'ansys_modal',
           'ansys_modal_prestressed',
           'ansys_harmonic',
           'ansys_harmonic_super',
           'ansys_harmonic_field']


def ansys_static(structure, fields, license='introductory'):

    # add modal step -----------------------------------------------------------
    step = StaticStep(name=structure.name + '_modal', 
                     displacements=list(structure.displacements.keys()),
                     loads=list(structure.loads.keys()),
                     nlgeom=structure.nl_geom,
                     )
    structure.add(step)

    # analyse and extraxt results ----------------------------------------------
    write_command_file_static(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)
    extract_data(structure, fields, 'static')
    return structure


def ansys_modal(structure, fields, num_modes, license='introductory'):

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=structure.name + '_modal', 
                     displacements=list(structure.displacements.keys()),
                     modes=num_modes)
    structure.add(step)

    # analyse and extraxt results ----------------------------------------------
    write_command_file_modal(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)
    extract_data(structure, fields, 'modal')
    return structure


def ansys_modal_prestressed(structure, fields, num_modes, license='introductory'):

    # add static step -----------------------------------------------------------
    step = StaticStep(name=structure.name + '_modal', 
                     displacements=list(structure.displacements.keys()),
                     loads=list(structure.loads.keys()),
                     nlgeom=structure.nl_geom,
                     )
    structure.add(step)

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=structure.name + '_modal', 
                     displacements=list(structure.displacements.keys()),
                     modes=num_modes)
    structure.add(step)

    # analyse and extraxt results ----------------------------------------------
    write_command_file_modal_prestressed(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)
    extract_data(structure, fields, 'modal')
    return structure


def ansys_harmonic(structure, freq_list, fields='all', damping=0.02):

    # # add harmonic step --------------------------------------------------------
    loads = [structure.loads[lk].name for lk in structure.loads]
    step = HarmonicStep(name=structure.name + '_harmonic',
                        displacements=list(structure.displacements.keys()),
                        loads=loads,
                        freq_list=freq_list,
                        damping=damping)
    structure.add(step)
    structure.steps_order = [structure.name + '_harmonic']

    # analyse and extraxt results ----------------------------------------------
    write_command_file_harmonic(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)
    extract_data(structure, fields, 'harmonic')
    return structure


def ansys_harmonic_super(structure, num_modes, freq_list, fields='all', damping=0.02):

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=structure.name + '_modal', 
                     displacements=[list(structure.displacements.keys())[0]],
                     modes=num_modes)
    structure.add(step)

    # # add harmonic step --------------------------------------------------------
    loads = [structure.loads[lk].name for lk in structure.loads]
    step = HarmonicStep(name=structure.name + '_harmonic',
                        displacements=[list(structure.displacements.keys())[0]],
                        loads=loads,
                        freq_list=freq_list,
                        damping=damping)
    structure.add(step)
    structure.steps_order = [structure.name + '_harmonic']

    # analyse and extraxt results ----------------------------------------------
    write_command_file_harmonic_super(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)
    extract_data(structure, fields, 'harmonic_s')
    return structure


def ansys_harmonic_field(structure, num_modes, freq_list, fields='all', damping=0.02):

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=structure.name + '_modal', 
                     displacements=[list(structure.displacements.keys())[0]],
                     modes=num_modes)
    structure.add(step)

    # structure.steps_order = []
    field = structure.loads[list(structure.loads.keys())[0]].fields
    for i, fk in enumerate(field):
        # add harmonic step --------------------------------------------------------
        loads = [structure.loads[lk].name for lk in structure.loads]
        step = HarmonicFieldStep(name='{}_f_{}'.format(structure.name, fk),
                                 freq_list=[fk],
                                 index=i,
                                 displacements=[list(structure.displacements.keys())[0]],
                                 loads=loads,
                                 damping=damping)
        structure.add(step)
        # structure.steps_order.append('{}_f_{}'.format(structure.name, fk))

    # # analyse and extraxt results ----------------------------------------------
    write_command_file_harmonic_field(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)
    extract_data(structure, fields, 'harmonic_field')
    return structure


def extract_data(structure, fields, results_type):
    path = structure.path
    name = structure.name
    out_path = os.path.join(path, name + '_output')

    if results_type == 'modal' or results_type == 'harmonic_s':
        mfreq = read_modal_freq(out_path)
        rdict = {fk: Result(mfreq[fk], name='VibroResult_{}'.format(fk), type='modal') for fk in mfreq}
        structure.results.update({'modal':rdict})

        pfact = read_participation_factor(out_path)
        for fk in pfact:
            structure.results['modal'][fk].pfact = pfact[fk]


        efmass = read_effective_mass(out_path)
        for fk in efmass:
            structure.results['modal'][fk].efmass   = efmass[fk]
            for ok in efmass[fk]:
                structure.results['modal'][fk].efmass_r[ok] = efmass[fk][ok] / structure.mass


        if 'u' in fields or 'all' in fields:
            for fk in mfreq:
                d = read_modal_displacements(out_path, fk)
                structure.results['modal'][fk].displacements = d
    
    if results_type == 'harmonic' or results_type == 'harmonic_s':
        # if results_type == 'harmonic':
        freq_list = structure.step['harmonic'].freq_list 
        # elif results_type == 'harmonic_field':
        #     skeys = structure.step['harmonic_field'].keys()
        #     freq_list = [structure.step['harmonic_field'][k].freq_list[0] for k in skeys]
        fdict = {i:freq_list[i] for i in range(len(freq_list))}
        rdict = {fk: Result(fdict[fk], name='VibroResult_{}'.format(fk), type='harmonic') for fk in fdict}
        structure.results.update({'harmonic':rdict})

        if 'u' in fields or 'all' in fields:
            # this is still not great, frequencies are from structure, not files...
            hd = read_harmonic_displacements(structure, out_path, freq_list)
            # structure.tomas = hd
            for fkey in hd:
                structure.results['harmonic'][fkey].displacements = hd[fkey]

    if results_type == 'harmonic_field':
        skeys = structure.step['harmonic_field'].keys()
        freq_list = [structure.step['harmonic_field'][k].freq_list[0] for k in skeys]
        fdict = {i:f for i, f in enumerate(freq_list)}
        rdict = {fk: Result(fdict[fk], name='VibroResult_{}'.format(fk), type='harmonic_field') for fk in fdict}
        structure.results.update({'harmonic_field':rdict})

        if 'u' in fields or 'all' in fields:
            # this is still not great, frequencies are from structure, not files...
            hd = read_harmonic_displacements_field(structure, out_path, freq_list)
            # structure.tomas = hd
            for fkey in hd:
                structure.results['harmonic_field'][fkey].displacements = hd[fkey]
    
    if results_type == 'harmonic_s':
        ncd = read_modal_coordinates(structure, out_path)
        for k in ncd:
            structure.results['harmonic'][k].modal_coordinates = ncd[k]

    if results_type =='static':
        result = Result('static', name='VibroResult', type='static')
        structure.results['static'] = {0: result}
        if 'u' in fields or 'all' in fields:
            ud = read_static_displacements(out_path)
            structure.results['static'][0].displacements = ud
        if 's' in fields or 'all' in fields:
            sd = read_static_stresses(out_path)
            structure.results['static'][0].stresses = sd
        if 'sp' in fields or 'all' in fields:
            spd = read_principal_stresses(out_path)
            structure.results['static'][0].principal_stresses = spd
        if 'ss' in fields or 'all' in fields:
            ssd = read_shear_stresses(out_path)
            structure.results['static'][0].shear_stresses = ssd
        if 'rf' in fields or 'all' in fields:
            rfd = read_reactions(out_path)
            structure.results['static'][0].reactions = rfd
    return structure


def ansys_launch_process(structure, cpus=2, license='introductory', delete=True):
    """ Launches an analysis using Ansys.

    Parameters:
        path (str): Path to the Ansys input file.
        name (str): Name of the structure.
        cpus (int): Number of CPU cores to use.
        license (str): Type of Ansys license.
        delete (Bool): Path to the Ansys input file.

    Returns:
        None
    """
    path = structure.path
    name = structure.name

    if not os.path.exists(os.path.join(path, name + '_output')):
        os.makedirs(os.path.join(path, name + '_output'))
    elif delete:
        delete_result_files(path, name)

    ansys_path = 'MAPDL.exe'
    inp_path = os.path.join(path, name + '.txt')
    work_dir = os.path.join(path, name + '_output')

    create_results_folders(structure, work_dir)

    out_path = os.path.join(work_dir, name + '.out')

    if license == 'research':
        lic_str = 'aa_r'
    elif license == 'teaching':
        lic_str = 'aa_t_a'
    elif license == 'introductory':
        lic_str = 'aa_t_i'
    else:
        lic_str = 'aa_t_i'  # temporary default.

    launch_string = '\"' + ansys_path + '\" -g -p ' + lic_str + ' -np ' + str(cpus)
    launch_string += ' -dir \"' + work_dir
    launch_string += '\" -j \"' + name + '\" -s read -l en-us -b -i \"'
    launch_string += inp_path + ' \" -o \"' + out_path + '\"'
    # print(launch_string)
    subprocess.call(launch_string)


def delete_result_files(path, name):
    """ Deletes Ansys result files.

    Parameters:
        path (str): Path to the Ansys input file.
        name (str): Name of the structure.

    Returns:
        None
    """
    out_path = os.path.join(path, name + '_output')
    shutil.rmtree(out_path, ignore_errors=True)


def create_results_folders(structure, work_dir):
    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
    if 'harmonic_field' in structure.step:
        skeys = structure.step['harmonic_field'].keys()
        for skey in skeys:
            out_path = os.path.join(work_dir, 'freq_{}'.format(skey))
            if not os.path.exists(out_path):
                os.makedirs(out_path)


if __name__ == '__main__':
    pass