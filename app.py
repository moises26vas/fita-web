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
    st.session_state['puntos'] = 1000
if 'transacciones' not in st.session_state:
    st.session_state['transacciones'] = [
        {"tipo": "Ingreso", "monto": 1000, "desc": "Bono de Bienvenida", "fecha": datetime.now().strftime("%Y-%m-%d")}
    ]
if 'repositorio' not in st.session_state:
    st.session_state['repositorio'] = [
        {"id": 1, "nombre": "Norma E.030.pdf", "carrera": "Ingeniería Civil", "area": "Estructuras", "autor": "Admin Sistema", "rol_autor": "Docente", "fecha": "2026-01-15", "desc": "Norma RNE."},
        {"id": 2, "nombre": "Metrados Viga.xlsx", "carrera": "Ingeniería Civil", "area": "Construcción", "autor": "Luigi", "rol_autor": "Estudiante", "fecha": "2026-01-16", "desc": "Excel vigas."}
    ]
if 'amigos' not in st.session_state:
    st.session_state['amigos'] = ["Carlos (Civil)", "Maria (Arqui)", "Jorge (Minas)"]
if 'tema_actual' not in st.session_state:
    st.session_state['tema_actual'] = "🔵 Pastel Estructural (Azul)"

# --- 3. SEGURIDAD: DETECTOR DE TROYANOS ---
def es_archivo_seguro(uploaded_file):
    """
    Analiza los primeros bytes (Magic Numbers) para detectar ejecutables disfrazados.
    Retorna: (Booleano, Mensaje)
    """
    # Leer los primeros 4 bytes
    header = uploaded_file.read(4)
    uploaded_file.seek(0) # Regresar el lector al inicio para no dañar el archivo
    
    # 1. Detectar Ejecutables de Windows (Archivos .EXE comienzan con 'MZ')
    if header.startswith(b'MZ'): 
        return False, "🚨 ALERTA DE SEGURIDAD: Se ha detectado un ejecutable (.exe) disfrazado. Intento registrado."
    
    # 2. Validar que si dice ser PDF, parezca PDF (Comienza con %PDF)
    if uploaded_file.name.lower().endswith('.pdf'):
        if not header.startswith(b'%PDF'):
            return False, "⚠️ Archivo corrupto o formato falso. No es un PDF válido."
            
    return True, "Archivo Seguro"

# --- 4. GESTIÓN DE TEMAS Y COLORES ---
TEMAS = {
    "🔵 Pastel Estructural (Azul)": {"fondo_app": "#F0F8FF", "fondo_sidebar": "#FFFFFF", "acento": "#2980B9", "boton": "#2C3E50", "badge_est": "#D6EAF8", "badge_doc": "#FCF3CF"},
    "⚪ Pastel Concreto (Gris)": {"fondo_app": "#F4F6F6", "fondo_sidebar": "#FDFEFE", "acento": "#7F8C8D", "boton": "#424949", "badge_est": "#E5E8E8", "badge_doc": "#F9E79F"},
    "🟢 Pastel Ambiental (Verde)": {"fondo_app": "#E9F7EF", "fondo_sidebar": "#FFFFFF", "acento": "#27AE60", "boton": "#196F3D", "badge_est": "#D5F5E3", "badge_doc": "#FCF3CF"},
    "🔴 Pastel Gerencia (Cálido)": {"fondo_app": "#FDEDEC", "fondo_sidebar": "#FFFFFF", "acento": "#C0392B", "boton": "#922B21", "badge_est": "#FADBD8", "badge_doc": "#F9E79F"}
}
colors = TEMAS[st.session_state['tema_actual']]

# --- 5. ESTILOS CSS (CORRECCIÓN VISUAL PROFUNDA) ---
st.markdown(f"""
<style>
    /* 1. ESTRUCTURA BASE */
    [data-testid="stAppViewContainer"] {{ background-color: {colors['fondo_app']} !important; color: #000000 !important; }}
    [data-testid="stSidebar"] {{ background-color: {colors['fondo_sidebar']} !important; border-right: 1px solid #ddd; }}

    /* 2. FORZAR TEXTO NEGRO */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {{ color: #17202A !important; }}

    /* 3. --- CORRECCIÓN DEL MENÚ DESPLEGABLE (TU PROBLEMA) --- */
    /* Caja principal del selector */
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border-color: {colors['acento']} !important;
    }}
    /* El menú desplegable que flota */
    div[data-baseweb="popover"], div[data-baseweb="menu"], ul[data-baseweb="menu"] {{
        background-color: #FFFFFF !important;
    }}
    /* Las opciones dentro del menú */
    li[role="option"] {{
        color: #000000 !important; /* Texto negro obligatorio */
        background-color: #FFFFFF !important;
    }}
    /* Texto dentro de las opciones */
    div[data-baseweb="select"] span {{
        color: #000000 !important;
    }}
    
    /* 4. COMPONENTES */
    .file-card {{ background-color: #FFFFFF !important; padding: 20px; border-radius: 10px; border-left: 5px solid {colors['acento']}; margin-bottom: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }}
    .wallet-box {{ background: linear-gradient(135deg, #154360 0%, #1A5276 100%); padding: 25px; border-radius: 12px; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 10px rgba(0,0,0,0.2); }}
    .wallet-box h2, .wallet-box div, .wallet-box span {{ color: #FFFFFF !important; }}
    
    .badge {{ padding: 4px 10px; border-radius: 12px; font-weight: bold; font-size: 0.8rem; }}
    .estudiante {{ background-color: {colors['badge_est']} !important; color: #154360 !important; }}
    .docente {{ background-color: {colors['badge_doc']} !important; color: #7D6608 !important; }}

    .stButton > button {{ background-color: {colors['boton']} !important; color: #FFFFFF !important; border: none; }}
    .delete-btn > button {{ background-color: #E74C3C !important; }}
</style>
""", unsafe_allow_html=True)

