import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="F.I.T.A. System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed" # Colapsado al inicio para el login
)

# --- GESTIÓN DE ESTADO (MEMORIA DEL SISTEMA) ---
# Aquí guardamos si el usuario ya entró, sus puntos y sus datos
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'setup_completo' not in st.session_state:
    st.session_state['setup_completo'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = {}
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = 0
if 'repositorio' not in st.session_state:
    st.session_state['repositorio'] = []

# --- ESTILOS CSS (DISEÑO DE LOGIN Y APP) ---
st.markdown("""
<style>
    /* Estilo del Login */
    .login-container {
        border: 2px solid #E5E7E9;
        padding: 40px;
        border-radius: 15px;
        text-align: center;
        background-color: #FDFEFE;
    }
    .main-title {font-size: 2.5rem; color: #154360; font-weight: bold;}
    
    /* Estilo de Tarjetas de Usuario */
    .user-card {
        padding: 15px;
        background-color: #E8F8F5;
        border-radius: 10px;
        border-left: 5px solid #1ABC9C;
        margin-bottom: 20px;
    }
    
    /* Botones */
    div.stButton > button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# =======================================================
# FUNCIÓN 1: PANTALLA DE LOGIN (SIMULADA)
# =======================================================
def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/2554/2554044.png", width=120)
        st.markdown('<p class="main-title" style="text-align:center;">F.I.T.A. ACCESS</p>', unsafe_allow_html=True)
        st.markdown("<h4 style='text-align:center; color:grey;'>Sistema de Ingeniería Civil</h4>", unsafe_allow_html=True)
        
        st.write("---")
        
        # Simulamos el botón de Google
        if st.button("🔵 Iniciar Sesión con Google (Simulado)", type="primary"):
            st.session_state['logged_in'] = True
            st.session_state['usuario']['nombre'] = "Luigi" # Aquí tomaría el nombre real de Google
            st.session_state['usuario']['email'] = "luigi.ing@gmail.com"
            st.session_state['usuario']['foto'] = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            st.rerun()

# =======================================================
# FUNCIÓN 2: CUESTIONARIO DE INICIO (ONBOARDING)
# =======================================================
def onboarding_page():
    st.markdown('<p class="main-title">🛠️ Configuración de Perfil</p>', unsafe_allow_html=True)
    st.write("Para darte acceso a los recursos adecuados, necesitamos validar tu información académica.")
    
    with st.form("form_onboarding"):
        col1, col2 = st.columns(2)
        with col1:
            uni = st.selectbox("Universidad", ["UPN - Universidad Privada del Norte", "UPC", "UTP", "UNI", "Otra"])
            carrera = st.selectbox("Carrera Profesional", ["Ingeniería Civil", "Arquitectura", "Ing. Industrial"])
        with col2:
            ciclo = st.slider("Ciclo Actual", 1, 10, 5)
            interes = st.multiselect("Áreas de Interés", ["Estructuras", "Hidráulica", "Gestión", "Geotecnia"])
        
        submit = st.form_submit_button("💾 Guardar y Acceder al Sistema")
        
        if submit:
            st.session_state['usuario']['universidad'] = uni
            st.session_state['usuario']['carrera'] = carrera
            st.session_state['usuario']['ciclo'] = ciclo
            st.session_state['setup_completo'] = True
            st.balloons()
            time.sleep(1)
            st.rerun()

# =======================================================
# FUNCIÓN 3: APLICACIÓN PRINCIPAL (DASHBOARD)
# =======================================================
def main_app():
    # --- BARRA LATERAL CON PERFIL ---
    with st.sidebar:
        # Tarjeta de Usuario
        st.image(st.session_state['usuario']['foto'], width=80)
        st.markdown(f"### Hola, {st.session_state['usuario']['nombre']}")
        
        # Estatus y Puntos
        st.markdown(f"""
        <div class="user-card">
            🎓 <b>{st.session_state['usuario']['universidad']}</b><br>
            📚 {st.session_state['usuario']['carrera']} (Ciclo {st.session_state['usuario']['ciclo']})<br>
            ⭐ <b>Puntos FITA: {st.session_state['puntos']}</b>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state['puntos'] > 50:
            st.success("🏅 Rango: INGENIERO JUNIOR")
        else:
            st.info("Rango: ESTUDIANTE")
            
        st.markdown("---")
        menu = st.radio("Navegación", ["🏠 Inicio", "☁️ Repositorio (Ganar Puntos)", "📊 Excel Tool"])
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['setup_completo'] = False
            st.rerun()

    # --- PÁGINA: INICIO ---
    if menu == "🏠 Inicio":
        st.title("🏠 Panel de Control")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Estado", "🟢 Activo Online")
        col2.metric("Puntos Acumulados", st.session_state['puntos'], "+10 último archivo")
        col3.metric("Nivel de Acceso", "Premium")
        
        st.info("👋 Bienvenido al sistema. Sube archivos al repositorio para aumentar tu puntaje.")

    # --- PÁGINA: REPOSITORIO (SISTEMA DE PUNTOS) ---
    elif menu == "☁️ Repositorio (Ganar Puntos)":
        st.title("☁️ Repositorio Colaborativo")
        st.markdown("Comparte material académico. **Recompensa: +10 Puntos por archivo.**")
        
        col_up, col_list = st.columns([1, 2])
        
        with col_up:
            st.subheader("📤 Subir Aporte")
            archivo = st.file_uploader("Documento (PDF/Excel/DWG)", type=["pdf", "xlsx", "dwg"])
            desc = st.text_input("Descripción")
            
            if st.button("Publicar Aporte"):
                if archivo:
                    # Lógica de Gamificación
                    st.session_state['puntos'] += 10
                    nuevo_archivo = {
                        "nombre": archivo.name,
                        "desc": desc,
                        "autor": st.session_state['usuario']['nombre'],
                        "fecha": datetime.now().strftime("%H:%M")
                    }
                    st.session_state['repositorio'].append(nuevo_archivo)
                    st.toast("¡+10 Puntos obtenidos! 🚀", icon="⭐")
                    time.sleep(1)
                    st.rerun()
        
        with col_list:
            st.subheader("🗂️ Archivos de la Comunidad")
            if not st.session_state['repositorio']:
                st.warning("Aún no hay archivos. ¡Sé el primero en ganar puntos!")
            
            for file in reversed(st.session_state['repositorio']):
                st.markdown(f"""
                <div style="padding:10px; border-bottom:1px solid #ddd;">
                    <b>📄 {file['nombre']}</b> <br>
                    <small>Subido por: {file['autor']} | {file['desc']} | 🕒 {file['fecha']}</small>
                </div>
                """, unsafe_allow_html=True)

    # --- PÁGINA: EXCEL ---
    elif menu == "📊 Excel Tool":
        st.title("📊 Visor de Metrados")
        st.write("Herramienta de visualización de datos.")
        up = st.file_uploader("Cargar Excel", type=["xlsx"])
        if up:
            df = pd.read_excel(up)
            st.dataframe(df)

# =======================================================
# 🧠 LÓGICA DE CONTROL DE FLUJO (EL CEREBRO)
# =======================================================

if not st.session_state['logged_in']:
    login_page()
elif not st.session_state['setup_completo']:
    onboarding_page()
else:
    main_app()
