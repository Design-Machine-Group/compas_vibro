__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'




def compute_mobility_matrix(structure):
    nks = structure.radiating_nodes()
    


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    s = Structure.from_obj(os.path.join(compas_vibro.DATA, 'structures', 'flat_10x10.obj'))
    compute_mobility_matrix(s)