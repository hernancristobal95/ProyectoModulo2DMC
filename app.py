import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Indice")
modulo = st.sidebar.selectbox("Elija una sección", ["Módulo 1", "Módulo 2", "Módulo 3"])

class DataAnalyzer:
    def __init__(self, datos):
        self.datos = datos
    def clasificar_variables(self):
        numericas = self.datos.select_dtypes(include=np.number).columns.tolist()
        categoricas = self.datos.select_dtypes(exclude=np.number).columns.tolist()
        return numericas, categoricas
    def estadisticas_descriptivas(self):
        return self.datos.describe()
    def valores_nulos(self):
        return self.datos.isnull().sum()
    def calcular_moda(self, columna):
        moda = self.datos[columna].mode()
        if len(moda) > 0:
            return moda.iloc[0]
        return "No disponible"
        
if modulo == "Módulo 1":
    st.title("Home")
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

elif modulo == "Módulo 2":
    st.title("Analisis del dataset")
    st.subheader("Carga del archivo")
    archivo = st.file_uploader("Seleccione su archivo", type=["csv"])
    if archivo is None:
        st.info("Cargue un archivo csv para visualizar los datos")
        st.stop()
    try:
        datos = pd.read_csv(archivo)
        st.session_state["datos"] = datos
        st.success("Su archivo ha sido cargado correctamente")
    except Exception as error:
        st.error(f"No fue posible leer el archivo: {error}")
        st.stop()
    st.subheader("Vista previa de los datos")
    st.dataframe(datos.head(), use_container_width = True)
    st.subheader("Dimensiones del dataset")
    st.write(f"**Filas:** {datos.shape[0]}")
    st.write(f"**Columnas:** {datos.shape[1]}")

elif modulo == "Módulo 3":
    st.title("Analisis Exploratorio de Datos")
    if "datos" not in st.session_state:
        st.warning ("Primero debes cargar el dataset a trabajar")
        st.stop()
    datos = st.session_state["datos"]
    analyzer = DataAnalyzer(datos)
    variables_numericas, variables_categoricas (analisis.clasificar_variables())
    
    #Item 1: Información general del dataset
    datos.info()
