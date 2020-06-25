import os


# Author(s): Tomas Mendez Echenagucia (github.com/tmsmendez)


def set_current_step(path, filename, step_index):
    cFile = open(os.path.join(path, filename), 'a')
    cFile.write('! \n')
    cFile.write('/POST1 \n')
    cFile.write('SET, ' + str(step_index + 1) + '! \n')
    cFile.write('!\n')
    cFile.close()


def write_loadstep(structure, output_path, filename):
    cFile = open(os.path.join(output_path, filename), 'a')
    cFile.write('! \n')
    cFile.write('LSWRITE ! \n')
    cFile.write('!\n')
    cFile.close()


def write_solve_step(structure, output_path, filename):
    cFile = open(os.path.join(output_path, filename), 'a')
    cFile.write('! \n')
    cFile.write('LSSOLVE, 1, 1, 1! \n')
    cFile.write('!\n')
    cFile.close()
