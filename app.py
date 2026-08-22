import streamlit as st
import numpy as np
import pandas as pd

st.sidebar.title("Indice")

modulo = st.sidebar.selectbox("Elija una sección", ["Módulo 1: Home", "Módulo 2: Carga del dataset"])

if modulo == "Módulo 1: Home":
    st.title("Proyecto Módulo 2 Fundamentals")
    st.subheader("Breve descripción del objetivo del análisis:")
    st.write("...")
    st.subheader("Nombre del alumno:")
    st.write("Hernan Martin Cristobal Ramos")
    st.subheader("Nombre del módulo:")
    st.write("Módulo Python Data Analytics")
    st.subheader("Descripción del dataset:")
    st.write("El archivo TelcoCustomerChurn.csv, que contiene información sobre los clientes, sus servicios contratados, facturación mensual, tiempo de permanencia y estado actual en la empresa.")
    st.subheader("Tecnologías usadas:")
    st.write("Python, Pandas, NumPy, Matplotlib, Seaborn, Github, Sreamlit")
    st.markdown("***2026***")

else:
    st.title("Analisis del dataset")
    st.subheader("Carga del archivo")
    archivo = st.file_uploader("Seleccione su archivo", type=["csv"])
    if archivo is None:
        st.info("Cargue un archivo csv para visualizar los datos")
        st.stop()
        try:
            datos = pd.read_csv(archivo)
            st.success("Su archivo ha sido cargado correctamente")
        except Exception as error:
            st.error(f"No fue posible leer el archivo: {error}")
            st.stop()
        st.subheader("Vista previa de los datos")
        st.dataframe(datos.head(), use_container_width = True)
        st.subheader("Dimensiones del dataset")
        st.write(f"**Filas:** {datos.shape[0]}")
        st.write(f"**Columnas:** {datos.shape[1]}")
