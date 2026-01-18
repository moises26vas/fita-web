import streamlit as st
import pandas as pd
import time
from datetime import datetime

# ==============================================================================
# 1. CONFIGURACIÓN GENERAL DE LA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="F.I.T.A. Construction Hub | Plataforma Profesional",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==============================================================================
# 2. SISTEMA DE GESTIÓN DE ESTADO (DATABASE EN MEMORIA)
# ==============================================================================
# Inicializamos todas las variables de sesión necesarias para que el sistema
# tenga "memoria" mientras el usuario navega.

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'setup_completo' not in st.session_state:
    st.session_state['setup_completo'] = False

if 'usuario' not in st.session_state:
    st.session_state['usuario'] = {}

# Billetera: Saldo inicial de 1000 puntos
if 'puntos' not in st.session_state:
    st.session_state['puntos'] = 1000

# Historial de Transacciones (Log Financiero)
if 'transacciones' not in st.session_state:
    st.session_state['transacciones'] = [
        {
            "tipo": "Ingreso",
            "monto": 1000,
            "desc": "Bono de Bienvenida por Registro",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
    ]

# Repositorio de Archivos (Base de datos de documentos)
if 'repositorio' not in st.session_state:
    st.session_state['repositorio'] = [
        {
            "id": 101,
            "nombre": "Norma E.030 Diseño Sismorresistente.pdf",
            "carrera": "Ingeniería Civil",
            "area": "Estructuras",
            "autor": "Admin Sistema",
            "rol_autor": "Docente",
            "fecha": "2026-01-15",
            "desc": "Norma actualizada del Reglamento Nacional de Edificaciones."
        },
        {
            "id": 102,
            "nombre": "Plantilla Automatizada Metrados.xlsx",
            "carrera": "Ingeniería Civil",
            "area": "Construcción",
            "autor": "Luigi",
            "rol_autor": "Estudiante",
            "fecha": "2026-01-16",
            "desc": "Hoja de cálculo para vigas y columnas con macros."
        },
        {
            "id": 103,
            "nombre": "Plano Topográfico Lote 4B.dwg",
            "carrera": "Topografía",
            "area": "Levantamientos",
            "autor": "Carlos Topo",
            "rol_autor": "Profesional",
            "fecha": "2026-01-17",
            "desc": "Levantamiento con estación total, curvas de nivel."
        }
    ]

# Lista de Amigos/Contactos para transferencias
if 'amigos' not in st.session_state:
    st.session_state['amigos'] = [
        "Carlos (Ing. Civil)", 
        "Maria (Arquitectura)", 
        "Jorge (Ing. Minas)", 
        "Ana (Topografía)",
        "Pedro (Docente)"
    ]

# Configuración del Tema Visual
if 'tema_actual' not in st.session_state:
    st.session_state['tema_actual'] = "🔵 Pastel Estructural (Azul)"


# ==============================================================================
# 3. BASES DE DATOS DE CONTEXTO PERUANO
# ==============================================================================
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
    "SENCICO (Escuela Superior Técnica)",
    "Otra Institución"
]

CARRERAS = {
    "Ingeniería Civil": [
        "Estructuras y Diseño", 
        "Geotecnia y Suelos", 
        "Hidráulica e Hidrología", 
        "Vías y Transportes", 
        "Gestión de la Construcción (BIM)",
        "Tecnología del Concreto"
    ],
    "Arquitectura": [
        "Diseño Arquitectónico", 
        "Urbanismo y Territorio", 
        "Diseño de Interiores", 
        "Paisajismo",
        "Restauración de Monumentos"
    ],
    "Ingeniería de Minas": [
        "Seguridad Minera", 
        "Operaciones y Voladura", 
        "Planeamiento de Minas", 
        "Geología Económica"
    ],
    "Topografía y Geodesia": [
        "Levantamientos Topográficos", 
        "Fotogrametría y Drones", 
        "Sistemas GIS y Catastro",
        "Geodesia Satelital"
    ]
}

