from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
import json

from compas.geometry import area_polygon

from compas.datastructures import Mesh

from compas_vibro.structure._mixins.nodemixins import NodeMixins
from compas_vibro.structure._mixins.elementmixins import ElementMixins
from compas_vibro.structure._mixins.objectmixins import ObjectMixins

from compas_vibro.fea.ansys.ansys import ansys_static
from compas_vibro.fea.ansys.ansys import ansys_modal
from compas_vibro.fea.ansys.ansys import ansys_modal_prestressed
from compas_vibro.fea.ansys.ansys import ansys_harmonic
from compas_vibro.fea.ansys.ansys import ansys_harmonic_super
from compas_vibro.fea.ansys.ansys import ansys_harmonic_field

from compas_vibro.fea.opensees.opensees import opensees_modal
from compas_vibro.fea.opensees.opensees import opensees_harmonic
from compas_vibro.fea.opensees.opensees import opensees_static

from compas_vibro.structure.load import PointLoad

from compas_vibro.structure.element_properties import ElementProperties

from compas_vibro.vibro.rayleigh import compute_rad_power_structure
from compas_vibro.vibro import from_W_to_dB

from compas.geometry import centroid_points
from compas.geometry import distance_point_point
from compas.geometry import rotate_points
from compas.geometry import subtract_vectors

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2022, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


TPL = """

compas_vibro Structure: {}
----------------------

Number of Nodes ------------- {}
Number of Elements ---------- {}
Number of Modes ------------- {}
Number of Harmonic Freqs. --- {}
Number of Rad. Pow. Freqs. -- {}
"""

