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
    variables_numericas, variables_categoricas = (analyzer.clasificar_variables())
    
    #Item 1
    st.header("Item 1: Información general del dataset")
    info_dataset = pd.DataFrame({"Variable": datos.columns, "Tipo": datos.dtypes.astype(str), "Valores nulos": datos.isnull().sum().values})
    st.dataframe(info_dataset, use_container_width=True)
    st.divider()
    
    #Item 2
    st.header("Item 2: Clasificación de variables")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Variables numéricas =", len(variables_numericas))
        for variable in variables_numericas:
            st.write(f"• {variable}")
    with col2:
        st.write("Variables categóricas =", len(variables_categoricas))
        for variable in variables_categoricas:
            st.write(f"• {variable}")
    st.divider()
    
    #Item 3
    st.header("Item 3: Estadísticas descriptivas")
    st.dataframe(analyzer.estadisticas_descriptivas(), use_container_width=True)
    st.divider()

    #Item 4
    st.header("Item 4: Analisis de valores faltantes")
    valores_nulos = analyzer.valores_nulos()
    valores_nulos = valores_nulos.sort_values(ascending=False)
    st.dataframe(valores_nulos.to_frame("Valores nulos"), use_container_width=True)
    nulos_grafico = valores_nulos[valores_nulos > 0]
    if len(nulos_grafico) == 0:
        st.success("No existen valores faltantes")
    else:
        fig, ax = plt.subplots(figsize=(10, 4))
        nulos_grafico.plot(kind="bar",color="red",ax=ax)
        ax.set_title("Cantidad de valores faltantes por variable")
        ax.set_xlabel("Variable")
        ax.set_ylabel("Cantidad")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    st.divider()
    
    #Item 5
    st.header("Item 5: Distribución de variables numéricas")
    if len(variables_numericas) > 0:
        variable_hist = st.selectbox("Seleccione una variable numérica",variables_numericas)
        fig, ax = plt.subplots(figsize=(9, 4))
        sns.histplot(datos[variable_hist], kde=True, color="blue", ax=ax)
        ax.set_title(f"Distribución de {variable_hist}")
        ax.set_xlabel(variable_hist)
        ax.set_ylabel("Frecuencia")
        st.pyplot(fig)
    st.divider()
    
    #Item 6
    st.header("Item 6: Análisis de variables categóricas")
    variable1 = st.selectbox("Seleccione una variable", variables_categoricas)
    conteo = datos[variable1].value_counts()
    st.dataframe(conteo)
    fig, ax = plt.subplots()
    conteo.plot(kind="bar", ax=ax)
    ax.set_title(f"Distribución de {variable1}")
    st.pyplot(fig)
    st.divider()

    #Item 7
    st.header("Item 7: Análisis numérico vs Churn")
    variable2 = st.selectbox("Seleccione variable numérica", ["tenure", "MonthlyCharges"])
    st.dataframe(datos.groupby("Churn")[variable2].agg(["mean", "median"]).round(2))
    fig, ax = plt.subplots()
    sns.boxplot(data=datos, x="Churn", y=variable2, ax=ax)
    ax.set_title(f"{variable2} vs Churn")
    st.pyplot(fig)
    st.divider()

    #Item 8
    st.header("Item 8: Análisis categórico vs Churn")
    variable3 = st.selectbox("Seleccione variable categórica",["Contract", "InternetService"])
    tasa = datos.groupby(variable3)["Churn"].apply(lambda x: (x == "Yes").mean() * 100)
    st.dataframe(tasa.round(2).to_frame("Churn %"))
    fig, ax = plt.subplots()
    tasa.plot(kind="bar", ax=ax)
    ax.set_title(f"Churn según {variable3}")
    st.pyplot(fig)
    st.divider()

    #Item 9
    st.header("Item 9: Análisis basado en parámetros")
    variable4 = st.selectbox("Seleccione una variable", ["Contract", "InternetService", "TechSupport", "PaymentMethod"])
    variables = st.multiselect("Seleccione variables adicionales", ["tenure", "MonthlyCharges"])
    st.dataframe(datos.groupby(variable4)["Churn"].apply(lambda x: (x == "Yes").mean() * 100).round(2).to_frame("Churn %"))
    for v in variables:
        st.write(f"**{v}**")
        st.write(datos.groupby(variable4)[v].mean().round(2))
    st.divider()

    # Item 10
    st.header("Item 10: Hallazgos clave")
    churn = (datos["Churn"] == "Yes").mean() * 100
    col1, col2, col3 = st.columns(3)
    col1.metric("Clientes", len(datos))
    col2.metric("Churn", f"{churn:.1f}%")
    col3.metric("Permanencia", f"{100-churn:.1f}%")
    st.subheader("Principales segmentos con mayor Churn")
    resumen = pd.Series({"Month-to-month":(datos[datos["Contract"] == "Month-to-month"]["Churn"] == "Yes").mean() * 100,
        "Fiber optic":
            (datos[datos["InternetService"] == "Fiber optic"]["Churn"] == "Yes").mean() * 100,
        "Sin TechSupport":
            (datos[datos["TechSupport"] == "No"]["Churn"] == "Yes").mean() * 100,
        "Electronic check":
            (datos[datos["PaymentMethod"] == "Electronic check"]["Churn"] == "Yes").mean() * 100
    })
    st.bar_chart(resumen)
    st.write("**Insights principales:**")
    st.write("• Month-to-month presenta una tasa alta de Churn.")
    st.write("• Fiber optic presenta mayor Churn que DSL.")
    st.write("• Los clientes sin TechSupport presentan mayor Churn.")
    st.write("• Electronic check presenta una tasa elevada de Churn.")
    st.divider()
