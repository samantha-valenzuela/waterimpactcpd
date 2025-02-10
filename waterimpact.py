import streamlit as st
import pandas as pd
import plotly.express as px

#Título de la app
st.title("Gráfico Básico con Plotly")

#Subir archivo CSV
uploaded_file = st.file_uploader("Sube tu archivo CSV", type=["csv"])

#Verificar si el archivo se ha subido
if uploaded_file:
    #Leer el archivo CSV
    data = pd.read_csv(uploaded_file)

    # Mostrar los primeros 5 registros del archivo subido
    st.subheader("Vista previa de los datos")
    st.dataframe(data.head())

    # Crear un gráfico  de barras sencillo con Plotly
    fig = px.bar(data, x=data.columns[0], y=data.columns[1], title="Gráfico de barras")

    # Mostrar el gráfico en la app
    st.plotly_chart(fig)
else:
    st.info("Sube un archivo CSV para ver el gráfico.")
    