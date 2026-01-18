import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DEL SISTEMA ---
st.set_page_config(
    page_title="F.I.T.A. Construction Hub",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. GESTIÓN DE MEMORIA Y ESTADO (DATABASE SIMULADA) ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'setup_completo' not in st.session_state:
    st.session_state['setup_completo'] = False
if 'usuario' not in st.session_state:
    st.session_state['usuario'] = {}
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = 1000  # Bono inicial
if 'transacciones' not in st.session_state:
    st.session_state['transacciones'] = [
        {"tipo": "Ingreso", "monto": 1000, "desc": "Bono de Bienvenida", "fecha": datetime.now().strftime("%Y-%m-%d")}
    ]
if 'repositorio' not in st.session_state:
    st.session_state['repositorio'] = [
        {"nombre": "Norma E.030 Diseño Sismorresistente.pdf", "carrera": "Ingeniería Civil", "area": "Estructuras", "autor": "Admin Sistema", "rol_autor": "Docente", "fecha": "2026-01-15", "desc": "Norma actualizada del RNE."},
        {"nombre": "Plantilla Metrados Acero.xlsx", "carrera": "Ingeniería Civil", "area": "Construcción", "autor": "Luigi", "rol_autor": "Estudiante", "fecha": "2026-01-16", "desc": "Excel automatizado para vigas."}
    ]

# --- 3. LISTAS DE DATOS PERÚ ---
UNIVERSIDADES = ["UPN - Universidad Privada del Norte", "UNI - Universidad Nacional de Ingeniería", "PUCP - Católica", "UPC", "UTP", "UNMSM", "UCV", "URP", "SENCICO", "Otra"]
CARRERAS = {
    "Ingeniería Civil": ["Estructuras", "Geotecnia", "Hidráulica", "Vías y Transportes", "Gestión de Proyectos (BIM)"],
    "Arquitectura": ["Diseño Arquitectónico", "Urbanismo", "Interiores", "Paisajismo"],
    "Ing. de Minas": ["Seguridad Minera", "Operaciones", "Planeamiento", "Geología"],
    "Topografía": ["Levantamientos", "Fotogrametría", "Sistemas GIS"]
}

# --- 4. ESTILOS CSS (CORRECCIÓN DE MENÚS DESPLEGABLES) ---
st.markdown("""
<style>
    /* 1. FONDO GENERAL */
    [data-testid="stAppViewContainer"] {
        background-color: #F4F6F7;
    }

    /* 2. TEXTO NEGRO GENERAL */
    h1, h2, h3, h4, h5, h6, p, span, label, div {
        color: #17202A;
    }

    /* 3. --- ARREGLO CRÍTICO DE MENÚS (DROPDOWNS) --- */
    /* Forzar fondo BLANCO y texto NEGRO en la caja de selección */
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #BDC3C7;
    }
    
    /* Forzar fondo BLANCO en la lista desplegable (el menú que se abre) */
    div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        border: 1px solid #BDC3C7;
    }
    
    /* Forzar fondo BLANCO en cada opción de la lista */
    ul[data-baseweb="menu"] {
        background-color: #FFFFFF !important;
    }
    
    /* Forzar color NEGRO en el texto de las opciones */
    li[data-baseweb="option"] {
        color: #000000 !important;
    }
    
    /* Color azulito cuando pasas el mouse por encima de una opción */
    li[data-baseweb="option"]:hover, li[aria-selected="true"] {
        background-color: #D6EAF8 !important;
        color: #000000 !important;
    }
    
    /* Color del texto seleccionado dentro de la caja */
    div[data-testid="stMarkdownContainer"] p {
        color: #17202A !important;
    }

    /* 4. TARJETAS */
    .login-card {
        background-color: white; padding: 40px; border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 5px solid #E74C3C;
    }
    .file-card {
        background-color: white; padding: 20px; border-radius: 10px;
        border-left: 5px solid #2980B9; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    .wallet-box {
        background: linear-gradient(135deg, #154360 0%, #1A5276 100%);
        padding: 25px; border-radius: 12px; text-align: center;
        margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    /* Excepción para texto blanco SOLO en billetera y botones */
    .wallet-box h2, .wallet-box div { color: #FFFFFF !important; }
    .stButton > button { color: #FFFFFF !important; background-color: #212F3D; border: none; }
    
    /* Badges */
    .badge { padding: 5px 12px; border-radius: 15px; font-weight: bold; font-size: 0.85rem; }
    .estudiante { background-color: #D4E6F1; color: #154360 !important; }
    .docente { background-color: #FCF3CF; color: #7D6608 !important; }

</style>
""", unsafe_allow_html=True)

# =======================================================
# LÓGICA DE NEGOCIO
# =======================================================
def registrar_transaccion(tipo, monto, descripcion):
    st.session_state['transacciones'].append({
        "tipo": tipo, "monto": monto, "desc": descripcion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

# =======================================================
# PANTALLA 1: LOGIN
# =======================================================
def login_page():
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <div class="login-card">
            <img src="https://cdn-icons-png.flaticon.com/512/9387/9387877.png" width="90">
            <h1 style="margin-top:10px;">F.I.T.A. ACCESS</h1>
            <p>Plataforma Nacional de Ingeniería</p>
            <hr>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔐 Iniciar Sesión Segura (Google Auth)", type="primary", use_container_width=True):
            with st.spinner("Validando credenciales..."):
                time.sleep(1.5)
                st.session_state['logged_in'] = True
                st.session_state['usuario'] = {
                    'nombre': "Ing. Luigi", 'email': "luigi.ing@upn.pe",
                    'foto': "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                }
                st.rerun()

# =======================================================
# PANTALLA 2: ONBOARDING
# =======================================================
def onboarding_page():
    st.markdown("<h1 style='text-align:center;'>🛠️ Configuración de Perfil Académico</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Personalización de contenido.</p>", unsafe_allow_html=True)
    st.write("---")

    with st.container():
        rol = st.radio("Selecciona tu Jerarquía:", ["Estudiante Universitario/Técnico", "Docente / Profesional"], horizontal=True)
        
        c1, c2 = st.columns(2)
        with c1:
            # Estos son los menús que ahora saldrán con fondo blanco
            uni = st.selectbox("Institución Educativa", UNIVERSIDADES)
            carrera = st.selectbox("Carrera Profesional", list(CARRERAS.keys()))
        with c2:
            area = st.selectbox("Especialidad / Interés", CARRERAS[carrera])
            if "Estudiante" in rol:
                nivel = st.slider("Ciclo Académico", 1, 10, 5)
                nivel_txt = f"Ciclo {nivel}"
                rol_corto = "Estudiante"
            else:
                nivel_txt = st.selectbox("Grado Académico", ["Bachiller", "Titulado", "Magíster", "Doctor"])
                rol_corto = "Docente"

        st.info("ℹ️ Al registrarte, se creará automáticamente tu Billetera Digital con 1000 Puntos.")
        
        if st.button("💾 Guardar e Ingresar", use_container_width=True):
            st.session_state['usuario'].update({
                'rol': rol_corto, 'universidad': uni, 'carrera': carrera,
                'especialidad': area, 'nivel': nivel_txt
            })
            st.session_state['setup_completo'] = True
            st.balloons()
            time.sleep(1)
            st.rerun()

# =======================================================
# PANTALLA 3: APP PRINCIPAL
# =======================================================
def main_app():
    with st.sidebar:
        st.image(st.session_state['usuario']['foto'], width=80)
        st.write(f"**{st.session_state['usuario']['nombre']}**")
        
        if st.session_state['usuario']['rol'] == "Estudiante":
            st.markdown('<span class="badge estudiante">🎓 Estudiante</span>', unsafe_allow_html=True)
        else:
            st.markdown('<span class="badge docente">👨‍🏫 Docente</span>', unsafe_allow_html=True)
            
        st.caption(st.session_state['usuario']['universidad'])
        st.markdown("---")
        
        st.markdown(f"""
        <div class="wallet-box">
            <div style="font-size:0.8rem; opacity:0.8;">SALDO DISPONIBLE</div>
            <h2 style="margin:5px 0;">{st.session_state['puntos']} pts</h2>
            <div style="font-size:0.7rem;">🪙 FitaCoins</div>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("Navegación", ["🏠 Inicio", "📂 Repositorio Global", "📤 Subir Material", "👤 Mi Perfil & Wallet"])
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['setup_completo'] = False
            st.rerun()

    # --- INICIO ---
    if menu == "🏠 Inicio":
        st.title("🏠 Panel de Control")
        col1, col2, col3 = st.columns(3)
        col1.metric("Archivos", len(st.session_state['repositorio']))
        col2.metric("Tu Saldo", f"{st.session_state['puntos']} pts")
        col3.metric("Nivel", "Premium")
        
        c1, c2 = st.columns(2)
        with c1:
            st.info("📂 **Buscar Archivos:** Encuentra planos y normas.")
        with c2:
            st.success("📤 **Subir Archivos:** Gana +10 puntos por aporte.")

    # --- REPOSITORIO ---
    elif menu == "📂 Repositorio Global":
        st.title("📂 Biblioteca Técnica")
        st.markdown("Costo por descarga: **20 pts**.")
        
        with st.expander("🔍 Filtros de Búsqueda", expanded=True):
            colf1, colf2 = st.columns(2)
            f_carrera = colf1.selectbox("Carrera", ["Todas"] + list(CARRERAS.keys()))
            opciones_area = ["Todas"] + CARRERAS[f_carrera] if f_carrera != "Todas" else ["Todas"]
            f_area = colf2.selectbox("Especialidad", opciones_area)

        archivos = st.session_state['repositorio']
        if f_carrera != "Todas": archivos = [a for a in archivos if a['carrera'] == f_carrera]
        if f_area != "Todas": archivos = [a for a in archivos if a['area'] == f_area]

        if not archivos: st.warning("No se encontraron archivos.")
        
        for idx, file in enumerate(archivos):
            with st.container():
                col_info, col_btn = st.columns([4, 1])
                with col_info:
                    st.markdown(f"""
                    <div class="file-card">
                        <h4 style="margin:0;">📄 {file['nombre']}</h4>
                        <p style="margin:5px 0;">{file['desc']}</p>
                        <small>{file['carrera']} | {file['area']} | Autor: <b>{file['autor']}</b></small>
                    </div>
                    """, unsafe_allow_html=True)
                with col_btn:
                    st.write("")
                    if st.button(f"⬇️ Bajar", key=f"dl_{idx}"):
                        if st.session_state['puntos'] >= 20:
                            st.session_state['puntos'] -= 20
                            registrar_transaccion("Gasto", 20, f"Descarga: {file['nombre']}")
                            st.toast("✅ Descarga iniciada (-20 pts)", icon="📉")
                        else:
                            st.error("❌ Saldo insuficiente")

    # --- SUBIR ---
    elif menu == "📤 Subir Material":
        st.title("📤 Aportar a la Comunidad")
        with st.form("upload_form"):
            st.write("Gana **10 Puntos** por aporte.")
            uploaded = st.file_uploader("Archivo")
            c1, c2 = st.columns(2)
            u_carrera = c1.selectbox("Carrera", list(CARRERAS.keys()))
            u_area = c2.selectbox("Área", CARRERAS[u_carrera])
            desc = st.text_input("Descripción")
            
            if st.form_submit_button("🚀 Publicar Aporte"):
                if uploaded and desc:
                    st.session_state['puntos'] += 10
                    registrar_transaccion("Ingreso", 10, f"Aporte: {uploaded.name}")
                    st.session_state['repositorio'].append({
                        "nombre": uploaded.name, "carrera": u_carrera, "area": u_area,
                        "autor": st.session_state['usuario']['nombre'],
                        "rol_autor": st.session_state['usuario']['rol'],
                        "fecha": datetime.now().strftime("%Y-%m-%d"), "desc": desc
                    })
                    st.success("¡Subido! (+10 pts)")
                    time.sleep(1.5)
                    st.rerun()

    # --- PERFIL ---
    elif menu == "👤 Mi Perfil & Wallet":
        st.title("👤 Mi Perfil")
        c1, c2 = st.columns([1, 2])
        with c1: st.image(st.session_state['usuario']['foto'], width=150)
        with c2:
            st.markdown(f"## {st.session_state['usuario']['nombre']}")
            st.info(f"🎓 **{st.session_state['usuario']['rol']}** - {st.session_state['usuario']['nivel']}")
            st.write(f"🏛️ {st.session_state['usuario']['universidad']}")
            st.write(f"🏗️ {st.session_state['usuario']['carrera']}")

        st.markdown("### 💰 Historial de Billetera")
        if st.session_state['transacciones']:
            df_trans = pd.DataFrame(st.session_state['transacciones']).iloc[::-1]
            st.dataframe(df_trans, use_container_width=True, hide_index=True)
        else:
            st.write("No hay movimientos.")

# =======================================================
# EJECUCIÓN
# =======================================================
if not st.session_state['logged_in']:
    login_page()
elif not st.session_state['setup_completo']:
    onboarding_page()
else:
    main_app()
