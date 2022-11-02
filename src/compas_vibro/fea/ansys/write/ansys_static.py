
# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)

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


def write_command_file_static(structure, fields):
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
    write_static_results(structure, fields, filename)


def write_static_solve(structure, path, filename, is_pstress):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('! \n')
    fh.write('/SOLU ! \n')
    fh.write('ERESX, NO \n')  # this copies IP results to nodes
    fh.write('ANTYPE,0\n')
    if is_pstress:
        fh.write('PSTRES,1 \n')
        fh.write('rescontrol,,all,1  ! Get restart files for all substeps\n')
    fh.write('!\n')
    if structure.step['static'].nlgeom:
        fh.write('NLGEOM,ON\n')  # add automatic time steps and max substeps/increments
        fh.write('NSUBST,20,1000,1\n')
        fh.write('AUTOTS,1\n')
        fh.write('!\n')
    fh.close()


def write_static_results(structure, fields, filename, step_index=0):

    if type(fields) == str:
        fields = [fields]

    if 'u' in fields or 'all' in fields:
        write_request_node_displacements(structure, filename)
        
    # if 'sf' in fields or 'all' in fields:
    #     write_request_element_forces(structure, step_index)  # not there yet

    if 's' in fields or 'all' in fields:
        write_request_nodal_stresses(structure, filename)  # not there yet
        # write_request_element_stresses(structure, step_index)

    if 'rf' in fields or 'all' in fields:
        write_request_reactions(structure, filename)

    if 'sp' in fields or 'all' in fields:
        write_request_pricipal_stresses(structure, filename)

    # if 'e' in fields or 'all' in fields:
    #     write_request_principal_strains(structure, step_index)

    if 'ss' in fields or 'all' in fields:
        write_request_shear_stresses(structure, filename)
    else:
        pass


def write_request_node_displacements(structure, filename):

    name = structure.name
    path = structure.path
    step_name = 'static'

    out_path = os.path.join(path, name + '_output')

    fname = str(step_name) + '_' + 'displacements'
    name_ = 'nds_d'
    name_x = 'dispX'
    name_y = 'dispY'
    name_z = 'dispZ'

    fh = open(os.path.join(path, filename), 'a')
    fh.write('/POST1 \n')
    fh.write('!\n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,' + name_x + ', \n')
    fh.write('*dim,' + name_x + ',array,numNodes,1 \n')
    fh.write('*set,' + name_y + ', \n')
    fh.write('*dim,' + name_y + ',array,numNodes,1 \n')
    fh.write('*set,' + name_z + ', \n')
    fh.write('*dim,' + name_z + ',array,numNodes,1 \n')
    fh.write('*dim,' + name_ + ', ,numNodes \n')
    fh.write('*VGET, ' + name_x + ', node, all, u, X,,,2 \n')
    fh.write('*VGET, ' + name_y + ', node, all, u, Y,,,2 \n')
    fh.write('*VGET, ' + name_z + ', node, all, u, Z,,,2 \n')
    fh.write('*vfill,' + name_ + '(1),ramp,1,1 \n')
    fh.write('*cfopen,' + out_path + '/' + fname + ',txt \n')
    fh.write('*vwrite, ' + name_ + '(1) , \',\'  , ' + name_x + '(1) , \',\' , ')
    fh.write(name_y + '(1) , \',\' ,' + name_z + '(1) \n')
    fh.write('(          F9.0,       A,       ES,           A,          ES,          A,      ES) \n')
    fh.write('*cfclose \n')
    fh.write('!\n')
    fh.write('!\n')
    fh.close()


