import streamlit as st
import requests
from datetime import datetime

# Your API key (Replace with your actual API key)
API_KEY = st.secrets["API_KEY"]

# Custom CSS for improved aesthetics
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
    }
    .main {
        background-color: #f8fbff;
        color: #22303c;
    }
    h1 {
        color: #102a43;
        font-weight: 700;
    }
    h2, h3, h4, h5, h6 {
        color: #334e68;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #334e68;
        color: #ffffff;
        border-radius: 8px;
    }
    .stSuccess {
        background-color: #e3fcef;
        border-left: 4px solid #27ae60;
        color: #27ae60;
    }
    .stInfo {
        background-color: #e6f7ff;
        border-left: 4px solid #3498db;
        color: #3498db;
    }
    .stError {
        background-color: #ffe8e6;
        border-left: 4px solid #e74c3c;
        color: #e74c3c;
    }
    .css-18e3th9 {
        padding-top: 2rem;
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        color: #627d98;
    }
    a {
        color: #3498db;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

# Title of the app
st.title("Currency Converter \nMade by EngRashed1 ")

# Display current date and time
now = datetime.now()
current_date = now.strftime("%A, %d %B %Y")
current_time = now.strftime("%H:%M:%S")
st.write(f"Date: {current_date} | Time: {current_time}")

# Input fields
st.subheader("Convert Your Currency")
amount = st.number_input("Enter Amount", min_value=0.01, value=1.0)

# Supported currencies
currencies = ["USD", "EUR", "SAR", "GBP", "JPY", "AED", "EGP", "KWD", "QAR", "INR"]

col1, col2 = st.columns(2)
with col1:
    from_currency = st.selectbox("From Currency", currencies, index=0)
with col2:
    to_currency = st.selectbox("To Currency", currencies, index=2)

# Conversion logic using ExchangeRate-API
if st.button("Convert"):
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data["result"] == "success":
            exchange_rate = data["conversion_rates"][to_currency]
            converted_amount = amount * exchange_rate

            st.success(f"{amount} {from_currency} equals {converted_amount:.2f} {to_currency}")
            st.info(f"Exchange Rate: 1 {from_currency} = {exchange_rate:.4f} {to_currency}")
        else:
            st.error("Error: Invalid response structure received.")
    else:
        st.error("Error fetching exchange rate. Please try again later.")

# Displaying currency rates against USD
st.subheader("Today's Rates against USD")
usd_response = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD")
if usd_response.status_code == 200:
    usd_data = usd_response.json()
    if usd_data["result"] == "success":
        usd_rates = usd_data["conversion_rates"]
        rates_to_display = {currency: usd_rates[currency] for currency in currencies if currency != "USD"}
        st.table(rates_to_display)
    else:
        st.error("Error: Invalid response structure received for USD rates.")
else:
    st.error("Unable to fetch currency rates at the moment.")

# Footer
st.markdown("""
    <div class="footer">
        Made by <a href="https://www.linkedin.com/in/EngRashed1" target="_blank">EngRashed1</a>
    </div>
""", unsafe_allow_html=True)
