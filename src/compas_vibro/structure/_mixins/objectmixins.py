
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from compas_vibro.structure.displacement import GeneralDisplacement
from compas_vibro.structure.section import Section
from compas_vibro.structure.load import Load
from compas_vibro.structure.element_properties import ElementProperties
from compas_vibro.structure.material import Material
from compas_vibro.structure.set import Set
from compas_vibro.structure.step import Step


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

__all__ = ['ObjectMixins']


class ObjectMixins(object):

    def add(self, objects):

        """ Adds object(s) to their correct attribute dictionary in the structure.

        Parameters
        ----------
        objects : obj, list
            The object or list of objects to add.

        Returns
        -------
        None

        """

        if not isinstance(objects, list):
            objects = [objects]

        for i in objects:
            cl = i.__class__

            if issubclass(cl, GeneralDisplacement) or isinstance(i, GeneralDisplacement):
                self.add_displacement(i)

            elif issubclass(cl, Material):
                self.add_material(i)

            elif issubclass(cl, Section):
                self.add_section(i)

            elif issubclass(cl, Load):
                self.add_load(i)

            elif isinstance(i, ElementProperties):
                self.add_element_properties(i)

            elif issubclass(cl, Step):
                self.add_step(i)

            elif issubclass(cl, Set):
                self.add_set(i)

            else:
                print('***** WARNING: object type not found using structure.add() *****')

    def add_displacement(self, displacement):

        """ Adds a Displacement object to structure.displacements.

        Parameters
        ----------
        displacement : obj
            The Displacement object.

        Returns
        -------
        None

        """

        displacement.index = len(self.displacements)
        self.displacements[displacement.name] = displacement

    def add_displacements(self, displacements):

        """ Adds Displacement objects to structure.displacements.

        Parameters
        ----------
        displacements : list
            The Displacement objects.

        Returns
        -------
        None

        """

        for displacement in displacements:
            self.add_displacement(displacement)

    def add_load(self, load):

        """ Adds a Load object to structure.loads.

        Parameters
        ----------
        load : obj
            The Load object.

        Returns
        -------
        None

        """

        load.index = len(self.loads)
        self.loads[load.name] = load

    def add_section(self, section):

        """ Adds a Section object to structure.sections.

        Parameters
        ----------
        section : obj
            The Section object.

        Returns
        -------
        None

        """

        section.index = len(self.sections)
        self.sections[section.name] = section

    def add_material(self, material):

        """ Adds a Material object to structure.materials.

        Parameters
        ----------
        material : obj
            The Material object.

        Returns
        -------
        None

        """

        material.index = len(self.materials)
        self.materials[material.name] = material

    def add_element_properties(self, element_properties):

        """ Adds ElementProperties object(s) to structure.element_properties.

        Parameters
        ----------
        element_properties : obj, list
            The ElementProperties object(s).

        Returns
        -------
        None

        """

        if isinstance(element_properties, list):
            for element_property in element_properties:
                element_property.index = len(self.element_properties)
                self.element_properties[element_property.name] = element_property
                self.assign_element_property(element_property)
        else:
            element_properties.index = len(self.element_properties)
            self.element_properties[element_properties.name] = element_properties
            self.assign_element_property(element_properties)

    def add_set(self, name, type, selection):

        """ Adds a node, element or surface set to structure.sets.

        Parameters
        ----------
        name : str
            Name of the Set.
        type : str
            'node', 'element', 'surface_node', surface_element'.
        selection : list, dict
            The integer keys of the nodes, elements or the element numbers and sides.

        Returns
        -------
        None

        """

        if isinstance(selection, int):
            selection = [selection]

        self.sets[name] = Set(name=name, type=type, selection=selection, index=len(self.sets))

    def add_step(self, step):

        """ Adds a Step object to structure.steps.

        Parameters
        ----------
        step : obj
            The Step object.

        Returns
        -------
        None

        """

        step.index = 0
        self.step = step

if __name__ == "__main__":
    pass
