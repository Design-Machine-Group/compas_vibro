__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


try:
    import numpy as np
except:
    pass

from compas_vibro.structure.load import PointLoad
from compas.geometry import length_vector

#TODO: the force component is still missing, should it be the vector magnitude? XYZ?



def compute_mobility_matrices(structure, freq_list, fx, fy, fz, damping=.02, backend='ansys'):

    rad_nks = structure.radiating_nodes()
    inc_nks = structure.incident_nodes()

    mm = [[] for _ in range(len(freq_list))]

    fvl = length_vector([fx, fy, fz])

    for ink in inc_nks:
        load = PointLoad(name='pload', nodes=[ink], x=fx, y=fy, z=fz, xx=0, yy=0, zz=0)
        structure.add(load)
        structure.analyze_harmonic(freq_list,
                                   fields=['u'],
                                   backend=backend, 
                                   damping=damping)
        fkeys = structure.results['harmonic']
        for fkey in fkeys:
            structure.results['harmonic'][fkey].compute_node_velocities()
            vr = [structure.results['harmonic'][fkey].velocities[nkey].real for nkey in rad_nks]
            vi = [structure.results['harmonic'][fkey].velocities[nkey].imag for nkey in rad_nks]
            v = [complex(vr[i], vi[i]) for i in range(len(vr))]
            v = [vi / fvl for vi in v]
            
            mm[fkey].append(v)

    mob_mats = []
    for a in mm:
        mob_mats.append(np.array(a))
    return mob_mats



if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    s = Structure.from_obj(os.path.join(compas_vibro.DATA, 'structures', 'flat_10x10.obj'))

    freq_list = list(range(20, 200, 5))
    damping=.02
    fx = 0
    fy = 0
    fz = 1
    mob_mats = compute_mobility_matrices(s, freq_list, fx, fy, fz, damping=damping)

    print(len(mob_mats))
    for mm in mob_mats:
        print(mm.shape)
