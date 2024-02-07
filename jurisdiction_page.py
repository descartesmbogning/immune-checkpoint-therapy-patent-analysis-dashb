# Import required libraries
from components import Navbar, Footer
from dash import dcc, html, Input, Output, dash_table, callback, State, callback_context, no_update
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
import numpy as np
from dash.dash_table.Format import Format, Scheme

# Load your data
df = pd.read_csv('./data/jurisdication_table.csv')
df_trend = pd.read_csv('./data/jurisdiction_year_table.csv')

# Drop 'Unnamed: 0' column if it exists
if 'Unnamed: 0' in df.columns:
    df = df.drop(columns=['Unnamed: 0'])

# Define helper functions for dynamic content (Placeholder content for now)
def get_total_jurisdictions():
    return str(df['Jurisdiction'].count())

# Layout for the jurisdiction page
layout = dbc.Container([
    Navbar(),  # Include navbar at the top
    dbc.Row(dbc.Col(html.H1("Jurisdictions"), width={'size': 6, 'offset': 3}, className="text-center mt-1 mb-1")),
    dbc.Row([
        dbc.Col(html.P("On Lens.org, “jurisdiction” refers to the different legal territories or countries where a patent is filed or granted."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Explore the contributions of jurisdictions in the field of immune checkpoint therapy."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center"),
        dbc.Col(html.P("Use the table below to sort, filter, and understand the landscape of patent contributions."), width={'size': 10, 'offset': 0}, className="d-flex justify-content-center")
        ], className="mb-2 d-flex justify-content-center"
    ),  
     # Key Metrics in Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H5("Total Jurisdictions", className="card-title"),
                html.P(get_total_jurisdictions(), className="card-text")
            ])
        ]), className="text-center mt-1 mb-1", width=4),
        # dbc.Col(dbc.Card([
        #     dbc.CardBody([
        #         html.H5("Top Inventor", className="card-title"),
        #         html.P(get_top_inventor(), className="card-text")
        #     ])
        # ]), width=4),
        # # ... Add more cards as needed ...
    ], className="mb-2 d-flex justify-content-center"),

    
    
    # Buttons for downloading data
    dbc.Row([
        dbc.Col(html.Button("Download Full Data", id="btn_download_full_jurisdiction"), width={'size': 2, 'offset': 0}),
        dbc.Col(html.Button("Download Selected Data", id="btn_download_selected_jurisdiction"), width=2),
    ], justify="start", className="mb-0"),
    
    # Data Table
    dash_table.DataTable(
        id='jurisdiction-datatable-interactivity',
        columns=[
            {
                "name": f"{i} (use: >, <, =)" if df[i].dtype in [np.float64, np.int64] else i,
                "id": i,
                "type": "numeric",
                "format": Format(precision=4, scheme=Scheme.decimal_or_exponent) if df[i].dtype in [np.float64, np.int64] else None
            } for i in df.columns
        ],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        column_selectable="single",
        row_selectable="multi",
        page_action="native",
        page_current= 0,
        page_size= 10,
        style_table={'height': '400px', 'overflowY': 'auto'},
        style_cell={
            'height': 'auto',
            'minWidth': '80px', 'width': '120px', 'maxWidth': '180px',
            'whiteSpace': 'normal'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold'
        }
    ),
    
    # Place the metric dropdown right above the Data Table
    dbc.Row(
        [
            dbc.Col(html.Label("Select Metric:"), width=2),
            dbc.Col(
                dcc.Dropdown(
                    id='jurisdiction-metric-dropdown',
                    options=[
                        {'label': 'Patent Count', 'value': 'Patent Count'},
                        {'label': 'Total Citations', 'value': 'Total Citations'},
                        # {'label': 'Degree Centrality', 'value': 'Degree Centrality'},
                        # {'label': 'Betweenness Centrality', 'value': 'Betweenness Centrality'},
                        {'label': 'Duration (Years)', 'value': 'Duration (Years)'}
                    ],
                    value='Patent Count'  # default value
                ),
                width=3
            ),
        ],
        className="mb-0  d-flex justify-content-center"
    ),

    # Bar Chart
    dbc.Row(dbc.Col(dcc.Graph(id='jurisdiction-bar-chart'), width=12)),
    
    # Line Chart
    dbc.Row(dbc.Col(dcc.Graph(id='jurisdiction-line-chart'), width=12)),

    # Hidden Divs for JSON-serialized data
    html.Div(id='jurisdiction-data-storage-full', style={'display': 'none'}),
    html.Div(id='jurisdiction-data-storage-selected', style={'display': 'none'}),

    # Hidden element for triggering downloads
    dcc.Download(id="jurisdiction-download-dataframe-csv"),
    
    
    Footer()  # Include footer at the bottom

], fluid=True)


