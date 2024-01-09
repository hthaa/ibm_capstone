import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc, Input, Output

url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
df = pd.read_csv(url)

app = dash.Dash(__name__)

launch_sites_options = [{"label": "All", "value": "All"}] + [
    {"label": site, "value": site} for site in df["Launch Site"].unique()
]

app.layout = html.Div([
    html.Div([
        html.Label("Select a Launch Site"),
        dcc.Dropdown(
            id = "launch-site-dropdown",
            options = launch_sites_options,
            value = "All",
            multi = False
        ),
        html.Label("Select Payload Range (kg)"),
        dcc.RangeSlider(
            id = "payload-range-slider",
            min = 0,
            max = 10000,
            step = 1000,
            marks = {i: str(i) for i in range(0, 10001, 1000)},
            value = [0, 10000]
        ),
    ], style = {"width": "30%", "display": "inline-block", "margin-right": "2%"}),

    html.Div([
        dcc.Graph(id = "success-pie-chart"),
        dcc.Graph(id = "success-scatter-plot"),
    ]),
])

@app.callback(
    [Output("success-pie-chart", "figure"),
     Output("success-scatter-plot", "figure")],
    [Input("launch-site-dropdown", "value"),
     Input("payload-range-slider", "value")]
)
def update_charts(selected_site, payload_range):
    if selected_site == "All":
        filtered_df = df[(df["Payload Mass (kg)"] >= payload_range[0]) & (df["Payload Mass (kg)"] <= payload_range[1])]
        pie_chart_data = filtered_df.groupby("Launch Site")["class"].sum().reset_index()
        pie_chart = px.pie(pie_chart_data, names = "Launch Site", values = "class", title = "Successes by Launch Site")

        scatter_plot = px.scatter(filtered_df, x = "Payload Mass (kg)", y = "class",
                                  color = "Booster Version Category", title = "Success Rate vs Payload Mass")
    else:
        filtered_df = df[(df["Launch Site"] == selected_site) & (df["Payload Mass (kg)"] >= payload_range[0]) & (df["Payload Mass (kg)"] <= payload_range[1])]
        pie_chart_data = filtered_df["class"].value_counts().reset_index()
        pie_chart_data.columns = ["class", "count"]
        pie_chart = px.pie(pie_chart_data, names = "class", values = "count", title = f"Successes and Failures at {selected_site}")

        scatter_plot = px.scatter(filtered_df, x = "Payload Mass (kg)", y = "class",
                                  color = "Booster Version Category", title = f"Success Rate vs Payload Mass at {selected_site}")

    return pie_chart, scatter_plot

if __name__ == "__main__":
    app.run_server(debug=True)
