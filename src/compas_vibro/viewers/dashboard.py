import math
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from plotly.subplots import make_subplots
from compas.datastructures import Mesh
from compas.geometry import length_vector
from compas.utilities import i_to_rgb


__author__     = ['Tomas Mendez Echenagucia <tmendeze@uw.edu>']
__copyright__  = 'Copyright 2020, Design Machine Group - University of Washington'
__license__    = 'MIT License'
__email__      = 'tmendeze@uw.edu'


class Dashboard(object):
    def __init__(self, structures):
        self.structures = structures
        self.current_structure = 0
        self.rad_curve_fig = None
        self.slider = None
        self.slider_div = None
        self.dropdown = None
        self.all_curves_fig = None
        s = structures[0]
        self.freq_key = {s.results['radiation'][k].frequency: k for k in s.results['radiation']}

    def show(self):
        app = dash.Dash(__name__)
        self.add_dropdown()
        self.add_fslider()
        self.add_sslider()

        rad_curve = dcc.Graph(id='rad_curve',
                              style={'display': 'inline-block', 'width':'100%'})

        rad_comp = dcc.Graph(id='rad_comparison',
                             style={'display': 'inline-block', 'width':'100%'})

        rad_shape = dcc.Graph(id='rad_shape',
                              style={'display': 'inline-block', 'width':'100%'})

        mod_shape1 = dcc.Graph(id='modal_shape1',
                               style={'display': 'inline-block', 'width':'33%'})
        
        mod_shape2 = dcc.Graph(id='modal_shape2',
                               style={'display': 'inline-block', 'width':'33%'})        

        mod_shape3 = dcc.Graph(id='modal_shape3',
                               style={'display': 'inline-block', 'width':'33%'})

        app.layout = html.Div([
            html.Div([
            self.dropdown,
            rad_curve,
            self.fslider,
            mod_shape1,
            mod_shape2,
            mod_shape3,
            ],
            style={'height': '300px', 'width': '60%', 'display': 'inline-block'}
            ),
            html.Div([
            rad_comp,
            rad_shape,
            self.sslider,
            ],
            style={'height': '300px', 'width': '40%', 'display': 'inline-block'})
        ])


        @app.callback(
            Output('rad_curve', 'figure'),
            Input('slider_freq', 'value'),
            Input('structure', 'value'),
            )
        def update_graph1(freq, s_index):
            fig = self.add_rad_curve_fig(freq, s_index)
            return fig

        @app.callback(
            Output('rad_shape', 'figure'),
            Input('slider_freq', 'value'),
            Input('structure', 'value'),
            Input('slider_scale', 'value'),
            )
        def update_graph2(freq, s_index, scale):
            fig = self.add_rad_shape_fig(freq, s_index, scale)
            return fig

        @app.callback(
            Output('rad_comparison', 'figure'),
            Input('structure', 'value'),
            )
        def update_graph3(s_index):
            fig = self.add_all_curves_fig(s_index)  
            return fig

        @app.callback(
            Output('modal_shape1', 'figure'),
            Input('slider_freq', 'value'),
            Input('structure', 'value'),
            )
        def update_graph4(freq, s_scale):
            fig = self.add_modal_shapes(freq, s_scale, 0)
            return fig

        @app.callback(
            Output('modal_shape2', 'figure'),
            Input('slider_freq', 'value'),
            Input('structure', 'value'),
            )
        def update_graph5(freq, s_scale):
            fig = self.add_modal_shapes(freq, s_scale, 1)
            return fig


        @app.callback(
            Output('modal_shape3', 'figure'),
            Input('slider_freq', 'value'),
            Input('structure', 'value'),
            )
        def update_graph6(freq, s_scale):
            fig = self.add_modal_shapes(freq, s_scale, 2)
            return fig
        
        app.run_server(debug=True)

    def add_rad_curve_fig(self, freq, s_index):
        s = self.structures[s_index]
        self.current_structure = s_index
        x1 = [s.results['radiation'][k].frequency for k in s.results['radiation']]
        y1 = [s.results['radiation'][k].radiated_p for k in s.results['radiation']]
        y1 = [(10 * math.log10(w)) + 120 for w in y1]

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x=x1,
                                 y=y1,
                                 mode='lines',
                                 name=s.name,
                                 legendgroup=s.name,
                                 line={'color':'darkcyan'},
                                 opacity=.8,
                                 )
                                 )

        fig.update_layout(xaxis_title='Frequency (Hz)')
        fig.update_layout(yaxis_title='Radiated sound power (dB)')

        if 'modal' in list(s.results.keys()):

            y2 = [s.results['modal'][k].efmass['z'] for k in s.results['modal']]
            mfreqs = [s.results['modal'][k].frequency for k in s.results['modal']]
            font={'size':9, 'color':'red'}
            for i, f in enumerate(mfreqs):
                fig.add_vline(x=f,line_width=.7, line_color='red', opacity=.5)
                fig.add_annotation(x=f, y=max(y1), text='{}'.format(i),font=font, opacity=.5,arrowwidth=.25, arrowcolor='red')
            
            fig.add_trace(go.Scatter(x=mfreqs,
                                    y=y2,
                                    mode='markers',
                                    line={'color':'red'},
                                    opacity=.5,
                                    ),
                                    secondary_y=True,
                                    )

        fig.update_yaxes(
                        #  type='log',
                         secondary_y=True)
        fig.update_yaxes(title_text='Effective mass (kg)',secondary_y=True)
        fig.update_layout(showlegend=False)
        fig.update_layout(margin=dict(l=25, r=25, t=40, b=25), plot_bgcolor='rgb(255,255,255)')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', zerolinecolor='grey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', zerolinecolor='grey')

        
        w = s.results['radiation'][self.freq_key[freq]].radiated_p
        y3 = (10 * math.log10(w)) + 120
        fig.add_trace(go.Scatter(x=[freq],
                                    y=[y3],
                                    mode='markers+text',
                                    text=['{}Hz'.format(freq)],
                                    marker={'color':'LightSkyBlue',
                                            'size':10,
                                            'line':{'color':'blue',
                                                    'width':12},
                                        },
                                    opacity=.5,
                                    textposition='bottom right',
                                    ),
                                    secondary_y=False,
                                    )
        
        fig.update_xaxes(range=(x1[0] - 5, x1[-1] + 5),)
        return fig

    def add_fslider(self):
        s = self.structures[self.current_structure]
        freqs = [s.results['radiation'][k].frequency for k in s.results['radiation']]
        f0 = min(freqs)
        fmax = max(freqs)
        fslider = dcc.Slider(id='slider_freq',
                             min=f0,
                             max=fmax,
                             step=None,
                             value=f0,
                             marks={i:{'label':'', 'style':{'dots':False}} for i in freqs},
                             included=False,
                             tooltip={'always_visible':True},
                             )
        self.fslider = html.Div(fslider,id='slider-div1', style={'display': 'inline-block', 'width':'100%'})

    def add_sslider(self):
        m = 0
        M = 20
        s = .2
        sslider = dcc.Slider(id='slider_scale',
                             min=m,
                             max=M,
                             step=s,
                             value=1,
                             marks={i:{'label':'', 'style':{'dots':False}} for i in range(m, M)},
                             included=False,
                             tooltip={'always_visible':False},
                             )
        self.sslider = html.Div(sslider,id='slider-div2', style={'display': 'inline-block', 'width':'100%'})

    def add_dropdown(self):
        div = html.Div([html.Label('Structure'),
                        dcc.Dropdown(id='structure',
                         options=[{'label': self.structures[i].name, 'value': i} for i in range(len(self.structures))],
                         clearable=False,
                         value=self.current_structure,
                         ),
                         ],
                         style={
                             'width': '50%',
                             'display': 'inline-block',
                             'font-family':'open sans',
                             'font-size':'12px'},
                        )
        self.dropdown = div

    def add_all_curves_fig(self, s_index):

        data = []
        for s in self.structures:
            x1 = [s.results['radiation'][k].frequency for k in s.results['radiation']]
            y1 = [s.results['radiation'][k].radiated_p for k in s.results['radiation']]
            y1 = [(10 * math.log10(w)) + 120 for w in y1]
            if s.name == self.structures[s_index].name:
                width = 4
                opacity = .9
                color = None
            else:
                width = 1
                opacity = .7
                color = None
            curve = go.Scatter(x=x1,
                               y=y1,
                               mode='lines',
                               name=s.name,
                               legendgroup=s.name,
                               opacity=opacity,
                               line=dict(color=color, width=width)
            )
            data.append(curve)
        
        fig  = go.Figure(data=data, layout=None)
        fig.update_yaxes(title_text='Radiated sound power (dB)')
        fig.update_xaxes(title_text='Frequency (Hz)')
        fig.update_layout(showlegend=True)
        fig.update_layout(margin=dict(l=25, r=25, t=40, b=25), plot_bgcolor='rgb(255,255,255)')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', zerolinecolor='grey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', zerolinecolor='grey')
        return fig

    def add_rad_shape_fig(self, freq, s_index, scale):
        mode = self.freq_key[freq]
        s = self.structures[s_index]
        eks = radiating_faces(s)
        faces = [s.elements[ek].nodes for ek in eks]

        f = s.results['radiation'][mode].frequency
        W = s.results['radiation'][mode].radiated_p_faces
        w = s.results['radiation'][mode].radiated_p
        w = round((10 * math.log10(w)) + 120, 2)

        
        f = s.results['harmonic'][mode].frequency
        vertices = []
        nodes = sorted(s.nodes.keys(), key=int)
        # scale = 1.
        scale *= 1e8
        dm = []
        for vk in nodes:
            x, y, z = s.nodes[vk].xyz()
            dx = s.results['harmonic'][mode].displacements[vk]['real']['x']
            dy = s.results['harmonic'][mode].displacements[vk]['real']['y']
            dz = s.results['harmonic'][mode].displacements[vk]['real']['z']
            
            xyz = [x + dx * scale, y + dy * scale, z + dz * scale]
            dm.append(length_vector([dx, dy, dz]))
            vertices.append(xyz)
        # wlist = [(10 * math.log10(W[k])) + 120 for k in W]
        wlist = [W[k] for k in W]

        vertices_ = []
        faces_ = []
        count = 0
        for i, f in enumerate(faces):
            face = []
            for vk in f:
                vertices_.append(vertices[vk])
                face.append(count)
                count += 1
            faces_.append(face)

        mesh = Mesh.from_vertices_and_faces(vertices, faces)
        edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
        line_marker = dict(color='rgb(0,0,0)', width=1.5)
        lines = []
        x, y, z = [], [],  []
        for u, v in edges:
            x.extend([u[0], v[0], [None]])
            y.extend([u[1], v[1], [None]])
            z.extend([u[2], v[2], [None]])

        lines = [go.Scatter3d(x=x, y=y, z=z, mode='lines', line=line_marker)]
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

        # intensity = [d * 1e3 for d in dm]
        intensity = wlist


        intensity_ = []
        for m, fk in enumerate(mesh.face):
            intensity_.append(intensity[m])
            if len(mesh.face[fk]) == 4:
                intensity_.append(intensity[m])

        data = []
        faces = [go.Mesh3d(x=x,
                           y=y,
                           z=z,
                           i=i,
                           j=j,
                           k=k,
                           opacity=1.,
                           # contour={'show':True},
                           # vertexcolor=vcolor,
                           colorbar_title='Amplitude',
                           colorbar_thickness=10,
                           colorscale= 'agsunset', # 'viridis'
                           intensity=intensity_,
                           intensitymode='cell',
                           showscale=True,
                )]
        data.extend(lines)
        data.extend(faces)
        layout = self.make_layout(freq)
        fig  = go.Figure(data=data, layout=layout)
        return fig

    def make_layout(self, freq):
        name = self.structures[self.current_structure].name
        title = '{} - Radiated Sound Power {:.2f}Hz'.format(name, freq)

        layout = go.Layout(title=title,
                           margin=go.layout.Margin(
                           l=2, #left margin
                           r=2, #right margin
                           b=2, #bottom margin
                           t=30, #top margin
                    ),
                          scene=dict(aspectmode='data',
                                    xaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    yaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    zaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)')
                                    ),
                          showlegend=False,
                            )
        return layout

    def make_layout2(self, mode, factor):
        name = self.structures[self.current_structure].name
        # title = '{} - Radiated Sound Power {:.2f}Hz'.format(name, mode)
        title = 'Mode {} - Factor {:0.2f}'.format(mode, factor)

        layout = go.Layout(title=title,
                           title_font_size=12,
                           margin=go.layout.Margin(
                                  l=2, #left margin
                                  r=2, #right margin
                                  b=2, #bottom margin
                                  t=30, #top margin
                    ),
                          scene=dict(aspectmode='data',
                                    xaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    yaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)'),
                                    zaxis=dict(
                                               gridcolor='rgb(255, 255, 255)',
                                               zerolinecolor='rgb(255, 255, 255)',
                                               showbackground=True,
                                               backgroundcolor='rgb(230, 230,230)')
                                    ),
                          showlegend=False,
                            )
        return layout

    def add_modal_shapes(self, freq, s_scale, mode_k):
        
        s = self.structures[s_scale]
        mode = self.freq_key[freq]
        if 'modal' in s.results:
            ks = s.results['harmonic'][mode].modal_coordinates.keys()
            if not ks:
                return go.Figure(data=[], layout=None)
            norm = []
            for k in ks:
                if k != 'f':
                    n = s.results['harmonic'][mode].modal_coordinates[k]['norm']
                    norm.append((n, k))

            norm = sorted(norm)[::-1]
            
            factor, k = norm[mode_k]
            # for factor, k in norm[:3]:
            vertices = []
            nodes = sorted(s.nodes.keys(), key=int)
            scale = 35
            dm = []
            for vk in nodes:
                x, y, z = s.nodes[vk].xyz()
                dx = s.results['modal'][k].displacements['ux'][vk]
                dy = s.results['modal'][k].displacements['uy'][vk]
                dz = s.results['modal'][k].displacements['uz'][vk]
                
                xyz = [x + dx * scale, y + dy * scale, z + dz * scale]
                dm.append(length_vector([dx, dy, dz]))
                vertices.append(xyz)

            vertices_ = []
            faces_ = []
            count = 0
            faces = [s.elements[ek].nodes for ek in s.elements]
            for i, f in enumerate(faces):
                face = []
                for vk in f:
                    vertices_.append(vertices[vk])
                    face.append(count)
                    count += 1
                faces_.append(face)

            mesh = Mesh.from_vertices_and_faces(vertices, faces)
            edges = [[mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)] for u,v in mesh.edges()]
            line_marker = dict(color='rgb(0,0,0)', width=1.5)
            lines = []
            x, y, z = [], [],  []
            for u, v in edges:
                x.extend([u[0], v[0], [None]])
                y.extend([u[1], v[1], [None]])
                z.extend([u[2], v[2], [None]])

            lines = go.Scatter3d(x=x, y=y, z=z, mode='lines', line=line_marker)
            triangles = []
            for face in faces:
                triangles.append(face[:3])
                if len(face) == 4:
                    triangles.append([face[2], face[3], face[0]])
            
            i = [v[0] for v in triangles]
            j = [v[1] for v in triangles]
            l = [v[2] for v in triangles]

            x = [v[0] for v in vertices]
            y = [v[1] for v in vertices]
            z = [v[2] for v in vertices]

            intensity_ = [d * 1e3 for d in dm]
            # m = min(dm)
            # M = max(dm)
            # colors = [i_to_rgb((z-m)/(M-m)) for z in dm]
            # colors = ['rgb({},{},{})'.format(r,g,b) for r,g,b in colors]

            faces = go.Mesh3d(x=x,
                            y=y,
                            z=z,
                            i=i,
                            j=j,
                            k=l,
                            opacity=1.,
                            intensity=intensity_,
                            colorscale= 'viridis',
                            showscale=False,
                    )

            data = [lines, faces]
            layout = self.make_layout2(k, factor)
            fig  = go.Figure(data=data, layout=layout)
            fig.update_layout()
            return fig
        else:
            return go.Figure(data=[], layout=None)


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure
    for i in range(50): print('')
    
    filepath = os.path.join(compas_vibro.DATA, 'structures', 'flat_mesh_20x20_radiation_t10.obj')
    s1 = Structure.from_obj(filepath)
    s1.name = 't10'

    # print(dir(s1.results['modal'][0]))
    # print('')
    # print(s1.results['modal'][0].frequency)

    filepath = os.path.join(compas_vibro.DATA, 'structures', 'flat_mesh_20x20_radiation_t20.obj')
    s2 = Structure.from_obj(filepath)
    s2.name = 't20'

    filepath = os.path.join(compas_vibro.DATA, 'structures', 'flat_mesh_20x20_radiation_t30.obj')
    s3 = Structure.from_obj(filepath)
    s3.name = 't30'

    db = Dashboard([s1, s2, s3])
    db.show()





