import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="F.I.T.A. Construction Hub",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. BASE DE DATOS SIMULADA (SESSION STATE) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'setup_completo' not in st.session_state:
    st.session_state['setup_completo'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = {}
# Billetera inicial: 1000 Puntos
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = 1000 
if 'repositorio' not in st.session_state:
    # Datos de prueba para que no se vea vacío al inicio
    st.session_state['repositorio'] = [
        {"nombre": "Norma E.060 Concreto Armado.pdf", "carrera": "Ingeniería Civil", "area": "Estructuras", "precio": 20, "autor": "Sistema", "fecha": "2026-01-01"},
        {"nombre": "Plantilla Metrados Vias.xlsx", "carrera": "Ingeniería Civil", "area": "Transportes y Vías", "precio": 20, "autor": "Sistema", "fecha": "2026-01-02"},
        {"nombre": "Bloques AutoCAD Sanitarias.dwg", "carrera": "Arquitectura", "area": "Instalaciones", "precio": 20, "autor": "Sistema", "fecha": "2026-01-05"}
    ]

# --- 3. LISTAS DE DATOS (CONTEXTO PERÚ) ---
UNIVERSIDADES = [
    "UPN - Universidad Privada del Norte",
    "UNI - Universidad Nacional de Ingeniería",
    "PUCP - Pontificia Universidad Católica del Perú",
    "UPC - Universidad Peruana de Ciencias Aplicadas",
    "UTP - Universidad Tecnológica del Perú",
    "UNMSM - Universidad Nacional Mayor de San Marcos",
    "UCV - Universidad César Vallejo",
    "URP - Universidad Ricardo Palma",
    "UNFV - Universidad Nacional Federico Villarreal",
    "SENCICO (Técnico)",
    "Otra"
]

CARRERAS = {
    "Ingeniería Civil": ["Estructuras", "Geotecnia", "Hidráulica", "Transportes y Vías", "Construcción y Gestión (BIM)", "Materiales"],
    "Arquitectura": ["Diseño Arquitectónico", "Urbanismo", "Paisajismo", "Interiorismo", "Instalaciones"],
    "Ingeniería Geológica": ["Mecánica de Suelos", "Hidrogeología", "Geofísica", "Riesgos Geológicos"],
    "Ingeniería de Minas": ["Seguridad Minera", "Voladura", "Ventilación", "Planeamiento"],
    "Topografía y Geodesia": ["Levantamientos", "Fotogrametría", "Sistemas GIS", "Catastro"]
}

# --- 4. ESTILOS CSS (DISEÑO INGENIERIL) ---
st.markdown("""
<style>
    /* Fondo general */
    .stApp {background-color: #F8F9F9;}
    
    /* Login Box - Estilo Ingeniero */
    .login-box {
        background: white;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.1);
        border-top: 6px solid #C0392B; /* Rojo Ladrillo */
        text-align: center;
    }
    
    /* Billetera Digital */
    .wallet-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #154360 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
        margin-bottom: 20px;
    }
    .wallet-amount { font-size: 2rem; font-weight: bold; color: #F1C40F; }
    .wallet-label { font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; }

    /* Botones */
    div.stButton > button {
        border-radius: 6px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    /* Títulos */
    h1, h2, h3 { color: #2C3E50; }
</style>
""", unsafe_allow_html=True)

# =======================================================
# PÁGINA 1: LOGIN (DISEÑO MEJORADO)
# =======================================================
def login_page():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Contenedor visual del login
        st.markdown("""
        <div class="login-box">
            <img src="https://cdn-icons-png.flaticon.com/512/9387/9387877.png" width="100" style="margin-bottom:15px;">
            <h1 style="margin:0; font-size:2rem;">F.I.T.A. HUB</h1>
            <p style="color:grey; font-size:1.1rem;">Plataforma de Intercambio Técnico</p>
            <hr>
            <p style="font-size:0.9rem;">Acceso exclusivo para Ingenieros y Estudiantes</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Espacio
        
        # Botón grande de Google
        if st.button("🔐 Iniciar Sesión con Google", type="primary", use_container_width=True):
            with st.spinner("Autenticando credenciales..."):
                time.sleep(1.5) # Simula tiempo de carga
                st.session_state['logged_in'] = True
                # Simulamos datos de Google
                st.session_state['usuario']['nombre'] = "Ing. Luigi"
                st.session_state['usuario']['email'] = "luigi@fita.pe"
                st.session_state['usuario']['foto'] = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                st.rerun()

# =======================================================
# PÁGINA 2: ONBOARDING (REGISTRO ACADÉMICO)
# =======================================================
def onboarding_page():
    st.markdown("<h2 style='text-align:center;'>👷 Configuración de Perfil Profesional</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Completa tus datos para personalizar el repositorio.</p>", unsafe_allow_html=True)
    st.write("---")

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            uni = st.selectbox("🏛️ Casa de Estudios", UNIVERSIDADES)
            carrera_sel = st.selectbox("🎓 Carrera Profesional", list(CARRERAS.keys()))
        
        with col2:
            # Las especialidades dependen de la carrera seleccionada
            especialidad = st.selectbox("⭐ Área de Interés Principal", CARRERAS[carrera_sel])
            ciclo = st.slider("📅 Ciclo / Nivel", 1, 10, 7)

        st.info("🎁 **Bono de Bienvenida:** Al completar el registro recibirás **1000 Puntos F.I.T.A.** en tu billetera digital.")
        
        if st.button("💾 Guardar y Acceder", type="primary", use_container_width=True):
            st.session_state['usuario']['universidad'] = uni
            st.session_state['usuario']['carrera'] = carrera_sel
            st.session_state['usuario']['especialidad'] = especialidad
            st.session_state['usuario']['ciclo'] = ciclo
            st.session_state['setup_completo'] = True
            st.balloons()
            time.sleep(1)
            st.rerun()

# =======================================================
# PÁGINA 3: SISTEMA PRINCIPAL
# =======================================================
def main_app():
    # --- BARRA LATERAL (WALLET Y PERFIL) ---
    with st.sidebar:
        st.image("https://cdn-icons-png.flaticon.com/512/2554/2554044.png", width=60)
        st.markdown(f"**{st.session_state['usuario']['nombre']}**")
        st.caption(f"{st.session_state['usuario']['carrera']}")
        
        st.markdown("---")
        
        # BILLETERA DIGITAL
        st.markdown(f"""
        <div class="wallet-card">
            <div class="wallet-label">Saldo Disponible</div>
            <div class="wallet-amount">{st.session_state['puntos']} pts</div>
            <div style="font-size:0.8rem; margin-top:5px;">🪙 FitaCoins</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("📥 Descarga: **-20 pts**\n\n📤 Subida: **+10 pts**")
        
        st.markdown("---")
        menu = st.radio("Navegación", ["📂 Repositorio de Archivos", "📤 Subir Aporte (+10 pts)", "👤 Mi Perfil"])
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['setup_completo'] = False
            st.rerun()

    # --- PESTAÑA: REPOSITORIO (DESCARGAS) ---
    if menu == "📂 Repositorio de Archivos":
        st.title("📂 Biblioteca Técnica Nacional")
        st.markdown("Explora recursos organizados por carrera y especialidad.")
        
        # FILTROS
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            filtro_carrera = st.selectbox("Filtrar por Carrera", ["Todas"] + list(CARRERAS.keys()))
        with col_f2:
            if filtro_carrera != "Todas":
                filtro_area = st.selectbox("Filtrar por Especialidad", ["Todas"] + CARRERAS[filtro_carrera])
            else:
                filtro_area = "Todas"
                st.selectbox("Especialidad", ["Selecciona una carrera primero"], disabled=True)

        st.markdown("---")

        # LOGICA DE FILTRADO
        archivos_mostrar = st.session_state['repositorio']
        if filtro_carrera != "Todas":
            archivos_mostrar = [f for f in archivos_mostrar if f['carrera'] == filtro_carrera]
            if filtro_area != "Todas":
                archivos_mostrar = [f for f in archivos_mostrar if f['area'] == filtro_area]

        # MOSTRAR ARCHIVOS
        if not archivos_mostrar:
            st.warning("No hay archivos en esta categoría. ¡Sube uno y gana puntos!")
        else:
            for idx, archivo in enumerate(archivos_mostrar):
                with st.container():
                    c1, c2, c3 = st.columns([3, 1, 1])
                    with c1:
                        st.subheader(f"📄 {archivo['nombre']}")
                        st.caption(f"📌 {archivo['carrera']} | {archivo['area']} | Autor: {archivo['autor']}")
                    with c2:
                        st.write("") # Espacio
                    with c3:
                        st.write("")
                        # BOTON DE DESCARGA CON COBRO
                        if st.button(f"⬇️ Bajar (-20 pts)", key=f"btn_{idx}"):
                            if st.session_state['puntos'] >= 20:
                                st.session_state['puntos'] -= 20
                                st.toast(f"✅ Descarga iniciada. Nuevo saldo: {st.session_state['puntos']}", icon="📉")
                                # Simulación de descarga
                                st.download_button(
                                    label="Confirmar Guardado",
                                    data="Contenido Simulado del Archivo",
                                    file_name=archivo['nombre'],
                                    key=f"dl_{idx}"
                                )
                            else:
                                st.error("❌ Saldo insuficiente. Sube archivos para ganar puntos.")
                    st.divider()

    # --- PESTAÑA: SUBIR (GANAR PUNTOS) ---
    elif menu == "📤 Subir Aporte (+10 pts)":
        st.title("📤 Contribuye a la Comunidad")
        st.markdown("Comparte exámenes pasados, plantillas excel o planos. **Ganancia: +10 Puntos.**")
        
        with st.form("upload_form"):
            uploaded = st.file_uploader("Selecciona archivo (PDF, DWG, XLSX)", type=["pdf", "xlsx", "dwg", "docx"])
            
            c1, c2 = st.columns(2)
            with c1:
                # Selectores inteligentes basados en las listas peruanas
                u_carrera = st.selectbox("Carrera", list(CARRERAS.keys()))
            with c2:
                u_area = st.selectbox("Especialidad", CARRERAS[u_carrera])
            
            submit = st.form_submit_button("🚀 Publicar y Ganar Puntos")
            
            if submit and uploaded:
                # Simulación de carga
                with st.spinner("Subiendo a la nube F.I.T.A..."):
                    time.sleep(1)
                
                # Lógica de Puntos
                st.session_state['puntos'] += 10
                
                # Guardar en repositorio
                nuevo_doc = {
                    "nombre": uploaded.name,
                    "carrera": u_carrera,
                    "area": u_area,
                    "precio": 20,
                    "autor": st.session_state['usuario']['nombre'],
                    "fecha": datetime.now().strftime("%Y-%m-%d")
                }
                st.session_state['repositorio'].append(nuevo_doc)
                
                st.balloons()
                st.success(f"¡Archivo subido! Has ganado 10 puntos. Saldo actual: {st.session_state['puntos']}")
                time.sleep(2)
                st.rerun()

    # --- PESTAÑA: PERFIL ---
    elif menu == "👤 Mi Perfil":
        st.title("👤 Legajo Personal")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(st.session_state['usuario']['foto'], width=150)
        with col2:
            st.header(st.session_state['usuario']['nombre'])
            st.write(f"**Universidad:** {st.session_state['usuario']['universidad']}")
            st.write(f"**Carrera:** {st.session_state['usuario']['carrera']}")
            st.write(f"**Especialidad:** {st.session_state['usuario']['especialidad']}")
            st.write(f"**Ciclo:** {st.session_state['usuario']['ciclo']}")
            
        st.markdown("### Historial de Transacciones")
        st.info("Apertura de cuenta: +1000 pts (Bono Inicial)")


# =======================================================
# EJECUCIÓN (MAIN)
# =======================================================
if not st.session_state['logged_in']:
    login_page()
elif not st.session_state['setup_completo']:
    onboarding_page()
else:
    main_app()
