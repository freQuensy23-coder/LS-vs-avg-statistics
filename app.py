from dash import Dash, dcc, html, Input, Output
import plotly.express as px
from utils import *
import pandas as pd
app = Dash(__name__)

text_style = {"margin-top": "20px", "margin-bottom": "20px", "margin-left": "20px", "font-family":"Courier New, monospace"}

app.layout = html.Div([
    html.H1("МНК vs Среднее значение", style=text_style),
    dcc.Graph(id='linear_graph'),
    dcc.Graph(id='hist_graph'),
    html.H4('Высота начального выброса', style=text_style),
    dcc.Slider(
        0,
        30,
        id='height-slider',
        value=10
    ),
    html.H4('Размер начального выброса', style=text_style),
    dcc.Slider(
        0,
        750,
        value=250,
        id='size-slider'
    ),
    html.H4('Число экспериментальных точек', style=text_style),
    dcc.Slider(
        0,
        100,
        value=25,
        id='points-count-slider'
    ),
    html.H4('Сопротивление R', style=text_style),
    dcc.Slider(
        1,
        2500,
        value=100,
        id='R-slider'
    ),
    html.H4('Плотность гистограммы', style=text_style),
    dcc.Slider(
        0,
        500,
        value=300,
        id='hist_density'
    )
    dcc.Link(href='https://t.me/miptphyshub', title="Что тут происходит?")
])


@app.callback(
    Output('linear_graph', 'figure'),
    Output('hist_graph', 'figure'),
    Input('height-slider', 'value'),
    Input('size-slider', 'value'),
    Input('points-count-slider', 'value'),
    Input('R-slider', 'value'),
    Input('hist_density', 'value'))
def update_figure(height, size, points_count, R, hist_density):
    R = R
    U = make_noise(np.linspace(0, 3000, points_count, dtype=int))
    I = make_noise(U / R, mu=0.15) + hill(U, scale=size, height=height)
    # через усреднение
    Gs = []
    for i in range(len(I)):
        if U[i] != 0:
            G = I[i] / U[i]
            Gs.append(G)

    Gs = np.array(Gs)
    G_avg = np.average(Gs)

    # через статистику
    G_mnk = mnk(U, I)

    I_mnk = U * G_mnk
    I_avg = U * G_avg

    fig_vah = go.Figure()
    fig_vah.add_trace(go.Scatter(x=U, y=I, mode='markers', name="experimental points"))
    fig_vah.add_trace(go.Scatter(x=U, y=I_mnk, mode='lines', name="МНК"))
    fig_vah.add_trace(go.Scatter(x=U, y=I_avg, mode='lines', name="Среднее"))

    fig_vah.update_layout(
        title="МНК VS усреднение",
        xaxis_title="U, мВ",
        yaxis_title="I, мА",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    angles = I / U
    df = pd.DataFrame({"U": U, "I": I, "angles": angles})
    fig_hist = px.histogram(
        df, x="angles", range_x=[0, np.max(angles)], nbins=hist_density)
    fig_hist.add_vline(x=G_avg, line_width=3, line_dash="dash", line_color="green")
    fig_hist.add_vline(x=G_mnk, line_width=3, line_dash="dash", line_color="red")

    fig_hist.update_layout(
        title="Гистограмма углов",
        xaxis_title="k, В/А",
        yaxis_title="N, (число таких углов)",
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="RebeccaPurple"
        )
    )
    return fig_vah, fig_hist


if __name__ == '__main__':
    app.run_server(debug=True, port=80, host='0.0.0.0')