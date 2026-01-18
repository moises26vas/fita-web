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

# --- 2. BASE DE DATOS SIMULADA ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'setup_completo' not in st.session_state:
    st.session_state['setup_completo'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = {}
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = 1000 
if 'repositorio' not in st.session_state:
    st.session_state['repositorio'] = [
        {"nombre": "Silabo Estática 2026.pdf", "carrera": "Ingeniería Civil", "area": "Estructuras", "autor": "Docente Admin", "rol_autor": "Docente", "fecha": "2026-01-10"},
        {"nombre": "Examen Parcial Pasado.pdf", "carrera": "Ingeniería Civil", "area": "Geotecnia", "autor": "Pepito Estudiante", "rol_autor": "Estudiante", "fecha": "2026-01-12"}
    ]

# --- 3. LISTAS DE DATOS ---
UNIVERSIDADES = ["UPN", "UNI", "PUCP", "UPC", "UTP", "UNMSM", "UCV", "URP", "UNFV", "SENCICO", "Otra"]
CARRERAS = {
    "Ingeniería Civil": ["Estructuras", "Geotecnia", "Hidráulica", "Transportes", "Construcción"],
    "Arquitectura": ["Diseño", "Urbanismo", "Interiores"],
    "Ing. de Minas": ["Seguridad", "Operaciones", "Planeamiento"],
    "Topografía": ["Cadastral", "Satelital"]
}

# --- 4. ESTILOS CSS ---
st.markdown("""
<style>
    .stApp {background-color: #F4F6F7;}
    .login-box {
        background: white; padding: 40px; border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.1); border-top: 6px solid #C0392B;
        text-align: center;
    }
    .profile-card {
        background: white; padding: 20px; border-radius: 10px;
        border-left: 5px solid #2980B9; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .role-badge-estudiante {
        background-color: #D6EAF8; color: #2E86C1; padding: 5px 10px; border-radius: 15px; font-weight: bold; font-size: 0.8rem;
    }
    .role-badge-docente {
        background-color: #FCF3CF; color: #B7950B; padding: 5px 10px; border-radius: 15px; font-weight: bold; font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# =======================================================
# PÁGINA 1: LOGIN
# =======================================================
def login_page():
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="login-box">
            <img src="https://cdn-icons-png.flaticon.com/512/9387/9387877.png" width="80">
            <h2>F.I.T.A. ACCESS</h2>
            <p>Identificación Digital para Ingenieros</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔐 Acceder con Google", type="primary", use_container_width=True):
            with st.spinner("Verificando identidad..."):
                time.sleep(1)
                st.session_state['logged_in'] = True
                # Datos simulados de la cuenta Google
                st.session_state['usuario']['nombre'] = "Luigi" 
                st.session_state['usuario']['email'] = "luigi@upn.pe"
                st.session_state['usuario']['foto'] = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                st.rerun()

# =======================================================
# PÁGINA 2: ONBOARDING (CONFIGURACIÓN DE ROL)
# =======================================================
def onboarding_page():
    st.markdown("<h2 style='text-align:center;'>🛠️ Configuración de Perfil</h2>", unsafe_allow_html=True)
    st.write("---")

    with st.container():
        # PREGUNTA CLAVE: ¿ESTUDIANTE O DOCENTE?
        rol = st.radio("Selecciona tu Rol Académico:", ["Estudiante", "Docente / Maestro"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            uni = st.selectbox("Universidad / Institución", UNIVERSIDADES)
            carrera_sel = st.selectbox("Carrera / Facultad", list(CARRERAS.keys()))
        
        with col2:
            especialidad = st.selectbox("Área de Enfoque", CARRERAS[carrera_sel])
            
            # LÓGICA DINÁMICA SEGÚN ROL
            if rol == "Estudiante":
                nivel_dato = st.slider("Ciclo Actual", 1, 10, 5)
                etiqueta_nivel = f"Ciclo {nivel_dato}"
            else:
                nivel_dato = st.selectbox("Grado Académico", ["Bachiller", "Ingeniero Titulado", "Magister", "Doctor"])
                etiqueta_nivel = nivel_dato

        st.info(f"Registrando usuario como: **{rol}** de **{carrera_sel}**")
        
        if st.button("💾 Finalizar Registro", type="primary", use_container_width=True):
            st.session_state['usuario']['rol'] = "Estudiante" if rol == "Estudiante" else "Docente"
            st.session_state['usuario']['universidad'] = uni
            st.session_state['usuario']['carrera'] = carrera_sel
            st.session_state['usuario']['especialidad'] = especialidad
            st.session_state['usuario']['nivel'] = etiqueta_nivel # Guarda "Ciclo 5" o "Magister"
            st.session_state['setup_completo'] = True
            st.rerun()

# =======================================================
# PÁGINA 3: SISTEMA PRINCIPAL
# =======================================================
def main_app():
    # --- BARRA LATERAL ---
    with st.sidebar:
        st.image(st.session_state['usuario']['foto'], width=60)
        st.write(f"**{st.session_state['usuario']['nombre']}**")
        
        # Etiqueta de Rol debajo del nombre
        rol_user = st.session_state['usuario']['rol']
        if rol_user == "Estudiante":
            st.markdown(f'<span class="role-badge-estudiante">🎓 Estudiante</span>', unsafe_allow_html=True)
        else:
            st.markdown(f'<span class="role-badge-docente">👨‍🏫 Docente</span>', unsafe_allow_html=True)
            
        st.write(f"_{st.session_state['usuario']['universidad']}_")
        
        st.markdown("---")
        st.markdown(f"💰 **Billetera:** {st.session_state['puntos']} pts")
        st.markdown("---")
        
        menu = st.radio("Menú", ["📂 Repositorio", "📤 Subir Archivo", "👤 Mi Perfil"])
        
        st.markdown("---")
        if st.button("Salir"):
            st.session_state['logged_in'] = False
            st.session_state['setup_completo'] = False
            st.rerun()

    # --- PESTAÑA PERFIL (AQUÍ SE VEN LOS DATOS) ---
    if menu == "👤 Mi Perfil":
        st.title("👤 Datos del Usuario")
        
        # Diseño de Tarjeta de Identificación
        st.markdown(f"""
        <div class="profile-card">
            <div style="display:flex; align-items:center; gap:20px;">
                <img src="{st.session_state['usuario']['foto']}" width="100" style="border-radius:50%;">
                <div>
                    <h2 style="margin:0;">{st.session_state['usuario']['nombre']}</h2>
                    <p style="color:grey; margin:0;">{st.session_state['usuario']['email']}</p>
                    <br>
                    <span class="{'role-badge-estudiante' if st.session_state['usuario']['rol'] == 'Estudiante' else 'role-badge-docente'}">
                        {st.session_state['usuario']['rol'].upper()}
                    </span>
                </div>
            </div>
            <hr>
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:20px;">
                <div>
                    <small>INSTITUCIÓN</small><br>
                    <b>{st.session_state['usuario']['universidad']}</b>
                </div>
                <div>
                    <small>CARRERA</small><br>
                    <b>{st.session_state['usuario']['carrera']}</b>
                </div>
                <div>
                    <small>ESPECIALIDAD</small><br>
                    <b>{st.session_state['usuario']['especialidad']}</b>
                </div>
                <div>
                    <small>{'CICLO ACTUAL' if st.session_state['usuario']['rol'] == 'Estudiante' else 'GRADO ACADÉMICO'}</small><br>
                    <b>{st.session_state['usuario']['nivel']}</b>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- PESTAÑA REPOSITORIO ---
    elif menu == "📂 Repositorio":
        st.title("📂 Archivos Académicos")
        
        st.write("Explora documentos subidos por Estudiantes y Docentes.")
        
        for arch in st.session_state['repositorio']:
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    icon = "👨‍🏫" if arch.get('rol_autor') == "Docente" else "🎓"
                    st.subheader(f"📄 {arch['nombre']}")
                    st.caption(f"{icon} Subido por: {arch['autor']} ({arch.get('rol_autor', 'Usuario')}) | {arch['carrera']}")
                with c2:
                    if st.button(f"⬇️ Bajar (-20 pts)", key=arch['nombre']):
                        if st.session_state['puntos'] >= 20:
                            st.session_state['puntos'] -= 20
                            st.toast("Descarga iniciada", icon="✅")
                        else:
                            st.error("Saldo insuficiente")
                st.divider()

    # --- PESTAÑA SUBIR ---
    elif menu == "📤 Subir Archivo":
        st.title("📤 Aportar Material")
        with st.form("up_form"):
            file = st.file_uploader("Archivo")
            desc = st.text_input("Descripción")
            if st.form_submit_button("Subir"):
                if file:
                    st.session_state['puntos'] += 10
                    # Guardamos quién lo subió y qué rol tiene
                    st.session_state['repositorio'].append({
                        "nombre": file.name,
                        "carrera": st.session_state['usuario']['carrera'],
                        "area": st.session_state['usuario']['especialidad'],
                        "autor": st.session_state['usuario']['nombre'],
                        "rol_autor": st.session_state['usuario']['rol'], # IMPORTANTE: Guardamos el rol
                        "fecha": datetime.now().strftime("%Y-%m-%d")
                    })
                    st.success("Subido correctamente (+10 pts)")
                    time.sleep(1)
                    st.rerun()

# =======================================================
# MAIN
# =======================================================
if not st.session_state['logged_in']:
    login_page()
elif not st.session_state['setup_completo']:
    onboarding_page()
else:
    main_app()