# Diccionario de Estilos Visuales (Temas)
TEMAS = {
    "🔵 Pastel Estructural (Azul)": {
        "fondo_app": "#F0F8FF",
        "fondo_sidebar": "#FFFFFF",
        "acento": "#2980B9",
        "boton": "#2C3E50",
        "badge_est": "#D6EAF8",
        "badge_doc": "#FCF3CF"
    },
    "⚪ Pastel Concreto (Gris)": {
        "fondo_app": "#F4F6F6",
        "fondo_sidebar": "#FDFEFE",
        "acento": "#7F8C8D",
        "boton": "#424949",
        "badge_est": "#E5E8E8",
        "badge_doc": "#F9E79F"
    },
    "🟢 Pastel Ambiental (Verde)": {
        "fondo_app": "#E9F7EF",
        "fondo_sidebar": "#FFFFFF",
        "acento": "#27AE60",
        "boton": "#196F3D",
        "badge_est": "#D5F5E3",
        "badge_doc": "#FCF3CF"
    },
    "🔴 Pastel Gerencia (Cálido)": {
        "fondo_app": "#FDEDEC",
        "fondo_sidebar": "#FFFFFF",
        "acento": "#C0392B",
        "boton": "#922B21",
        "badge_est": "#FADBD8",
        "badge_doc": "#F9E79F"
    }
}

# Cargar colores actuales
colors = TEMAS[st.session_state['tema_actual']]


# ==============================================================================
# 4. ESTILOS CSS PROFESIONALES (CORRECCIÓN VISUAL COMPLETA)
# ==============================================================================
# Este bloque CSS garantiza que los menús se vean blancos con letras negras
# independientemente del modo oscuro/claro del usuario.

