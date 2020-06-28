from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

from .ansys_nodes import write_constraints
from .ansys_nodes import write_nodes

from .ansys_elements import write_elements

from .ansys_materials import write_materials

from .ansys_process import write_preprocess

from .ansys_steps import write_loadstep
from .ansys_steps import write_solve_step


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['write_command_file_harmonic']


def write_command_file_harmonic(structure, fields):
    path = structure.path
    filename = structure.name + '.txt'
    
    write_preprocess(path, filename)
    write_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    write_harmonic_solve(structure, path, filename)
    write_constraints(structure, path, filename)
    write_loadstep(structure, path, filename)
    write_solve_step(structure, path, filename)
    # write_harmonic_results(structure, fields, path, filename)


def write_harmonic_solve(structure, path, filename):

    freq_list = structure.step.freq_list
    damping = structure.step.damping
    # out_path = os.path.join(path, structure.name + '_output')
    sind = 0

    n = 10
    freq_list_ = [freq_list[i:i + n] for i in range(0, len(freq_list), n)]

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('FINISH \n')
    cFile.write('/SOLU \n')
    cFile.write('ANTYPE,3            ! Harmonic analysis \n')
    cFile.write('*dim, freq_list{0}, array, {1} \n'.format(sind, len(freq_list)))
    for i, freq in enumerate(freq_list_):
        cFile.write('freq_list{0}('.format(sind) + str(i * n + 1) + ') = ' + ', '.join([str(f) for f in freq]) + '\n')
    cFile.write('HARFRQ, , , , , %freq_list{0}%, , ! Frequency range / list \n'.format(sind))
    cFile.write('KBC,1                ! Stepped loads \n')

    if damping:
        # cFile.write('ALPHAD,'+ str(damping)+'   ! mass matrix multiplier for damping \n')
        # cFile.write('BETAD,' + str(damping) + '   ! stiffness matrix multiplier for damping \n')
        cFile.write('DMPRAT,' + str(damping) + '   ! constant modal damping ratio \n')

    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_harmonic_results_from_ansys_rst(name, path, fields, freq_list, step_index=0, step_name='step', sets=None):

    step_folder = 'harmonic_out'
    if not os.path.exists(os.path.join(path, name + '_output', step_folder)):
        os.makedirs(os.path.join(path, name + '_output', step_folder))

    # write_harmonic_post_process(path, name)

    if type(fields) == str:
        fields = [fields]
    if 'u' in fields or 'all' in fields:
        if len(freq_list) == 1:
            freq = freq_list[0]
            write_request_complex_displacements(path, name, freq, step_index)
        else:
            write_request_per_freq_nodal_displacements(path, name, freq_list, step_index, sets)
        # write_something(path, name)
    if 'geo' in fields or 'all' in fields:
        write_request_element_nodes(path, name)