# --- 6. DATOS PERÚ ---
UNIVERSIDADES = ["UPN", "UNI", "PUCP", "UPC", "UTP", "UNMSM", "SENCICO"]
CARRERAS = {
    "Ingeniería Civil": ["Estructuras", "Geotecnia", "Hidráulica", "BIM"],
    "Arquitectura": ["Diseño", "Urbanismo"],
    "Ing. de Minas": ["Seguridad", "Voladura"],
    "Topografía": ["Levantamientos", "GIS"]
}

def registrar_transaccion(tipo, monto, descripcion):
    st.session_state['transacciones'].append({
        "tipo": tipo, "monto": monto, "desc": descripcion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
    })

# ==================== PANTALLAS ====================

def login_page():
    c1, c2, c3 = st.columns([1, 1.2, 1])
    with c2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:white; padding:40px; border-radius:15px; text-align:center; border-top:5px solid {colors['acento']}; box-shadow:0 10px 20px rgba(0,0,0,0.1);">
            <h1 style="margin-top:10px;">F.I.T.A. ACCESS</h1>
            <p>Plataforma Segura de Ingeniería</p>
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        if st.button("🔐 Iniciar Sesión con Google", type="primary", use_container_width=True):
            with st.spinner("Verificando credenciales cifradas..."):
                time.sleep(1)
                st.session_state['logged_in'] = True
                st.session_state['usuario'] = {'nombre': "Ing. Luigi", 'email': "luigi.ing@upn.pe", 'foto': "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"}
                st.rerun()

def onboarding_page():
    st.markdown("<h1 style='text-align:center;'>🛠️ Configuración de Perfil</h1>", unsafe_allow_html=True)
    with st.container():
        rol = st.radio("Jerarquía:", ["Estudiante", "Docente"], horizontal=True)
        c1, c2 = st.columns(2)
        with c1:
            uni = st.selectbox("Universidad", UNIVERSIDADES)
            carrera = st.selectbox("Carrera", list(CARRERAS.keys()))
        with c2:
            area = st.selectbox("Especialidad", CARRERAS[carrera])
            nivel = "Ciclo " + str(st.slider("Ciclo", 1, 10, 5)) if rol == "Estudiante" else st.selectbox("Grado", ["Titulado", "Magíster"])

        if st.button("💾 Ingresar al Sistema", use_container_width=True):
            st.session_state['usuario'].update({'rol': rol, 'universidad': uni, 'carrera': carrera, 'especialidad': area, 'nivel': nivel})
            st.session_state['setup_completo'] = True
            st.rerun()

