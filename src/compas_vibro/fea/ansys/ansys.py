from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil
import subprocess

from compas_vibro.structure.result import Result

from compas_vibro.structure.step import ModalStep
from compas_vibro.structure.step import HarmonicStep

from compas_vibro.fea.ansys.write import write_command_file_modal
from compas_vibro.fea.ansys.write import write_command_file_harmonic

from compas_vibro.fea.ansys.read import read_modal_freq
from compas_vibro.fea.ansys.read import read_modal_displacements

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['modal_from_structure',
           'harmonic_from_structure']


def modal_from_structure(structure, fields, num_modes, license='introductory'):

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=structure.name + '_modal', 
                     displacements=[list(structure.displacements.keys())[0]],
                     modes=num_modes)
    structure.add(step)

    # analyse and extraxt results ----------------------------------------------
    write_command_file_modal(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)
    extract_data(structure, fields, 'modal')
    return structure


def extract_data(structure, fields, results_type):
    path = structure.path
    name = structure.name
    out_path = os.path.join(path, name + '_output')

    if results_type == 'modal':
        mfreq = read_modal_freq(out_path)
        rdict = {fk: Result(mfreq[fk], name='VibroResult_{}'.format(fk), type='modal') for fk in mfreq}
        structure.results = {'modal':rdict}

        if 'u' in fields or 'all' in fields:
            for fk in mfreq:
                structure.results['modal'][fk].displacements = read_modal_displacements(out_path, fk)
    return structure


def harmonic_from_structure(structure, freq_list, fields='all', damping=0.05):

    # add harmonic step --------------------------------------------------------
    loads = [structure.loads[lk].name for lk in structure.loads]
    step = HarmonicStep(name=structure.name + '_harmonic',
                        displacements=[list(structure.displacements.keys())[0]],
                        loads=loads,
                        freq_list=freq_list,
                        damping=damping)
    structure.add(step)
    structure.steps_order = [structure.name + '_harmonic']

    # analyse and extraxt results ----------------------------------------------
    write_command_file_harmonic(structure, fields)
    ansys_launch_process(structure, cpus=4, license=license, delete=True)

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

    if not os.path.exists(work_dir):
        os.makedirs(work_dir)
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
    shutil.rmtree(out_path)

if __name__ == '__main__':
    pass