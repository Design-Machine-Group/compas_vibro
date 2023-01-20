
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = [
    'Material',
    'ElasticIsotropic',
    'ElasticOrthotropic',
]


class Material(object):

    """ Initialises base Material object.

    Parameters
    ----------
    name : str
        Name of the Material object.

    Attributes
    ----------
    name : str
        Name of the Material object.

    """

    def __init__(self, name):

        self.__name__  = 'Material'
        self.name      = name
        self.attr_list = ['name']

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))

        for attr in self.attr_list:
            print('{0:<11} : {1}'.format(attr, getattr(self, attr)))

        return ''

    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


# ==============================================================================
# linear elastic
# ==============================================================================

class ElasticIsotropic(Material):

    """ Elastic, isotropic and homogeneous material.

    Parameters
    ----------
    name : str
        Material name.
    E : float
        Young's modulus E [Pa].
    v : float
        Poisson's ratio v [-].
    p : float
        Density [kg/m3].
    tension : bool
        Can take tension.
    compression : bool
        Can take compression.

    """

    def __init__(self, name, E, v, p, tension=True, compression=True):
        Material.__init__(self, name=name)

        self.__name__    = 'ElasticIsotropic'
        self.index       = None
        self.name        = name
        self.E           = {'E': E}
        self.v           = {'v': v}
        self.G           = {'G': 0.5 * E / (1 + v)}
        self.p           = p
        self.tension     = tension
        self.compression = compression
        self.attr_list.extend(['E', 'v', 'G', 'p', 'tension', 'compression'])



class ElasticOrthotropic(Material):

    """ Elastic orthotropic material.

    Parameters
    ----------
    name : str
        Material name.
    Ex : float
        Young's modulus E in the X direction [Pa].
    Ey : float
        Young's modulus E in the Y direction [Pa].
    Ez : float
        Young's modulus E in the Z direction [Pa].
    vxy : float
        Poisson's ratio v in the XY plane [-].
    vyz : float
        Poisson's ratio v in the YZ plane [-].
    vxz : float
        Poisson's ratio v in the XZ plane [-].
    p : float
        Density [kg/m3].
    tension : bool
        Can take tension.
    compression : bool
        Can take compression.

    """

    def __init__(self, name, Ex, Ey, Ez, vxy, vyz, vxz, p, tension=True, compression=True):
        Material.__init__(self, name=name)

        self.__name__    = 'ElasticOrthotropic'
        self.index       = None
        self.name        = name
        self.E           = {'Ex': Ex, 'Ey': Ey, 'Ez': Ez,}
        self.v           = {'vxy': vxy, 'vyz': vyz, 'vxz': vxz}
        self.G           = {'Gx': 0.5 * Ex / (1 + vxy),
                            'Gy': 0.5 * Ey / (1 + vyz),
                            'Gz': 0.5 * Ez / (1 + vxz)}
        self.p           = p
        self.tension     = tension
        self.compression = compression
        self.attr_list.extend(['Ex', 'Ey', 'Ez',
                               'vxy', 'vyz', 'vxz',
                               'Gx', 'Gy', 'Gz',
                               'p', 'tension', 'compression'])