# Callbacks for the jurisdiction page
@callback(
    Output('jurisdiction-bar-chart', 'figure'),
    [Input('jurisdiction-datatable-interactivity', 'derived_virtual_data'),
     Input('jurisdiction-datatable-interactivity', 'derived_virtual_selected_rows'),
     Input('jurisdiction-metric-dropdown', 'value')]  # Input from the dropdown
)
def update_jurisdiction_bar_chart(rows, derived_virtual_selected_rows, selected_metric):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    # When the table is first loaded and there's no filtering or sorting, use original data
    dff = pd.DataFrame(rows) if rows is not None else df

    if len(derived_virtual_selected_rows) == 0:
        # Sort the DataFrame by the selected metric and take the top 20
        filtered_df = dff.sort_values(selected_metric, ascending=False).head(20)
        title = f'Top 20 Jurisdictions by {selected_metric}'
    else:
        filtered_df = dff.iloc[derived_virtual_selected_rows]
        # Even when specific jurisdictions are selected, sort them by the selected metric
        filtered_df = filtered_df.sort_values(selected_metric, ascending=False)
        title = f'Selected Jurisdictions by {selected_metric}'

    # Plotting the bar chart
    # fig = px.bar(filtered_df, x="Jurisdiction", y=selected_metric, color="2023 Classification", barmode="group",
    #              category_orders={"Jurisdiction": filtered_df["Jurisdiction"].tolist()})  # Ensure consistent ordering
    # fig.update_layout(title=title)
    fig = px.bar(filtered_df, x="Jurisdiction", y=selected_metric, color="2023 Classification",
             hover_data=[selected_metric, 'First Year', 'Last Year','Mean Patents/Year'],
             barmode="group",
             category_orders={"Jurisdiction": filtered_df["Jurisdiction"].tolist()})  # Ensure consistent ordering
             
    fig.update_traces(hovertemplate="Jurisdiction: %{x}<br>" + selected_metric + ": %{y}<br>First Year: %{customdata[0]}<br>Last Year: %{customdata[1]}<br>Mean Patents/Year: %{customdata[2]}")
    fig.update_layout(title=title)
    return fig

# ... (other callbacks for your app)


@callback(
    Output('jurisdiction-line-chart', 'figure'),
    [Input('jurisdiction-datatable-interactivity', 'derived_virtual_data'),  # Get the filtered data from the table
     Input('jurisdiction-datatable-interactivity', 'derived_virtual_selected_rows'),  # Get the selected rows from the table
     Input('jurisdiction-bar-chart', 'clickData')]  # Get the click data from the bar chart
)
def update_jurisdiction_line_chart(all_rows_data, slctd_row_indices, clickData):
    # Process the data from the table
    dff = pd.DataFrame(all_rows_data) if all_rows_data is not None else pd.DataFrame()
    selected_jurisdictions = dff.iloc[slctd_row_indices]['Jurisdiction'].tolist() if slctd_row_indices else []

    # Process the click data from the bar chart
    if clickData:
        clicked_jurisdiction = clickData['points'][0]['x']
        if clicked_jurisdiction not in selected_jurisdictions:
            selected_jurisdictions.append(clicked_jurisdiction)

    # Aggregate data: count patents per year for each jurisdiction
    jurisdiction_yearly_counts = df_trend.groupby(['Application Year', 'Jurisdiction']).size().reset_index(name='Patent Count')

    # Create the line chart
    if selected_jurisdictions:
        filtered_df = jurisdiction_yearly_counts[jurisdiction_yearly_counts['Jurisdiction'].isin(selected_jurisdictions)]
        fig = px.line(filtered_df, x='Application Year', y='Patent Count', color='Jurisdiction',markers=True)
        fig.update_layout(title='Contribution Trends of Selected jurisdictions Over Years')
    else:
        # When no jurisdictions are selected, show the global trend
        df_trend2 = df_trend[['Lens ID','Application Year']].drop_duplicates()
        global_yearly_counts = df_trend2.groupby(['Application Year']).size().reset_index(name='Total Patents')
        fig = px.line(global_yearly_counts, x='Application Year', y='Total Patents',markers=True)
        fig.update_layout(title='Global Trend of Patent Contributions Over Years')
    
    return fig

@callback(
    [Output('jurisdiction-data-storage-full', 'children'),
     Output('jurisdiction-data-storage-selected', 'children')],
    [Input('jurisdiction-datatable-interactivity', 'derived_virtual_data'),
     Input('jurisdiction-datatable-interactivity', 'derived_virtual_selected_rows')]
)
def store_jurisdiction_data(all_rows_data, slctd_row_indices):
    if all_rows_data is None:
        raise PreventUpdate
    
    # Store full data
    full_data_str = pd.DataFrame(all_rows_data).to_json(date_format='iso', orient='split')

    # Store selected data
    if slctd_row_indices is None or len(slctd_row_indices) == 0:
        selected_data_str = None
    else:
        selected_data_str = pd.DataFrame([all_rows_data[i] for i in slctd_row_indices]).to_json(date_format='iso', orient='split')
    
    return full_data_str, selected_data_str

@callback(
    Output("jurisdiction-download-dataframe-csv", "data"),
    [Input("btn_download_full_jurisdiction", "n_clicks"),
     Input("btn_download_selected_jurisdiction", "n_clicks"),
     Input('jurisdiction-data-storage-full', 'children'),
     Input('jurisdiction-data-storage-selected', 'children')],
    prevent_initial_call=True,
)
def download_jurisdiction_csv(btn_full, btn_selected, full_data_str, selected_data_str):
    ctx = callback_context
    if not ctx.triggered:
        return dash.no_update
    
    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if button_id == "btn_download_full_jurisdiction":
        df = pd.read_json(full_data_str, orient='split')
        return dcc.send_data_frame(df.to_csv, filename="full_data_jurisdiction.csv")
    elif button_id == "btn_download_selected_jurisdiction":
        if selected_data_str:
            df = pd.read_json(selected_data_str, orient='split')
            return dcc.send_data_frame(df.to_csv, filename="selected_data_jurisdiction.csv")
    return no_update

# No need for `app.run_server()` here, as this will be run from index.py
