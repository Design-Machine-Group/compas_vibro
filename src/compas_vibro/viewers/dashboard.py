import dash

class Dashboard(object):
    def __init__(self, structures):
        self.structures = structures

    def show(self):
        pass

if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure
    for i in range(50): print('')
    
    filepath = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20_radiation_t10.obj')
    s1 = Structure.from_obj(filepath)

    filepath = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20_radiation_t20.obj')
    s2 = Structure.from_obj(filepath)

    filepath = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20_radiation_t30.obj')
    s3 = Structure.from_obj(filepath)

    db = Dashboard([s1, s2, s3])
    print(db)



