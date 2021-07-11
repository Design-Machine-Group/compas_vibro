from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle

from compas.geometry import area_polygon

from compas_vibro.structure._mixins.nodemixins import NodeMixins
from compas_vibro.structure._mixins.elementmixins import ElementMixins
from compas_vibro.structure._mixins.objectmixins import ObjectMixins

from compas_vibro.fea.ansys.ansys import ansys_modal
from compas_vibro.fea.ansys.ansys import ansys_harmonic
from compas_vibro.fea.ansys.ansys import ansys_harmonic_super

from compas_vibro.fea.opensees.opensees import opensees_modal
from compas_vibro.fea.opensees.opensees import opensees_harmonic
from compas_vibro.fea.opensees.opensees import opensees_static

from compas_vibro.structure.load import PointLoad

from compas_vibro.vibro import compute_rad_power_structure

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
        """
        Properties
        ----------

        displacements(dict): The displacements dictionary. The keys are intergers
        and the values are dispplacement objects.

        """

        self.displacements          = {}
        self.elements               = {}
        self.element_index          = {}
        self.element_properties     = {}
        self.loads                  = {}
        self.materials              = {}
        self.name                   = name
        self.nodes                  = {}
        self.node_index             = {}
        self.path                   = path
        self.results                = {}
        self.sections               = {}
        self.sets                   = {}
        self.step                   = {'modal': None, 'static': None, 'harmonic': None}
        self.tol                    = '3'
        self.mass                   = None
        self.c                      = 340.0
        self.rho                    = 1.225

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

    def add_gravity_from_mesh(self, mesh, thickness, density):
        for vk in mesh.vertices():
            area = mesh.vertex_area(vk)
            l = area * thickness * density
            load = PointLoad(vk, vk, z=-l)
            self.loads[vk] = load

    def analyze_modal(self, fields, backend='ansys', num_modes=10):
        self.compute_mass()
        if backend == 'ansys':
            ansys_modal(self, fields, num_modes=num_modes)
        elif backend == 'opensees':
            opensees_modal(self, fields, num_modes=num_modes)
        else:
            raise NameError('This backend is not implemented')

    def analyze_static(self, fields, backend='ansys'):
        if backend == 'ansys':
            raise NameError('This backend is not implemented')
        elif backend == 'opensees':
            opensees_static(self, fields)
        else:
            raise NameError('This backend is not implemented')

    def analyze_harmonic(self, freq_list, fields, damping=.05, backend='ansys'):
        if backend == 'ansys':
            ansys_harmonic(self, freq_list, fields, damping=damping)
        elif backend == 'opensees':
            opensees_harmonic(self, freq_list, fields=fields, damping=damping)
        else:
            raise NameError('This backend is not implemented')
        
    def analyze_harmonic_super(self, num_modes, freq_list, fields, damping=.05, backend='ansys'):
        self.compute_mass()
        if backend == 'ansys':
            ansys_harmonic_super(self, num_modes, freq_list, fields, damping=damping)
        else:
            raise NameError('This backend is not implemented yet')

    def to_obj(self, output=True, path=None, name=None):

        """ Exports the Structure object to an .obj file through Pickle.

        Parameters
        ----------
        output : bool
            Print terminal output.

        Returns
        -------
        None

        """
        if not path:
            path = self.path
        if not name:
            name = self.name
        filename = os.path.join(path, name + '.obj')

        with open(filename, 'wb') as f:
            pickle.dump(self, f, protocol=2)

        if output:
            print('***** Structure saved to: {0} *****\n'.format(filename))

    def compute_mass(self):
        mass = 0
        for epk in self.element_properties:
            mat = self.element_properties[epk].material
            section = self.element_properties[epk].section
            thick = self.sections[section].geometry['t']
            density = self.materials[mat].p
            elset = self.element_properties[epk].elset
            ekeys = self.sets[elset].selection
            for ek in ekeys:
                pl = [self.nodes[nk].xyz() for nk in self.elements[ek].nodes]
                mass += area_polygon(pl) * thick * density
        self.mass = mass

    def compute_rad_power(self):
        compute_rad_power_structure(self)

    @staticmethod
    def from_obj(filename, output=True):

        """ Imports a Structure object from an .obj file through Pickle.

        Parameters
        ----------
        filename : str
            Path to load the Structure .obj from.
        output : bool
            Print terminal output.

        Returns
        -------
        obj
            Imported Structure object.

        """

        with open(filename, 'rb') as f:
            structure = pickle.load(f)

        if output:
            print('***** Structure loaded from: {0} *****'.format(filename))

        return structure


if __name__ == '__main__':
    pass
