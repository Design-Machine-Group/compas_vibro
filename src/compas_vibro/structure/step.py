
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = [
    'Step',
    'StaticStep',
    'ModalStep',
    'HarmonicStep',
]


class Step(object):

    """ Initialises base Step object.

    Parameters
    ----------
    name : str
        Name of the Step object.

    Attributes
    ----------
    name : str
        Name of the Step object.

    """

    def __init__(self, name):

        self.__name__  = 'StepObject'
        self.name      = name
        self.attr_list = ['name']


    def __str__(self):

        print('\n')
        print('compas_fea {0} object'.format(self.__name__))
        print('-' * (len(self.__name__) + 10))

        for attr in self.attr_list:
            print('{0:<13} : {1}'.format(attr, getattr(self, attr)))

        return ''


    def __repr__(self):

        return '{0}({1})'.format(self.__name__, self.name)


class StaticStep(Step):

    """ Initialises StaticStep object for use in a static analysis.

    Parameters
    ----------
    name : str
        Name of the StaticStep.
    increments : int
        Number of step increments.
    iterations : int
        Number of step iterations.
    tolerance : float
        A tolerance for analysis solvers.
    factor : float, dict
        Proportionality factor(s) on the loads and displacements.
    nlgeom : bool
        Analyse non-linear geometry effects.
    nlmat : bool
        Analyse non-linear material effects.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    type : str
        'static','static,riks'.
    modify : bool
        Modify the previously added loads.

    """

    def __init__(self, name, factor=1.0, nlgeom=True, nlmat=True, 
                 displacements=None, loads=None, type='static'):
                 
        Step.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        self.__name__      = 'StaticStep'
        self.name          = name
        # self.increments    = increments
        # self.iterations    = iterations
        # self.tolerance     = tolerance
        self.factor        = factor
        self.nlgeom        = nlgeom
        self.nlmat         = nlmat
        self.displacements = displacements
        self.loads         = loads
        # self.modify        = modify
        self.type          = type
        self.attr_list.extend(['increments', 'iterations', 'factor', 'nlgeom', 'nlmat', 'displacements', 'loads',
                               'type', 'tolerance', 'modify'])



class ModalStep(Step):

    """ Initialises ModalStep object for use in a modal analysis.

    Parameters
    ----------
    name : str
        Name of the ModalStep.
    modes : int
        Number of modes to analyse.
    increments : int
        Number of increments.
    displacements : list
        Displacement object names.
    type : str
        'modal'.

    """

    def __init__(self, name, modes=10, increments=100, displacements=None, type='modal'):
        
        Step.__init__(self, name=name)

        if not displacements:
            displacements = []

        self.__name__      = 'ModalStep'
        self.name          = name
        self.modes         = modes
        self.increments    = increments
        self.displacements = displacements
        self.type          = type
        self.attr_list.extend(['modes', 'increments', 'displacements', 'type'])


class HarmonicStep(Step):

    """ Initialises HarmonicStep object for use in a harmonic analysis.

    Parameters
    ----------
    name : str
        Name of the HarmonicStep.
    freq_list : list
        Sorted list of frequencies to analyse.
    displacements : list
        Displacement object names.
    loads : list
        Load object names.
    factor : float
        Proportionality factor on the loads and displacements.
    damping : float
        Constant harmonic damping ratio.
    type : str
        'harmonic'.

    """

    def __init__(self, name, freq_list, displacements=None, loads=None, factor=1.0, 
                 damping=None, type='harmonic'):
        
        Step.__init__(self, name=name)

        if not displacements:
            displacements = []

        if not loads:
            loads = []

        self.__name__      = 'HarmonicStep'
        self.name          = name
        self.freq_list     = freq_list
        self.displacements = displacements
        self.loads         = loads
        self.factor        = factor
        self.damping       = damping
        self.type          = type
        self.attr_list.extend(['freq_list', 'displacements', 'loads', 'factor', 'damping', 'type'])


class HarmonicFieldStep(HarmonicStep):

    """
    """

    def __init__(self, name, freq_list, index, displacements=None, loads=None, factor=1.0, 
                 damping=None, type='harmonic_field'):
        
        HarmonicStep.__init__(self, name=name, freq_list=freq_list, displacements=displacements,
                              loads=loads, factor=factor)
        self.__name__       = 'HarmonicFieldStep'
        self.index          = index

