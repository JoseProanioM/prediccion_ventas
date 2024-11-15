import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

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
fig, ax = plt.subplots(figsize=(12, 6))

# Plot the original data
ax.plot(filtered_data['Periodo'], filtered_data['ventasTotales'], color='#002A5C', label='Serie Original')

# Plot the forecast based on the selected prediction
if selected_prediction == "ARIMA":
    ax.plot(filtered_data['Periodo'], filtered_data['ARIMA_Forecast'], color='#017DC3', linestyle='dashed', label='Predicción ARIMA')
    ax.fill_between(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                    filtered_data['ARIMA_Upper80'].tolist() + filtered_data['ARIMA_Lower80'][::-1].tolist(),
                    alpha=0.2, color='orange')
    ax.fill_between(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                    filtered_data['ARIMA_Upper95'].tolist() + filtered_data['ARIMA_Lower95'][::-1].tolist(),
                    alpha=0.1, color='purple')
elif selected_prediction == "RW":
    ax.plot(filtered_data['Periodo'], filtered_data['RW_Forecast'], color='#FF5733', linestyle='dotted', label='Predicción RW')
    ax.fill_between(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                    filtered_data['RW_Upper80'].tolist() + filtered_data['RW_Lower80'][::-1].tolist(),
                    alpha=0.2, color='lightgreen')
    ax.fill_between(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                    filtered_data['RW_Upper95'].tolist() + filtered_data['RW_Lower95'][::-1].tolist(),
                    alpha=0.1, color='red')
elif selected_prediction == "Combined":
    ax.plot(filtered_data['Periodo'], filtered_data['Combined_Forecast'], color='#800080', linestyle='dashdot', label='Predicción Combinada')
    ax.fill_between(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                    filtered_data['Combined_Upper80'].tolist() + filtered_data['Combined_Lower80'][::-1].tolist(),
                    alpha=0.2, color='lightblue')
    ax.fill_between(filtered_data['Periodo'].tolist() + filtered_data['Periodo'][::-1].tolist(),
                    filtered_data['Combined_Upper95'].tolist() + filtered_data['Combined_Lower95'][::-1].tolist(),
                    alpha=0.1, color='blue')

# Set the plot title and axis labels
ax.set_title(f"Volumen de Ventas - {selected_ciiu}")
ax.set_xlabel("Periodo")
ax.set_ylabel("Miles de Millones de USD")
ax.legend()

# Display the plot in Streamlit
st.pyplot(fig)
