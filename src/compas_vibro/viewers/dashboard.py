import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

class Dashboard(object):
    def __init__(self, structures):
        self.structures = structures
        self.current_structure = 0
        self.rad_curve_fig = None
        self.slider = None
        self.slider_div = None

    def show(self):
        app = dash.Dash(__name__)
        self.add_slider()
        self.add_rad_curve_fig()
        graph = dcc.Graph(id='rad_curve', figure=self.rad_curve_fig)
        app.layout = html.Div([graph,
                               self.slider,
                               self.slider_div,
                               ])
        app.run_server(debug=True)

    def add_slider(self):
        s = self.structures[self.current_structure]
        freqs = [s.results['radiation'][k].frequency for k in s.results['radiation']]
        f0 = min(freqs)
        fmax = max(freqs)
        self.slider = dcc.Slider(id='freq',
                                 min=f0,
                                 max=fmax,
                                 step=None,
                                 value=f0,
                                 marks={i:'' for i in freqs},
                                 included=False)
        self.slider_div = html.Div(id='slider-div')

    def add_rad_curve_fig(self):
        s = self.structures[self.current_structure]
        x = [s.results['radiation'][k].frequency for k in s.results['radiation']]
        y = [s.results['radiation'][k].radiated_p for k in s.results['radiation']]
        y = [(10 * math.log10(w)) + 120 for w in y]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # fig= go.Figure(layout_title_text='Radiated Sound Power (dB)')
        fig.add_trace(go.Scatter(x=x,
                                 y=y,
                                 mode='lines',
                                 name=s.name,
                                 legendgroup=s.name,
                                 line={'color':'darkcyan'},
                                 opacity=.8,
                                 )
                                 )

        y = [s.results['modal'][k].efmass['z'] for k in s.results['modal']]
        mfreqs = [s.results['modal'][k].frequency for k in s.results['modal']]
        for f in mfreqs:
            fig.add_vline(x=f,line_width=.7, line_color='red', opacity=.5)
        
        fig.add_trace(go.Scatter(x=mfreqs,
                                 y=y,
                                 mode='markers',
                                #  name=s.name,
                                #  legendgroup=s.name,
                                 line={'color':'red'},
                                 opacity=.5,
                                 ),
                                 secondary_y=True,
                                 )


        fig.update_layout(margin=dict(l=25, r=25, t=40, b=25), plot_bgcolor='rgb(255,255,255)')
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', zerolinecolor='grey')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='lightgrey', zerolinecolor='grey')

        self.rad_curve_fig = fig


if __name__ == '__main__':
    import os
    import compas_vibro
    from compas_vibro.structure import Structure
    for i in range(50): print('')
    
    filepath = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20_radiation_t10.obj')
    s1 = Structure.from_obj(filepath)
    s1.name = 't10'

    # print(dir(s1.results['modal'][0]))
    # print('')
    # print(s1.results['modal'][0].frequency)

    filepath = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20_radiation_t20.obj')
    s2 = Structure.from_obj(filepath)
    s2.name = 't20'

    filepath = os.path.join(compas_vibro.DATA, 'flat_mesh_20x20_radiation_t30.obj')
    s3 = Structure.from_obj(filepath)
    s3.name = 't30'

    db = Dashboard([s1, s2, s3])
    db.show()





