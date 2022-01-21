from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_vibro.structure.node import Node

from compas.utilities import geometric_key

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'



__all__ = [
    'NodeMixins',
]


class NodeMixins(object):

    def add_node(self, xyz, virtual=False):

        """ Adds a node to structure.nodes at co-ordinates xyz.

        Parameters
        ----------
        xyz : list
            [x, y, z] co-ordinates of the node.

        Returns
        -------
        int
            Key of the added or pre-existing node.

        Notes
        -----
        - Nodes are numbered sequentially starting from 0.

        """

        xyz = [float(i) for i in xyz]
        key = self.check_node_exists(xyz)

        if key is None:
            key = self.node_count()
            self.nodes[key] = Node(key=key, xyz=xyz)
            self.add_node_to_node_index(key, xyz, virtual=virtual)
        return key

    def add_node_to_node_index(self, key, xyz, virtual=False):

        """ Adds the node to the node_index dictionary.

        Parameters
        ----------
        key : int
            Prescribed node key.
        xyz : list
            [x, y, z] co-ordinates of the node.
        virtual: bool
            Is the node virtual or not.

        Returns
        -------
        None

        """

        gkey = geometric_key(xyz, '{0}f'.format(self.tol))
        if virtual:
            self.virtual_node_index[gkey] = key
        else:
            self.node_index[gkey] = key

    def check_node_exists(self, xyz):

        """ Check if a node already exists at given x, y, z co-ordinates.

        Parameters
        ----------
        xyz : list
            [x, y, z] co-ordinates of node to check.

        Returns
        -------
        int
            The node index if the node already exists, None if not.

        Notes
        -----
        - Geometric key check is made according to self.tol [m] tolerance.

        """

        xyz = [float(i) for i in xyz]
        return self.node_index.get(geometric_key(xyz, '{0}f'.format(self.tol)), None)

    def node_count(self):

        """ Return the number of nodes in the Structure.

        Parameters
        ----------
        None

        Returns
        -------
        int
            Number of nodes stored in the Structure object.

        """

        return len(self.nodes)

    def node_xyz(self, node):

        """ Return the xyz co-ordinates of a node.

        Parameters
        ----------
        node : int
            Node number.

        Returns
        -------
        list
            [x, y, z] co-ordinates.

        """

        return [getattr(self.nodes[node], i) for i in 'xyz']

if __name__ == "__main__":
    for i in range(60):
        print('')

    from compas_vibro.structure import Structure

    import compas_vibro
    path = compas_vibro.TEMP
    name = 'test_vibro'
    s = Structure(path, name)
    s.add_node([0, 0, 0])
    print(s.node_index)
