import os

from compas_fea.structure import CircularSection
from compas_fea.structure import ElasticIsotropic
from compas_fea.structure import ElementProperties as Properties
from compas_fea.structure import GeneralDisplacement
from compas_fea.structure import GeneralStep
from compas_fea.structure import PinnedDisplacement
from compas_fea.structure import PointLoad
from compas_fea.structure import Structure
from compas_fea.structure import Set

from math import pi

import compas_vibro

from compas.datastructures import Network

for i in range(60): print()

# Structure

mdl = Structure(name='beam_simple', path=compas_vibro.TEMP + '/')

# Elements

filepath = os.path.join(compas_vibro.DATA, 'network_10x10.json')

network = Network.from_json(filepath)
mdl.add_nodes_elements_from_network(network=network, element_type='BeamElement',
                                    elset='elset_lines', axes={'ex': [0, 0, 1]})

# Materials

mdl.add(ElasticIsotropic(name='mat_elastic', E=20*10**9, v=0.3, p=1500))

# Sets

mdl.add_set(name='load_pts', selection=[15, 14], type='node')

# Section

mdl.add(CircularSection(name='cirsec', r=.05))
mdl.add(Properties(name='ep', material='mat_elastic', section='cirsec', elset='elset_lines'))

# Displacements
boundary = network.leaves()
mdl.add(PinnedDisplacement(name='disp', nodes=boundary))

# Loads

mdl.add(PointLoad(name='load_weights', nodes='load_pts', z=-100))

# Steps

mdl.add([
    GeneralStep(name='step_bc', displacements=['disp']),
    GeneralStep(name='step_load', loads='load_weights'),
])
mdl.steps_order = ['step_bc', 'step_load']

# Summary

# mdl.summary()

# Run
exe = '/Applications/OpenSees3.2.1/OpenSees'
mdl.analyse_and_extract(software='opensees', exe=exe, fields=['u'])


print(mdl.results['step_load']['nodal']['um'][0])