st.markdown(f"""
<style>
    /* 1. ESTRUCTURA PRINCIPAL */
    [data-testid="stAppViewContainer"] {{
        background-color: {colors['fondo_app']} !important;
        color: #000000 !important;
    }}
    
    [data-testid="stSidebar"] {{
        background-color: {colors['fondo_sidebar']} !important;
        border-right: 1px solid #BDC3C7;
    }}

    /* 2. FORZADO DE TIPOGRAFÍA OSCURA (Anti-Modo Oscuro) */
    h1, h2, h3, h4, h5, h6, p, div, span, label, li, td, th {{
        color: #17202A !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}

    /* 3. CORRECCIÓN CRÍTICA DE MENÚS DESPLEGABLES (Selectbox) */
    /* Caja del input */
    div[data-baseweb="select"] > div {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid {colors['acento']} !important;
    }}
    
    /* El contenedor flotante de opciones */
    div[data-baseweb="popover"], ul[data-baseweb="menu"] {{
        background-color: #FFFFFF !important;
        border: 1px solid #ccc;
    }}
    
    /* Cada opción individual */
    li[role="option"] {{
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }}
    
    /* Hover sobre opción */
    li[role="option"]:hover {{
        background-color: {colors['badge_est']} !important;
        font-weight: bold;
    }}
    
    /* Texto seleccionado dentro de la caja */
    div[data-testid="stMarkdownContainer"] p {{
        color: #000000 !important;
    }}

    /* 4. COMPONENTES DE INTERFAZ PERSONALIZADOS */
    
    /* Tarjeta de Login */
    .login-card {{
        background-color: #FFFFFF !important;
        padding: 50px;
        border-radius: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        text-align: center;
        border-top: 8px solid {colors['acento']};
    }}
    
    /* Tarjeta de Archivo */
    .file-card {{
        background-color: #FFFFFF !important;
        padding: 25px;
        border-radius: 12px;
        border-left: 6px solid {colors['acento']};
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }}
    .file-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.1);
    }}
    
    /* Billetera Digital (Excepción de Texto Blanco) */
    .wallet-box {{
        background: linear-gradient(135deg, #154360 0%, #1A5276 100%);
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    /* Forzamos blanco SOLO dentro de la billetera */
    .wallet-box h2, .wallet-box div, .wallet-box span {{
        color: #FFFFFF !important;
    }}

    /* Etiquetas de Rol */
    .badge {{
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 0.85rem;
        display: inline-block;
        margin-top: 5px;
    }}
    .estudiante {{
        background-color: {colors['badge_est']} !important;
        color: #154360 !important;
        border: 1px solid #AED6F1;
    }}
    .docente {{
        background-color: {colors['badge_doc']} !important;
        color: #7D6608 !important;
        border: 1px solid #F9E79F;
    }}

    /* Botones Globales */
    .stButton > button {{
        background-color: {colors['boton']} !important;
        color: #FFFFFF !important;
        border-radius: 8px;
        padding: 10px 24px;
        border: none;
        font-weight: 600;
        transition: background-color 0.3s;
    }}
    .stButton > button:hover {{
        opacity: 0.9;
    }}

</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 5. FUNCIONES DE LÓGICA Y SEGURIDAD
# ==============================================================================

def es_archivo_seguro(uploaded_file):
    """
    Sistema de Ciberseguridad F.I.T.A.
    Analiza los 'Magic Numbers' (Cabecera binaria) del archivo para evitar
    que usuarios malintencionados suban .exe o scripts disfrazados de PDF/Excel.
    """
    # Leer los primeros 4 bytes del archivo
    header = uploaded_file.read(4)
    # Regresar el puntero al inicio para no corromper la subida
    uploaded_file.seek(0)
    
    # Check 1: Ejecutables de Windows (MZ Header)
    if header.startswith(b'MZ'): 
        return False, "🚨 ALERTA DE SEGURIDAD CRÍTICA: Se ha detectado un archivo ejecutable (.exe) camuflado. Su IP ha sido registrada."
    
    # Check 2: Scripts de Shell (#! Header)
    if header.startswith(b'#!'):
        return False, "⚠️ ALERTA: Se ha detectado un script potencialmente peligroso. Bloqueado."

    return True, "Archivo Seguro Verificado"


def registrar_transaccion(tipo, monto, descripcion):
    """
    Sistema de Log Financiero.
    Registra cualquier movimiento de puntos en la cadena de bloques simulada.
    """
    nueva_transaccion = {
        "tipo": tipo,
        "monto": monto,
        "desc": descripcion,
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state['transacciones'].append(nueva_transaccion)


# ==============================================================================
# 6. PANTALLAS DE LA APLICACIÓN
# ==============================================================================

def login_page():
    """Pantalla de Inicio de Sesión"""
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # Tarjeta HTML
        st.markdown(f"""
        <div class="login-card">
            <img src="https://cdn-icons-png.flaticon.com/512/9387/9387877.png" width="100" style="margin-bottom:20px;">
            <h1 style="margin:0; font-size:2.5rem; color:{colors['boton']} !important;">F.I.T.A. ACCESS</h1>
            <p style="color:#7F8C8D !important; font-size:1.2rem;">Plataforma Nacional de Ingeniería y Construcción</p>
            <hr style="margin:20px 0;">
            <p style="font-size:0.9rem;">Acceso Seguro v6.0</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("") # Espaciador
        
        # Botón de Login
        if st.button("🔐 Iniciar Sesión con Google Workspace", type="primary", use_container_width=True):
            with st.spinner("Estableciendo conexión segura con servidores F.I.T.A..."):
                time.sleep(1.5) # Simulación de carga
                st.session_state['logged_in'] = True
                
                # Carga de datos de usuario simulados desde Google
                st.session_state['usuario'] = {
                    'nombre': "Ing. Luigi",
                    'email': "luigi.ing@upn.pe",
                    'foto': "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
                }
                st.rerun()


def onboarding_page():
    """Pantalla de Registro de Datos Académicos (Onboarding)"""
    st.markdown("<h1 style='text-align:center;'>🛠️ Configuración de Perfil Profesional</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>Personaliza tu experiencia seleccionando tu especialidad.</p>", unsafe_allow_html=True)
    st.write("---")

    with st.container():
        # Selección de Rol con CSS corregido
        rol = st.radio("Selecciona tu Jerarquía Académica:", 
                       ["Estudiante Universitario/Técnico", "Docente / Profesional Colegiado"], 
                       horizontal=True)
        
        st.write("") # Espacio
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Datos Institucionales")
            uni = st.selectbox("Institución Educativa", UNIVERSIDADES, index=0)
            carrera = st.selectbox("Carrera Profesional", list(CARRERAS.keys()), index=0)
        
        with col2:
            st.subheader("Datos de Especialidad")
            area = st.selectbox("Área de Enfoque Principal", CARRERAS[carrera])
            
            # Lógica dinámica para Nivel
            if "Estudiante" in rol:
                nivel_val = st.slider("Ciclo Académico Actual", 1, 10, 5)
                nivel_txt = f"Ciclo {nivel_val}"
                rol_corto = "Estudiante"
            else:
                nivel_txt = st.selectbox("Grado Académico Alcanzado", ["Bachiller", "Ingeniero Titulado", "Magíster", "Doctor (PhD)"])
                rol_corto = "Docente"

        st.markdown("---")
        st.info("ℹ️ **Bono de Inicio:** Al completar este registro, tu Billetera Digital será creada automáticamente con **1000 FitaCoins**.")
        
        if st.button("💾 Guardar Perfil e Ingresar al Sistema", type="primary", use_container_width=True):
            # Guardamos todo en la sesión
            st.session_state['usuario'].update({
                'rol': rol_corto,
                'universidad': uni,
                'carrera': carrera,
                'especialidad': area,
                'nivel': nivel_txt
            })
            st.session_state['setup_completo'] = True
            st.balloons() # Animación de celebración
            time.sleep(1)
            st.rerun()


def main_app():
    """Aplicación Principal (Dashboard)"""
    
    # --------------------------------------------------------------------------
    # BARRA LATERAL (SIDEBAR)
    # --------------------------------------------------------------------------
    with st.sidebar:
        # 1. Perfil Mini
        st.image(st.session_state['usuario']['foto'], width=90)
        st.markdown(f"### {st.session_state['usuario']['nombre']}")
        
        # Badge de Rol
        badge_class = "estudiante" if st.session_state['usuario']['rol'] == "Estudiante" else "docente"
        st.markdown(f'<span class="badge {badge_class}">{st.session_state["usuario"]["rol"]}</span>', unsafe_allow_html=True)
            
        st.caption(st.session_state['usuario']['universidad'])
        st.markdown("---")
        
        # 2. Selector de Temas (Visual)
        with st.expander("🎨 Personalizar Interfaz", expanded=False):
            st.write("Selecciona un estilo visual:")
            tema_selec = st.selectbox("Tema:", list(TEMAS.keys()), index=list(TEMAS.keys()).index(st.session_state['tema_actual']))
            
            if tema_selec != st.session_state['tema_actual']:
                st.session_state['tema_actual'] = tema_selec
                st.rerun()

        st.markdown("---")
        
        # 3. Billetera Resumida
        st.markdown(f"""
        <div class="wallet-box">
            <div style="font-size:0.8rem; opacity:0.8; text-transform:uppercase;">Saldo Disponible</div>
            <h2 style="margin:5px 0; font-size:2.2rem;">{st.session_state['puntos']}</h2>
            <div style="font-size:0.8rem;">🪙 FitaCoins</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Menú de Navegación Principal
        menu_options = [
            "🏠 Panel de Control", 
            "📂 Repositorio Global", 
            "📤 Subir Material (+10)", 
            "💰 Billetera & Transferencias", 
            "🔧 Panel Admin (Privado)"
        ]
        menu = st.radio("Navegación del Sistema", menu_options)
        
        st.markdown("---")
        if st.button("Cerrar Sesión"):
            st.session_state['logged_in'] = False
            st.session_state['setup_completo'] = False
            st.rerun()


    # --------------------------------------------------------------------------
    # MÓDULO 1: PANEL DE CONTROL (HOME)
    # --------------------------------------------------------------------------
    if menu == "🏠 Panel de Control":
        st.title("🏠 Dashboard Principal")
        st.markdown(f"Bienvenido nuevamente, **{st.session_state['usuario']['nombre']}**.")
        
        # Métricas KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("Biblioteca Digital", f"{len(st.session_state['repositorio'])} Documentos", "Actualizado")
        col2.metric("Tu Patrimonio", f"{st.session_state['puntos']} FitaCoins", "+1000 Bono")
        col3.metric("Nivel de Seguridad", "Alto (Protegido)", "Verificado")
        
        st.markdown("### 📢 Novedades y Accesos")
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"🎨 Estilo Visual Activo: **{st.session_state['tema_actual']}**")
            st.write("Hemos actualizado la normativa de subidas. Ahora escaneamos archivos en busca de virus automáticamente.")
        with c2:
            st.success("💡 **Tip del Día:** Puedes transferir puntos a tus colegas desde el menú 'Billetera' si necesitan descargar planos urgentes.")


    # --------------------------------------------------------------------------
    # MÓDULO 2: REPOSITORIO DE ARCHIVOS (CON LÓGICA DE BORRADO)
    # --------------------------------------------------------------------------
    elif menu == "📂 Repositorio Global":
        st.title("📂 Biblioteca Técnica Nacional")
        st.markdown("Acceso a documentación técnica. **Costo por descarga: 20 FitaCoins.**")
        
        # Filtros Avanzados
        with st.container():
            colf1, colf2 = st.columns(2)
            f_carrera = colf1.selectbox("Filtrar por Carrera", ["Todas"] + list(CARRERAS.keys()))
            
            # Lógica dependiente del primer filtro
            opciones_area = ["Todas"]
            if f_carrera != "Todas":
                opciones_area += CARRERAS[f_carrera]
            
            f_area = colf2.selectbox("Filtrar por Especialidad", opciones_area)

        # Aplicar Filtros
        archivos_visibles = st.session_state['repositorio']
        if f_carrera != "Todas":
            archivos_visibles = [a for a in archivos_visibles if a['carrera'] == f_carrera]
        if f_area != "Todas":
            archivos_visibles = [a for a in archivos_visibles if a['area'] == f_area]

        st.divider()

        if not archivos_visibles:
            st.warning("No se encontraron documentos con los filtros seleccionados.")
        
        # Renderizado de Tarjetas
        for idx, file in enumerate(archivos_visibles):
            with st.container():
                col_info, col_action = st.columns([4, 1])
                
                with col_info:
                    st.markdown(f"""
                    <div class="file-card">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div>
                                <h3 style="margin:0;">📄 {file['nombre']}</h3>
                                <p style="margin:5px 0; color:#555 !important;">{file['desc']}</p>
                            </div>
                            <div style="text-align:right;">
                                <span style="background:#EAEDED; padding:5px 10px; border-radius:10px; font-size:0.8rem;">{file['carrera']}</span>
                            </div>
                        </div>
                        <hr style="border-top: 1px solid #eee;">
                        <small>
                            <b>Autor:</b> {file['autor']} ({file['rol_autor']}) | 
                            <b>Fecha:</b> {file['fecha']} | 
                            <b>Área:</b> {file['area']}
                        </small>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_action:
                    st.write("") # Espacio vertical
                    st.write("") 
                    
                    # Lógica: ¿Es mi archivo? -> Puedo borrarlo. ¿No es mío? -> Puedo descargarlo.
                    es_mi_archivo = file['autor'] == st.session_state['usuario']['nombre']
                    
                    if es_mi_archivo:
                        if st.button("🗑️ Eliminar", key=f"del_own_{idx}", type="secondary"):
                            st.session_state['repositorio'].remove(file)
                            st.toast("Archivo eliminado correctamente.", icon="🗑️")
                            time.sleep(1)
                            st.rerun()
                    else:
                        if st.button("⬇️ Descargar", key=f"dl_{idx}", type="primary"):
                            if st.session_state['puntos'] >= 20:
                                # Proceso de cobro
                                st.session_state['puntos'] -= 20
                                registrar_transaccion("Gasto", 20, f"Descarga de documento: {file['nombre']}")
                                
                                # Simulación de descarga
                                st.toast("✅ Compra realizada. Iniciando descarga...", icon="download")
                                st.success(f"Descargando: {file['nombre']}")
                            else:
                                st.error("❌ Saldo insuficiente (Req: 20 pts). Sube archivos para ganar más.")


    # --------------------------------------------------------------------------
    # MÓDULO 3: SUBIDA DE ARCHIVOS (CON CIBERSEGURIDAD)
    # --------------------------------------------------------------------------
    elif menu == "📤 Subir Material (+10)":
        st.title("📤 Centro de Carga Segura")
        st.markdown("Comparte conocimiento y gana FitaCoins. **Recompensa: +10 Puntos por archivo.**")
        
        st.warning("🔒 **Protocolo de Seguridad Activo:** Todos los archivos son escaneados en tiempo real para detectar malware.")
        
        with st.form("formulario_subida"):
            uploaded_file = st.file_uploader("Seleccionar Archivo (PDF, XLSX, DWG, DOCX)", type=["pdf", "xlsx", "dwg", "docx", "doc"])
            
            c1, c2 = st.columns(2)
            u_carrera = c1.selectbox("Clasificación: Carrera", list(CARRERAS.keys()))
            u_area = c2.selectbox("Clasificación: Especialidad", CARRERAS[u_carrera])
            
            u_desc = st.text_input("Descripción del contenido (Obligatorio)")
            
            submitted = st.form_submit_button("🚀 Escanear y Publicar")
            
            if submitted:
                if uploaded_file and u_desc:
                    # 1. EJECUCIÓN DE ESCANEO DE SEGURIDAD
                    es_seguro, mensaje_seguridad = es_archivo_seguro(uploaded_file)
                    
                    if es_seguro:
                        # 2. LOGICA DE RECOMPENSA
                        st.session_state['puntos'] += 10
                        registrar_transaccion("Ingreso", 10, f"Recompensa por subir: {uploaded_file.name}")
                        
                        # 3. GUARDADO EN BASE DE DATOS
                        nuevo_archivo = {
                            "id": len(st.session_state['repositorio']) + 100,
                            "nombre": uploaded_file.name,
                            "carrera": u_carrera,
                            "area": u_area,
                            "autor": st.session_state['usuario']['nombre'],
                            "rol_autor": st.session_state['usuario']['rol'],
                            "fecha": datetime.now().strftime("%Y-%m-%d"),
                            "desc": u_desc
                        }
                        st.session_state['repositorio'].append(nuevo_archivo)
                        
                        st.balloons()
                        st.success("✅ Verificación de Seguridad: APROBADA.")
                        st.success(f"¡Archivo publicado! Has ganado 10 FitaCoins.")
                        time.sleep(2)
                        st.rerun()
                    else:
                        # BLOQUEO POR VIRUS
                        st.error(mensaje_seguridad)
                        st.error("La subida ha sido cancelada por motivos de seguridad.")
                else:
                    st.warning("Por favor, sube un archivo y añade una descripción.")


    # --------------------------------------------------------------------------
    # MÓDULO 4: BILLETERA DIGITAL Y TRANSFERENCIAS (CON HISTORIAL)
    # --------------------------------------------------------------------------
    elif menu == "💰 Billetera & Transferencias":
        st.title("💰 Gestión Financiera Personal")
        
        col_wallet_main, col_transfers = st.columns([1.5, 1])
        
        with col_wallet_main:
            st.subheader("📊 Balance y Movimientos")
            st.info(f"Saldo Actual: **{st.session_state['puntos']} FitaCoins**")
            
            st.write("### 📜 Historial de Transacciones")
            
            if st.session_state['transacciones']:
                # Convertimos la lista de diccionarios a DataFrame para mostrarla bonita
                df_trans = pd.DataFrame(st.session_state['transacciones'])
                # Reordenamos para que lo más reciente salga arriba
                df_trans = df_trans.iloc[::-1]
                
                # Mostramos tabla interactiva
                st.dataframe(
                    df_trans, 
                    use_container_width=True, 
                    hide_index=True,
                    column_config={
                        "tipo": "Tipo",
                        "monto": st.column_config.NumberColumn("Monto", format="%d pts"),
                        "desc": "Detalle",
                        "fecha": "Fecha/Hora"
                    }
                )
            else:
                st.info("Aún no tienes movimientos registrados.")

        with col_transfers:
            st.subheader("💸 Transferencia P2P")
            st.markdown("""
            <div style="background:white; padding:20px; border-radius:10px; border:1px solid #ddd; box-shadow:0 2px 5px rgba(0,0,0,0.05);">
                <h4 style="margin:0;">Enviar Puntos a Colega</h4>
                <p style="font-size:0.9rem;">Apoya a otros estudiantes o docentes.</p>
            </div>
            """, unsafe_allow_html=True)
            st.write("")
            
            with st.form("form_transferencia"):
                destinatario = st.selectbox("Destinatario", st.session_state['amigos'])
                monto_envio = st.number_input("Cantidad a enviar", min_value=1, max_value=st.session_state['puntos'], step=10)
                nota_envio = st.text_input("Nota (Opcional)", placeholder="Ej: Para el plano...")
                
                btn_enviar = st.form_submit_button("➡️ Realizar Transferencia")
                
                if btn_enviar:
                    if st.session_state['puntos'] >= monto_envio:
                        # 1. Descuento
                        st.session_state['puntos'] -= monto_envio
                        # 2. Registro
                        desc_log = f"Transferencia a {destinatario}"
                        if nota_envio: desc_log += f" ({nota_envio})"
                        
                        registrar_transaccion("Egreso (P2P)", monto_envio, desc_log)
                        
                        st.success(f"¡Éxito! Has enviado {monto_envio} pts a {destinatario}.")
                        time.sleep(1.5)
                        st.rerun()
                    else:
                        st.error("Saldo insuficiente para realizar esta operación.")


    # --------------------------------------------------------------------------
    # MÓDULO 5: PANEL DE ADMINISTRADOR (CONTROL TOTAL)
    # --------------------------------------------------------------------------
    elif menu == "🔧 Panel Admin (Privado)":
        st.title("🔧 Panel de Control - Administrador")
        st.markdown("""
        <div style="background:#FDEDEC; padding:15px; border-radius:10px; border-left:5px solid #E74C3C;">
            <b>Zona de Alto Privilegio:</b> Desde aquí puedes gestionar la economía del sistema y moderar contenido.
        </div>
        """, unsafe_allow_html=True)
        st.write("")
        
        tab_eco, tab_files, tab_users = st.tabs(["🖨️ Economía (Minting)", "🗑️ Moderación Archivos", "👥 Gestión Usuarios"])
        
        # TAB 1: ECONOMÍA (GENERAR PUNTOS INFINITOS)
        with tab_eco:
            st.subheader("Banco Central F.I.T.A.")
            st.write("Generación de puntos para pruebas o bonificaciones administrativas.")
            
            c1, c2 = st.columns(2)
            with c1:
                monto_mint = st.number_input("Cantidad a imprimir", min_value=100, max_value=100000, value=1000, step=100)
            with c2:
                motivo_mint = st.text_input("Motivo de la emisión", value="Ajuste Administrativo")
            
            if st.button("🖨️ Generar Puntos", type="primary"):
                st.session_state['puntos'] += monto_mint
                registrar_transaccion("ADMIN MINT", monto_mint, motivo_mint)
                st.success(f"Se han añadido {monto_mint} puntos a tu cuenta de administrador.")
                time.sleep(1)
                st.rerun()

        # TAB 2: MODERACIÓN (BORRAR CUALQUIER ARCHIVO)
        with tab_files:
            st.subheader("Gestión de Contenido")
            st.write("Lista completa de archivos en el servidor. Puedes eliminar cualquiera.")
            
            if st.session_state['repositorio']:
                for idx, file in enumerate(st.session_state['repositorio']):
                    with st.container():
                        c_det, c_del = st.columns([4, 1])
                        with c_det:
                            st.write(f"📄 **{file['nombre']}** | Subido por: {file['autor']} | {file['fecha']}")
                        with c_del:
                            if st.button("❌ Eliminar", key=f"admin_del_{idx}"):
                                st.session_state['repositorio'].pop(idx)
                                st.toast(f"Archivo {file['nombre']} eliminado por Administrador.", icon="🚫")
                                time.sleep(1)
                                st.rerun()
                        st.divider()
            else:
                st.info("El repositorio está vacío.")

        # TAB 3: USUARIOS
        with tab_users:
            st.subheader("Directorio de Usuarios")
            st.write("Añadir nuevos usuarios a la lista de contactos global.")
            
            nuevo_user = st.text_input("Nombre del nuevo usuario")
            if st.button("Añadir Usuario"):
                if nuevo_user:
                    st.session_state['amigos'].append(nuevo_user)
                    st.success(f"Usuario {nuevo_user} añadido a la base de datos.")


# ==============================================================================
# 7. CONTROLADOR DE FLUJO PRINCIPAL (MAIN LOOP)
# ==============================================================================

# Esta estructura lógica determina qué pantalla ver según el estado del usuario

if not st.session_state['logged_in']:
    # Si no está logueado -> Mostrar Login
    login_page()

elif not st.session_state['setup_completo']:
    # Si está logueado pero no ha configurado su perfil -> Mostrar Onboarding
    onboarding_page()

else:
    # Si todo está listo -> Mostrar la App Principal
    main_app()