def write_harmonic_post_process(path, name):
    filename = name + '_extract.txt'
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/POST26 \n')
    cFile.write('PRCPLX, 0 \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_request_per_freq_nodal_displacements(path, name, freq_list, step_index, sets=None):

    step_folder = 'harmonic_out'.format(step_index)
    filename = name + '_extract.txt'
    harmonic_outpath = os.path.join(path, name + '_output', step_folder)

    cFile = open(os.path.join(path, filename), 'a')

    if sets:
        cFile.write('/POST1 \n')
        cFile.write('SET, {}, \n'.format(step_index + 1))
        cFile.write('/POST26 \n')
        cFile.write('PRCPLX, 0 \n')
        cFile.write('!\n')
        cFile.write('!\n')

        for n in sets:
            cFile.write('curr_n=' + str(n + 1) + ' \n')
            cFile.write('nsol,2,curr_n,u,x ! output UX \n')
            cFile.write('nsol,3,curr_n,u,y ! output UY \n')
            cFile.write('nsol,4,curr_n,u,z ! output UZ \n')

            cFile.write('*dim,N%curr_n%_output,array,' + str(len(freq_list)) + ',7 \n')

            cFile.write('vget,N%curr_n%_output(1,1),1 ! put time in array \n')
            cFile.write('vget,N%curr_n%_output(1,2),2,,0 ! put UX in array \n')
            cFile.write('vget,N%curr_n%_output(1,3),3,,0 ! put UY in array \n')
            cFile.write('vget,N%curr_n%_output(1,4),4,,0 ! put UZ in array \n')

            cFile.write('vget,N%curr_n%_output(1,5),2,,1 ! put UX in array \n')
            cFile.write('vget,N%curr_n%_output(1,6),3,,1 ! put UY in array \n')
            cFile.write('vget,N%curr_n%_output(1,7),4,,1 ! put UZ in array \n')

            cFile.write('*cfopen,' + harmonic_outpath + '/node_real_%curr_n%,txt \n')
            cFile.write('*vwrite,N%curr_n%_output(1,1),\',\' ,N%curr_n%_output(1,2),\',\' ,')
            cFile.write('N%curr_n%_output(1,3),\',\' ,N%curr_n%_output(1,4) \n')
            cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
            cFile.write('*cfclose\n')

            cFile.write('*cfopen,' + harmonic_outpath + '/node_imag_%curr_n%,txt \n')
            cFile.write('*vwrite,N%curr_n%_output(1,1),\',\' ,N%curr_n%_output(1,5),\',\' ')
            cFile.write(' ,N%curr_n%_output(1,6),\',\' ,N%curr_n%_output(1,7)\n')
            cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
            cFile.write('*cfclose\n')
            cFile.write('!\n')
            cFile.write('!\n')
            cFile.write('!\n')
            cFile.write('!\n')

    else:
        cFile.write('/POST1 \n')
        cFile.write('SET, {}, \n'.format(step_index + 1))
        cFile.write('*get,num_n,NODE,0,COUNT ! get number of nodes \n')
        cFile.write('*get,n_min,NODE,0,NUM,MIN ! get min node number \n')

        cFile.write('/POST26 \n')
        cFile.write('PRCPLX, 0 \n')
        cFile.write('!\n')
        cFile.write('!\n')

        cFile.write('*do,i,1,num_n,1   ! output to ascii by looping over nodes \n')
        cFile.write('curr_n=n_min \n')
        cFile.write('nsol,2,curr_n,u,x ! output UX \n')
        cFile.write('nsol,3,curr_n,u,y ! output UY \n')
        cFile.write('nsol,4,curr_n,u,z ! output UZ \n')

        cFile.write('*dim,N%curr_n%_output,array,' + str(len(freq_list)) + ',7 \n')

        cFile.write('vget,N%curr_n%_output(1,1),1 ! put time in array \n')
        cFile.write('vget,N%curr_n%_output(1,2),2,,0 ! put UX in array \n')
        cFile.write('vget,N%curr_n%_output(1,3),3,,0 ! put UY in array \n')
        cFile.write('vget,N%curr_n%_output(1,4),4,,0 ! put UZ in array \n')

        cFile.write('vget,N%curr_n%_output(1,5),2,,1 ! put UX in array \n')
        cFile.write('vget,N%curr_n%_output(1,6),3,,1 ! put UY in array \n')
        cFile.write('vget,N%curr_n%_output(1,7),4,,1 ! put UZ in array \n')

        cFile.write('*cfopen,' + harmonic_outpath + '/node_real_%curr_n%,txt \n')
        cFile.write('*vwrite,N%curr_n%_output(1,1),\',\' ,N%curr_n%_output(1,2),\',\' ,')
        cFile.write('N%curr_n%_output(1,3),\',\' ,N%curr_n%_output(1,4) \n')
        cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
        cFile.write('*cfclose\n')

        cFile.write('*cfopen,' + harmonic_outpath + '/node_imag_%curr_n%,txt \n')
        cFile.write('*vwrite,N%curr_n%_output(1,1),\',\' ,N%curr_n%_output(1,5),\',\' ')
        cFile.write(' ,N%curr_n%_output(1,6),\',\' ,N%curr_n%_output(1,7)\n')
        cFile.write('(F8.0, A, E12.5, A, E12.5, A, E12.5, A, E12.5)  \n')
        cFile.write('*cfclose\n')

        cFile.write('*get,n_min,NODE,curr_n,NXTH \n')
        cFile.write('*enddo \n')
        cFile.write('!\n')
        cFile.write('!\n')
    cFile.close()


def write_request_complex_displacements(path, name, freq, step_index):

    step_folder = 'harmonic_out'.format(step_index)
    filename = name + '_extract.txt'
    harmonic_outpath = os.path.join(path, name + '_output', step_folder)

    fname_real = 'harmonic_disp_real_{0}_Hz'.format(freq)
    fname_imag = 'harmonic_disp_imag_{0}_Hz'.format(freq)
    name_ = 'nds_d' + str(freq)
    name_x = 'dispX' + str(freq)
    name_y = 'dispY' + str(freq)
    name_z = 'dispZ' + str(freq)

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/POST1 \n')
    cFile.write('!\n')
    cFile.write('SET, {0}, , , 0!\n'.format(step_index + 1))
    cFile.write('*get,numNodes,node,,count \n')
    cFile.write('*set,' + name_x + ', \n')
    cFile.write('*dim,' + name_x + ',array,numNodes,1 \n')
    cFile.write('*set,' + name_y + ', \n')
    cFile.write('*dim,' + name_y + ',array,numNodes,1 \n')
    cFile.write('*set,' + name_z + ', \n')
    cFile.write('*dim,' + name_z + ',array,numNodes,1 \n')
    cFile.write('*dim,' + name_ + ', ,numNodes \n')
    cFile.write('*VGET, ' + name_x + ', node, all, u, X,,,2 \n')
    cFile.write('*VGET, ' + name_y + ', node, all, u, Y,,,2 \n')
    cFile.write('*VGET, ' + name_z + ', node, all, u, Z,,,2 \n')
    cFile.write('*vfill,' + name_ + '(1),ramp,1,1 \n')
    cFile.write('*cfopen,' + harmonic_outpath + '/' + fname_real + ',txt \n')
    cFile.write('*vwrite, ' + name_ + '(1) , \',\'  , ' + name_x + '(1) , \',\' , ')
    cFile.write(name_y + '(1) , \',\' ,' + name_z + '(1) \n')
    cFile.write('(          F9.0,       A,       ES,           A,          ES,          A,      ES) \n')
    cFile.write('*cfclose \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/POST1 \n')
    cFile.write('!\n')
    cFile.write('SET, {0}, , , 1!\n'.format(step_index + 1))
    cFile.write('*get,numNodes,node,,count \n')
    cFile.write('*set,' + name_x + ', \n')
    cFile.write('*dim,' + name_x + ',array,numNodes,1 \n')
    cFile.write('*set,' + name_y + ', \n')
    cFile.write('*dim,' + name_y + ',array,numNodes,1 \n')
    cFile.write('*set,' + name_z + ', \n')
    cFile.write('*dim,' + name_z + ',array,numNodes,1 \n')
    cFile.write('*dim,' + name_ + ', ,numNodes \n')
    cFile.write('*VGET, ' + name_x + ', node, all, u, X,,,2 \n')
    cFile.write('*VGET, ' + name_y + ', node, all, u, Y,,,2 \n')
    cFile.write('*VGET, ' + name_z + ', node, all, u, Z,,,2 \n')
    cFile.write('*vfill,' + name_ + '(1),ramp,1,1 \n')
    cFile.write('*cfopen,' + harmonic_outpath + '/' + fname_imag + ',txt \n')
    cFile.write('*vwrite, ' + name_ + '(1) , \',\'  , ' + name_x + '(1) , \',\' , ')
    cFile.write(name_y + '(1) , \',\' ,' + name_z + '(1) \n')
    cFile.write('(          F9.0,       A,       ES,           A,          ES,          A,      ES) \n')
    cFile.write('*cfclose \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()
