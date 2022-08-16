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

from .ansys_loads import write_loads
from .ansys_loads import write_prestress

from .ansys_static import write_static_solve
from .ansys_static import write_static_results

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['write_command_file_modal',
           'write_command_file_modal_prestressed',
          ]


def write_command_file_modal(structure, fields):
    path = structure.path
    filename = structure.name + '.txt'
    
    write_preprocess(path, filename)
    write_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    write_modal_solve(structure, path, filename)
    write_constraints(structure, 'modal', path, filename)
    write_loadstep(structure, path, filename)
    write_solve_step(structure, path, filename)
    write_modal_results(structure, fields, path, filename)


def write_command_file_modal_prestressed(structure, fields):
    path = structure.path
    filename = structure.name + '.txt'
    
    write_preprocess(path, filename)
    write_materials(structure, path, filename)
    write_nodes(structure, path, filename)
    write_elements(structure, path, filename)
    is_pstress = write_prestress(structure, path, filename)
    write_static_solve(structure, path, filename,is_pstress)
    write_constraints(structure, 'static', path, filename)
    write_loads(structure, 'static', path, filename)
    write_loadstep(structure, path, filename)
    write_solve_step(structure, path, filename)
    # write_static_results(structure, fields, filename)

    write_linear_perturbation_modal(structure, path, filename)
    write_modal_results(structure, fields, path, filename, restart=True)


def write_modal_solve(structure, path, filename):
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
    cFile.write('PSTRES,0 \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_modal_freq(structure, path, filename, restart=False):
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

    if restart:
        cFile.write('file,,rstp  ! Use *.rstp file to review results from linear perturbation!\n')

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


def write_participation_factor(structure, path, filename, restart=False):
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

    if restart:
        cFile.write('file,,rstp  ! Use *.rstp file to review results from linear perturbation!\n')

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


def write_effective_mass(structure, path, filename, restart=False):
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

    if restart:
        cFile.write('file,,rstp  ! Use *.rstp file to review results from linear perturbation!\n')

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


def write_modal_shapes(structure, path, filename, restart=False):
    num_modes = structure.step['modal'].modes

    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/POST1 \n')
    if restart:
        cFile.write('file,,rstp  ! Use *.rstp file to review results from linear perturbation!\n')
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


def write_modal_results(structure, fields, path, filename, restart=False):

    if type(fields) == str:
        fields = [fields]
    write_modal_freq(structure, path, filename, restart=restart)
    write_participation_factor(structure, path, filename, restart=restart)
    write_effective_mass(structure, path, filename, restart=restart)

    if 'u' in fields or 'all' in fields:
        write_modal_shapes(structure, path, filename, restart=restart)
    # if 'geo' in fields:
    #     write_request_element_nodes(path, name)
    else:
        pass


def write_linear_perturbation_modal(structure, path, filename):
    num_modes = structure.step['modal'].modes
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('/prep7\n')
    # cFile.write('/finish!\n')
    cFile.write('/solu!\n')

    cFile.write('/com    FIRST PHASE OF LINEAR PERTURBATION!\n')
    
    cFile.write('antype,,restart,,,perturb  ! Restart \n')
    cFile.write('perturb, modal!\n')
    cFile.write('solve,elform     ! Execute 1st phase of linear perturbation, recovering Kt of NLGEOM,on!\n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.write('!\n')

    cFile.write('/com    SECOND PHASE OF LINEAR PERTURBATION!\n')

    

    cFile.write('MODOPT,LANB,' + str(num_modes) + ' \n')
    cFile.write('EQSLV,SPAR \n')                                # check is this should be there or not
    cFile.write('MXPAND,' + str(num_modes) + ', , ,1 \n')
    # cFile.write('LUMPM,0 \n')                                # check is this should be there or not
    # cFile.write('PSTRES,0 \n')                                # check is this should be there or not

    # cFile.write('outres,esol,all !\n')
    cFile.write('solve            ! Execute 2nd phase of linear perturbation: modal analysis!\n')

    cFile.write('fini!\n')
    cFile.write('!\n')
    cFile.write('/post1!\n')
    # cFile.write('file,,rstp  ! Use *.rstp file to review results from linear perturbation!\n')
    # cFile.write('set,list    ! It should list 3 eigen-modes!\n')
    # cFile.write('set,last    ! List stresses of the 3rd mode!\n')
    # cFile.write('esel,s,elem,,1!\n')
    # cFile.write('etable,seqv,s,eqv!\n')
    # cFile.write('allsel,all!\n')
    # cFile.write('etable,seqv,s,eqv!\n')
    # cFile.write('pretab,seqv!\n')
    # cFile.write('finish!\n')
    cFile.close()