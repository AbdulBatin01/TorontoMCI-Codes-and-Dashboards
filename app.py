from dash import Dash, html,dcc, Input, Output
import pandas as pd
import plotly.express as px
from data import pd_Data, MCI_by_Occurence, hood_by_MCI_Count

app = Dash(__name__)
data_copy = pd_Data
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig1 = px.pie(MCI_by_Occurence, values='Occurence', names='MCI',
             title='Major Crime Indicator Percentages')
fig1.update_traces(textposition='inside', textinfo='percent+label')
fig1.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

app.layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1(children='TORONTO MCI DASHBOARD', style={
        'textAlign': 'center',
        'color': colors['text']}),
        dcc.Graph(
        id='mci_occur',
        figure=fig1
    ),
html.Div([

        html.Div([
            dcc.Dropdown(
                id='slct_mci',
                options = data_copy['MCI'].unique(),
                value = 'Assault',
                clearable=False,
            ),

        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
                id='slct_ptype',
                options=data_copy['premises_type'].unique(),
                value='House',
                clearable=False,
            ),
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ]),
    
    dcc.Graph(id='Neigh_by_MCI'),
   # dcc.Graph(id='neigh_map'),
])

@app.callback(
    Output('Neigh_by_MCI', 'figure'),
    Input('slct_mci','value'),
    Input('slct_ptype', 'value')
)
def update_graph(mci_slctd,ptype_slctd):
    print(mci_slctd,ptype_slctd)
    print(type(mci_slctd),type(ptype_slctd))

    #container = "The MCI chosen by user was: {}".format(option_slctd)

    data_copy1 = hood_by_MCI_Count.copy()
    data_copy1 = data_copy1[data_copy1["MCI"] == mci_slctd ]
    data_copy1 = data_copy1[data_copy1["premises_type"] == ptype_slctd]
    fig2 = px.bar(data_copy1, x="Neighbourhood", y="Occurence",
              color="MCI", title="Major Crime Indicators per Neighbourhood",
              labels={'Occurence':'Total Crime Cases'}, height=1000)
    fig2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
    )
    return fig2


if __name__ == '__main__':
    app.run_server(debug=True)  