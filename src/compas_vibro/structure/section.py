
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = [
    'Section',
    'ShellSection',
    'SolidSection',
    'SpringSection',
]


class Section(object):

    """ Initialises base Section object.

    Parameters
    ----------
    name : str
        Section object name.

    Attributes
    ----------
    name : str
        Section object name.
    geometry : dict
        Geometry of the Section.

    """

    def __init__(self, name):

        self.__name__ = 'Section'
        self.name     = name
        self.geometry = {}

    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 18))
        print('name  : {0}'.format(self.name))

        for i, j in self.geometry.items():
            print('{0:<5} : {1}'.format(i, j))

        return ''

    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


# ==============================================================================
# 1D
# ==============================================================================


class SpringSection(Section):

    """ For use with spring elements.

    Parameters
    ----------
    name : str
        Section name.
    forces : dict
        Forces data for non-linear springs.
    displacements : dict
        Displacements data for non-linear springs.
    stiffness : dict
        Elastic stiffness for linear springs.

    Notes
    -----
    - Force and displacement data should range from negative to positive values.
    - Requires either a stiffness dict for linear springs, or forces and displacement lists for non-linear springs.
    - Directions are 'axial', 'lateral', 'rotation'.

    """

    def __init__(self, name, forces={}, displacements={}, stiffness={}):
        Section.__init__(self, name=name)

        self.__name__      = 'SpringSection'
        self.name          = name
        self.geometry      = None
        self.forces        = forces
        self.displacements = displacements
        self.stiffness     = stiffness


# ==============================================================================
# 2D
# ==============================================================================

class ShellSection(Section):

    """ Section for shell elements.

    Parameters
    ----------
    name : str
        Section name.
    t : float
        Thickness.

    """

    def __init__(self, name, t):
        Section.__init__(self, name=name)

        self.__name__ = 'ShellSection'
        self.name     = name
        self.geometry = {'t': t}


# ==============================================================================
# 3D
# ==============================================================================

class SolidSection(Section):

    """ Section for solid elements.

    Parameters
    ----------
    name : str
        Section name.

    """

    def __init__(self, name):
        Section.__init__(self, name=name)

        self.__name__ = 'SolidSection'
        self.name     = name
        self.geometry = None
