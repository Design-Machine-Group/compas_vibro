from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas.geometry import centroid_points

from compas.utilities import geometric_key

from compas_vibro.structure.element import ShellElement
from compas_vibro.structure.element import BeamElement
from compas_vibro.structure.element import TieElement
from compas_vibro.structure.element import StrutElement
from compas_vibro.structure.element import TrussElement
from compas_vibro.structure.element import MassElement

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = [
    'ElementMixins',
]

func_dict = {'ShellElement': ShellElement,
             'BeamElement': BeamElement,
             'TieElement': TieElement,
             'StrutElement': StrutElement,
             'TrussElement': TrussElement,
             'MassElement': MassElement,
             }


class ElementMixins(object):

    def add_element(self, nodes, type, axes={}, check=True):

        """ Adds an element to structure.elements with centroid geometric key.

        Parameters
        ----------
        nodes : list
            Nodes the element is connected to.
        type : str
            Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.

        Returns
        -------
        int
            Key of the added or existing element.

        Notes
        -----
        - Elements are numbered sequentially starting from 0.

        """

        if len(nodes) == len(set(nodes)):
            if check:
                ekey = self.check_element_exists(nodes)
            else:
                ekey = None

            if ekey is None:

                ekey                = self.element_count()
                element             = func_dict[type]()
                element.nodes       = nodes
                element.number      = ekey
                element.axes        = axes
                self.elements[ekey] = element

                self.add_element_to_element_index(ekey, nodes)

            return ekey

        else:
            return None

    def add_elements(self, elements, type, thermal=False, axes={}):

        """ Adds multiple elements of the same type to structure.elements.

        Parameters
        ----------
        elements : list
            List of lists of the nodes the elements are connected to.
        type : str
            Element type: 'HexahedronElement', 'BeamElement, 'TrussElement' etc.
        thermal : bool
            Thermal properties on or off.
        axes : dict
            The local element axes 'ex', 'ey' and 'ez' for all elements.

        Returns
        -------
        list
            Keys of the added or existing elements.

        Notes
        -----
        - Elements are numbered sequentially starting from 0.

        """

        return [self.add_element(nodes=nodes, type=type, thermal=thermal, axes=axes) for nodes in elements]

    def add_element_to_element_index(self, key, nodes, virtual=False):

        """ Adds the element to the element_index dictionary.

        Parameters
        ----------
        key : int
            Prescribed element key.
        nodes : list
            Node numbers the element is connected to.
        virtual: bool
            If true, adds element to the virtual_element_index dictionary.

        Returns
        -------
        None

        """

        centroid = centroid_points([self.node_xyz(node) for node in nodes])
        gkey     = geometric_key(centroid, '{0}f'.format(self.tol))

        if virtual:
            self.virtual_element_index[gkey] = key
        else:
            self.element_index[gkey] = key

    def check_element_exists(self, nodes=None, xyz=None, virtual=False):

        """ Check if an element already exists based on nodes or centroid.

        Parameters
        ----------
        nodes : list
            Node numbers the element is connected to.
        xyz : list
            Direct co-ordinates of the element centroid to check.
        virtual: bool
            Is the element to be checked a virtual element.

        Returns
        -------
        int
            The element index if the element already exists, None if not.

        Notes
        -----
        - Geometric key check is made according to self.tol [m] tolerance.

        """

        if not xyz:
            xyz = centroid_points([self.node_xyz(node) for node in nodes])

        gkey = geometric_key(xyz, '{0}f'.format(self.tol))

        if virtual:
            return self.virtual_element_index.get(gkey, None)
        else:
            return self.element_index.get(gkey, None)

    def element_count(self):

        """ Return the number of elements in the Structure.

        Parameters
        ----------
        None

        Returns
        -------
        int
            Number of elements stored in the Structure object.

        """

        return len(self.elements)

    def element_centroid(self, element):

        """ Return the centroid of an element.

        Parameters
        ----------
        element : int
            Number of the element.

        Returns
        -------
        list
            Co-ordinates of the element centroid.

        """

        return centroid_points(self.nodes_xyz(nodes=self.elements[element].nodes))

    def assign_element_property(self, element_property):

        """ Assign the ElementProperties object name to associated Elements.

        Parameters
        ----------
        element_property : obj
            ElementProperties object.

        Returns
        -------
        None

        """

        if element_property.elset:
            elements = self.sets[element_property.elset].selection
        else:
            elements = element_property.elements

        for element in elements:
            self.elements[element].element_property = element_property.name


if __name__ == "__main__":
    pass
