import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.figure_factory as ff
import plotly.graph_objects as go
import pandas as pd
import numpy as np

df = pd.read_csv('../data/demo_data_ite.csv')

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

#Create dropdowns
options = [{'label':'All Age Groups','value':'All'}]
options.extend([{'label': i, 'value': i} for i in np.sort(df['age group'].unique())])
dropdown_age = dcc.Dropdown(id='dropdown_age',options = options,value='All' )

options = [{'label':'All Gender','value':'All'}]
options.extend([{'label': i, 'value': i} for i in np.sort(df['gender'].unique())])
dropdown_gender = dcc.Dropdown(id='dropdown_gender',options = options,value='All')

options = [{'label':'All Frequency','value':'All'}]
options.extend([{'label': i, 'value': i} for i in np.sort(df['exercise frequency'].unique())])
dropdown_ec = dcc.Dropdown(id='dropdown_ec',options = options,value='All')

options = [{'label':'All Income Groups','value':'All'}]
options.extend([{'label': i, 'value': i} for i in np.sort(df['income group'].unique())])
dropdown_income = dcc.Dropdown(id='dropdown_income',options = options, value='All')


options = [{'label':'All Condition Groups','value':'All'}]
options.extend([{'label': i, 'value': i} for i in np.sort(df['pre existing conditions'].unique())])
dropdown_pre = dcc.Dropdown(id='dropdown_pre',options = options, value='All')

options = [{'label':'All Diet Groups','value':'All'}]
options.extend([{'label': i, 'value': i} for i in np.sort(df['vegetarian/vegan'].unique())])
dropdown_diet = dcc.Dropdown(id='dropdown_diet',options = options, value='All')

#Build control card and design layout
controls = dbc.Card(
    [
        dbc.FormGroup([dbc.Label("Select Age Group"),dropdown_age,]),
        dbc.FormGroup([dbc.Label("Select Gender"),dropdown_gender,]),
        dbc.FormGroup([dbc.Label("Pre Existing Conditions?"),dropdown_pre,]),
        dbc.FormGroup([dbc.Label("Exercise Frequency"),dropdown_ec,]),
        dbc.FormGroup([dbc.Label("Low Income Status?"),dropdown_income,]),
        dbc.FormGroup([dbc.Label("Vegetarian/Vegan?"),dropdown_diet]),

    ],
    body=True,
)

app.layout = dbc.Container(
    [
        html.H1("Exploring the Effect of Health Intervention"),
        html.Hr(),
        dbc.Row(
            [
                dbc.Col(controls, md=3),
                dbc.Col(dcc.Graph(id="distplot"), md=9),
            ],
            align="center",
        ),
    ],
    fluid=True,
)

@app.callback(Output('distplot', 'figure'),
              [Input('dropdown_age', 'value'),
              Input('dropdown_gender','value'),
              Input('dropdown_pre','value'),
              Input('dropdown_ec','value'),
              Input('dropdown_income','value'),
              Input('dropdown_diet','value')])

def update_graph(age_value,gender_value,pre_value,ec_value,income_value,diet_value):
    df_sub = df[df['age group'] == age_value] if age_value != 'All' else df
    df_sub = df_sub[df_sub['gender'] == gender_value] if gender_value != 'All' else df_sub
    df_sub = df_sub[df_sub['pre existing conditions'] == pre_value] if pre_value != 'All' else df_sub
    df_sub = df_sub[df_sub['exercise frequency'] == ec_value] if ec_value != 'All' else df_sub
    df_sub = df_sub[df_sub['income group'] == income_value] if income_value != 'All' else df_sub
    df_sub = df_sub[df_sub['vegetarian/vegan'] == diet_value] if diet_value != 'All' else df_sub
    
    group_labels = ['All Sample','Subgroup']
    colors = ['rgb(192, 192, 191)', 'rgb(255, 153, 51)']
    fig = ff.create_distplot([df['cate_t'],df_sub['cate_t']],group_labels,colors=colors,bin_size=0.1)
    fig.add_shape(dict(type="line",x0=np.mean(df['cate_t']),y0=0,x1=np.mean(df['cate_t']),y1=0.85,
                       line=dict(color='rgb(192, 192, 191)',width=2,dash="dot")))
    fig.add_shape(dict(type="line",x0=np.mean(df_sub['cate_t']),y0=0,x1=np.mean(df_sub['cate_t']),y1=0.85,
                       line=dict(color='rgb(255, 102, 0)',width=2,dash="dot")))

    fig.update_shapes(dict(xref='x', yref='y'))
    
    fig.add_trace(go.Scatter(x=[1,1],y=[0.8,0.7],
    text=["Mean ITE (Subgroup) = "+str(round(np.mean(df_sub['cate_t']),2)),
          "Mean ITE (All) = "+str(round(np.mean(df['cate_t']),2))],
         mode="text",showlegend=False
    ))



    fig.update_layout(title_text='Treatment Effect Distribution for the Specified Subgroup',height=600)

    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
