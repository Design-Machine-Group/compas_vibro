import os

# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)



def write_nodes(structure, output_path, filename):
    cFile = open(os.path.join(output_path, filename), 'a')
    nodes = structure.nodes
    for i in range(len(nodes)):
        node = nodes[i]
        string = 'N,' + str(i + 1) + ',' + str(node.x) + ',' + str(node.y) + ',' + str(node.z) + ',0,0,0 \n'
        cFile.write(string)
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_request_node_displacements(structure, step_index, mode=None):

    name = structure.name
    path = structure.path
    step_name = structure.steps_order[step_index]

    out_path = os.path.join(path, name + '_output')
    filename = name + '_extract.txt'
    if mode:
        fname = 'modal_shape_' + str(mode)
        name_ = 'nds_d' + str(mode)
        name_x = 'dispX' + str(mode)
        name_y = 'dispY' + str(mode)
        name_z = 'dispZ' + str(mode)
        out_path = os.path.join(out_path, 'modal_out')
    else:
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

    # fh = open(os.path.join(path, filename), 'a')
    # fh.write('*get, nnodes, node,, count \n')
    # fh.write('*dim, u, array, nnodes, 5 \n')
    # fh.write('! \n')

    # fh.write('*do, i, 1, nnodes \n')
    # fh.write('u(i,1) = i                         !Collumn 1 is node number \n')
    # fh.write('*get, u(i,2), NODE, u(i,1), U, X   !Collumn 2 is Ux \n')
    # fh.write('*get, u(i,3), NODE, u(i,1), U, Y   !Collumn 3 is Uy \n')
    # fh.write('*get, u(i,4), NODE, u(i,1), U, Z   !Collumn 4 is Uz \n')
    # fh.write('*get, u(i,5), NODE, u(i,1), U, SUM !Collumn 5 is Um \n')
    # fh.write('*Enddo \n')
    # fh.write('! \n')

    # fh.write('*cfopen,' + out_path + '/' + fname + ',txt \n')
    # fh.write('*CFWRITE, node U, num, ux, uy, uz, uSUM \n')
    # fh.write('*do,i,1,nnodes \n')
    # fh.write('*CFWRITE, node U, u(i,1), u(i,2), u(i,3), u(i,4), u(i,5) \n')
    # fh.write('*Enddo \n')
    # fh.close()


def write_constraints(structure, output_path, filename):

    displacements = structure.step.displacements
    cFile = open(os.path.join(output_path, filename), 'a')

    cdict = {'x' : 'UX', 'y' : 'UY', 'z' : 'UZ', 'xx' : 'ROTX', 'yy' : 'ROTY', 'zz' : 'ROTZ'}

    if type(displacements) != list:
        displacements = [displacements]

    for dkey in displacements:
        components = structure.displacements[dkey].components
        nodes = structure.displacements[dkey].nodes
        if type(nodes) == str:
            nodes = structure.sets[nodes].selection
        for node in nodes:
            for com in components:
                if components[com] != None:
                    string = 'D, {0}, {1}, {2} \n'.format(str(node + 1), cdict[com], components[com])
                    cFile.write(string)

    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_nodes_as_keypoints(structure, output_path, filename):
    cFile = open(os.path.join(output_path, filename), 'a')
    nodes = structure.nodes
    for i in range(len(nodes)):
        node = nodes[i]
        string = 'K,' + str(i + 1) + ',' + str(node['x']) + ',' + str(node['y']) + ',' + str(node['z']) + '\n'
        cFile.write(string)
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()