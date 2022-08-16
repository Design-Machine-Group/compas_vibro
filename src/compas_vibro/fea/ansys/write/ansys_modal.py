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


__all__ = ['write_command_file_modal']


def write_command_file_modal(structure, fields, pstress='0'):
    path = structure.path
    filename = structure.name + '.txt'
    
    write_preprocess(path, filename)
    write_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    write_modal_solve(structure, path, filename, pstress=pstress)
    write_constraints(structure, 'modal', path, filename)
    write_loadstep(structure, path, filename)
    write_solve_step(structure, path, filename)
    write_modal_results(structure, fields, path, filename)


def write_modal_solve(structure, path, filename, pstress='0'):
    num_modes = structure.step['modal'].modes
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('ANTYPE,2 \n')

    cFile.write('MODOPT,LANB,' + str(num_modes) + ' \n')
    # cFile.write('MODOPT,SNODE,' + str(num_modes) + ' \n')
    cFile.write('EQSLV,SPAR \n')
    cFile.write('MXPAND,' + str(num_modes) + ', , ,1 \n')
    cFile.write('LUMPM,0 \n')
    cFile.write('PSTRES,{} \n'.format(pstress))
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
    num_modes = structure.step['modal'].modes
    out_path = os.path.join(path, name + '_output')

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('!\n')
    cFile.write('/POST1 \n')
    cFile.write('*set,n_freq, \n')
    cFile.write('*dim,n_freq,array,' + str(num_modes) + ', \n')

    cFile.write('*set,pfacx, \n')
    cFile.write('*dim,pfacx,array,' + str(num_modes) + ', \n')

    cFile.write('*set,pfacy, \n')
    cFile.write('*dim,pfacy,array,' + str(num_modes) + ', \n')

    cFile.write('*set,pfacz, \n')
    cFile.write('*dim,pfacz,array,' + str(num_modes) + ', \n')

    for i in range(num_modes):
        cFile.write('SET, 1,' + str(i + 1) + '\n')
        cFile.write('*GET,n_freq({}),ACTIVE, 0, SET, FREQ \n'.format(i + 1))

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


def write_participation_factor(structure, path, filename):
    path = structure.path
    name = structure.name
    num_modes = structure.step['modal'].modes
    out_path = os.path.join(path, name + '_output')

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('!\n')
    cFile.write('/POST1 \n')

    cFile.write('*set,pfacx, \n')
    cFile.write('*dim,pfacx,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacy, \n')
    cFile.write('*dim,pfacy,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacz, \n')
    cFile.write('*dim,pfacz,array,{}, \n'.format(num_modes))

    cFile.write('*set,pfacrx, \n')
    cFile.write('*dim,pfacrx,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacry, \n')
    cFile.write('*dim,pfacry,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacrz, \n')
    cFile.write('*dim,pfacrz,array,{}, \n'.format(num_modes))


    for i in range(num_modes):
        cFile.write('SET, 1,' + str(i + 1) + '\n')
        cFile.write('*GET,pfacx({0}),MODE, {0}, PFACT,, DIREC, X \n'.format(i + 1))
        cFile.write('*GET,pfacy({0}),MODE, {0}, PFACT,, DIREC, Y \n'.format(i + 1))
        cFile.write('*GET,pfacz({0}),MODE, {0}, PFACT,, DIREC, Z \n'.format(i + 1))
        cFile.write('*GET,pfacrx({0}),MODE, {0}, PFACT,, DIREC, ROTX \n'.format(i + 1))
        cFile.write('*GET,pfacry({0}),MODE, {0}, PFACT,, DIREC, ROTY \n'.format(i + 1))
        cFile.write('*GET,pfacrz({0}),MODE, {0}, PFACT,, DIREC, ROTZ \n'.format(i + 1))


    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('*dim,nds,,' + str(num_modes) + ',1 \n')
    cFile.write('*vfill,nds(1),ramp,1,1 \n')

    cFile.write('*cfopen,' + os.path.join(out_path, 'modal_pfact') + ',txt \n')
    cFile.write('*vwrite, nds(1) {0} pfacx(1) {0} pfacy(1) {0} pfacz(1) {0} pfacrx {0} pfacry {0} pfacrz \n'.format(',\',\','))
    cFile.write('(F8.0, A, ES, A, ES, A, ES, A, ES, A, ES, A, ES) \n')
    cFile.write('*cfclose \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_effective_mass(structure, path, filename):
    path = structure.path
    name = structure.name
    num_modes = structure.step['modal'].modes
    out_path = os.path.join(path, name + '_output')

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('!\n')
    cFile.write('/POST1 \n')

    cFile.write('*set,pfacx, \n')
    cFile.write('*dim,pfacx,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacy, \n')
    cFile.write('*dim,pfacy,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacz, \n')
    cFile.write('*dim,pfacz,array,{}, \n'.format(num_modes))

    cFile.write('*set,pfacrx, \n')
    cFile.write('*dim,pfacrx,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacry, \n')
    cFile.write('*dim,pfacry,array,{}, \n'.format(num_modes))
    cFile.write('*set,pfacrz, \n')
    cFile.write('*dim,pfacrz,array,{}, \n'.format(num_modes))


    for i in range(num_modes):
        cFile.write('SET, 1,' + str(i + 1) + '\n')
        cFile.write('*GET,pfacx({0}),MODE, {0}, EFFM,, DIREC, X \n'.format(i + 1))
        cFile.write('*GET,pfacy({0}),MODE, {0}, EFFM,, DIREC, Y \n'.format(i + 1))
        cFile.write('*GET,pfacz({0}),MODE, {0}, EFFM,, DIREC, Z \n'.format(i + 1))
        cFile.write('*GET,pfacrx({0}),MODE, {0}, EFFM,, DIREC, ROTX \n'.format(i + 1))
        cFile.write('*GET,pfacry({0}),MODE, {0}, EFFM,, DIREC, ROTY \n'.format(i + 1))
        cFile.write('*GET,pfacrz({0}),MODE, {0}, EFFM,, DIREC, ROTZ \n'.format(i + 1))


    cFile.write('/SOL \n')
    cFile.write('!\n')
    cFile.write('*dim,nds,,' + str(num_modes) + ',1 \n')
    cFile.write('*vfill,nds(1),ramp,1,1 \n')

    cFile.write('*cfopen,' + os.path.join(out_path, 'modal_efmass') + ',txt \n')
    cFile.write('*vwrite, nds(1) {0} pfacx(1) {0} pfacy(1) {0} pfacz(1) {0} pfacrx {0} pfacry {0} pfacrz \n'.format(',\',\','))
    cFile.write('(F8.0, A, ES, A, ES, A, ES, A, ES, A, ES, A, ES) \n')
    cFile.write('*cfclose \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_modal_shapes(structure, path, filename):
    num_modes = structure.step['modal'].modes

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
    write_participation_factor(structure, path, filename)
    write_effective_mass(structure, path, filename)

    if 'u' in fields or 'all' in fields:
        write_modal_shapes(structure, path, filename)
    # if 'geo' in fields:
    #     write_request_element_nodes(path, name)
    else:
        pass
