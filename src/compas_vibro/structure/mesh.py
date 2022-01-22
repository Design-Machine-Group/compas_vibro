from compas.datastructures import Mesh
from compas.utilities import geometric_key_xy
from compas.geometry import centroid_points_xy
from compas.geometry import distance_point_point_xy

class Mesh(Mesh):

    def __init__(self):
        super(Mesh, self).__init__()
        self.default_face_attributes.update({'set':None,
                                             'is_boundary':False,
                                             'is_fin':False})
    
    def centroid_gkey_key(self):
        self.face_gk = {geometric_key_xy(self.face_centroid(fk)): fk for fk in self.faces()}

    def identify_center_face(self):
        self.centroid_gkey_key()
        xyz = [self.vertex_coordinates(k) for k in self.vertex]
        cpt = centroid_points_xy(xyz)
        return self.face_gk[geometric_key_xy(cpt)]

    def identify_faces_within_radius(self, r):
        xyz = [self.vertex_coordinates(k) for k in self.vertex]
        cpt = centroid_points_xy(xyz)
        faces = []
        for fk in self.faces():
            pt = self.face_centroid(fk)
            if distance_point_point_xy(cpt, pt) <= r:
                faces.append(fk)
        return faces

    def identify_center_point(self):
        xyz = [self.vertex_coordinates(k) for k in self.vertex]
        cpt = centroid_points_xy(xyz)
        center = xyz[0]
        for v in self.vertices():
            if distance_point_point_xy(cpt, self.vertex_coordinates(v)) <= distance_point_point_xy(cpt, center):
                center = self.vertex_coordinates(v)
                centerIndex = v
        return centerIndex


if __name__ == '__main__':
    mesh = Mesh()
    print(mesh)
    print(mesh.default_face_attributes)