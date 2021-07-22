from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from .ansys_nodes import write_constraints
from .ansys_nodes import write_nodes
from .ansys_elements import write_elements, write_surface_elements
from .ansys_materials import write_materials
from .ansys_process import write_preprocess
from .ansys_loads import write_fields_loads
from .ansys_modal import write_modal_results

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['write_command_file_harmonic_field']


def write_command_file_harmonic_field(structure, fields):
    path = structure.path
    filename = structure.name + '.txt'

    write_preprocess(path, filename)
    write_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    write_surface_elements(structure, path, filename, structure.radiating_faces())
    write_modalsuper_solve(structure, path, filename)
    write_constraints(structure, 'modal', path, filename)
    write_super_solve_step(structure, path, filename)

    steps = sorted(structure.step['harmonic_field'])
    for sk in steps:
        write_harmonic_field_solve(structure, path, filename, sk)
        write_fields_loads(structure, sk, path, filename)
        write_super_solve_step(structure, path, filename)
        write_harmonic_field_results(structure, sk, fields, path, filename)
    write_modal_results(structure, fields, path, filename)


def write_modalsuper_solve(structure, path, filename):
    num_modes = structure.step['modal'].modes
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('FINISH\n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('ANTYPE,MODAL \n')

    cFile.write('MODOPT,LANB,' + str(num_modes) + ' \n')
    cFile.write('EQSLV,SPAR \n')
    cFile.write('MXPAND,' + str(num_modes) + ', , ,1 \n')
    # cFile.write('LUMPM,0 \n')
    # cFile.write('PSTRES,0 \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_super_solve_step(structure, path, filename):
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('SAVE\n')
    cFile.write('SOLVE\n')
    cFile.write('FINISH\n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_harmonic_field_solve(structure, path, filename, index):

    freq_list = structure.step['harmonic_field'][index].freq_list
    damping = structure.step['harmonic_field'][index].damping
    # out_path = os.path.join(path, structure.name + '_output')

    n = 10
    freq_list_ = [freq_list[i:i + n] for i in range(0, len(freq_list), n)]

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('FINISH \n')
    cFile.write('/SOLU \n')

    # cFile.write('ANTYPE,HARMIC                ! Harmonic analysis \n')
    # cFile.write('HROPT,MSUP,,,YES,,YES        ! Mode-superposition method; number of modes to use \n')
    # cFile.write('HROUT,,,,,                   ! Harmonic analysis output options; cluster option\n')

    cFile.write('ANTYPE,3            ! Harmonic analysis \n')


    cFile.write('*dim, freq_list{0}, array, {1} \n'.format(index, len(freq_list)))
    for i, freq in enumerate(freq_list_):
        cFile.write('freq_list{0}('.format(index) + str(i * n + 1) + ') = ' + ', '.join([str(f) for f in freq]) + '\n')
    cFile.write('HARFRQ, , , , , %freq_list{0}%, , ! Frequency range / list \n'.format(index))
    cFile.write('KBC,1                ! Stepped loads \n')

    if damping:
        # cFile.write('ALPHAD,'+ str(damping)+'   ! mass matrix multiplier for damping \n')
        # cFile.write('BETAD,' + str(damping) + '   ! stiffness matrix multiplier for damping \n')
        cFile.write('DMPRAT,' + str(damping) + '   ! constant modal damping ratio \n')

    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_harmonic_field_results(structure, index, fields, path, filename):

    if type(fields) == str:
        fields = [fields]
    if 'u' in fields or 'all' in fields:
        write_freq_displacements_field(structure, index, path, filename)


def write_freq_displacements_field(structure, index, path, filename):
    
    freq_list = structure.step['harmonic_field'][index].freq_list
    out_path = os.path.join(path, '{}_output'.format(structure.name), 'freq_{}'.format(index))

    cFile = open(os.path.join(path, filename), 'a')

    cFile.write('/POST1 \n')
    cFile.write('SET, 0, \n')
    cFile.write('*get,num_n,NODE,0,COUNT ! get number of nodes \n')
    cFile.write('*get,n_min,NODE,0,NUM,MIN ! get min node number \n')

    cFile.write('/POST26 \n')
    # cFile.write('FILE,,RFRQ \n')  # this should be back for modal super
    cFile.write('PRCPLX, 0 \n')
    cFile.write('!\n')
    cFile.write('!\n')

    cFile.write('*do,i,1,num_n,1   ! output to ascii by looping over nodes \n')
    cFile.write('curr_n=n_min \n')
    cFile.write('nsol,2,curr_n,u,x ! output UX \n')
    cFile.write('nsol,3,curr_n,u,y ! output UY \n')
    cFile.write('nsol,4,curr_n,u,z ! output UZ \n')

    cFile.write('*dim,N%curr_n%_output_{0},array, {1},7 \n'.format(index, len(freq_list)))

    cFile.write('vget,N%curr_n%_output_{0}(1,1),1 ! put time in array \n'.format(index))
    cFile.write('vget,N%curr_n%_output_{0}(1,2),2,,0 ! put UX in array \n'.format(index))
    cFile.write('vget,N%curr_n%_output_{0}(1,3),3,,0 ! put UY in array \n'.format(index))
    cFile.write('vget,N%curr_n%_output_{0}(1,4),4,,0 ! put UZ in array \n'.format(index))

    cFile.write('vget,N%curr_n%_output_{0}(1,5),2,,1 ! put UX in array \n'.format(index))
    cFile.write('vget,N%curr_n%_output_{0}(1,6),3,,1 ! put UY in array \n'.format(index))
    cFile.write('vget,N%curr_n%_output_{0}(1,7),4,,1 ! put UZ in array \n'.format(index))

    cFile.write('*cfopen,' + out_path + '\\node_real_%curr_n%,txt \n')
    cFile.write('*vwrite,N%curr_n%_output_{0}(1,1),\',\' ,N%curr_n%_output_{0}(1,2),\',\' ,'.format(index))
    cFile.write('N%curr_n%_output_{0}(1,3),\',\' ,N%curr_n%_output_{0}(1,4) \n'.format(index))
    cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
    cFile.write('*cfclose\n')

    cFile.write('*cfopen,' + out_path + '/node_imag_%curr_n%,txt \n')
    cFile.write('*vwrite,N%curr_n%_output_{0}(1,1),\',\' ,N%curr_n%_output_{0}(1,5),\',\' '.format(index))
    cFile.write(' ,N%curr_n%_output_{0}(1,6),\',\' ,N%curr_n%_output_{0}(1,7)\n'.format(index))
    cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
    cFile.write('*cfclose\n')

    cFile.write('*get,n_min,NODE,curr_n,NXTH \n')
    cFile.write('*enddo \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()

