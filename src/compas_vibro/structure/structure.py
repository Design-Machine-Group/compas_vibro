from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_vibro.structure._mixins.nodemixins import NodeMixins
from compas_vibro.structure._mixins.elementmixins import ElementMixins
from compas_vibro.structure._mixins.objectmixins import ObjectMixins

from compas_vibro.fea.ansys.ansys import modal_from_structure

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


TPL = """
################################################################################
compas_vibro Structure: {}
################################################################################

Nodes
-----
{}

Elements
--------
{}
"""


class Structure(NodeMixins, ElementMixins, ObjectMixins):

    def __init__(self, path, name='VibroStructure'):

        self.displacements         = {}
        self.elements              = {}
        self.element_index         = {}
        self.element_properties    = {}
        # self.frequencies           = {}
        self.loads                 = {}
        self.materials             = {}
        self.name                  = name
        self.nodes                 = {}
        self.node_index            = {}
        self.path                  = path
        # self.results               = {}
        self.sections              = {}
        self.sets                  = {}
        self.steps                 = {}
        self.tol                   = '3'

    def __str__(self):
        return TPL.format(self.name, self.node_count(), self.element_count())

    def add_nodes_elements_from_mesh(self, mesh, element_type='ShellElement', elset=None):

        """ Adds the nodes and faces of a Mesh to the Structure object.

        Parameters
        ----------
        mesh : obj
            Mesh datastructure object.
        element_type : str
            Element type: 'ShellElement', 'SolidElement' etc.

        Returns
        -------
        list
            Keys of the created elements.

        """

        for key in sorted(list(mesh.vertices()), key=int):
            self.add_node(mesh.vertex_coordinates(key))

        ekeys = []

        for fkey in list(mesh.faces()):
            face = [self.check_node_exists(mesh.vertex_coordinates(i)) for i in mesh.face[fkey]]
            ekeys.append(self.add_element(nodes=face, type=element_type))

        if elset:
            self.add_set(name=elset, type='element', selection=ekeys)

        return ekeys

    def analyze(self, type='Modal', backend='Ansys'):
        if type == 'Modal' and backend == 'Ansys':
            modal_from_structure(self)



if __name__ == '__main__':
    pass
