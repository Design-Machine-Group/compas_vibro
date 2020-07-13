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
__all__ = ['write_command_file_harmonic']


def write_command_file_harmonic(structure, fields):
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
    write_harmonic_step(structure, path, filename)

    # write_harmonic_solve(structure, path, filename)



def write_harmonic_solve(structure, path, filename):
    pass

def write_harmonic_step(structure, path, filename):
    #TODO: Fix frequency, period, analyze, load control to make sense, minimize calc time
    # This configuration does one full period no matter the frquency
    # I dont think using LoadControl integrator is ideal, must be a faster way
    # How many analysys cycles do I need??? Why???

    outpath = os.path.join(path, '{}_output'.format(structure.name))
    numnodes = structure.node_count()
    f = 100.
    t = (1 / f)  # in ms??
    fh = open(os.path.join(path, filename), 'a')
    fh.write('#\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('# Harmonic Step\n')
    fh.write('#-{} \n'.format('-'*80))
    fh.write('#\n')

    fh.write('timeSeries Sine 1 {0} {1} {2} \n'.format(0.0, t, t))
    # fh.write('timeSeries Constant 1\n')
    fh.write('pattern Plain 1 1 -fact 1 {\n')
    fh.write('#\n')
    fh.write('#\n')

    fh.write('load 100 0.0 0.0 -100.0 0.0 0.0 0.0\n')
    fh.write('load 200 0.0 0.0 100.0 0.0 0.0 0.0\n')
    fh.write('}\n')
    fh.write('#\n')
    fh.write('#\n')
    fh.write('recorder Node -file {0}/harmonic_disp.out -time -nodeRange 1 {1} -dof 1 2 3 disp\n'.format(outpath, numnodes))
    fh.write('#\n')
    fh.write('#\n')
    fh.write('constraints Transformation\n')
    fh.write('numberer RCM\n')
    fh.write('system ProfileSPD\n')
    fh.write('test NormUnbalance 0.01 100 5\n')
    fh.write('algorithm NewtonLineSearch\n')
    fh.write('integrator LoadControl {}\n'.format(t / 10))
    fh.write('analysis Static\n')
    fh.write('analyze {}\n'.format(int(10)))

    fh.close()