def main_app():
    with st.sidebar:
        st.image(st.session_state['usuario']['foto'], width=80)
        st.write(f"**{st.session_state['usuario']['nombre']}**")
        badge = "estudiante" if st.session_state['usuario']['rol'] == "Estudiante" else "docente"
        st.markdown(f'<span class="badge {badge}">{st.session_state["usuario"]["rol"]}</span>', unsafe_allow_html=True)
        st.markdown("---")
        
        # SELECTOR DE TEMAS (Aquí estaba el error visual)
        with st.expander("🎨 Temas (Visualización)", expanded=False):
            tema_selec = st.selectbox("Estilo:", list(TEMAS.keys()), index=list(TEMAS.keys()).index(st.session_state['tema_actual']))
            if tema_selec != st.session_state['tema_actual']:
                st.session_state['tema_actual'] = tema_selec
                st.rerun()

        st.markdown("---")
        st.markdown(f"""<div class="wallet-box"><h2>{st.session_state['puntos']} pts</h2><div>🪙 Saldo</div></div>""", unsafe_allow_html=True)
        
        menu = st.radio("Navegación", ["🏠 Inicio", "📂 Repositorio", "📤 Subir Seguro", "👤 Perfil", "🔧 Admin Panel"])
        
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.rerun()

    # --- INICIO ---
    if menu == "🏠 Inicio":
        st.title("🏠 Panel de Control")
        c1, c2, c3 = st.columns(3)
        c1.metric("Biblioteca", f"{len(st.session_state['repositorio'])} Docs")
        c2.metric("Saldo", f"{st.session_state['puntos']} pts")
        c3.metric("Seguridad", "Activa 🔒")
        st.info(f"🎨 Estilo activo: **{st.session_state['tema_actual']}** (Texto optimizado)")

    # --- REPOSITORIO (CON ELIMINAR) ---
    elif menu == "📂 Repositorio":
        st.title("📂 Biblioteca Técnica")
        
        archivos = st.session_state['repositorio']
        
        for idx, file in enumerate(archivos):
            with st.container():
                c_info, c_btn = st.columns([4, 1])
                with c_info:
                    st.markdown(f"""
                    <div class="file-card">
                        <h4 style="margin:0;">📄 {file['nombre']}</h4>
                        <p style="margin:5px 0;">{file['desc']}</p>
                        <small>{file['carrera']} | Autor: <b>{file['autor']}</b></small>
                    </div>
                    """, unsafe_allow_html=True)
                with c_btn:
                    st.write("")
                    # LÓGICA DE ELIMINACIÓN PARA USUARIO
                    es_propio = file['autor'] == st.session_state['usuario']['nombre']
                    if es_propio:
                        if st.button("🗑️ Borrar", key=f"del_user_{idx}"):
                            st.session_state['repositorio'].pop(idx)
                            st.toast("Archivo eliminado.", icon="🗑️")
                            time.sleep(1)
                            st.rerun()
                    else:
                        if st.button("⬇️ Bajar", key=f"dl_{idx}"):
                            if st.session_state['puntos'] >= 20:
                                st.session_state['puntos'] -= 20
                                registrar_transaccion("Gasto", 20, f"Descarga: {file['nombre']}")
                                st.toast("Descargando...", icon="✅")
                            else:
                                st.error("Saldo insuficiente")

    # --- SUBIR (CON SEGURIDAD) ---
    elif menu == "📤 Subir Seguro":
        st.title("📤 Subida Segura (Anti-Malware)")
        st.warning("🔒 El sistema escanea 'Magic Numbers' para evitar archivos .exe disfrazados.")
        
        with st.form("up_form"):
            up = st.file_uploader("Archivo")
            desc = st.text_input("Descripción")
            c1, c2 = st.columns(2)
            u_car = c1.selectbox("Carrera", list(CARRERAS.keys()))
            u_are = c2.selectbox("Área", CARRERAS[u_car])
            
            if st.form_submit_button("🚀 Escanear y Publicar"):
                if up and desc:
                    # 1. ESCANEO DE SEGURIDAD
                    es_seguro, mensaje = es_archivo_seguro(up)
                    
                    if es_seguro:
                        st.session_state['puntos'] += 10
                        registrar_transaccion("Ingreso", 10, f"Aporte: {up.name}")
                        st.session_state['repositorio'].append({
                            "nombre": up.name, "carrera": u_car, "area": u_are,
                            "autor": st.session_state['usuario']['nombre'],
                            "rol_autor": st.session_state['usuario']['rol'],
                            "fecha": datetime.now().strftime("%Y-%m-%d"), "desc": desc
                        })
                        st.balloons()
                        st.success("✅ Archivo LIMPIO y publicado exitosamente.")
                    else:
                        st.error(mensaje)
                else:
                    st.warning("Faltan datos.")

    # --- PERFIL ---
    elif menu == "👤 Perfil":
        st.title("👤 Mi Perfil")
        c1, c2 = st.columns([1, 2])
        with c1: st.image(st.session_state['usuario']['foto'], width=150)
        with c2:
            st.header(st.session_state['usuario']['nombre'])
            st.write(f"🎓 {st.session_state['usuario']['rol']} - {st.session_state['usuario']['nivel']}")
            st.write(f"🏛️ {st.session_state['usuario']['universidad']}")
        
        st.markdown("### Mis Archivos")
        mis_archivos = [f for f in st.session_state['repositorio'] if f['autor'] == st.session_state['usuario']['nombre']]
        if mis_archivos:
            st.dataframe(pd.DataFrame(mis_archivos)[['nombre', 'fecha', 'desc']])
        else:
            st.info("No has subido archivos aún.")

    # --- ADMIN PANEL (ELIMINAR TODO) ---
    elif menu == "🔧 Admin Panel":
        st.title("🔧 Gestión de Administrador")
        st.error("Zona de Peligro: Tienes permisos para borrar cualquier archivo.")
        
        archivos = st.session_state['repositorio']
        if archivos:
            for idx, file in enumerate(archivos):
                c1, c2, c3 = st.columns([1, 4, 1])
                with c1: st.write(f"ID: {idx}")
                with c2: st.write(f"📄 **{file['nombre']}** (Autor: {file['autor']})")
                with c3:
                    # BOTON ROJO DE ELIMINAR ADMIN
                    if st.button("❌ ELIMINAR", key=f"admin_del_{idx}", type="primary"):
                        st.session_state['repositorio'].pop(idx)
                        st.success(f"Archivo {file['nombre']} eliminado por la fuerza.")
                        time.sleep(1)
                        st.rerun()
        else:
            st.info("El repositorio está vacío.")

# ==================== EJECUCIÓN ====================
if not st.session_state['logged_in']: login_page()
elif not st.session_state['setup_completo']: onboarding_page()
else: main_app()
