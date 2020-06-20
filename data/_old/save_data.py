from compas_rhino.helpers.mesh import mesh_from_guid
from compas.datastructures import Mesh
import rhinoscriptsyntax as rs
import json

guid = rs.ObjectsByLayer('mesh')
mesh = mesh_from_guid(Mesh, guid)
mesh_data = mesh.to_data()

spts = rs.ObjectsByLayer('spts')
spts = [list(rs.PointCoordinates(pt)) for pt in spts]

fpts = rs.ObjectsByLayer('fpts')
fpts = [list(rs.PointCoordinates(pt)) for pt in fpts]

set_pts = rs.ObjectsByLayer('pt_set')
set_pts = [list(rs.PointCoordinates(pt)) for pt in set_pts]

data = {'pts':spts,'mesh':mesh_data, 'fpts':fpts, 'set_pts':set_pts}
# data = {'mesh': mesh_data}
with open('flat_2x2.json', 'w') as outfile:
    json.dump(data, outfile)
