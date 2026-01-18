import streamlit as st
import pandas as pd

st.set_page_config(page_title="F.I.T.A. Web", layout="wide")
st.title("🏗️ F.I.T.A. CONSTRUCTION")
st.write("Bienvenido al Hub de Ingeniería.")

menu = st.sidebar.radio("Menú", ["Inicio", "Calculadora"])

if menu == "Inicio":
    st.info("Sistema Online.")

if menu == "Calculadora":
    st.header("Calculadora de Vigas")
    w = st.number_input("Carga (w)", value=1000)
    L = st.number_input("Longitud (L)", value=5)
    if st.button("Calcular"):
        st.success(f"Momento Máximo: {(w*L**2)/8}")
