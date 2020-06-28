from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


TPL = """
################################################################################
compas_vibro Result
################################################################################

Frequency
---------
{0}

Type
----
{1}
"""


class Result(object):

    def __init__(self, frequency, name='VibroResult', type=None):

        self.displacements         = {}
        # self.elements              = {}
        # self.element_index         = {}
        self.frequency             = frequency
        self.name                  = name
        # self.nodes                 = {}
        # self.node_index            = {}
        self.tol                   = '3'
        self.type                  = type

    def __str__(self):
        return TPL.format(self.frequency, self.type)


if __name__ == '__main__':
    pass
