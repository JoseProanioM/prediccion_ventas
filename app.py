import streamlit as st
import pandas as pd

# Load the dataset
@st.cache_data
def load_data():
    # Replace with the path to your dataset
    data = pd.read_csv("https://raw.githubusercontent.com/JoseProanioM/prediccion_ventas/refs/heads/main/predicci%C3%B3n_ventas.csv", parse_dates=["Periodo"])
    return data

# Load data
ventas_industria_extended = load_data()

# Streamlit App Layout
st.title("Ventas Totales por Industria: Predicciones 2025")

# Dropdown filter for CIIU_industria
ciiu_options = ventas_industria_extended['CIIU_industria'].unique()
selected_ciiu = st.selectbox("Seleccionar Industria:", ciiu_options)

# Dropdown filter for type of prediction
prediction_options = ["ARIMA", "RW", "Combined"]
selected_prediction = st.selectbox("Seleccionar Tipo de Predicción:", prediction_options)

# Filter the data based on the selected industry
filtered_data = ventas_industria_extended[ventas_industria_extended['CIIU_industria'] == selected_ciiu]

# Create the figure
st.line_chart(filtered_data['ventasTotales'], x=filtered_data['Periodo'], use_container_width=True)
st.caption("Serie Original")

with st.expander("Ver Predicciones"):
    if selected_prediction == "ARIMA":
        st.line_chart(filtered_data['ARIMA_Forecast'], x=filtered_data['Periodo'], use_container_width=True)
        st.caption("Predicción ARIMA")
        st.area_chart(pd.DataFrame({
            'upper': filtered_data['ARIMA_Upper80'],
            'lower': filtered_data['ARIMA_Lower80']
        }, index=filtered_data['Periodo']), use_container_width=True)
        st.caption("ARIMA 80% Interval")
        st.area_chart(pd.DataFrame({
            'upper': filtered_data['ARIMA_Upper95'],
            'lower': filtered_data['ARIMA_Lower95']
        }, index=filtered_data['Periodo']), use_container_width=True)
        st.caption("ARIMA 95% Interval")
    elif selected_prediction == "RW":
        st.line_chart(filtered_data['RW_Forecast'], x=filtered_data['Periodo'], use_container_width=True)
        st.caption("Predicción RW")
        st.area_chart(pd.DataFrame({
            'upper': filtered_data['RW_Upper80'],
            'lower': filtered_data['RW_Lower80']
        }, index=filtered_data['Periodo']), use_container_width=True)
        st.caption("RW 80% Interval")
        st.area_chart(pd.DataFrame({
            'upper': filtered_data['RW_Upper95'],
            'lower': filtered_data['RW_Lower95']
        }, index=filtered_data['Periodo']), use_container_width=True)
        st.caption("RW 95% Interval")
    elif selected_prediction == "Combined":
        st.line_chart(filtered_data['Combined_Forecast'], x=filtered_data['Periodo'], use_container_width=True)
        st.caption("Predicción Combinada")
        st.area_chart(pd.DataFrame({
            'upper': filtered_data['Combined_Upper80'],
            'lower': filtered_data['Combined_Lower80']
        }, index=filtered_data['Periodo']), use_container_width=True)
        st.caption("Combined 80% Interval")
        st.area_chart(pd.DataFrame({
            'upper': filtered_data['Combined_Upper95'],
            'lower': filtered_data['Combined_Lower95']
        }, index=filtered_data['Periodo']), use_container_width=True)
        st.caption("Combined 95% Interval")
