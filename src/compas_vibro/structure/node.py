
__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = [
    'Node',
]


class Node(object):

    """ Initialises base Node object.

    Parameters
    ----------
    key : int
        Node key number.
    xyz : list
        [x, y, z] co-ordinates of the node.


    Attributes
    ----------
    key : int
        Node key number.
    x : float
        x co-ordinates of the node.
    y : float
        y co-ordinates of the node.
    z : float
        z co-ordinates of the node.
    """

    def __init__(self, key, xyz):

        self.__name__ = 'Node'
        self.key      = key
        self.x        = xyz[0]
        self.y        = xyz[1]
        self.z        = xyz[2]

    def __str__(self):

        print('\n')
        print('compas_vibro {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in ['key', 'x', 'y', 'z']:
            print('{0:<5} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.key)
