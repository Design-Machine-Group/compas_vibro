from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


__all__ = ['write_elements']


def write_elements(structure, path, filename):

    structure.et_dict = {}
    # combine elementa and virtual elements ------------------------------------
    elements = {}
    elements.update(structure.elements)
    # elements.update(structure.virtual_elements)

    # group sorted elements by type and properties -----------------------------
    ekeys = sorted(elements.keys(), key=int)
    et = elements[ekeys[0]].__name__
    ep = elements[ekeys[0]].element_property
    count = 0
    ekey_lists = [[]]
    for ekey in ekeys:
        if elements[ekey].__name__ == et and elements[ekey].element_property == ep:
            ekey_lists[count].append(ekey)
        else:
            et = elements[ekey].__name__
            ep = elements[ekey].element_property
            ekey_lists.append([ekey])
            count += 1

    # write sorted elements ----------------------------------------------------
    ekeys = structure.elements
    for ekeys in ekey_lists:
        etype = elements[ekeys[0]].__name__
        ep = elements[ekeys[0]].element_property

        if ep:
            ep = structure.element_properties[elements[ekeys[0]].element_property]
        if ep:
            section = ep.section
            material = ep.material

        if etype == 'ShellElement':
            write_shells(structure, path, filename, ekeys, section, material)
        if etype == 'BeamElement':
            write_beams(structure, path, filename, ekeys, section, material)
        if etype == 'TrussElement':
            write_trusses(structure, path, filename, ekeys, section, material)
        if etype == 'SolidElement':
            write_solids(structure, path, filename, ekeys, section, material)

def write_beams(structure, path, filename, ekeys, section, material):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Beam elements\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')

    e = 'element elasticBeamColumn'
    for ek in ekeys:
        nodes = [i + 1 for i in structure.elements[ek].nodes] 
        A = structure.sections[section].geometry['A']
        J = structure.sections[section].geometry['J']
        Ixx = structure.sections[section].geometry['Ixx']
        Iyy = structure.sections[section].geometry['Iyy']
        E = structure.materials[material].E['E']
        G = structure.materials[material].G['G']
        n = ek + 1
        density = structure.materials[material].p
        mass = A * density * 1

        ex = structure.elements[ek].axes['x']
        fh.write('geomTransf Corotational {0} {1} \n'.format(n, ' '.join([str(i) for i in ex])))
        fh.write('{} {} {} {} {} {} {} {} {} {} {} {} \n'.format(e, n, nodes[0], nodes[1], A, E, G, J, Ixx, Iyy, n, mass))


def write_trusses(structure, path, filename, ekeys, section, material):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Truss elements\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')


    # for ekey in ekeys:
        # e = 'element corotTruss'
        # fh.write('{0} {1} {2} {3} {4} {5} \n'.format(e, n, nodes[0], nodes[1], A, m_index))

def write_shells(structure, path, filename, ekeys, section, material):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Shell elements\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')

    # fh.write('puts \"Begin Elements \"\n')  # printouts from opensees

    # TODO: understand which opensees element type works best
    string = 'element ShellMITC4 {0} {1} {2} {3} {4} {5} \n' # not finished!
    string3 = 'element ShellDKGT {0} {1} {2} {3} {4} \n' # not finished!
    # string = 'element quad  {0} {1} {2} {3} {4} {5} "PlaneStrain" {6}\n'
    for ek in ekeys:
        nodes = structure.elements[ek].nodes
        # t = structure.sections[section].geometry['t']
        # mat = structure.materials[material].index + 1
        sec = structure.sections[section].index + 1
        if len(nodes) == 4:
            i, j, k, l = structure.elements[ek].nodes
            fh.write(string.format(ek + 1, i + 1, j + 1, k + 1, l + 1, sec))
        elif len(nodes) == 3:
            i, j, k = structure.elements[ek].nodes
            fh.write(string3.format(ek + 1, i + 1, j + 1, k + 1, sec))

    # fh.write('puts \"End Elements \"\n')  # printouts from opensees

    fh.close()


def write_solids(structure, path, filename, ekeys, section, material):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Solid elements\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')

    string_tetra = 'element FourNodeTetrahedron {0} {1} {2} {3} {4} {5} \n' # not finished!
    # string_cube = 'element Block3D {0} {1} {2} {3} {4} \n' # not finished!
    for ek in ekeys:
        nodes = structure.elements[ek].nodes
        # t = structure.sections[section].geometry['t']
        mat = structure.materials[material].index + 1
        # sec = structure.sections[section].index + 1
        if len(nodes) == 4:
            i, j, k, l = structure.elements[ek].nodes
            fh.write(string_tetra.format(ek + 1, i + 1, j + 1, k + 1, l + 1, mat))
        else:
            pass
    fh.close()
