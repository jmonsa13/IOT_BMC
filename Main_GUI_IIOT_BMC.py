# Python File for streamlit tools
# BMC planta Girardota
# 18-Agosto-2022
# ----------------------------------------------------------------------------------------------------------------------
# Libraries
import datetime

import streamlit as st
from st_aggrid import AgGrid

# Internal Function
from Plot_Function_BMC import plot_html_BMC4
from SQL_Function_BMC import get_data_day, get_data_range


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Functions definition
@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Streamlit Setting
st.set_page_config(page_title="IIOT - Corona - BMC Girardota",
                   initial_sidebar_state="collapsed",
                   page_icon="📈",
                   layout="wide")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Initial page
st.title(' 📈 IIOT|Corona: BMC Planta Girardota')

st.markdown("""---""")
st.header("1) Selección de BMC a Visualizar")
bmc = st.radio("¿Que maquina desea visualizar?", ["BMC4"], 0)
st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
st.subheader("2) Selección de Periodo a Analizar")
col1, col2 = st.columns(2)
with col1:
    sel_fecha = st.radio("¿Que periodo de tiempo desea analizar?",
                         ('Por día', 'Por rango de días'), key="fecha")

    # Descargar nuevamente flag
    flag_download = False

with col2:
    # Opciones por día
    if sel_fecha == "Por día":
        sel_dia = st.date_input("¿Que dia desea analizar?", datetime.date.today(), key="dia")
        if sel_dia > datetime.date.today():
            st.error("Recuerda que el día seleccionado no puede ser superior a la día actual")
            st.stop()
        st.info("Analizaras el día " + str(sel_dia))

    # Opciones por rango de días
    elif sel_fecha == "Por rango de días":
        sel_dia_ini = st.date_input("Seleccione el día inicial", datetime.date.today() -
                                    datetime.timedelta(days=1), key="dia_ini")
        sel_dia_fin = st.date_input("Seleccione el día final", datetime.date.today(), key="dia_fin")

        if sel_dia_fin <= sel_dia_ini:
            st.error("Recuerda seleccionar una fecha inicial anterior a la fecha final!!!")
            st.stop()
        elif sel_dia_fin > datetime.date.today():
            st.error("Recuerda que la fecha final no puede ser superior a la fecha actual")
            st.stop()
        else:
            st.info("Analizaras un periodo de tiempo de " + str((sel_dia_fin - sel_dia_ini).days + 1) + " días.")

st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Visualizando la información
st.subheader("3) Graficar Información")
graficar = st.checkbox("Graficar", key="bmc")

if graficar is True:
    # Descargando la información
    with st.spinner('Descargando la información...'):
        if sel_fecha == "Por día":
            df, salud_list, salud_datos, title = get_data_day(sel_dia, bmc, flag_download)
            text_dia = str(sel_dia)
        elif sel_fecha == "Por rango de días":
            df, salud_list, salud_datos, title = get_data_range(sel_dia_ini, sel_dia_fin, bmc, flag_download)
            text_dia = "from_" + str(sel_dia_ini) + "_to_" + str(sel_dia_fin)
        # ----------------------------------------------------------------------------------------------------------
        # Salud de los datos descargada
        c1, c2, c3 = st.columns(3)
        c1.success("Información descargada")
        c2.metric(label="Salud global de los datos", value="{:.2f}%".format(salud_datos))
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    if bmc == "BMC4":
        st.header("Banco BMC 4")

        # Button to refresh the data
        if st.button("Refrescar gráfica", key="refrescar"):
            flag_download = True
            st.legacy_caching.clear_cache()
            st.experimental_rerun()

        # Dibujando la grafica
        with st.spinner('Dibujando la información...'):
            fig = plot_html_BMC4(df, title)
            st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # Visualización de los datos
    with st.expander("Ver los datos y descargar"):
        # Converting to csv file
        csv = convert_df(df)

        # Button to export the data
        st.download_button(label="Descargar datos como un archivo *.CSV",
                           data=csv,
                           file_name='Raw_datos_BMC_GR.csv',
                           mime='text/csv')

        # Showing the table
        tabla = AgGrid(df,
                       editable=False,
                       sortable=True,
                       filter=True,
                       resizable=True,
                       defaultWidth=5,
                       fit_columns_on_grid_load=False,
                       theme="streamlit",  # "light", "dark", "blue", "fresh", "material"
                       key='analisis_table',
                       reload_data=True,
                       )
    st.markdown("""---""")
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
    # Visualizando la información
    st.subheader("4) Analizar los datos")
    st.info(" Sección en Construcción")
# ----------------------------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------------------------
st.sidebar.header("Acerca de la App")
st.sidebar.markdown("**Creado por:**")
st.sidebar.write("Juan Felipe Monsalvo Salazar")
st.sidebar.write("jmonsalvo@corona.com.co")
st.sidebar.markdown("**Creado el:** 17/08/2022")