def write_request_nodal_stresses(structure, filename):

    name = structure.name
    path = structure.path
    step_name = 'static'

    out_path = os.path.join(path, name + '_output')

    fname = str(step_name) + '_' + 'nodal_stresses'
    name = 'nds_s'

    # fh = open(os.path.join(path, filename), 'a')
    fh = open(os.path.join(path, filename), 'a')
    fh.write('SET, LAST \n')
    fh.write('SHELL,TOP  \n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,SXtop, \n')
    fh.write('*dim,SXtop,array,numNodes,1 \n')
    fh.write('*set,SYtop, \n')
    fh.write('*dim,SYtop,array,numNodes,1 \n')
    fh.write('*set,SZtop, \n')
    fh.write('*dim,SZtop,array,numNodes,1 \n')
    fh.write('*dim,' + name + ', ,numNodes \n')
    fh.write('*VGET, SXtop, node, all, S, X,,,2 \n')
    fh.write('*VGET, SYtop, node, all, S, Y,,,2 \n')
    fh.write('*VGET, SZtop, node, all, S, Z,,,2 \n')

    fh.write('SHELL,BOT  \n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,SXbot, \n')
    fh.write('*dim,SXbot,array,numNodes,1 \n')
    fh.write('*set,SYbot, \n')
    fh.write('*dim,SYbot,array,numNodes,1 \n')
    fh.write('*set,SZbot, \n')
    fh.write('*dim,SZbot,array,numNodes,1 \n')
    # fh.write('*dim,nds, ,numNodes \n')
    fh.write('*VGET, SXbot, node, all, S, X,,,2 \n')
    fh.write('*VGET, SYbot, node, all, S, Y,,,2 \n')
    fh.write('*VGET, SZbot, node, all, S, Z,,,2 \n')

    fh.write('*vfill,' + name + '(1),ramp,1,1 \n')
    fh.write('*cfopen,' + out_path + '/' + fname + ',txt \n')
    fh.write('*vwrite, ' + name + '(1) , \',\'  , SXtop(1) ,   \',\' ,   SYtop(1) ')
    fh.write(',   \',\' ,  SZtop(1) , \',\',    SXbot(1) ,   \',\' ,   SYbot(1) ,   \',\' ,  SZbot(1) \n')
    fh.write('(F9.0, A, ES, A, ES, A, ES, A, ES, A, ES, A, ES) \n')
    fh.write('*cfclose \n')
    fh.write('!\n')
    fh.write('!\n')
    fh.close()


def write_request_pricipal_stresses(structure, filename):

    name = structure.name
    path = structure.path
    step_name = 'static'

    out_path = os.path.join(path, name + '_output')

    fname = str(step_name) + '_' + 'principal_stresses'
    name = 'nds_p'
    fh = open(os.path.join(path, filename), 'a')
    fh.write('SET, LAST \n')
    fh.write('SHELL,TOP  \n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,S1top, \n')
    fh.write('*dim,S1top,array,numNodes,1 \n')
    fh.write('*set,S2top, \n')
    fh.write('*dim,S2top,array,numNodes,1 \n')
    fh.write('*set,S3top, \n')
    fh.write('*dim,S3top,array,numNodes,1 \n')
    fh.write('*dim,' + name + ', ,numNodes \n')
    fh.write('*VGET, S1top, node, all, S, 1,,,2 \n')
    fh.write('*VGET, S2top, node, all, S, 2,,,2 \n')
    fh.write('*VGET, S3top, node, all, S, 3,,,2 \n')

    fh.write('SHELL,BOT  \n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,S1bot, \n')
    fh.write('*dim,S1bot,array,numNodes,1 \n')
    fh.write('*set,S2bot, \n')
    fh.write('*dim,S2bot,array,numNodes,1 \n')
    fh.write('*set,S3bot, \n')
    fh.write('*dim,S3bot,array,numNodes,1 \n')
    # fh.write('*dim,nds, ,numNodes \n')
    fh.write('*VGET, S1bot, node, all, S, 1,,,2 \n')
    fh.write('*VGET, S2bot, node, all, S, 2,,,2 \n')
    fh.write('*VGET, S3bot, node, all, S, 3,,,2 \n')

    fh.write('*vfill,' + name + '(1),ramp,1,1 \n')
    fh.write('*cfopen,' + out_path + '/' + fname + ',txt \n')
    fh.write('*vwrite, ' + name + '(1), \',\', S1top(1), \',\', S2top(1), \',\',')
    fh.write(' S3top(1), \',\', S1bot(1), \',\', S2bot(1), \',\', S3bot(1) \n')
    fh.write('(F9.0, A, ES, A, ES, A, ES, A, ES, A, ES, A, ES) \n')
    fh.write('*cfclose \n')
    fh.write('!\n')
    fh.write('!\n')
    fh.close()