# TODO: The function that adds beams from lines should be done considering
#       previous meshes, if lines go by meshes, beams should be divided. 


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
        self.virtual_node_index     = {}
        self.path                   = path
        self.results                = {}
        self.sections               = {}
        self.sets                   = {}
        self.step                   = {'modal': None, 'static': None, 'harmonic': None}
        self.tol                    = '3'
        self.mass                   = None
        self.c                      = 340.0
        self.rho                    = 1.225
        self.beam_sections          = ['ISection','BoxSection','RectangularSection',
                                       'TieSection', 'StrutSection', 'TrussSection',
                                       ]
        self.inc_mesh               = None
        self.nl_geom                = False
        self.num_dof                = 6

    def __str__(self):
        string = ''
        num_modes = 0
        num_freq = 0
        num_rpf = 0
        if 'modal' in self.results:
            num_modes = len(self.results['modal'])
        if 'harmonic' in self.results:
            num_freq = len(self.results['harmonic'])
        if 'radiation' in self.results:
            num_rpf = len(self.results['radiation'])
        return TPL.format(self.name,
                          self.node_count(),
                          self.element_count(),
                          num_modes,
                          num_freq,
                          num_rpf)

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

    def add_nodes_elements_from_volmesh(self, volmesh, element_type='SolidElement', elset=None):

        """ Adds the nodes and cells of a VolMesh to the Structure object.

        Parameters
        ----------
        volmesh : obj
            VolMesh datastructure object.
        element_type : str
            Element type: 'SolidElement', etc.

        Returns
        -------
        list
            Keys of the created elements.

        """

        for key in sorted(list(volmesh.vertices()), key=int):
            self.add_node(volmesh.vertex_coordinates(key))

        ekeys = []
        for cell in volmesh.cells():
            v = volmesh.cell_vertices(cell)
            cell = [self.check_node_exists(volmesh.vertex_coordinates(i)) for i in volmesh.cell_vertices(cell)]
            ekeys.append(self.add_element(nodes=cell, type=element_type))
        if elset:
            self.add_set(name=elset, type='element', selection=ekeys)

        return ekeys

    def add_nodes_elements_from_lines(self, lines, element_type='BeamElement', elset=None, normal=[0,0,1]):
        ekeys = []
        for u, v in lines:
            uk = self.add_node(u)
            vk = self.add_node(v)
            x = rotate_points([subtract_vectors(u, v)], 1.5708, axis=normal)[0]
            ekeys.append(self.add_element(nodes =[uk, vk], type=element_type, axes={'x':x}, check=False))
        if elset:
            self.add_set(name= elset, type='element', selection=ekeys)
        return ekeys
        
    def add_gravity_from_mesh(self, mesh, thickness, density):
        for vk in mesh.vertices():
            area = mesh.vertex_area(vk)
            l = area * thickness * density
            load = PointLoad(vk, vk, z=-l)
            self.loads[vk] = load

    def add_incident_elements_from_mesh(self, mesh):
        self.inc_mesh = mesh
        eps = {}
        for fk in mesh.faces():
            cpt = mesh.face_centroid(fk)
            ek = self.check_element_exists(xyz=cpt)
            ep = self.elements[ek].element_property
            if ep in eps:
                eps[ep].append(ek)
            else:
                eps[ep] = [ek]
            # print(fk, ek, ep)

        for epk in eps:
            mat = self.element_properties[epk].material
            sec = self.element_properties[epk].section
            is_rad = self.element_properties[epk].is_rad
            elset = self.element_properties[epk].elset

            self.add_set(name='{}_incident'.format(elset), type='element', selection=eps[epk])

            el_prop = ElementProperties('{}_incident_prop'.format(ep),
                                        material=mat,
                                        section=sec,
                                        elset='{}_incident'.format(elset),
                                        is_rad=is_rad,
                                        is_incident=True)
            self.add(el_prop)

            self.element_properties[epk].remove_elements(eps[epk])
            
            if elset:
                self.sets[elset].remove_elements(eps[epk])

    def analyze_modal(self, fields, backend='ansys', num_modes=10, exe=None):
        self.compute_mass()
        if backend == 'ansys':
            ansys_modal(self, fields, num_modes=num_modes)
        elif backend == 'opensees':
            opensees_modal(self, fields, num_modes=num_modes, exe=exe)
        else:
            raise NameError('This backend is not implemented')

    def analyze_modal_prestressed(self, fields, backend='ansys', num_modes=10, exe=None):
        self.compute_mass()
        if backend == 'ansys':
            ansys_modal_prestressed(self, fields, num_modes=num_modes)
        elif backend == 'opensees':
            NameError('This backend is not implemented')
        else:
            raise NameError('This backend is not implemented')

    def analyze_static(self, fields, backend='ansys', exe=None):
        if backend == 'ansys':
            ansys_static(self,fields)
        elif backend == 'opensees':
            opensees_static(self, fields, exe=exe)
        else:
            raise NameError('This backend is not implemented')

    def analyze_harmonic(self, freq_list, fields, damping=.02, backend='ansys', exe=None):
        if backend == 'ansys':
            ansys_harmonic(self, freq_list, fields, damping=damping)
        elif backend == 'opensees':
            opensees_harmonic(self, freq_list, fields=fields, damping=damping, exe=exe)
        else:
            raise NameError('This backend is not implemented')
        
    def analyze_harmonic_super(self, num_modes, freq_list, fields, damping=.02, backend='ansys'):
        self.compute_mass()
        if backend == 'ansys':
            ansys_harmonic_super(self, num_modes, freq_list, fields, damping=damping)
        else:
            raise NameError('This backend is not implemented yet')

    def analyze_harmonic_field(self, num_modes, freq_list, fields, damping=.02, backend='ansys'):
        self.compute_mass()
        if backend == 'ansys':
            ansys_harmonic_field(self, num_modes, freq_list, fields, damping=damping)
        else:
            raise NameError('This backend is not implemented')

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
        for ek in self.elements:
            mass += self.compute_element_mass(ek)
        self.mass = mass

    def compute_element_mass(self, element_key):
        epk = self.elements[element_key].element_property
        el_prop = self.element_properties[epk]
        material = el_prop.material
        section = el_prop.section
        if material:
            density = self.materials[material].p
        if self.sections[section].__name__ == 'ShellSection':
            thick = self.sections[section].geometry['t']
            polygon = [self.nodes[nk].xyz() for nk in self.elements[element_key].nodes]
            area = area_polygon(polygon)
            mass = area * thick * density
        elif self.sections[section].__name__  in self.beam_sections:
            area = self.sections[section].geometry['A']
            u, v = self.elements[element_key].nodes
            length = distance_point_point(self.node_xyz(u), self.node_xyz(v))
            mass = area * length * density
        elif self.sections[section].__name__ == 'MassSection':
            mass = self.sections[section].geometry['M']
        return mass

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

    def support_nodes(self):
        nks = []
        for dk in self.displacements:
            nks.extend(self.displacements[dk].nodes)
        return nks

    def incident_nodes(self):
        snks = self.support_nodes()
        eks = self.incident_faces()
        nks = []
        for ek in eks:
            nks_ = self.elements[ek].nodes
            for nk in nks_:
                if nk not in snks and nk not in nks:
                    nks.append(nk)
        return nks

    def radiating_nodes(self):
        snks = self.support_nodes()
        eks = self.radiating_faces()
        nks = []
        for ek in eks:
            nks_ = self.elements[ek].nodes
            for nk in nks_:
                if nk not in snks and nk not in nks:
                    nks.append(nk)
        return nks 
 
    def radiating_faces(self):
        eps = sorted(list(self.element_properties.keys()))
        eks = []
        for ep in eps:
            if self.element_properties[ep].is_rad:
                elements = self.element_properties[ep].elements
                elset = self.element_properties[ep].elset
                if elements:
                    eks.extend(elements)
                elif elset:
                    eks.extend(self.sets[elset].selection)
        return eks

    def incident_faces(self):
        eps = sorted(list(self.element_properties.keys()))
        eks = []
        for ep in eps:
            if self.element_properties[ep].is_incident:
                elements = self.element_properties[ep].elements
                elset = self.element_properties[ep].elset
                if elements:
                    eks.extend(elements)
                elif elset:
                    eks.extend(self.sets[elset].selection)
        return eks

    def radiating_face_centers(self):
        eks = self.radiating_faces()
        centers = []
        for ek in eks:
            pl = [self.nodes[nk].xyz() for nk in self.elements[ek].nodes]
            centers.append(centroid_points(pl))
        return centers

    def radiating_center(self):
        centers = self.radiating_face_centers()
        cpt = centroid_points(centers)
        return cpt

    def radiating_mesh(self):
        faces = [self.elements[fk].nodes for fk in self.radiating_faces()]
        vertices = [self.nodes[k].xyz() for k in self.nodes]
        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        mesh.cull_vertices()
        return mesh

    @property
    def results_data(self):
        self.compute_mass()
        data = {'modal':{},
                # 'harmonic':{},
                'radiation': {},
                'structure_mass': self.mass,
                }

        if 'modal' in self.results:
            for mode in self.results['modal']:
                mr = self.results['modal'][mode]
                f = mr.frequency
                mass = mr.efmass
                md = {'frequency': f, 'eff_mass': mass}
                data['modal'][mode] = md
        
        if 'radiation' in self.results:
            for fkey in self.results['radiation']:
                r = self.results['radiation'][fkey]
                f = r.frequency
                rad = r.radiated_p
                rad_db = from_W_to_dB(rad)
                rd = {'frequency': f, 'radiated_p': rad, 'radiated_p_db': rad_db}
                data['radiation'][fkey] =rd

        return data

    def to_results_json(self, path=None, name=None, add_data=None):
        if not path:
            path = self.path
        if not name:
            name = self.name
        filepath = os.path.join(path, name + '_results.json')
        data = self.results_data
        if add_data:
            data.update(add_data)
        with open(filepath, 'w+') as fp:
            json.dump(data, fp)


if __name__ == '__main__':
    pass

    # import compas_vibro
    # from compas_vibro.viewers import StructureViewer

    # # fp = os.path.join(compas_vibro.DATA, 'structures', 'shell_beams_harmonic.obj')
    # # s = Structure.from_obj(fp)
    # # s.to_results_json(path=compas_vibro.TEMP)
    # # print(s)
    
    # s = Structure.from_obj(os.path.join(compas_vibro.DATA, 'structures', 'flat_10x10.obj'))

    # print(s.radiating_nodes())

    # v = StructureViewer(s)
    # v.show_rad_nodes = True
    # v.show_incident_nodes = True
    # v.show()

    
