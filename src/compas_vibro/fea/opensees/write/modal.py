from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from compas_vibro.fea.opensees.write.process import write_heading
from compas_vibro.fea.opensees.write.nodes import write_nodes
from compas_vibro.fea.opensees.write.nodes import write_displacements
from compas_vibro.fea.opensees.write.materials import write_material
from compas_vibro.fea.opensees.write.sections import write_section
from compas_vibro.fea.opensees.write.elements import write_elements


def write_command_file_modal(structure, fields):
    path = structure.path
    filename = structure.name + '.tcl'

    write_heading(path, filename)
    write_nodes(structure, path, filename)
    write_displacements(structure, path, filename)

    eps = structure.element_properties
    for ep in eps:
        material = structure.materials[eps[ep].material]
        section = structure.sections[eps[ep].section]

        write_material(structure, path, filename, material)
        write_section(structure, path, filename, section, ep)
    
    write_elements(structure, path, filename)
    write_modal_solve(structure, path, filename)
    
    if 'u' or 'all' in fields:
        write_modal_shape(structure, path, filename)
    if 'f' or 'all' in fields:
        write_modal_frequency(structure, path, filename)
    if 'm' or 'all' in fields:
        write_modal_masses(structure, path, filename)
    write_modal_record(structure, path, filename)    

def write_modal_masses(structure, path, filename):
    op = os.path.join(path, '{}_output'.format(structure.name), 'modal_masses.txt')
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('modalProperties -print -file \"{}\" -unorm\n'.format(op))
    fh.write('#\n')    
    fh.close()

def write_modal_record(structure, path, filename):
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('record\n')
    fh.write('#\n')    
    fh.close()

def write_modal_solve(structure, path, filename):
    modes = structure.step['modal'].modes

    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Eigen Analysis\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    # fh.write('eigen  {}\n'.format(modes))
    fh.write('set lambda [eigen  {}]\n'.format(modes))
    fh.write('#\n')
    fh.write('record\n')
    fh.write('#\n')
    fh.close()

def write_modal_shape(structure, path, filename):
    modes = structure.step['modal'].modes
    num_nodes = len(structure.nodes)
    outpath = os.path.join(path, '{}_output'.format(structure.name))

    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Modal shape recorders\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')
    op_= outpath.replace('\\', '/')
    string = 'recorder Node -file \"{0}/mode{1}.out\" -nodeRange 1 {2} -dof 1 2 3 "eigen {1}"\n'
    for i in range(modes):
        fh.write(string.format(op_, i + 1, num_nodes))
    fh.write('#\n')
    fh.write('#\n')
    fh.close()

def write_modal_frequency(structure, path, filename):
    # modes = structure.step['modal'].modes
    # num_nodes = len(structure.nodes)
    outpath = os.path.join(path, '{}_output'.format(structure.name))

    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Modal frequency out\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')

    fh.write('set F {}\n')
    fh.write('set pi 3.141593\n')
    fh.write('#\n')
    fh.write('foreach lam $lambda {\n')
    fh.write('    lappend F [expr sqrt($lam)/(2*$pi)]\n')
    fh.write('}\n')
    fh.write('#\n')
    # fh.write('puts "frequencies are $F"\n')
    fh.write('#\n')
    op_= outpath.replace('\\', '/')
    fh.write('set freq "{}/modal_frequencies.out"\n'.format(op_))
    fh.write('set Freq [open $freq "w"]\n')
    fh.write('foreach f $F {\n')
    fh.write('    puts $Freq " $f"\n')
    fh.write('}\n')
    fh.write('close $Freq\n')
    fh.close()