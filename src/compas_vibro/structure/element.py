from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['ShellElement',
           'BeamElement',
           'TieElement',
           'StrutElement',
           'TrussElement',
           'MassElement',
           ]


class Element(object):

    """ Initialises base Element object.

    Parameters
    ----------
    nodes : list
        Node keys the element connects to.
    number : int
        Number of the element.

    Attributes
    ----------
    nodes : list
        Node keys the element connects to.
    number : int
        Number of the element.

    """

    def __init__(self, nodes=None, number=None, axes={}):

        self.__name__   = 'Element'
        self.nodes      = nodes
        self.number     = number
        self.axes       = axes        

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['nodes', 'number']:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.number)


class ShellElement(Element):

    """ A 2D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        Element.__init__(self)

        self.__name__ = 'ShellElement'


class BeamElement(Element):

    """ A 1D element that resists axial, shear, bending and torsion.

    Parameters
    ----------
    None

    """

    def __init__(self):
        Element.__init__(self)

        self.__name__ = 'BeamElement'


class TieElement(Element):

    """ A 1D element that resists only axial forces in tension.

    Parameters
    ----------
    None

    """

    def __init__(self):
        Element.__init__(self)

        self.__name__ = 'TieElement'


class StrutElement(Element):

    """ A 1D element that resists only axial forces in compression.

    Parameters
    ----------
    None

    """

    def __init__(self):
        Element.__init__(self)

        self.__name__ = 'StrutElement'


class TrussElement(Element):

    """ A 1D element that resists axial forces in tension and compression.

    Parameters
    ----------
    None

    """

    def __init__(self):
        Element.__init__(self)

        self.__name__ = 'TrussElement'


class MassElement(Element):
    """
    """
    def __init__(self):
        Element.__init__(self)

        self.__name__ = 'MassElement'

if __name__ == "__main__":
    el = MassElement()
    print(el)
