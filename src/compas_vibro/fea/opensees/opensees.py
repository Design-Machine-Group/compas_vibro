from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import shutil

from time import time

from subprocess import Popen
from subprocess import PIPE

from compas_vibro.structure.step import ModalStep
from compas_vibro.structure.step import HarmonicStep

from compas_vibro.fea.opensees import write_command_file_modal


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['opensees_modal',
           'opensees_harmonic']


def opensees_modal(structure, fields, num_modes, license='introductory'):
    # TODO: opensees

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=structure.name + '_modal', 
                     displacements=[list(structure.displacements.keys())[0]],
                     modes=num_modes)
    structure.add(step)

    # analyse and extraxt results ----------------------------------------------
    write_command_file_modal(structure, fields)
    opensess_launch_process(structure)
    return structure


def opensees_harmonic(structure, freq_list, fields='all', damping=0.05):
    # TODO: opensees
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
    return structure


def extract_data(structure, fields, results_type):
    pass


# def opensees_launch_process(structure, cpus=2, license='introductory', delete=True):
def opensess_launch_process(structure, exe=None, output=True):

    """ Runs the analysis through OpenSees.

    Parameters
    ----------
    structure : obj
        Structure object.
    exe : str
        OpenSees exe path to bypass defaults.
    output : bool
        Print terminal output.

    Returns
    -------
    None

    """

    # try:

    name = structure.name
    path = structure.path
    temp = '{0}/{1}/'.format(path, name)

    try:
        os.stat(temp)
    except:
        os.mkdir(temp)

    tic = time()

    if not exe:
        exe = '/Applications/OpenSees3.2.1/OpenSees'

    command = '{0} {1}/{2}.tcl'.format(exe, path, name)
    p = Popen(command, stdout=PIPE, stderr=PIPE, cwd=temp, shell=True)

    print('Executing command ', command)

    while True:

        line = p.stdout.readline()
        if not line:
            break
        line = str(line.strip())

        if output:
            print(line)

    stdout, stderr = p.communicate()

    if output:
        print(stdout)
        print(stderr)

    toc = time() - tic

    print('\n***** OpenSees analysis time : {0} s *****'.format(toc))

    # except:

    #     print('\n***** OpenSees analysis failed')


def delete_result_files(path, name):
    """ Deletes opensees result files.

    Parameters:
        path (str): Path to the opensees input file.
        name (str): Name of the structure.

    Returns:
        None
    """
    out_path = os.path.join(path, name + '_output')
    shutil.rmtree(out_path)


if __name__ == '__main__':
    pass