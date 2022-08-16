
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
    write_prestress(structure, path, filename)
    write_static_solve(structure, path, filename)
    write_constraints(structure, 'static', path, filename)
    write_loads(structure, 'static', path, filename)
    write_loadstep(structure, path, filename)
    write_solve_step(structure, path, filename)
    write_static_results(structure, fields, filename)


def write_static_solve(structure, path, filename):
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('! \n')
    cFile.write('/SOLU ! \n')
    cFile.write('ERESX, NO \n')  # this copies IP results to nodes
    cFile.write('ANTYPE,0\n')
    pstress = '1'
    cFile.write('PSTRES,{} \n'.format(pstress))
    cFile.write('!\n')
    if structure.step['static'].nlgeom:
        cFile.write('NLGEOM,ON\n')  # add automatic time steps and max substeps/increments
        cFile.write('NSUBST,20,1000,1\n')
        cFile.write('AUTOTS,1\n')
        cFile.write('!\n')
    cFile.close()


def write_static_results(structure, fields, filename, step_index=0):

    if type(fields) == str:
        fields = [fields]
    if 'u' in fields or 'all' in fields:
        write_request_node_displacements(structure, step_index, filename)
    # if 'sf' in fields or 'all' in fields:
    #     write_request_element_forces(structure, step_index)  # not there yet
    # if 's' in fields or 'all' in fields:
    #     write_request_nodal_stresses(structure, step_index)  # not there yet
    #     write_request_element_stresses(structure, step_index)
    # if 'rf' in fields or 'all' in fields:
    #     write_request_reactions(structure, step_index)
    # if 'sp' in fields or 'all' in fields:
    #     write_request_pricipal_stresses(structure, step_index)
    # if 'e' in fields or 'all' in fields:
    #     write_request_principal_strains(structure, step_index)
    # if 'ss' in fields or 'all' in fields:
    #     write_request_shear_stresses(structure, step_index)
    else:
        pass


def write_request_node_displacements(structure, step_index, filename):

    name = structure.name
    path = structure.path
    step_name = 'static'

    out_path = os.path.join(path, name + '_output')

    fname = str(step_name) + '_' + 'displacements'
    name_ = 'nds_d'
    name_x = 'dispX'
    name_y = 'dispY'
    name_z = 'dispZ'

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
