import os


# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)


def write_preprocess(path, filename):
    cFile = open(os.path.join(path, filename), 'w')
    cFile.write('! Ansys command file written from compas_fea \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.write('/PREP7 \n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.close()


def write_postprocess(path, filename):
    cFile = open(os.path.join(path, filename), 'w')
    cFile.write('! Ansys post-process file written from compas_fea DUDE\n')
    cFile.write('!\n')
    cFile.write('!\n')
    cFile.write('/POST1 \n')
    cFile.write('!\n')
    cFile.close()