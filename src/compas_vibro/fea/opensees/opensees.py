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
from compas_vibro.structure.step import StaticStep

from compas_vibro.fea.opensees import write_command_file_modal
from compas_vibro.fea.opensees import write_command_file_harmonic
from compas_vibro.fea.opensees import write_command_file_static

from compas_vibro.fea.opensees.read import read_modal_displacements
from compas_vibro.fea.opensees.read import read_modal_frequencies
from compas_vibro.fea.opensees.read import read_harmonic_displacements
from compas_vibro.fea.opensees.read import read_static_displacements
from compas_vibro.fea.opensees.read import read_modal_masses


from compas_vibro.structure.result import Result


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['opensees_modal',
           'opensees_harmonic']


def opensees_modal(structure, fields, num_modes, license='introductory'):

    # add modal step -----------------------------------------------------------
    step = ModalStep(name=structure.name + '_modal', 
                     displacements=[list(structure.displacements.keys())[0]],
                     modes=num_modes)
    structure.add(step)

    # analyse and extraxt results ----------------------------------------------
    write_command_file_modal(structure, fields)
    opensess_launch_process(structure)
    extract_data(structure, fields, 'modal')
    return structure


def opensees_static(structure, fields, license='introductory'):
    # TODO: opensees

    # add modal step -----------------------------------------------------------
    step = StaticStep(name=structure.name + '_static', 
                     displacements=[list(structure.displacements.keys())[0]],
                     loads=None)
    structure.add(step)

    # analyse and extraxt results ----------------------------------------------
    write_command_file_static(structure, fields)
    opensess_launch_process(structure)
    extract_data(structure, fields, 'static')
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
    write_command_file_harmonic(structure, fields)
    opensess_launch_process(structure)
    extract_data(structure, fields, 'harmonic')
    return structure


def extract_data(structure, fields, results_type):
    path = structure.path
    name = structure.name
    out_path = os.path.join(path, name + '_output')
    num_modes = structure.step['modal'].modes

    if results_type == 'modal':
        mfreq = read_modal_frequencies(out_path)
        rdict = {fk: Result(mfreq[fk], name='VibroResult_{}'.format(fk), type='modal') for fk in mfreq}
        structure.results.update({'modal':rdict})

        if 'u' in fields or 'all' in fields:
            for fk in mfreq:
                d = read_modal_displacements(out_path, fk)
                structure.results['modal'][fk].displacements = d
        if 'm' in fields or 'all' in fields:
            mod_mass, mod_mass_r = read_modal_masses(out_path, num_modes)
            for fk in mfreq:
                structure.results['modal'][fk].efmass = mod_mass[fk]
                structure.results['modal'][fk].efmass_r = mod_mass_r[fk]

    elif results_type == 'harmonic':
        # freq_list = structure.step.freq_list
        # fdict = {i:freq_list[i] for i in range(len(freq_list))}
        # rdict = {fk: Result(fdict[fk], name='VibroResult_{}'.format(fk), type='harmonic') for fk in fdict}
        # structure.results.update({'harmonic':rdict})

        if 'u' in fields or 'all' in fields:
            # this is still not great, frequencies are from structure, not files...
            hd = read_harmonic_displacements(out_path)
            rdict = {fk: Result(fk, name='VibroResult_{}'.format(fk), type='harmonic') for fk in hd}
            structure.results.update({'harmonic':rdict})
            for fkey in hd:
                structure.results['harmonic'][fkey].displacements = hd[fkey]
    
    elif results_type == 'static':
        if 'u' in fields or 'all' in fields:
            structure.results['static'] = {}
            sd = read_static_displacements(out_path)
            structure.results['static'][0]  = Result('static', name='VibroResult'.format(0), type='static')
            structure.results['static'][0].displacements = sd

    return structure


def opensess_launch_process(structure, exe=None, output=True, delete=True):

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
    temp = '{0}/{1}_output/'.format(path, name)
    
    if delete:
        try:
            delete_result_files(path, name)
        except:
            pass
    try:
        os.stat(temp)

    except:
        os.mkdir(temp)

    tic = time()

    if not exe:
        # exe = '/Applications/OpenSees3.2.1/OpenSees'
        exe = 'opensees'

    path_ = os.path.join(path, '{}.tcl'.format(name))
    command = '{0} {1}'.format(exe, path_)

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