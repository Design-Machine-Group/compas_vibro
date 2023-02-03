from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'

from math import sqrt
from math import pi
from math import copysign

import plotly.graph_objects as go

from compas_vibro.structure import Mesh

from compas.geometry import subtract_vectors
from compas.geometry import normalize_vector
from compas.geometry import cross_vectors
from compas.geometry import scale_vector
from compas.geometry import add_vectors
from compas.geometry import length_vector
from compas.geometry import rotate_points
from compas.geometry import dot_vectors

# TODO: Add harmonic mode participation factors
# TODO: Add modal effective masses
# TODO: Add static scale slider option - THIS PROBABLY REQUIRES DASH
# TODO: Add displacement colors for beam/link elements
# TODO: Visualize prestress / colors with no results (initial condition)


class StructureViewer(object):

    def __init__(self, structure):
        self.structure                  = structure
        self.data                       = []
        self.layout                     = None
        self.sliders                    = None
        self.show_point_loads           = True
        self.show_supports              = True
        self.show_beams                 = True
        self.show_beam_sections         = True
        self.show_node_labels           = False
        self.show_rad_nodes             = False
        self.show_incident_nodes        = False
        self.contains_supports          = False
        self.beam_sec_names             = structure.beam_sections

        self.shell_elements             = []
        self.beam_elements              = []
        self.solid_elements             = []
        self.mesh                       = None

        self.modal_scale                = 4.
        self.harmonic_scale             = 2e7
        self.static_scale               = 2e5
        self.displacement_colorscale    =  'inferno'  # 'rainbow'  #'Portland' # 'Agsunset'
        self.bar_mode                   = 'displacements'
        self.beam_line_width            = 10
        self.show_legend                = True

    @property
    def num_traces(self):
        n = 0
        if self.shell_elements:
            n += 2
        if self.show_beams:
            if self.beam_elements:
                if self.show_beam_sections:
                    n += 2
                else:
                    n += 1
        return n
            
    def separate_element_types(self):
        for epk in self.structure.element_properties:
            section = self.structure.element_properties[epk].section
            sec_name = self.structure.sections[section].__name__
            if  sec_name == 'ShellSection' or sec_name == 'SolidSection':
                el_keys = self.structure.element_properties[epk].elements
                if el_keys == None:
                    elset = self.structure.element_properties[epk].elset
                    el_keys = self.structure.sets[elset].selection
                self.shell_elements.extend(el_keys)
            elif  sec_name in self.beam_sec_names:
                el_keys = self.structure.element_properties[epk].elements
                if el_keys == None:
                    elset = self.structure.element_properties[epk].elset
                    el_keys = self.structure.sets[elset].selection
                self.beam_elements.extend(el_keys)

    def make_shell_mesh(self, mode=None, frequency=None, load_step=None):

        elements = self.shell_elements
        nodes = sorted(self.structure.nodes.keys(), key=int)

        if mode != None:
            vertices = []
            for vk in nodes:
                vertices.append(self.move_node(vk, mode=mode))
        elif frequency != None:
            vertices = []
            for vk in nodes:
                vertices.append(self.move_node(vk, frequency=frequency))
        elif load_step != None:
            vertices = []
            for vk in nodes:
                vertices.append(self.move_node(vk, load_step=load_step))

        else:
            vertices = [self.structure.nodes[vk].xyz() for vk in nodes]
        faces = [self.structure.elements[ek].nodes for ek in elements]
        self.mesh = Mesh.from_vertices_and_faces(vertices, faces)
        self.mesh.cull_vertices()

    def make_layout(self):
        name = self.structure.name
        title = '{0} - Structure'.format(name)
        layout = go.Layout(title=title,
                          scene=dict(aspectmode='data',
                                    xaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=False,
                                               showgrid=False,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    yaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=False,
                                               showgrid=False,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    zaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=False,
                                               showgrid=False,
                                               backgroundcolor='rgb(230, 230,230)')
                                    ),
                          showlegend=True,
                            )
        self.layout = layout

    def add_sliders(self, modes=None, frequencies=None):
        
        nt = self.num_traces

        if modes:
            keys = modes
            plot_type = 'modal'
        if frequencies:
            keys = frequencies
            plot_type = 'harmonic'
            
        steps = []
        for i in keys:
            name = self.structure.name
            if plot_type == 'modal':
                prefix = 'Mode: '
                f = round(self.structure.results[plot_type][i].frequency, 4)
                title = '{0} - Modal Analysis - mode {1} - {2}Hz'.format(name, i, f)
                step_label = str(i)
            if plot_type == 'harmonic':
                prefix = 'Frequency: '
                f = round(self.structure.results[plot_type][i].frequency, 4)
                title = '{0} - Analysis - {1}Hz'.format(name, f)
                step_label = str(f)
            # else:
            #     title = '{0} - Analysis'.format(name)
            step = dict(
                method="update",
                args=[{"visible": [False] * len(self.data)},
                    {"title": title}],
                label=step_label)


            step["args"][0]["visible"][i * nt] = True
            step["args"][0]["visible"][i * nt + 1] = True
            
            if nt > 2:
                step["args"][0]["visible"][i * nt + 2] = True
                step["args"][0]["visible"][i * nt + 3] = True
            step["args"][0]["visible"][-1] = True
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": prefix},
            pad={"t": 50},
            steps=steps
        )]

        self.sliders = sliders

    def plot_3d_beams(self, mode=None, frequency=None, load_step=None):
        elements = self.beam_elements
        beam_mesh = Mesh()
        for ek in elements:
            epk = self.structure.elements[ek].element_property
            section = self.structure.element_properties[epk].section
            sec_name = self.structure.sections[section].__name__
            if sec_name == 'ISection':
                sec_pts = self.make_isection(ek, section, mode=mode, frequency=frequency, load_step=load_step)
            elif sec_name == 'RectangularSection':
                sec_pts = self.make_recsection(ek, section, mode=mode, frequency=frequency, load_step=load_step)
            elif sec_name == 'BoxSection':
                sec_pts = self.make_boxsection(ek, section, mode=mode, frequency=frequency,  load_step=load_step)
            elif sec_name in ['TieSection', 'TrussSection', 'StrutSection']:
                sec_pts = self.make_axialsection(ek, section, mode=mode, frequency=frequency,  load_step=load_step)
            self.add_beam_to_mesh(beam_mesh, sec_pts, ek, mode, frequency, load_step)
        self.add_beams_mesh(beam_mesh)

    def add_beams_mesh(self, beam_mesh):
        edges = [[beam_mesh.vertex_coordinates(u), beam_mesh.vertex_coordinates(v)] for u,v in beam_mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        lines = [go.Scatter3d(name='Beam elements',
                              x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              line=line_marker,
                              legendgroup='Beam Elements',
                              )]

        vertices, faces = beam_mesh.to_vertices_and_faces()

        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        faces = [go.Mesh3d(name='Beam elements',
                           x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           opacity=1.,
                           color='#1F77B4',
                           showscale=False,
                           legendgroup='Beam Elements',
                )]
        self.data.extend(lines)
        self.data.extend(faces)

    def add_beam_to_mesh(self, beam_mesh, sec_pts_list, ek, mode=None, frequency=None,  load_step=None):
        
        u, v = self.structure.elements[ek].nodes
        if mode != None:
            u_ = self.move_node(u, mode=mode)
            v_ = self.move_node(v, mode=mode)
        elif frequency != None:
            u_ = self.move_node(u, frequency=frequency)
            v_ = self.move_node(v, frequency=frequency)
        elif load_step != None:
            u_ = self.move_node(u, load_step=load_step)
            v_ = self.move_node(v, load_step=load_step) 
        else:
            u_, v_ = self.structure.node_xyz(u), self.structure.node_xyz(v)

        z = subtract_vectors(v_, u_)
        for sec_pts in sec_pts_list:
            sk = [beam_mesh.add_vertex(attr_dict={'x':p[0], 'y':p[1], 'z':p[2]}) for p in sec_pts]
            sec_pts_ = [add_vectors(u, z) for u in sec_pts]
            sk_ = [beam_mesh.add_vertex(attr_dict={'x':p[0], 'y':p[1], 'z':p[2]}) for p in sec_pts_]
            
            for i in range(len(sec_pts) -1):
                # mesh.add_face([sk[i], sk[i + 1], sk_[i]])
                beam_mesh.add_face([sk[i], sk[i + 1], sk_[i + 1], sk_[i]])

    def make_isection(self, ek, section, mode=None, frequency=None, load_step=None):
        u, v = self.structure.elements[ek].nodes
        if mode != None:
            u_ = self.move_node(u, mode=mode)
            v_ = self.move_node(v, mode=mode)
        elif frequency != None:
            u_ = self.move_node(u, frequency=frequency)
            v_ = self.move_node(v, frequency=frequency)
        elif load_step != None:
            u_ = self.move_node(u, load_step=load_step)
            v_ = self.move_node(v, load_step=load_step)
        else:
            u_, v_ = self.structure.node_xyz(u), self.structure.node_xyz(v)
        z = subtract_vectors(u_, v_)
        x = normalize_vector(self.structure.elements[ek].axes['x'])
        y = normalize_vector(cross_vectors(x, z))
        b = self.structure.sections[section].geometry['b']
        h = self.structure.sections[section].geometry['h']
        tf = self.structure.sections[section].geometry['tf']
        tw = self.structure.sections[section].geometry['tw']

        h2 = scale_vector(y, h / 2.)
        b2 = scale_vector(x, b /2.)
        h2_ = scale_vector(y, -h / 2.)
        b2_ = scale_vector(x, -b /2.)
        tfv = scale_vector(y, tf)
        tfv_ = scale_vector(y, -tf)
        twv = scale_vector(x, tw / 2.)
        twv_ = scale_vector(x, -tw / 2.)

        p0 = add_vectors(u_, add_vectors(b2_, h2_))
        p1 = add_vectors(p0, scale_vector(b2, 2))
        p2 = add_vectors(p1, tfv)
        p3 = add_vectors(p2, subtract_vectors(twv, b2))
        p11 = add_vectors(p0, tfv)
        p10 = add_vectors(p11, subtract_vectors(twv_, b2_))

        p7 = add_vectors(u_, add_vectors(h2, b2_))
        p6 = add_vectors(u_, add_vectors(h2, b2))
        p5 = add_vectors(p6, tfv_)
        p4 = add_vectors(p5, subtract_vectors(twv, b2))
        p8 = add_vectors(p7, tfv_)
        p9 = add_vectors(p8, subtract_vectors(twv_, b2_))

        return [[p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p0]]

    def make_recsection(self, ek, section, mode=None, frequency=None, load_step=None):
        u, v = self.structure.elements[ek].nodes
        if mode != None:
            u_ = self.move_node(u, mode=mode)
            v_ = self.move_node(v, mode=mode)
        elif frequency != None:
            u_ = self.move_node(u, frequency=frequency)
            v_ = self.move_node(v, frequency=frequency)
        elif load_step != None:
            u_ = self.move_node(u, load_step=load_step)
            v_ = self.move_node(v, load_step=load_step)
        else:
            u_, v_ = self.structure.node_xyz(u), self.structure.node_xyz(v)
        z = subtract_vectors(u_, v_)
        x = normalize_vector(self.structure.elements[ek].axes['x'])
        y = normalize_vector(cross_vectors(x, z))
        b = self.structure.sections[section].geometry['b']
        h = self.structure.sections[section].geometry['h']

        h2 = scale_vector(y, h / 2.)
        b2 = scale_vector(x, b / 2.)
        h2_ = scale_vector(y, -h / 2.)
        b2_ = scale_vector(x, -b /2.)

        p0 = add_vectors(u_, add_vectors(h2_, b2_))
        p1 = add_vectors(u_, add_vectors(h2_, b2))
        p2 = add_vectors(u_, add_vectors(h2, b2))
        p3 = add_vectors(u_, add_vectors(h2, b2_))

        return [[p0, p1, p2, p3, p0]]

    def make_boxsection(self, ek, section, mode=None, frequency=None, load_step=None):
        u, v = self.structure.elements[ek].nodes
        if mode != None:
            u_ = self.move_node(u, mode=mode)
            v_ = self.move_node(v, mode=mode)
        elif frequency != None:
            u_ = self.move_node(u, frequency=frequency)
            v_ = self.move_node(v, frequency=frequency)
        elif load_step != None:
            u_ = self.move_node(u, load_step=load_step)
            v_ = self.move_node(v, load_step=load_step)
        else:
            u_, v_ = self.structure.node_xyz(u), self.structure.node_xyz(v)
        z = subtract_vectors(u_, v_)
        x = normalize_vector(self.structure.elements[ek].axes['x'])
        y = normalize_vector(cross_vectors(x, z))
        b = self.structure.sections[section].geometry['b']
        h = self.structure.sections[section].geometry['h']
        tf = self.structure.sections[section].geometry['tf']
        tw = self.structure.sections[section].geometry['tw']

        h2 = scale_vector(y, h / 2.)
        b2 = scale_vector(x, b /2.)
        h2_ = scale_vector(y, -h / 2.)
        b2_ = scale_vector(x, -b /2.)
        tfv = scale_vector(y, tf)
        tfv_ = scale_vector(y, -tf)
        twv = scale_vector(x, tw)
        twv_ = scale_vector(x, -tw)

        p0 = add_vectors(u_, add_vectors(h2_, b2_))
        p1 = add_vectors(u_, add_vectors(h2_, b2))
        p2 = add_vectors(u_, add_vectors(h2, b2))
        p3 = add_vectors(u_, add_vectors(h2, b2_))

        p4 = add_vectors(p0, add_vectors(twv, tfv))
        p5 = add_vectors(p1, add_vectors(twv_, tfv))
        p6 = add_vectors(p2, add_vectors(twv_, tfv_))
        p7 = add_vectors(p3, add_vectors(twv, tfv_))

        return [[p0, p1, p2, p3, p0], [p4, p5, p6, p7, p4]]

    def make_axialsection(self, ek, section, mode=None, frequency=None, load_step=None):
        u, v = self.structure.elements[ek].nodes
        if mode != None:
            u_ = self.move_node(u, mode=mode)
            v_ = self.move_node(v, mode=mode)
        elif frequency != None:
            u_ = self.move_node(u, frequency=frequency)
            v_ = self.move_node(v, frequency=frequency)
        elif load_step != None:
            u_ = self.move_node(u, load_step=load_step)
            v_ = self.move_node(v, load_step=load_step)
        else:
            u_, v_ = self.structure.node_xyz(u), self.structure.node_xyz(v)
        z = subtract_vectors(u_, v_)
        x = normalize_vector(self.structure.elements[ek].axes['x'])
        y = normalize_vector(cross_vectors(x, z))
        area = self.structure.sections[section].geometry['A']
        radius = sqrt(area / pi)

        pt = add_vectors(u_, scale_vector(x, radius))
        pts = [pt]
        num = 5
        angle = (2 * pi) / num
        for i in range(1, num):
            pt_ = rotate_points([pt], angle * i, axis=z, origin=u_)
            pts.append(pt_[0])
        pts.append(pt)
        return [pts]

    def move_node(self, nk, mode=None, frequency=None, load_step=None):
        x, y, z = self.structure.nodes[nk].xyz()
        if mode != None:
            s = self.modal_scale
            plot_type = 'modal'
            dx = self.structure.results[plot_type][mode].displacements['ux'][nk]
            dy = self.structure.results[plot_type][mode].displacements['uy'][nk]
            dz = self.structure.results[plot_type][mode].displacements['uz'][nk]

        elif frequency != None:
            s = self.harmonic_scale
            plot_type = 'harmonic'
            dx = self.structure.results[plot_type][frequency].displacements[nk]['real']['x']
            dy = self.structure.results[plot_type][frequency].displacements[nk]['real']['y']
            dz = self.structure.results[plot_type][frequency].displacements[nk]['real']['z']

        elif load_step != None:
            s = self.static_scale
            plot_type = 'static'
            dx = self.structure.results[plot_type][load_step].displacements['ux'][nk]
            dy = self.structure.results[plot_type][load_step].displacements['uy'][nk]
            dz = self.structure.results[plot_type][load_step].displacements['uz'][nk]

        return [x + dx * s, y + dy * s, z + dz * s]

    def plot_beam_lines(self):
        elements = []
        for epk in self.structure.element_properties:
            section = self.structure.element_properties[epk].section
            sec_name = self.structure.sections[section].__name__
            if  sec_name in self.beam_sec_names:
                el_keys = self.structure.element_properties[epk].elements
                if el_keys == None:
                    elset = self.structure.element_properties[epk].elset
                    el_keys = self.structure.sets[elset].selection
                elements.extend(el_keys)

        attrs = ['elset', 'is_rad', 'material', 'section', 'base', 'height']
        lines = []
        x, y, z = [], [],  []
        text = []
        for ek in elements:
            u, v = self.structure.elements[ek].nodes
            u = self.structure.node_xyz(u)
            v = self.structure.node_xyz(v)
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

            ep = self.structure.elements[ek].element_property
            ep = self.structure.element_properties[ep]

            string = 'ekey:{}<br>'.format(ek)
            for att in attrs:
                val = 'None'
                if att == 'elset':
                    val = ep.elset
                elif att == 'is_rad':
                    val = ep.is_rad
                elif att == 'material':
                    val = ep.material
                elif att == 'section':
                    val = self.structure.sections[ep.section].__name__
                elif att == 'base' and 'b' in self.structure.sections[ep.section].geometry.keys():
                    val = self.structure.sections[ep.section].geometry['b']
                elif att == 'height'and 'h' in self.structure.sections[ep.section].geometry.keys():
                    val = self.structure.sections[ep.section].geometry['h']
                string += '{}: {}<br>'.format(att, val)
            text.append(string)

        line_marker = dict(color='rgb(0,0,200)', width=self.beam_line_width)
        lines = [go.Scatter3d(x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              text=text,
                              hoverinfo='text',
                              line=line_marker,
                            #   lighting={'ambient': 1}
                              )]
        self.data.extend(lines)

    def plot_shell_shape(self, mode=None, visualization_type='modal'):

        mesh = self.mesh
        vertices, faces = mesh.to_vertices_and_faces()
        elements = self.shell_elements

        linecolor = 'rgb(100,100,100)'  #'rgb(255,255,255)'
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color=linecolor, width=2)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        # x = []
        # y = []
        # z = []

        lines = [go.Scatter3d(name='Shell elements',
                              x=x,
                              y=y,
                              z=z,
                              mode='lines',
                              line=line_marker,
                              legendgroup='Shell elements',
                              )]
        triangles = []
        for face in faces:
            triangles.append(face[:3])
            if len(face) == 4:
                triangles.append([face[2], face[3], face[0]])
        
        i = [v[0] for v in triangles]
        j = [v[1] for v in triangles]
        k = [v[2] for v in triangles]

        x = [v[0] for v in vertices]
        y = [v[1] for v in vertices]
        z = [v[2] for v in vertices]

        if self.bar_mode == 'properties':
            showscale = False
            intensitymode = 'cell'
            colorscale = 'Emrld_r'
            attrs = ['elset', 'is_rad', 'material', 'thickess']
            intensity_ = []
            text = []
            for ek in elements:
                ep = self.structure.elements[ek].element_property
                ep = self.structure.element_properties[ep]
                intensity_.append(int(ep.is_rad) + .1)
                string = 'ekey:{}<br>'.format(ek)
                for att in attrs:
                    if att == 'elset':
                        val = ep.elset
                    elif att == 'is_rad':
                        val = ep.is_rad
                    elif att == 'material':
                        val = ep.material
                    elif att == 'thickess':
                        if 't' in self.structure.sections:
                            val = self.structure.sections[ep.section].geometry['t']
                        else:
                            val = ''
                    string += '{}: {}<br>'.format(att, val)
                text.append(string)
                if len(self.structure.elements[ek].nodes) == 4:
                    intensity_.append(int(ep.is_rad) + .1)
                    text.append(string)

        elif self.bar_mode == 'displacements':
            showscale = True
            intensitymode = None
            colorscale = self.displacement_colorscale
            intensity_ = []
            text = []
            if mode == None:
                mode = 0
            # for nk in self.structure.nodes:
            for nk in mesh.vertex:
                normal = mesh.vertex_normal(nk)
                dx = self.structure.results[visualization_type][mode].displacements['ux'][nk]
                dy = self.structure.results[visualization_type][mode].displacements['uy'][nk]
                dz = self.structure.results[visualization_type][mode].displacements['uz'][nk]
                vsign = copysign(1, dot_vectors([dx, dy, dz], normal))
                lv = length_vector([dx, dy, dz]) * vsign
                intensity_.append(lv)
                text.append(lv)

        faces = [go.Mesh3d(name='Shell elements',
                           x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           opacity=1.,
                           colorbar_title=self.bar_mode,
                           colorbar_thickness=10,
                           colorscale=colorscale,
                           intensity=intensity_,
                           intensitymode=intensitymode,
                           text=text,
                           hoverinfo='text',
                           showscale=showscale,
                           legendgroup='Shell elements',
                )]
        self.data.extend(lines)
        self.data.extend(faces)

    def plot_supports(self):
        dots = []
        red = 'rgb(255, 0, 0)'
        green = 'rgb(0, 255, 0)'
        for dk in self.structure.displacements:
            nodes = self.structure.displacements[dk].nodes
            x = [self.structure.nodes[nk].x for nk in nodes]
            y = [self.structure.nodes[nk].y for nk in nodes]
            z = [self.structure.nodes[nk].z for nk in nodes]
            n = self.structure.displacements[dk].__name__
            if n == 'FixedDisplacement':
                color = red
            else:
                color = green
            dots.append(go.Scatter3d(name=n, x=x, y=y, z=z, mode='markers', marker_color=color))
        self.data.extend(dots)

    def plot_point_loads(self):
        dots = []
        color = 'rgb(255, 215, 0)'  # orange
        for lk in self.structure.loads:
            load = self.structure.loads[lk]
            n = load.__name__
            if load.__name__ == 'PointLoad':
                nodes = load.nodes
                x = [self.structure.nodes[nk].x for nk in nodes]
                y = [self.structure.nodes[nk].y for nk in nodes]
                z = [self.structure.nodes[nk].z for nk in nodes]
                px = [load.components['x'] for _ in range(len(x))]
                py = [load.components['y'] for _ in range(len(x))]
                pz = [load.components['z'] for _ in range(len(x))]
                dots.append(go.Cone(name=n, x=x, y=y, z=z, u=px, v=py, w=pz, showscale=False, sizemode='scaled', sizeref=.12))
                # dots.append(go.Scatter3d(name=n, x=x, y=y, z=z, mode='markers',marker_color=color))
        self.data.extend(dots)

    def plot_node_labels(self):
        dots = []
        nodes = self.structure.nodes.keys()
        x = [self.structure.nodes[nk].x for nk in nodes]
        y = [self.structure.nodes[nk].y for nk in nodes]
        z = [self.structure.nodes[nk].z for nk in nodes]
        text = [nk for nk in nodes]
        dots = [go.Scatter3d(x=x, y=y, z=z, text=text, mode='markers+text')]
        self.data.extend(dots)

    def plot_rad_nodes(self):
        dots = []
        color = '#CCFF00'
        nodes = self.structure.radiating_nodes()

        x = [self.structure.nodes[nk].x for nk in nodes]
        y = [self.structure.nodes[nk].y for nk in nodes]
        z = [self.structure.nodes[nk].z for nk in nodes]

        dots.append(go.Scatter3d(name='radiading_nodes', x=x, y=y, z=z, mode='markers', marker_color=color))
        self.data.extend(dots)

    def plot_incident_nodes(self):
        dots = []
        color = '#CA38A8'
        nodes = self.structure.incident_nodes()

        x = [self.structure.nodes[nk].x for nk in nodes]
        y = [self.structure.nodes[nk].y for nk in nodes]
        z = [self.structure.nodes[nk].z for nk in nodes]

        dots.append(go.Scatter3d(name='incident_nodes', x=x, y=y, z=z, mode='markers', marker_color=color))
        self.data.extend(dots)

    def show_structure(self):
        self.make_shell_mesh()
        if self.shell_elements:
            self.plot_shell_shape()
        
        if self.beam_elements:
            if self.show_beam_sections:
                self.plot_3d_beams()
            else:
                self.plot_beam_lines()    
        
        if self.show_point_loads:
            self.plot_point_loads()
        
        if self.show_node_labels:
            self.plot_node_labels()
        
        if self.show_supports:
            self.plot_supports()

        if self.show_rad_nodes:
            self.plot_rad_nodes()

        if self.show_incident_nodes:
            self.plot_incident_nodes()
        
        fig = go.Figure(data=self.data, layout=self.layout)
        fig.show()

    def show_static(self):
        self.make_shell_mesh(load_step=0)
            
        if self.shell_elements:
            self.plot_shell_shape(visualization_type='static')

        if self.beam_elements and self.show_beams:
            if self.show_beam_sections:
                self.plot_3d_beams(load_step=0)
            else:
                self.plot_beam_lines(load_step=0)  

        if self.show_supports:
            self.plot_supports()

        fig = go.Figure(data=self.data, layout=self.layout)

        fig.update_layout(sliders=self.sliders)
        fig.update_layout(legend_orientation="h")

        fig.show()

    def show_modal(self):
        modes = sorted(self.structure.results['modal'].keys())
        for mode in modes:
            self.make_shell_mesh(mode=mode)
            
            if self.shell_elements:
                self.plot_shell_shape(mode=mode)
            
            if self.beam_elements and self.show_beams:
                if self.show_beam_sections:
                    self.plot_3d_beams(mode=mode)
                else:
                    self.plot_beam_lines()  

        if self.show_supports:
            self.plot_supports()

        self.add_sliders(modes=modes)
        fig = go.Figure(data=self.data, layout=self.layout)

        for i in range(4, len(modes) * self.num_traces):
            fig.data[i].visible = False

        fig.update_layout(sliders=self.sliders)
        fig.update_layout(showlegend=self.show_legend)
        fig.show()

    def show_harmonic(self):
        frqs = sorted(self.structure.results['harmonic'].keys())
        for f in frqs:
            self.make_shell_mesh(frequency=f)
            
            if self.shell_elements:
                self.plot_shell_shape()
            
            if self.beam_elements and self.show_beams:
                if self.show_beam_sections:
                    self.plot_3d_beams(frequency=f)
                else:
                    self.plot_beam_lines()  

        if self.show_supports:
            self.plot_supports()

        self.add_sliders(frequencies=frqs)
        fig = go.Figure(data=self.data, layout=self.layout)

        for i in range(self.num_traces, len(frqs) * self.num_traces):
            fig.data[i].visible = False

        fig.update_layout(sliders=self.sliders)
        fig.show()

    def show(self, result=None):
        
        self.separate_element_types()
        self.make_layout()

        if result == None:
            self.bar_mode = 'properties'
            self.show_structure()
        elif result == 'modal' or result == 'Modal':
            self.show_modal()
        elif result == 'harmonic' or result == 'Harmonic':
            self.show_harmonic()
        elif result == 'static' or result == 'Static':
            self.show_static()
        else:
            raise ValueError('This type of result plot has not been implemented')
        
if __name__ == '__main__':

    import os
    import compas_vibro
    from compas_vibro.structure import Structure

    # file = 'shell_beams_modal.obj'
    # file = 'shell_beams_harmonic.obj'
    # file = 'shell_boxbeams_modal.obj'
    # file = 'flat_web.obj'
    # file = 'volmesh.obj'
    file = 'opensees_flat_mesh_100x100_modal.obj'
    fp = os.path.join(compas_vibro.DATA, 'structures', file)
    # fp = os.path.join(compas_vibro.TEMP, file)
    s = Structure.from_obj(fp)

    v = StructureViewer(s)
    v.modal_scale = 40
    # v.show_beam_sections = False
    v.show_node_labels = False
    v.show('modal')
    