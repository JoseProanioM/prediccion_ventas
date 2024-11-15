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
fig = st.line_chart()

# Plot the original data
fig.add_lines(filtered_data['Periodo'], filtered_data['ventasTotales'], '#002A5C', 'Serie Original')

# Plot the forecast based on the selected prediction
if selected_prediction == "ARIMA":
    fig.add_lines(filtered_data['Periodo'], filtered_data['ARIMA_Forecast'], '#017DC3', 'Predicción ARIMA')
    fig.add_area(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                filtered_data['ARIMA_Upper80'].tolist() + filtered_data['ARIMA_Lower80'][::-1].tolist(),
                'orange', 0.2, 'ARIMA 80% Interval')
    fig.add_area(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                filtered_data['ARIMA_Upper95'].tolist() + filtered_data['ARIMA_Lower95'][::-1].tolist(),
                'purple', 0.1, 'ARIMA 95% Interval')
elif selected_prediction == "RW":
    fig.add_lines(filtered_data['Periodo'], filtered_data['RW_Forecast'], '#FF5733', 'Predicción RW')
    fig.add_area(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                filtered_data['RW_Upper80'].tolist() + filtered_data['RW_Lower80'][::-1].tolist(),
                'lightgreen', 0.2, 'RW 80% Interval')
    fig.add_area(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                filtered_data['RW_Upper95'].tolist() + filtered_data['RW_Lower95'][::-1].tolist(),
                'red', 0.1, 'RW 95% Interval')
elif selected_prediction == "Combined":
    fig.add_lines(filtered_data['Periodo'], filtered_data['Combined_Forecast'], '#800080', 'Predicción Combinada')
    fig.add_area(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                filtered_data['Combined_Upper80'].tolist() + filtered_data['Combined_Lower80'][::-1].tolist(),
                'lightblue', 0.2, 'Combined 80% Interval')
    fig.add_area(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                filtered_data['Combined_Upper95'].tolist() + filtered_data['Combined_Lower95'][::-1].tolist(),
                'blue', 0.1, 'Combined 95% Interval')