def write_request_shear_stresses(structure, filename):

    name = structure.name
    path = structure.path
    step_name = 'static'

    out_path = os.path.join(path, name + '_output')

    fname = str(step_name) + '_' + 'shear_stresses'
    name = 'nds_sh'

    fh = open(os.path.join(path, filename), 'a')
    fh.write('SET, LAST  \n')
    fh.write('SHELL,TOP  \n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,S1top, \n')
    fh.write('*dim,S1top,array,numNodes,1 \n')
    fh.write('*set,S2top, \n')
    fh.write('*dim,S2top,array,numNodes,1 \n')
    fh.write('*set,S3top, \n')
    fh.write('*dim,S3top,array,numNodes,1 \n')
    fh.write('*dim,' + name + ', ,numNodes \n')
    fh.write('*VGET, S1top, node, all, S, XY,,,2 \n')
    fh.write('*VGET, S2top, node, all, S, YZ,,,2 \n')
    fh.write('*VGET, S3top, node, all, S, XZ,,,2 \n')

    fh.write('SHELL,BOT  \n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,S1bot, \n')
    fh.write('*dim,S1bot,array,numNodes,1 \n')
    fh.write('*set,S2bot, \n')
    fh.write('*dim,S2bot,array,numNodes,1 \n')
    fh.write('*set,S3bot, \n')
    fh.write('*dim,S3bot,array,numNodes,1 \n')
    # fh.write('*dim,nds, ,numNodes \n')
    fh.write('*VGET, S1bot, node, all, S, XY,,,2 \n')
    fh.write('*VGET, S2bot, node, all, S, YZ,,,2 \n')
    fh.write('*VGET, S3bot, node, all, S, XZ,,,2 \n')

    fh.write('*vfill,' + name + '(1),ramp,1,1 \n')
    fh.write('*cfopen,' + out_path + '/' + fname + ',txt \n')
    fh.write('*vwrite, ' + name + '(1), \',\', S1top(1), \',\', S2top(1), \',\',')
    fh.write(' S3top(1), \',\', S1bot(1), \',\', S2bot(1), \',\', S3bot(1) \n')
    fh.write('(F9.0, A, ES, A, ES, A, ES, A, ES , A, ES, A, ES) \n')
    fh.write('*cfclose \n')
    fh.write('!\n')
    fh.write('!\n')
    fh.close()


def write_request_reactions(structure, filename):

    name = structure.name
    path = structure.path
    step_name = 'static'

    out_path = os.path.join(path, name + '_output')

    fname = str(step_name) + '_' + 'reactions'
    name = 'nds_r'

    fh = open(os.path.join(path, filename), 'a')
    fh.write('SET, LAST \n')
    fh.write('*get,numNodes,node,,count \n')
    fh.write('*set,RFX, \n')
    fh.write('*dim,RFX,array,numNodes,1 \n')
    fh.write('*set,RFY, \n')
    fh.write('*dim,RFY,array,numNodes,1 \n')
    fh.write('*set,RFZ, \n')
    fh.write('*dim,RFZ,array,numNodes,1 \n')

    fh.write('*set,RMX, \n')
    fh.write('*dim,RMX,array,numNodes,1 \n')
    fh.write('*set,RMY, \n')
    fh.write('*dim,RMY,array,numNodes,1 \n')
    fh.write('*set,RMZ, \n')
    fh.write('*dim,RMZ,array,numNodes,1 \n')

    fh.write('*dim,' + name + ', ,numNodes \n')
    fh.write('*VGET, RFX, node, all, RF, FX,,,2 \n')
    fh.write('*VGET, RFY, node, all, RF, FY,,,2 \n')
    fh.write('*VGET, RFZ, node, all, RF, FZ,,,2 \n')
    fh.write('*VGET, RMX, node, all, RF, MX,,,2 \n')
    fh.write('*VGET, RMY, node, all, RF, MY,,,2 \n')
    fh.write('*VGET, RMZ, node, all, RF, MZ,,,2 \n')

    fh.write('*vfill,' + name + '(1),ramp,1,1 \n')
    fh.write('*cfopen,' + out_path + '/' + fname + ',txt \n')
    fh.write('*vwrite, ' + name + '(1), \',\', RFX(1), \',\', RFY(1), \',\', ')
    fh.write('RFZ(1), \',\', RMX(1), \',\', RMY(1), \',\', RMZ(1) \n')
    fh.write('(F9.0, A, ES, A, ES, A, ES, A, ES, A, ES, A, ES) \n')
    fh.write('*cfclose \n')
    fh.write('!\n')
    fh.write('!\n')
    fh.close()