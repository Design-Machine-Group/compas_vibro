import gmsh
from compas.utilities import geometric_key
from timber_vibro.meshing.mesh import Mesh
from compas.datastructures import meshes_join
from compas.datastructures import mesh_weld

class GMSH(object):
    def __init__(self, mesh, size):
        self.mesh = mesh
        self.lc = size
        self.half_edges = {}
        
    def remesh(self):
        gmsh.initialize(['-noenv'])
        # gmsh.
        gmsh.model.add(self.mesh.name)

        self.gmsh_add_points()
        self.gmsh_add_lines()
        self.gmsh_add_curve_loops()
        self.gmsh_add_plane_surfaces()

        gmsh.model.geo.synchronize()
        gmsh.model.mesh.generate(2)
        gmsh.option.setNumber("Mesh.Algorithm", 8)

        v = gmsh.model.mesh.get_nodes()[1]
        f = gmsh.model.mesh.getElementFaceNodes(2, 3)
        vertices = [[v[i], v[i+1], v[i+2]] for i in range(0, len(v), 3)]
        faces = [[f[i] - 1, f[i+1] - 1, f[i+2]- 1] for i in range(0, len(f), 3)]
  
        # if '-nopopup' not in sys.argv:
        #     gmsh.fltk.run()

        self.mesh = Mesh.from_vertices_and_faces(vertices, faces)
        gmsh.finalize()
        
    def gmsh_add_points(self):
        for vk in self.mesh.vertices():
            x, y, z = self.mesh.vertex_coordinates(vk)
            gmsh.model.geo.add_point(x, y, z, self.lc, vk)

    def gmsh_add_lines(self):
        for i, (u, v) in enumerate(self.mesh.edges()):
            gmsh.model.geo.add_line(u, v, i + 1)
            self.half_edges[(u, v)] = str(i + 1)
            self.half_edges[(v, u)] = '-{}'.format(i + 1)

    def gmsh_add_curve_loops(self):
        for fk in self.mesh.faces():
            v = self.mesh.face_vertices(fk)
            ek = [self.half_edges[v[-i], v[-i - 1]] for i in range(len(v))]
            a = gmsh.model.geo.add_curve_loop(ek, fk + 1)
            # print(a)

    def gmsh_add_plane_surfaces(self):
        for fk in self.mesh.faces():
            # gmsh.model.geo.addPlaneSurface([fk + 1], fk + 1)
            gmsh.model.geo.addSurfaceFilling([fk + 1], fk + 1)


def remesh_mesh(mesh, size):
    gm = GMSH(mesh, size)
    gm.remesh()
    rmesh = gm.mesh

    cpt_dict = {}

    for fk in mesh.face:
        d = {geometric_key(rmesh.face_centroid(fk_)): fk for fk_ in rmesh.face}
        cpt_dict.update(d)

    for fk in rmesh.face:
        gk = geometric_key(rmesh.face_centroid(fk))
        rmesh.face_attribute(fk, 'set', cpt_dict[gk])
        rmesh.face_attribute(fk, 'is_boundary', mesh.face_attribute(cpt_dict[gk],'is_boundary'))
        rmesh.face_attribute(fk, 'is_fin', mesh.face_attribute(cpt_dict[gk],'is_fin'))


    return rmesh

def remesh_vertices_faces(vertices, faces, size):
    mesh = Mesh.from_vertices_and_faces(vertices, faces)
    gm = GMSH(mesh, size)
    gm.remesh()
    return gm.mesh.to_vertices_and_faces()

def remesh_face_by_face(mesh, size):
    rmeshes = []
    cpt_dict = {}

    for fk in mesh.face:
        vertices = [mesh.vertex_coordinates(vk) for vk in mesh.face_vertices(fk)]
        faces = [range(len(vertices))]
        fmesh = Mesh.from_vertices_and_faces(vertices, faces)
        rmesh = remesh_mesh(fmesh, size)
        rmeshes.append(rmesh)
        d = {geometric_key(rmesh.face_centroid(fk_)): fk for fk_ in rmesh.face}
        cpt_dict.update(d)

    rmesh = meshes_join(rmeshes)
    rmesh = mesh_weld(rmesh)

    for fk in rmesh.face:
        gk = geometric_key(rmesh.face_centroid(fk))
        # for att in mesh.face_attributes(cpt_dict[gk]):
        #     rmesh.face_attribute(fk, att, mesh.face_attribute(cpt_dict[gk],att))
        rmesh.face_attribute(fk, 'set', cpt_dict[gk])
        rmesh.face_attribute(fk, 'is_boundary', mesh.face_attribute(cpt_dict[gk],'is_boundary'))
        rmesh.face_attribute(fk, 'is_fin', mesh.face_attribute(cpt_dict[gk],'is_fin'))

    return rmesh


if __name__ == '__main__':
    import os
    for i in range(50): print('')
    import timber_vibro
    from timber_vibro.plotters import PlotlyMeshViewer
    from timber_vibro.fd import add_fins

    name = 'before_remesh'
    filepath = os.path.join(timber_vibro.DATA, 'meshes',  '{}.json'.format(name))
    mesh = Mesh.from_json(filepath)

    add_fins(mesh, .1)
    mesh = remesh_face_by_face(mesh, .4)
    # mesh = remesh_mesh(mesh, .4)
    pl = PlotlyMeshViewer(mesh)
    pl.color_face_attr = 'set'
    pl.show()
