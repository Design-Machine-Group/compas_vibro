import os

# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)



def write_nodes(structure, output_path, filename):
    cFile = open(os.path.join(output_path, filename), 'a')
    
    nodes = {}
    nodes.update(structure.nodes)

    for i in range(len(nodes)):
        node = nodes[i]
        string = 'N,' + str(i + 1) + ',' + str(node.x) + ',' + str(node.y) + ',' + str(node.z) + ',0,0,0 \n'
        cFile.write(string)
    cFile.write('!\n')
    cFile.write('!\n')
    # cFile.close()

    vnodes = structure.virtual_nodes
    for vnkey in vnodes:
        node = structure.nodes[vnkey]
        nkey = structure.virtual_nodes[vnkey]
        string = 'N,' + str(nkey + 1) + ',' + str(node.x) + ',' + str(node.y) + ',' + str(node.z) + ',0,0,0 \n'
        cFile.write(string)
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()

def write_constraints(structure, step_type, output_path, filename):

    displacements = structure.step[step_type].displacements
    # print(displacements)
    cFile = open(os.path.join(output_path, filename), 'a')

    cdict = {'x' : 'UX', 'y' : 'UY', 'z' : 'UZ', 'xx' : 'ROTX', 'yy' : 'ROTY', 'zz' : 'ROTZ'}

    if type(displacements) != list:
        displacements = [displacements]

    for dkey in displacements:
        # print(dkey)
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