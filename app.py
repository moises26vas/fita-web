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

# --- 2. GESTIÓN DE MEMORIA Y ESTADO ---
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
# Lista simulada de amigos para transferirles puntos
if 'amigos' not in st.session_state:
    st.session_state['amigos'] = ["Carlos (Civil)", "Maria (Arqui)", "Jorge (Minas)", "Ana (Topografía)"]

# --- 3. LISTAS DE DATOS PERÚ ---
UNIVERSIDADES = ["UPN", "UNI", "PUCP", "UPC", "UTP", "UNMSM", "UCV", "URP", "SENCICO", "Otra"]
CARRERAS = {
    "Ingeniería Civil": ["Estructuras", "Geotecnia", "Hidráulica", "Vías y Transportes", "Gestión de Proyectos (BIM)"],
    "Arquitectura": ["Diseño Arquitectónico", "Urbanismo", "Interiores", "Paisajismo"],
    "Ing. de Minas": ["Seguridad Minera", "Operaciones", "Planeamiento", "Geología"],
    "Topografía": ["Levantamientos", "Fotogrametría", "Sistemas GIS"]
}

# --- 4. ESTILOS CSS (SOLUCIÓN DEFINITIVA DE VISIBILIDAD) ---
st.markdown("""
<style>
    /* 1. FORZAR TEMA CLARO EN TODO EL APP (Fondo y Texto) */
    [data-testid="stAppViewContainer"] {
        background-color: #F0F2F5 !important; /* Gris muy claro profesional */
        color: #000000 !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF !important;
        border-right: 1px solid #ddd;
    }

    /* 2. FORZAR TEXTO NEGRO UNIVERSALMENTE */
    /* Esto arregla el problema de "letras oscuras invisibles" */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {
        color: #1C2833 !important; /* Negro azulado elegante */
    }

    /* 3. ARREGLO DE MENÚS DESPLEGABLES (Selectbox) */
    div[data-baseweb="select"] > div, div[data-baseweb="popover"] {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #ccc;
    }
    div[role="option"] {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    div[role="option"]:hover {
        background-color: #D4E6F1 !important; /* Azul claro al pasar mouse */
    }

    /* 4. TARJETAS PERSONALIZADAS */
    .login-card {
        background-color: #FFFFFF !important; padding: 40px; border-radius: 15px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1); text-align: center; border-top: 5px solid #C0392B;
    }
    .file-card {
        background-color: #FFFFFF !important; padding: 20px; border-radius: 10px;
        border-left: 5px solid #2980B9; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    /* BILLETERA (TEXTO BLANCO SOLO AQUÍ) */
    .wallet-box {
        background: linear-gradient(135deg, #154360 0%, #1A5276 100%);
        padding: 25px; border-radius: 12px; text-align: center;
        margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    .wallet-box h2, .wallet-box div, .wallet-box span {
        color: #FFFFFF !important; /* Excepción: Blanco en billetera */
    }

    /* BADGES */
    .badge { padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }
    .estudiante { background-color: #D6EAF8 !important; color: #154360 !important; }
    .docente { background-color: #FCF3CF !important; color: #7D6608 !important; }

    /* BOTONES */
    .stButton > button {
        background-color: #2C3E50 !important;
        color: #FFFFFF !important;
        border: none;
    }
</style>
""", unsafe_allow_html=True)

