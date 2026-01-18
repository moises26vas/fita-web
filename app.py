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

# --- 2. GESTIÓN DE MEMORIA (SESSION STATE) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'setup_completo' not in st.session_state:
    st.session_state['setup_completo'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = {}
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = 1000  # Bono inicial
if 'repositorio' not in st.session_state:
    # Datos iniciales de ejemplo
    st.session_state['repositorio'] = [
        {"nombre": "Norma E.030 Sismorresistente.pdf", "carrera": "Ingeniería Civil", "area": "Estructuras", "autor": "Ing. Admin", "rol_autor": "Docente", "fecha": "2026-01-15"},
        {"nombre": "Plano Topográfico Lote 4.dwg", "carrera": "Topografía", "area": "Levantamientos", "autor": "Juan Perez", "rol_autor": "Estudiante", "fecha": "2026-01-16"}
    ]

# --- 3. DATOS PERÚ ---
UNIVERSIDADES = ["UPN", "UNI", "PUCP", "UPC", "UTP", "UNMSM", "UCV", "URP", "UNFV", "SENCICO", "Otra"]
CARRERAS = {
    "Ingeniería Civil": ["Estructuras", "Geotecnia", "Hidráulica", "Vías y Transportes", "Construcción"],
    "Arquitectura": ["Diseño", "Urbanismo", "Interiores", "Paisajismo"],
    "Ing. de Minas": ["Seguridad", "Operaciones", "Planeamiento", "Geología"],
    "Topografía": ["Cadastral", "Satelital", "Geodesia"]
}

# --- 4. ESTILOS CSS (CORRECCIÓN DE COLORES Y TEXTO) ---
# Aquí forzamos colores oscuros para el texto y fondos claros para los contenedores
st.markdown("""
<style>
    /* Fondo General más claro */
    [data-testid="stAppViewContainer"] {
        background-color: #F2F4F4;
    }
    
    /* FORZAR TEXTO OSCURO EN TODA LA APP */
    h1, h2, h3, h4, h5, h6, p, div, span, label {
        color: #17202A !important;
    }
    
    /* Caja de Login */
    .login-box {
        background-color: #FFFFFF;
        padding: 40px;
        border-radius: 15px;
        box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
        border-top: 6px solid #C0392B; /* Rojo Ladrillo */
        text-align: center;
    }
    
    /* Tarjetas de Archivos */
    .file-card {
        background-color: #FFFFFF;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #2980B9;
        margin-bottom: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* Billetera Digital */
    .wallet-card {
        background: linear-gradient(135deg, #154360 0%, #1A5276 100%);
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        color: white !important; /* Excepción: Texto blanco en la billetera */
        margin-bottom: 20px;
    }
    .wallet-card div { color: white !important; } /* Asegurar hijos blancos */
    
    /* Etiquetas de Rol */
    .badge-estudiante {
        background-color: #D6EAF8; color: #2874A6 !important; 
        padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem;
    }
    .badge-docente {
        background-color: #FCF3CF; color: #9A7D0A !important; 
        padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem;
    }
    
    /* Ajuste de Botones */
    div.stButton > button {
        color: #FFFFFF !important; /* Texto botón blanco */
        background-color: #2C3E50;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# =======================================================
# PANTALLA 1: INICIO DE SESIÓN
# =======================================================
def login_page():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        # Contenedor HTML puro para control total del diseño
        st.markdown("""
        <div class="login-box">
            <img src="https://cdn-icons-png.flaticon.com/512/9387/9387877.png" width="80" style="margin-bottom:15px;">
            <h1 style="margin:0; font-size:2rem; color:#154360 !important;">F.I.T.A. HUB</h1>
            <p style="color:#7F8C8D !important; font-size:1.1rem;">Plataforma de Ingeniería Peruana</p>
            <hr>
            <p style="font-size:0.9rem; color:#2C3E50 !important;">Acceso exclusivo comunidad universitaria</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") 
        
        # Botón nativo de Streamlit
        if st.button("🔐 Iniciar Sesión con Google", type="primary", use_container_width=True):
            with st.spinner("Conectando con servidores..."):
                time.sleep(1.5)
                st.session_state['logged_in'] = True
                # Simulamos datos recibidos de Google
                st.session_state['usuario']['nombre'] = "Ing. Luigi"
                st.session_state['usuario']['email'] = "luigi@upn.pe"
                st.session_state['usuario']['foto'] = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                st.rerun()

# =======================================================
# PANTALLA 2: REGISTRO DE ROL (ONBOARDING)
# =======================================================
def onboarding_page():
    st.markdown("<h2 style='text-align:center;'>🛠️ Configuración de Perfil</h2>", unsafe_allow_html=True)
    st.write("---")

    with st.container():
        # Selección de Rol
        rol_seleccionado = st.radio("¿Cuál es tu rol académico?", ["Estudiante", "Docente / Maestro"], horizontal=True)
        
        c1, c2 = st.columns(2)
        with c1:
            uni = st.selectbox("Universidad / Instituto", UNIVERSIDADES)
            carrera = st.selectbox("Carrera Profesional", list(CARRERAS.keys()))
        
        with c2:
            area = st.selectbox("Especialidad Principal", CARRERAS[carrera])
            
            # Condicional según el rol
            if rol_seleccionado == "Estudiante":
                nivel = st.slider("Ciclo Actual", 1, 10, 5)
                nivel_txt = f"Ciclo {nivel}"
            else:
                nivel_txt = st.selectbox("Grado Académico", ["Bachiller", "Ing. Titulado", "Magíster", "Doctor"])
        
        st.info("🎁 **Bono de Bienvenida:** Recibirás 1000 FitaCoins al completar el registro.")
        
        if st.button("💾 Guardar Datos", type="primary", use_container_width=True):
            st.session_state['usuario']['rol'] = "Estudiante" if rol_seleccionado == "Estudiante" else "Docente"
            st.session_state['usuario']['universidad'] = uni
            st.session_state['usuario']['carrera'] = carrera
            st.session_state['usuario']['especialidad'] = area
            st.session_state['usuario']['nivel'] = nivel_txt
            st.session_state['setup_completo'] = True
            st.balloons()
            time.sleep(1)
            st.rerun()

# =======================================================
# PANTALLA 3: SISTEMA PRINCIPAL (APP)
# =======================================================
def main_app():
    # --- BARRA LATERAL ---
    with st.sidebar:
        # Foto y Datos
        st.image(st.session_state['usuario']['foto'], width=70)
        st.markdown(f"**{st.session_state['usuario']['nombre']}**")
        
        # Badge de Rol
        if st.session_state['usuario']['rol'] == "Estudiante":
            st.markdown('<span class="badge-estudiante">🎓 Estudiante</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge-docente">👨‍🏫 Docente</span>', unsafe_allow_html=True)
            
        st.caption(f"{st.session_state['usuario']['universidad']}")
        
        st.markdown("---")
        
        # Billetera
        st.markdown(f"""
        <div class="wallet-card">
            <div style="font-size:0.8rem; text-transform:uppercase;">Saldo F.I.T.A.</div>
            <div style="font-size:2rem; font-weight:bold; color:#F1C40F !important;">{st.session_state['puntos']}</div>
            <div style="font-size:0.8rem;">puntos disponibles</div>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("Menú", ["📂 Repositorio", "📤 Subir y Ganar (+10)", "👤 Mi Perfil"])
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['setup_completo'] = False
            st.rerun()

    # --- PESTAÑA 1: REPOSITORIO ---
    if menu == "📂 Repositorio":
        st.title("📂 Biblioteca Técnica")
        
        # Filtros
        colf1, colf2 = st.columns(2)
        with colf1:
            filtro_carrera = st.selectbox("Filtrar por Carrera", ["Todas"] + list(CARRERAS.keys()))
        
        # Mostrar Archivos
        archivos = st.session_state['repositorio']
        if filtro_carrera != "Todas":
            archivos = [f for f in archivos if f['carrera'] == filtro_carrera]
            
        if not archivos:
            st.warning("No hay archivos en esta categoría.")
        
        for idx, file in enumerate(archivos):
            # Tarjeta de archivo
            with st.container():
                st.markdown(f"""
                <div class="file-card">
                    <div style="display:flex; justify-content:space-between;">
                        <div>
                            <h4 style="margin:0;">📄 {file['nombre']}</h4>
                            <small><b>{file['carrera']}</b> | {file['area']}</small><br>
                            <small style="color:#566573 !important;">Subido por: {file['autor']} ({file.get('rol_autor','Usuario')}) | {file['fecha']}</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Botón de Descarga (fuera del HTML para que funcione la lógica Python)
                col_d1, col_d2 = st.columns([4, 1])
                with col_d2:
                    if st.button(f"⬇️ Bajar (-20 pts)", key=f"btn_{idx}"):
                        if st.session_state['puntos'] >= 20:
                            st.session_state['puntos'] -= 20
                            st.toast("✅ Descarga iniciada. Puntos descontados.", icon="📉")
                        else:
                            st.error("❌ Saldo insuficiente.")
                st.divider()

    # --- PESTAÑA 2: SUBIR ARCHIVOS ---
    elif menu == "📤 Subir y Ganar (+10)":
        st.title("📤 Aportar Conocimiento")
        st.info("Gana **10 Puntos** por cada documento académico útil que compartas.")
        
        with st.form("upload_form"):
            uploaded = st.file_uploader("Seleccionar Archivo (PDF, Excel, DWG)", type=["pdf","xlsx","dwg","docx"])
            desc = st.text_input("Descripción breve")
            
            c1, c2 = st.columns(2)
            with c1:
                cat_carrera = st.selectbox("Carrera", list(CARRERAS.keys()))
            with c2:
                cat_area = st.selectbox("Especialidad", CARRERAS[cat_carrera])
            
            if st.form_submit_button("🚀 Publicar Aporte"):
                if uploaded:
                    st.session_state['puntos'] += 10
                    nuevo_file = {
                        "nombre": uploaded.name,
                        "carrera": cat_carrera,
                        "area": cat_area,
                        "autor": st.session_state['usuario']['nombre'],
                        "rol_autor": st.session_state['usuario']['rol'],
                        "fecha": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state['repositorio'].append(nuevo_file)
                    st.success("¡Archivo subido exitosamente! (+10 pts)")
                    time.sleep(1.5)
                    st.rerun()

    # --- PESTAÑA 3: PERFIL ---
    elif menu == "👤 Mi Perfil":
        st.title("👤 Credencial Digital")
        
        # Tarjeta de Perfil
        st.markdown(f"""
        <div style="background:white; padding:30px; border-radius:10px; border-top: 5px solid #1F618D; box-shadow:0 4px 10px rgba(0,0,0,0.1);">
            <div style="display:flex; align-items:center; gap:20px;">
                <img src="{st.session_state['usuario']['foto']}" width="120" style="border-radius:50%; border:3px solid #EBEDEF;">
                <div>
                    <h2 style="margin:0; color:#154360 !important;">{st.session_state['usuario']['nombre'].upper()}</h2>
                    <p style="margin:0; color:grey !important;">{st.session_state['usuario']['email']}</p>
                    <br>
                    <span style="background:#EB984E; color:white; padding:5px 15px; border-radius:20px; font-weight:bold;">
                        {st.session_state['usuario']['rol'].upper()}
                    </span>
                </div>
            </div>
            <hr>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px; margin-top:20px;">
                <div>
                    <label style="font-weight:bold; font-size:0.8rem; color:#85929E !important;">UNIVERSIDAD</label>
                    <div style="font-size:1.1rem;">{st.session_state['usuario']['universidad']}</div>
                </div>
                <div>
                    <label style="font-weight:bold; font-size:0.8rem; color:#85929E !important;">CARRERA</label>
                    <div style="font-size:1.1rem;">{st.session_state['usuario']['carrera']}</div>
                </div>
                <div>
                    <label style="font-weight:bold; font-size:0.8rem; color:#85929E !important;">NIVEL ACADÉMICO</label>
                    <div style="font-size:1.1rem;">{st.session_state['usuario']['nivel']}</div>
                </div>
                <div>
                    <label style="font-weight:bold; font-size:0.8rem; color:#85929E !important;">ESPECIALIDAD</label>
                    <div style="font-size:1.1rem;">{st.session_state['usuario']['especialidad']}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# =======================================================
# CONTROL DE FLUJO
# =======================================================
if not st.session_state['logged_in']:
    login_page()
elif not st.session_state['setup_completo']:
    onboarding_page()
else:
    main_app()
