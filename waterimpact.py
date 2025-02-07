import streamlit as st
import pandas as pd
import plotly.express as px

# Título de la App
st.title("🌊 Water Impact Dashboard - CDP Data")

# Definir la leyenda de impacto
leyenda_impacto = {
    (15, 18): 'Critical',
    (11, 14): 'Very High',
    (8, 10): 'High',
    (5, 7): 'Medium',
    (0, 4): 'Low'
}

# Función para asignar categoría en función del valor numérico
def asignar_categoria(valor):
    for (rango_min, rango_max), categoria in leyenda_impacto.items():
        if pd.notnull(valor) and rango_min <= valor <= rango_max:
            return categoria
    return 'Sin categoría'

# Cargar Datos
uploaded_file = st.file_uploader("📤 Sube tu archivo CSV o Excel", type=["csv", "xlsx"])

if uploaded_file:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    st.subheader("Vista Previa de los Datos")
    st.dataframe(data.head())

    # Asignar categoría calculada
    data['CATEGORÍA CALCULADA'] = data['WATER IMPACT 2023'].apply(asignar_categoria)

    # Filtros Interactivos
    industry = st.selectbox("Selecciona la Industria", options=["Todos"] + list(data['CDP Industry'].unique()))
    activity_group = st.selectbox("Selecciona el Grupo de Actividad", options=["Todos"] + list(data['CDP Activity Group'].unique()))

    # Filtrado de Datos
    filtered_data = data.copy()
    if industry != "Todos":
        filtered_data = filtered_data[filtered_data['CDP Industry'] == industry]
    if activity_group != "Todos":
        filtered_data = filtered_data[filtered_data['CDP Activity Group'] == activity_group]

    # KPI
    st.metric("💧 Impacto Total del Agua (2023)", filtered_data['WATER IMPACT 2023'].sum())

    # Comparar categorías originales con las calculadas (si existe la columna original)
    if 'BANDING (WATER IMPACT 2021)' in data.columns:
        diferencias = data[data['CATEGORÍA CALCULADA'] != data['BANDING (WATER IMPACT 2021)']]
        if not diferencias.empty:
            st.warning(f"⚠️ Se encontraron discrepancias en {len(diferencias)} registros.")
            st.dataframe(diferencias)
        else:
            st.success("✅ Todas las categorías coinciden correctamente.")

    # Gráfico de Barras por Categoría
    st.subheader("📊 Impacto del Agua por Actividad y Categoría")
    fig = px.bar(filtered_data, x='CDP Activity', y='WATER IMPACT 2023', color='CATEGORÍA CALCULADA',
                 labels={'WATER IMPACT 2023': 'Impacto del Agua 2023'},
                 title='Impacto del Agua por Actividad y Categoría')
    st.plotly_chart(fig)

    # Tabla de Rankings
    st.subheader("🏆 Ranking General de Impacto del Agua")
    st.dataframe(filtered_data.sort_values(by='OVERALL WATER IMPACT RANK'))

else:
    st.info("Sube un archivo para empezar.")