# =======================================================
# FUNCIONES AUXILIARES
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
        if st.button("🔐 Iniciar Sesión con Google", type="primary", use_container_width=True):
            with st.spinner("Conectando..."):
                time.sleep(1)
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
    st.markdown("<h1 style='text-align:center;'>🛠️ Perfil Académico</h1>", unsafe_allow_html=True)
    st.write("---")

    with st.container():
        rol = st.radio("Jerarquía:", ["Estudiante", "Docente / Profesional"], horizontal=True)
        c1, c2 = st.columns(2)
        with c1:
            uni = st.selectbox("Universidad", UNIVERSIDADES)
            carrera = st.selectbox("Carrera", list(CARRERAS.keys()))
        with c2:
            area = st.selectbox("Especialidad", CARRERAS[carrera])
            if "Estudiante" in rol:
                nivel_txt = f"Ciclo {st.slider('Ciclo', 1, 10, 5)}"
                rol_corto = "Estudiante"
            else:
                nivel_txt = st.selectbox("Grado", ["Bachiller", "Titulado", "Magíster", "Doctor"])
                rol_corto = "Docente"

        if st.button("💾 Guardar y Entrar", use_container_width=True):
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
        
        badge_class = "estudiante" if st.session_state['usuario']['rol'] == "Estudiante" else "docente"
        st.markdown(f'<span class="badge {badge_class}">{st.session_state["usuario"]["rol"]}</span>', unsafe_allow_html=True)
            
        st.caption(st.session_state['usuario']['universidad'])
        st.markdown("---")
        
        st.markdown(f"""
        <div class="wallet-box">
            <div style="font-size:0.8rem; opacity:0.8;">SALDO DISPONIBLE</div>
            <h2 style="margin:5px 0;">{st.session_state['puntos']} pts</h2>
            <div style="font-size:0.7rem;">🪙 FitaCoins</div>
        </div>
        """, unsafe_allow_html=True)
        
        menu = st.radio("Navegación", ["🏠 Inicio", "📂 Repositorio", "📤 Subir (+10)", "👤 Billetera & Transferencias", "🔧 Admin Panel"])
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['setup_completo'] = False
            st.rerun()

    # --- INICIO ---
    if menu == "🏠 Inicio":
        st.title("🏠 Panel de Control")
        col1, col2, col3 = st.columns(3)
        col1.metric("Biblioteca", f"{len(st.session_state['repositorio'])} Docs")
        col2.metric("Saldo", f"{st.session_state['puntos']} pts")
        col3.metric("Estado", "Activo")
        st.info("👋 Hola Luigi. Tienes acceso total al sistema.")

    # --- REPOSITORIO ---
    elif menu == "📂 Repositorio":
        st.title("📂 Biblioteca Técnica")
        st.write("Descarga: **-20 pts**")
        
        # Filtros
        c1, c2 = st.columns(2)
        f_carrera = c1.selectbox("Filtrar Carrera", ["Todas"] + list(CARRERAS.keys()))
        opciones_area = ["Todas"] + CARRERAS[f_carrera] if f_carrera != "Todas" else ["Todas"]
        f_area = c2.selectbox("Filtrar Área", opciones_area)

        archivos = st.session_state['repositorio']
        if f_carrera != "Todas": archivos = [a for a in archivos if a['carrera'] == f_carrera]
        if f_area != "Todas": archivos = [a for a in archivos if a['area'] == f_area]

        for idx, file in enumerate(archivos):
            with st.container():
                c_info, c_btn = st.columns([4, 1])
                with c_info:
                    st.markdown(f"""
                    <div class="file-card">
                        <h4 style="margin:0;">📄 {file['nombre']}</h4>
                        <p style="margin:5px 0;">{file['desc']}</p>
                        <small>{file['carrera']} | Autor: {file['autor']}</small>
                    </div>
                    """, unsafe_allow_html=True)
                with c_btn:
                    st.write("")
                    if st.button(f"⬇️ Bajar", key=f"dl_{idx}"):
                        if st.session_state['puntos'] >= 20:
                            st.session_state['puntos'] -= 20
                            registrar_transaccion("Gasto", 20, f"Descarga: {file['nombre']}")
                            st.toast("✅ Descarga OK (-20 pts)", icon="📉")
                        else:
                            st.error("Saldo insuficiente")

    # --- SUBIR ---
    elif menu == "📤 Subir (+10)":
        st.title("📤 Subir Archivo")
        st.write("Gana **10 Puntos** por compartir.")
        with st.form("up_form"):
            up = st.file_uploader("Archivo")
            desc = st.text_input("Descripción")
            c1, c2 = st.columns(2)
            u_car = c1.selectbox("Carrera", list(CARRERAS.keys()))
            u_are = c2.selectbox("Área", CARRERAS[u_car])
            
            if st.form_submit_button("🚀 Publicar"):
                if up and desc:
                    st.session_state['puntos'] += 10
                    registrar_transaccion("Ingreso", 10, f"Aporte: {up.name}")
                    st.session_state['repositorio'].append({
                        "nombre": up.name, "carrera": u_car, "area": u_are,
                        "autor": st.session_state['usuario']['nombre'],
                        "rol_autor": st.session_state['usuario']['rol'],
                        "fecha": datetime.now().strftime("%Y-%m-%d"), "desc": desc
                    })
                    st.success("¡Subido! (+10 pts)")
                    time.sleep(1)
                    st.rerun()

    # --- BILLETERA & TRANSFERENCIAS ---
    elif menu == "👤 Billetera & Transferencias":
        st.title("💰 Gestión Financiera F.I.T.A.")
        
        col_wallet, col_transfer = st.columns(2)
        
        with col_wallet:
            st.subheader("💳 Mi Saldo")
            st.info(f"Tienes **{st.session_state['puntos']} FitaCoins** disponibles para usar.")
            
            st.write("### 📜 Historial")
            df = pd.DataFrame(st.session_state['transacciones']).iloc[::-1]
            st.dataframe(df, use_container_width=True, hide_index=True)

        with col_transfer:
            st.subheader("💸 Transferir a Amigos")
            st.markdown("""
            <div style="background:white; padding:20px; border-radius:10px; border:1px solid #ddd;">
                <h4 style="margin:0;">Enviar Puntos</h4>
                <p>Ayuda a un colega a descargar planos.</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            
            # FORMULARIO DE TRANSFERENCIA
            destinatario = st.selectbox("Seleccionar Destinatario", st.session_state['amigos'])
            monto_envio = st.number_input("Monto a enviar", min_value=1, max_value=st.session_state['puntos'], step=10)
            
            if st.button("➡️ Realizar Transferencia", type="primary"):
                if st.session_state['puntos'] >= monto_envio:
                    st.session_state['puntos'] -= monto_envio
                    registrar_transaccion("Egreso", monto_envio, f"Transferencia a {destinatario}")
                    st.balloons()
                    st.success(f"¡Has enviado {monto_envio} pts a {destinatario}!")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("No tienes saldo suficiente.")

    # --- PANEL ADMIN (NUEVO) ---
    elif menu == "🔧 Admin Panel":
        st.title("🔧 Panel de Control (Admin)")
        st.warning("Zona restringida para administradores del sistema.")
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("### 🖨️ Emisión Monetaria")
            st.write("Generar puntos para el sistema (Testing).")
            monto_mint = st.number_input("Cantidad a generar", 100, 10000, 1000)
            if st.button("Generar Puntos"):
                st.session_state['puntos'] += monto_mint
                registrar_transaccion("ADMIN", monto_mint, "Generación manual de puntos")
                st.success(f"Se generaron {monto_mint} puntos.")
                time.sleep(1)
                st.rerun()
        
        with c2:
            st.markdown("### 👥 Gestión de Usuarios")
            st.write("Agregar nuevo amigo a la lista de contactos.")
            nuevo_amigo = st.text_input("Nombre del nuevo usuario")
            if st.button("Agregar Usuario"):
                if nuevo_amigo:
                    st.session_state['amigos'].append(nuevo_amigo)
                    st.success(f"{nuevo_amigo} añadido a la red.")

# =======================================================
# EJECUCIÓN
# =======================================================
if not st.session_state['logged_in']:
    login_page()
elif not st.session_state['setup_completo']:
    onboarding_page()
else:
    main_app()
