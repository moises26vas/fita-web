import streamlit as st
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURACIÓN INICIAL (CERO DATOS PREVIOS) ---
st.set_page_config(
    page_title="F.I.T.A. System",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- GESTIÓN DE MEMORIA (SESSION STATE) ---
# Esto permite que lo que subas se mantenga en pantalla mientras usas la app
if 'repositorio' not in st.session_state:
    st.session_state['repositorio'] = []
if 'publicaciones' not in st.session_state:
    st.session_state['publicaciones'] = []

# --- ESTILOS VISUALES (PROFESIONAL & MINIMALISTA) ---
st.markdown("""
<style>
    .main-title {font-size: 2.2rem; color: #1B2631; font-weight: bold;}
    .section-header {font-size: 1.5rem; color: #283747; border-bottom: 2px solid #D5D8DC; padding-bottom: 10px;}
    .stButton>button {
        background-color: #212F3D;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    .file-card {
        background-color: #F8F9F9;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #2E86C1;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL (NAVEGACIÓN) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2554/2554044.png", width=80)
    st.markdown("### F.I.T.A. SYSTEM")
    st.markdown("---")
    
    menu = st.radio(
        "Módulos del Sistema:", 
        ["🏠 Panel de Control", "☁️ Repositorio Digital", "📊 Analizador Excel", "📝 Publicar Artículo"]
    )
    
    st.markdown("---")
    # Widget de fecha real (sin asunciones)
    fecha_hoy = datetime.now().strftime("%d/%m/%Y")
    st.caption(f"📅 Fecha: {fecha_hoy}")
    st.caption("🟢 Sistema: En Línea")

# =========================================================
# MÓDULO 1: PANEL DE CONTROL (DASHBOARD VACÍO)
# =========================================================
if menu == "🏠 Panel de Control":
    st.markdown('<p class="main-title">Bienvenido al Centro de Gestión</p>', unsafe_allow_html=True)
    st.write("Resumen general de la plataforma F.I.T.A.")
    
    # Métricas vacías para que tú las veas limpias
    col1, col2, col3 = st.columns(3)
    col1.metric("Archivos en Nube", f"{len(st.session_state['repositorio'])}")
    col2.metric("Artículos Publicados", f"{len(st.session_state['publicaciones'])}")
    col3.metric("Usuarios Activos", "1 (Admin)")

    st.info("ℹ️ El sistema está listo. Navega por el menú lateral para subir tu primer archivo o realizar cálculos.")

# =========================================================
# MÓDULO 2: REPOSITORIO DIGITAL (SUBIDA Y PUBLICACIÓN)
# =========================================================
elif menu == "☁️ Repositorio Digital":
    st.markdown('<p class="section-header">Gestión de Archivos y Planos</p>', unsafe_allow_html=True)
    
    col_upload, col_view = st.columns([1, 2])
    
    with col_upload:
        st.subheader("📤 Subir Nuevo Archivo")
        st.write("Sube PDFs, DWG, Excel o Imágenes para almacenarlos en la sesión.")
        
        archivo = st.file_uploader("Seleccionar archivo", type=["pdf", "docx", "xlsx", "dwg", "jpg", "png"])
        descripcion = st.text_input("Descripción corta del archivo (Opcional)")
        
        if st.button("Subir al Repositorio"):
            if archivo is not None:
                # Simulación de carga
                barra = st.progress(0)
                for i in range(100):
                    time.sleep(0.005)
                    barra.progress(i + 1)
                
                # Guardar en memoria
                nuevo_archivo = {
                    "nombre": archivo.name,
                    "tipo": archivo.type,
                    "desc": descripcion if descripcion else "Sin descripción",
                    "fecha": datetime.now().strftime("%H:%M:%S")
                }
                st.session_state['repositorio'].append(nuevo_archivo)
                st.success("✅ Archivo cargado exitosamente.")
                time.sleep(1)
                st.rerun() # Recarga para mostrar el archivo
            else:
                st.error("⚠️ Por favor selecciona un archivo primero.")

    with col_view:
        st.subheader("🗂️ Archivos Disponibles")
        
        if len(st.session_state['repositorio']) == 0:
            st.info("📂 El repositorio está vacío. Sube tu primer documento en el panel izquierdo.")
        else:
            for file in reversed(st.session_state['repositorio']):
                st.markdown(f"""
                <div class="file-card">
                    <b>📄 {file['nombre']}</b><br>
                    <small style="color:grey">{file['desc']} | Subido a las: {file['fecha']}</small>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# MÓDULO 3: ANALIZADOR EXCEL (HERRAMIENTA LIMPIA)
# =========================================================
elif menu == "📊 Analizador Excel":
    st.markdown('<p class="section-header">Visor de Hojas de Cálculo</p>', unsafe_allow_html=True)
    st.write("Herramienta para visualizar tablas y gráficos de metrados o diseños sin abrir Excel.")
    
    uploaded_file = st.file_uploader("Arrastra tu archivo .xlsx aquí", type=["xlsx"])
    
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            st.success(f"Archivo **{uploaded_file.name}** procesado.")
            
            # Pestañas para organizar la vista
            tab1, tab2 = st.tabs(["📄 Tabla de Datos", "📈 Gráficos Automáticos"])
            
            with tab1:
                st.dataframe(df, use_container_width=True)
            
            with tab2:
                st.write("Visualización rápida de columnas numéricas:")
                datos_numericos = df.select_dtypes(include=['float', 'int'])
                if not datos_numericos.empty:
                    st.line_chart(datos_numericos)
                else:
                    st.warning("No se encontraron datos numéricos para graficar.")
                    
        except Exception as e:
            st.error(f"Error al leer el archivo: {e}")

# =========================================================
# MÓDULO 4: PUBLICACIÓN DE ARTÍCULOS (BLOG)
# =========================================================
elif menu == "📝 Publicar Artículo":
    st.markdown('<p class="section-header">Gestión de Conocimiento</p>', unsafe_allow_html=True)
    
    tab_editor, tab_feed = st.tabs(["✍️ Editor", "📰 Publicaciones"])
    
    with tab_editor:
        st.subheader("Redactar Nuevo Documento")
        
        titulo_art = st.text_input("Título del Artículo / Nota")
        autor_art = st.text_input("Autor", value="Ing. Luigi")
        contenido_art = st.text_area("Contenido (Soporta Markdown y LaTeX)", height=200, placeholder="Escribe aquí tu investigación o apuntes...")
        
        st.caption("Tip: Puedes usar LaTeX escribiendo entre signos de dólar. Ej: $E = mc^2$")
        
        if st.button("Publicar en la Plataforma"):
            if titulo_art and contenido_art:
                nueva_pub = {
                    "titulo": titulo_art,
                    "autor": autor_art,
                    "cuerpo": contenido_art,
                    "fecha": datetime.now().strftime("%d/%m %H:%M")
                }
                st.session_state['publicaciones'].append(nueva_pub)
                st.success("Publicado correctamente.")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("El título y el contenido son obligatorios.")

    with tab_feed:
        st.subheader("Artículos Recientes")
        
        if len(st.session_state['publicaciones']) == 0:
            st.write("No hay artículos publicados aún.")
        else:
            for pub in reversed(st.session_state['publicaciones']):
                with st.expander(f"📌 {pub['titulo']} - Por {pub['autor']} ({pub['fecha']})", expanded=True):
                    st.markdown(pub['cuerpo'])

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("© 2026 F.I.T.A. Construction | Plataforma Privada")
