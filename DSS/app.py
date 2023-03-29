import pandas as pd
from dash import Dash, dash_table, html, dcc

df = pd.read_csv('sample_data.csv', delimiter=';')
df2 = pd.read_csv('results.csv')
print({i: i for i in df.columns})
app = Dash(__name__)

app.layout = html.Div([
    html.H1("FaaS Decision Support System"),
    html.P("Use the interactive table below to sort and filter the data. "),
    html.Div([dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns],
                                    # editable=True,
                                    filter_action="native",
                                    sort_action="native",
                                    sort_mode="multi",
                                    # column_selectable="single",
                                    # row_selectable="multi",
                                    # row_deletable=True,
                                    tooltip_header={'FaaS Platform': 'FaaS Platform', 'Installation Type': 'Installation Type', 'Runtime Customization': 'Runtime Customization', 'Github Stars': "Indicates the number of stars the GitHub repository a FaaS platform has", 'Stackoverflow questions': 'Stackoverflow questions'}
                                    )
    ]),
    html.H1("Updates found in Release Notes"),
    html.P("Please check the release notes and select the correct feature and the category (superclass) it belongs to"),
    dash_table.DataTable(
        style_data={
        'whiteSpace': 'normal',
        'height': 'auto',
        'width': '100px',
        'maxWidth': '100px',
        'minWidth': '100px',
        },
        id='table-dropdown',
        style_cell={'textAlign': 'left'},
        style_header={'textAlign': 'left'},
        data=df2[['Title', 'Date', 'Reference', 'Parsed Description', 'Superclass Suggestions', 'Feature Suggestions']].loc[:2].to_dict('records'),
        columns=[
            {'id': 'Title', 'name': 'Title'},
            {'id': 'Date', 'name': 'Date'},
            {'id': 'Parsed Description', 'name': 'Relevant Section'},
            {'id': 'Reference', 'name': 'Reference'},
            {'id': 'Superclass', 'name': 'Superclass', 'presentation': 'dropdown'},
            {'id': 'Feature', 'name': 'Feature', 'presentation': 'dropdown'},
        ],

        editable=True,
        dropdown_conditional=[{
            'if': {
                'column_id': 'Superclass', # skip-id-check
                'filter_query': '{Title} eq "Node.js 16 runtime"'
            },
            'options': [
                            {'label': i, 'value': i}
                            for i in [
                                'CICDPipelining',
                                'RuntimeOS',
                                'OpenSourceRepository'
                            ]
                        ]
        }, {
            'if': {
                'column_id': 'Feature',
                'filter_query': '{Title} eq "Node.js 16 runtime"'
            },
            'options': [
                            {'label': i, 'value': i}
                            for i in [
                                'Node.js',
                                'Amazon',
                                'Linux'
                            ]
                        ]
        },
        {
            'if': {
                'column_id': 'Superclass', # skip-id-check
                'filter_query': '{Title} eq "Lambda function URLs"'
            },
            'options': [
                            {'label': i, 'value': i}
                            for i in [
                                'FunctionMarketplace',
                                'FunctionRuntime',
                                'WorkflowDefinition'
                            ]
                        ]
        }, {
            'if': {
                'column_id': 'Feature',
                'filter_query': '{Title} eq "Lambda function URLs"'
            },
            'options': [
                            {'label': i, 'value': i}
                            for i in [
                                'HTTP(S)',
                                'Lambda',
                            ]
                        ]
        },
        {
            'if': {
                'column_id': 'Superclass', # skip-id-check
                'filter_query': '{Title} eq "Shared test events in the AWS Lambda console"'
            },
            'options': [
                            {'label': i, 'value': i}
                            for i in [
                                'LicenseType',
                                'PlatformDocumentation',
                                'License'
                            ]
                        ]
        }, {
            'if': {
                'column_id': 'Feature',
                'filter_query': '{Title} eq "Shared test events in the AWS Lambda console"'
            },
            'options': [
                            {'label': i, 'value': i}
                            for i in [
                                'IAM',
                                'AWS',
                            ]
                        ]
        },
        # {
        #     'if': {
        #         'column_id': 'Neighborhood',
        #         'filter_query': '{City} eq "Los Angeles"'
        #     },
        #     'options': [
        #                     {'label': i, 'value': i}
        #                     for i in [
        #                         'Venice',
        #                         'Hollywood',
        #                         'Los Feliz'
        #                     ]
        #                 ]
        # }
        ]
    ),
    html.Button('Submit', style={'margin-right': 1})
                ])
if __name__ == '__main__':
    app.run_server(debug=True)