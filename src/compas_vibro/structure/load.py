
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['Load',
           'PointLoad',
           'HarmonicPointLoad',
           'HarmonicPressureFieldLoad',
           ]


class Load(object):

    """ Initialises base Load object.

    Parameters
    ----------
    name : str
        Name of the Load object.
    axes : str
        Load applied via 'local' or 'global' axes.
    components : dict
        Load components.
    nodes : str, list
        Node set or node keys the load is applied to.
    elements : str, list
        Element set or element keys the load is applied to.

    Attributes
    ----------
    name : str
        Name of the Load object.
    axes : str
        Load applied via 'local' or 'global' axes.
    components : dict
        Load components.
    nodes : str, list
        Node set or node keys the load is applied to.
    elements : str, list
        Element set or element keys the load is applied to.

    """

    def __init__(self, name, axes='global', components={}, nodes=[], elements=[]):

        self.__name__   = 'LoadObject'
        self.name       = name
        self.axes       = axes
        self.components = components
        self.nodes      = nodes
        self.elements   = elements
        self.attr_list  = ['name', 'axes', 'components', 'nodes', 'elements']

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 10))

        for attr in self.attr_list:
            print('{0:<10} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


class FieldLoad(object):
    def __init__(self, name, field):

        self.__name__   = 'FieldLoadObject'
        self.name       = name
        self.field      = field

class PointLoad(Load):

    """ Concentrated forces and moments [units:N, Nm] applied to node(s).

    Parameters
    ----------
    name : str
        Name of the PointLoad object.
    nodes : str, list
        Node set or node keys the load is applied to.
    x : float
        x component of force.
    y : float
        y component of force.
    z : float
        z component of force.
    xx : float
        xx component of moment.
    yy : float
        yy component of moment.
    zz : float
        zz component of moment.

    """

    def __init__(self, name, nodes, x=0, y=0, z=0, xx=0, yy=0, zz=0):
        Load.__init__(self, name=name, nodes=nodes, axes='global')

        self.__name__   = 'PointLoad'
        self.components = {'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}


class HarmonicPointLoad(Load):

    """ Harmonic concentrated forces and moments [units:N, Nm] applied to node(s).

    Parameters
    ----------
    name : str
        Name of the HarmonicPointLoad object.
    nodes : str, list
        Node set or node keys the load is applied to.
    x : float
        x component of force.
    y : float
        y component of force.
    z : float
        z component of force.
    xx : float
        xx component of moment.
    yy : float
        yy component of moment.
    zz : float
        zz component of moment.

    """

    def __init__(self, name, nodes, x=0, y=0, z=0, xx=0, yy=0, zz=0):
        Load.__init__(self, name=name, nodes=nodes, axes='global')

        self.__name__   = 'HarmonicPointLoad'
        self.components = {'x': x, 'y': y, 'z': z, 'xx': xx, 'yy': yy, 'zz': zz}


class HarmonicPressureFieldLoad(FieldLoad):

    """
    """

    def __init__(self, name, field):
        FieldLoad.__init__(self, name=name, field=field)

        self.__name__   = 'HarmonicPressureFieldLoad'
        self.field      = field


