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

# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)

__all__ = ['write_command_file_modal']


def write_command_file_modal(structure, fields):
    path = structure.path
    filename = structure.name + '.txt'
    
    write_preprocess(path, filename)
    write_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    write_modal_solve(structure, path, filename)
    write_constraints(structure, path, filename)
    write_loadstep(structure, path, filename)
    write_solve_step(structure, path, filename)
    write_modal_results(structure, fields, path, filename)



def write_modal_solve(structure, path, filename):
    num_modes = structure.step.modes
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('ANTYPE,2 \n')

    cFile.write('MODOPT,LANB,' + str(num_modes) + ' \n')
    cFile.write('EQSLV,SPAR \n')
    cFile.write('MXPAND,' + str(num_modes) + ', , ,1 \n')
    cFile.write('LUMPM,0 \n')
    cFile.write('PSTRES,0 \n')
    cFile.write('!\n')
    cFile.write('!\n')

    # if structure.geom_nonlinearity is True:
    #     cFile.close()
    #     write_geom_nonlinearity(path, filename)
    #     cFile = open(path + "/" + filename, 'a')

    # cFile.write('SOLVE')
    # cFile.write('!\n')
    # cFile.write('!\n')
    cFile.close()


def write_modal_freq(structure, path, filename):
    path = structure.path
    name = structure.name
    num_modes = structure.step.modes
    out_path = os.path.join(path, name + '_output')

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('!\n')
    cFile.write('/POST1 \n')
    cFile.write('*set,n_freq, \n')
    cFile.write('*dim,n_freq,array,' + str(num_modes) + ', \n')

    for i in range(num_modes):
        cFile.write('SET, 1,' + str(i + 1) + '\n')
        cFile.write('*GET,n_freq(' + str(i + 1) + '),ACTIVE, 0, SET, FREQ \n')

    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('*dim,nds,,' + str(num_modes) + ',1 \n')
    cFile.write('*vfill,nds(1),ramp,1,1 \n')
    cFile.write('*cfopen,' + os.path.join(out_path, 'modal_freq') + ',txt \n')
    cFile.write('*vwrite, nds(1) , \',\'  , n_freq(1) \n')
    cFile.write('(F8.0, A, ES) \n')
    cFile.write('*cfclose \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_modal_shapes(structure, path, filename):
    num_modes = structure.step.modes

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/POST1 \n')
    cFile.close()
    for i in range(num_modes):
        cFile = open(os.path.join(path, filename), 'a')
        # cFile.write('SET,' + str(step_index + 1) + ' \n')
        cFile.write('SET, 1,' + str(i + 1) + '\n')
        cFile.write('! Mode ' + str(i + 1) + ' \n \n \n')
        cFile.close()
        write_modal_displacements(structure, i, filename)


def write_modal_displacements(structure, mode, filename):
    name = structure.name
    path = structure.path

    out_path = os.path.join(path, name + '_output')

    fname = 'modal_shape_' + str(mode)
    name_ = 'nds_d' + str(mode)
    name_x = 'dispX' + str(mode)
    name_y = 'dispY' + str(mode)
    name_z = 'dispZ' + str(mode)
    # out_path = os.path.join(out_path, 'modal_out')

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/POST1 \n')
    cFile.write('!\n')
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
    cFile.write('*cfopen,' + out_path + '/' + fname + ',txt \n')
    cFile.write('*vwrite, ' + name_ + '(1) , \',\'  , ' + name_x + '(1) , \',\' , ')
    cFile.write(name_y + '(1) , \',\' ,' + name_z + '(1) \n')
    cFile.write('(          F9.0,       A,       ES,           A,          ES,          A,      ES) \n')
    cFile.write('*cfclose \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()

def write_modal_results(structure, fields, path, filename):

    if type(fields) == str:
        fields = [fields]
    write_modal_freq(structure, path, filename)
    if 'u' in fields or 'all' in fields:
        write_modal_shapes(structure, path, filename)
    # if 'geo' in fields:
    #     write_request_element_nodes(path, name)
