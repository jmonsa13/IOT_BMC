# Python File function for streamlit tools
# BMC planta Girardota
# 18-Agosto-2022
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots


# ----------------------------------------------------------------------------------------------------------------------
def plot_on_off(fig, df, column, legend, rgb, visibility="legendonly", axis_y="y2", r=1, c=1):

    fig.add_trace(go.Scatter(x=df.index, y=df[column],
                             fill='tozeroy', mode="lines",
                             fillcolor=rgb,
                             line_color='rgba(0,0,0,0)',
                             legendgroup=legend,
                             showlegend=True,
                             name=legend,
                             yaxis=axis_y,
                             visible=visibility),
                  secondary_y=True, row=r, col=c)

    return fig


@st.cache(persist=False, allow_output_mutation=True, suppress_st_warning=True, show_spinner=True, ttl=24 * 3600)
def plot_html_BMC4(df, title):
    """
    Función para dibujar los datos de BMC4
    INPUT:
        df = pandas dataframe traído de la base de dato SQL
        title = Título de la gráfica
    OUTPUT:
        fig = objeto figura para dibujarlo externamente de la función
    """
    # Create figure with secondary y-axis
    fig = make_subplots(rows=3, cols=1,  specs=[[{"secondary_y": True}], [{"secondary_y": True}],
                                                [{"secondary_y": False}]],
                        shared_xaxes=True, vertical_spacing=0.02,
                        #subplot_titles=('Temperaturas Entradas',  'Temperatura y humedad Salon 3')
                        )

    # Temp Pasta
    fig.add_trace(go.Scatter(x=df.index, y=df["Temp_Pasta [°C]"],
                             line=dict(color='#ff9900', width=1), # dash='dash'),
                             mode='lines',  # 'lines+markers'
                             name='Temp Pasta [°C]',
                             yaxis="y",
                             ),
                  row=1, col=1,)

    # Temp Agua
    fig.add_trace(go.Scatter(x=df.index, y=df["Temp_Agua [°C]"],
                             line=dict(color='#1616a7', width=1),
                             mode='lines',  # 'lines+markers'
                             name='Temp Agua [°C]',
                             yaxis="y",
                             ),
                  row=1, col=1)

    # Nivel_Pasta
    fig = plot_on_off(fig, df, "Nivel_Pasta [bool]", "Niv Pasta", 'rgba(55,126,184,0.7)')

    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    # Presion_Cierre_Molde
    fig.add_trace(go.Scatter(x=df.index, y=df["Presion_Cierre_Molde [Psi]"],
                             line=dict(color='#b68100', width=1),  # dash='dash'),
                             mode='lines', name='Pres_Cierre_Molde',
                             yaxis="y3",
                             ),
                  row=2, col=1)

    # Presion_Interna_Molde
    fig.add_trace(go.Scatter(x=df.index, y=df["Presion_Interna_Molde [Psi]"],
                             line=dict(color='#7f7f7f', width=1),  # dash='dot'
                             mode='lines', name='Pres_Interna_Molde',
                             yaxis="y3",
                             ),
                  row=2, col=1)

    # Bomba Alta
    fig = plot_on_off(fig, df, 'Bomba_Alta [bool]', "Bomba_Alta ON/OFF", 'rgba(255,127,0,0.3)', axis_y="y2", r=2, c=1)

    # Bomba Baja
    fig = plot_on_off(fig, df, 'Bomba_Baja [bool]', "Bomba_Baja ON/OFF", 'rgba(77,175,74,0.3)', axis_y="y2", r=2, c=1)

    # Presion_Spagless
    fig.add_trace(go.Scatter(x=df.index, y=df["Presion_Spagless [Psi]"],
                             line=dict(color='#3366cc', width=1,),  # dash='dash'),
                             mode='lines', name='Pres_Spagless',
                             yaxis="y5",
                             ),
                  secondary_y=False, row=3, col=1)

    # Add figure title
    fig.update_layout(height=800, title=title)

    # Template
    fig.layout.template = 'seaborn'  # ggplot2, plotly_dark, seaborn, plotly, plotly_white
    fig.update_layout(modebar_add=["v1hovermode", "toggleSpikeLines"])

    # Set x-axis and y-axis title
    fig.update_layout(legend_title_text='Variables BMC 4')
    fig['layout']['xaxis2']['title'] = 'Fecha'

    fig['layout']['yaxis']['title'] = 'Temperaturas °C'
    #
    fig['layout']['yaxis2']['title'] = 'Estado Low/High'
    fig['layout']['yaxis2']['range'] = [0, 1]
    fig['layout']['yaxis2']['fixedrange'] = True

    fig['layout']['yaxis3']['title'] = 'Presion Cierre/Interna [Psi]'
    fig['layout']['yaxis3']['range'] = [0, 1000]
    fig['layout']['yaxis3']['fixedrange'] = False

    fig['layout']['yaxis4']['title'] = 'Estado On/Off'
    fig['layout']['yaxis4']['range'] = [0, 1]
    fig['layout']['yaxis4']['fixedrange'] = True

    fig['layout']['yaxis5']['title'] = 'Presion Spagless [Psi]'
    fig['layout']['yaxis5']['range'] = [20, 100]
    fig['layout']['yaxis5']['fixedrange'] = False

    fig.update_xaxes(showline=True, linewidth=0.5, linecolor='black')
    fig.update_yaxes(showline=True, linewidth=0.5, linecolor='black')

    return fig
