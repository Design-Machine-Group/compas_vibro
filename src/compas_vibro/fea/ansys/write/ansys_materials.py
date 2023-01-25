import os


# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)


def write_materials(structure, output_path, filename):
    materials = structure.materials
    for index, key in enumerate(materials):
        material = materials[key]
        if material.__name__ == 'ElasticIsotropic':
            write_elastic_material(material, index, output_path, filename)
        elif material.__name__ == 'ElasticOrthotropic':
            write_elastic_ortho_material(material, index, output_path, filename)
        elif material.__name__ == 'ConcreteMicroplane':
            write_concrete_microplane_material(material, index, output_path, filename)
        elif material.__name__ in ['ElasticPlastic', 'Steel']:
            write_elasticplastic_material(material, index, output_path, filename)
        else:
            raise ValueError(material.__name__ + ' Type of material is not yet implemented for Ansys')


def write_elastic_material(material, index, output_path, filename):
    E = material.E['E']
    P = material.v['v']
    material_index = index + 1
    density = material.p

    therm_exp = None  # material['therm_exp']
    ref_temp = None  # material['ref_temp']

    cFile = open(os.path.join(output_path, filename), 'a')
    cFile.write('MPTEMP,,,,,,,, \n')
    cFile.write('MPTEMP,1,0  \n')
    string = 'MPDATA,EX,' + str(material_index) + ',,' + str(E) + '\n'
    cFile.write(string)
    string = 'MPDATA,PRXY,' + str(material_index) + ',,' + str(P) + '\n'
    cFile.write(string)
    string = 'MPDATA,DENS,' + str(material_index) + ',,' + str(density) + '\n'
    cFile.write(string)
    if therm_exp:
        cFile.write('MPTEMP,,,,,,,, \n')
        cFile.write('MPTEMP,1,0  \n')
        string = 'MPDATA,ALPX,' + str(material_index) + ',,' + str(therm_exp) + '\n'
        cFile.write(string)
    if ref_temp:
        string = 'MP,REFT,' + str(material_index) + ',' + str(ref_temp) + '\n'
        cFile.write(string)
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_elastic_ortho_material(material, index, output_path, filename):
    Ex, Ey, Ez = material.E['Ex'], material.E['Ey'], material.E['Ez']
    vxy, vyz, vxz = material.v['vxy'], material.v['vyz'], material.v['vxz']
    gx, gy, gx = material.G['Gx'], material.G['Gy'], material.G['Gz']
    material_index = index + 1
    density = material.p

    therm_exp = None  # material['therm_exp']
    ref_temp = None  # material['ref_temp']

    fh = open(os.path.join(output_path, filename), 'a')
    fh.write('MPTEMP,,,,,,,, \n')
    fh.write('MPTEMP,1,0  \n')
    fh.write('MPDATA,EX,{},,{}\n'.format(material_index, Ex))
    fh.write('MPDATA,EY,{},,{}\n'.format(material_index, Ex))
    fh.write('MPDATA,EZ,{},,{}\n'.format(material_index, Ez))
    fh.write('MPDATA,PRXY,{},,{}\n'.format(material_index, vxy))
    fh.write('MPDATA,PRYZ,{},,{}\n'.format(material_index, vyz))
    fh.write('MPDATA,PRXZ,{},,{}\n'.format(material_index, vxz))
    fh.write('MPDATA,GXY,{},,{}\n'.format(material_index, gx)) 
    fh.write('MPDATA,GYZ,{},,{}\n'.format(material_index, gy)) 
    fh.write('MPDATA,GXZ,{},,{}\n'.format(material_index, gx)) 

    string = 'MPDATA,DENS,' + str(material_index) + ',,' + str(density) + '\n'
    fh.write(string)
    if therm_exp:
        fh.write('MPTEMP,,,,,,,, \n')
        fh.write('MPTEMP,1,0  \n')
        string = 'MPDATA,ALPX,' + str(material_index) + ',,' + str(therm_exp) + '\n'
        fh.write(string)
    if ref_temp:
        string = 'MP,REFT,' + str(material_index) + ',' + str(ref_temp) + '\n'
        fh.write(string)
    fh.write('!\n')
    fh.write('!\n')
    fh.close()



def write_elasticplastic_material(material, index, output_path, filename):

    write_elastic_material(material, index, output_path, filename)
    cFile = open(os.path.join(output_path, filename), 'a')
    # cFile.write('TB,MISO,{0}, {0}, {1} ,0 \n'.format(index + 1, len(material.tension['e'])))
    cFile.write('TB, PLASTIC, {0}, ,{1}, MISO \n'.format(index + 1, len(material.tension['e']) + 1))
    cFile.write('TBTEMP, 0  \n')
    cFile.write('TBPT, ,0, 5000 \n')
    for i, j in zip(material.tension['f'], material.tension['e']):
        cFile.write('TBPT, ,{1}, {0}\n'.format(i, j))
    cFile.close()


def write_concrete_microplane_material(material, index, output_path, filename):

    write_elastic_material(material, index, output_path, filename)

    material_index = index + 1
    E = material.E['E']
    P = material.v['v']
    fc = material.fc
    ft = material.ft

    # microplane model version 1
    k = fc / ft
    k0 = (k - 1) / (2 * k * (1 - 2 * P))
    k1 = k0
    k2 = 3 / k / (1 + P) / (1 + P)
    k3 = ft / E
    k4 = 0.9
    k5 = 100

    cFile = open(os.path.join(output_path, filename), 'a')
    cFile.write('PRED,OFF\n')

    cFile.write('tb,mplane,' + str(material_index) + ',,6, ! TB,lab,mat,ntemp,NPTS  \n')
    cFile.write('tbdata,1,' + str(k0) + ',' + str(k1) + ',' + str(k2) + ' !Equiv. Strain Parameter  \n')
    cFile.write('tbdata,4,' + str(k3) + ',' + str(k4) + ',' + str(k5) + ' ! Peerling Damage Function Parameter  \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()
