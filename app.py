import streamlit as st
import pandas as pd
from io import BytesIO
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(
    page_title="F.I.T.A. Hub",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- ESTILOS CSS (Diseño Bonito) ---
st.markdown("""
<style>
    .main-header {font-size: 2.5rem; color: #1E3A8A; font-weight: bold;}
    .sub-text {font-size: 1.1rem; color: #4B5563;}
    div.stButton > button:first-child {
        background-color: #1E3A8A;
        color: white;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stAlert {border-radius: 10px;}
</style>
""", unsafe_allow_html=True)

# --- MENÚ LATERAL ---
with st.sidebar:
    st.title("🏗️ F.I.T.A. SYSTEM")
    st.caption("Plataforma de Ingeniería Civil")
    st.markdown("---")
    
    opcion = st.radio(
        "Navegación:", 
        ["🏠 Inicio", "📚 Biblioteca Técnica", "📊 Visor de Metrados", "🧮 Calculadora Estructural", "☁️ Repositorio"]
    )
    
    st.markdown("---")
    st.info("👤 **Ing. Luigi**\n\n🟢 Estado: Online")

# --- PÁGINA: INICIO ---
if opcion == "🏠 Inicio":
    st.markdown('<p class="main-header">Centro de Comando F.I.T.A.</p>', unsafe_allow_html=True)
    st.markdown("Bienvenido al sistema de gestión de proyectos y análisis estructural.")
    
    # Dashboard de Métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Sprint Estructuras", "Día 1 / 30", "En Curso")
    col2.metric("Meta Principal", "Hibbeler Materiales", "Prioridad Alta")
    col3.metric("Próximo Hito", "Simulacro Estática", "Viernes")

    st.success("✅ **Sistema Operativo:** Conectado a GitHub y Streamlit Cloud.")
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("📅 Agenda del Día")
        st.write("- **Bloque I:** Teoría de Esfuerzos.")
        st.write("- **Bloque II:** Resolución de problemas tipo examen.")
    
    with col_b:
        st.subheader("📢 Avisos")
        st.warning("Recuerda subir los metrados actualizados al repositorio antes de las 18:00.")

# --- PÁGINA: BIBLIOTECA (LATEX) ---
elif opcion == "📚 Biblioteca Técnica":
    st.title("📚 Artículos de Investigación")
    st.write("Visualización de ecuaciones complejas y teoría avanzada.")
    
    tab1, tab2 = st.tabs(["📄 Análisis Matricial", "📝 Editor de Notas"])
    
    with tab1:
        st.header("Matriz de Rigidez en Pórticos")
        st.write("La ecuación fundamental para un elemento de pórtico plano es:")
        
        # Ecuación Matemática Profesional
        st.latex(r'''
        \begin{bmatrix} F_1 \\ M_1 \\ F_2 \\ M_2 \end{bmatrix} = 
        \frac{EI}{L^3} 
        \begin{bmatrix} 
        12 & 6L & -12 & 6L \\ 
        6L & 4L^2 & -6L & 2L^2 \\ 
        -12 & -6L & 12 & -6L \\ 
        6L & 2L^2 & -6L & 4L^2 
        \end{bmatrix}
        \begin{bmatrix} \delta_1 \\ \theta_1 \\ \delta_2 \\ \theta_2 \end{bmatrix}
        ''')
        
        st.info("Esta formulación es la base del software SAP2000 y ETABS.")
    
    with tab2:
        st.subheader("Tus Notas Rápidas")
        nota = st.text_area("Escribe aquí ideas o borradores:", height=150)
        if st.button("Guardar Nota"):
            st.toast("Nota guardada temporalmente.", icon="💾")

# --- PÁGINA: VISOR EXCEL ---
elif opcion == "📊 Visor de Metrados":
    st.title("📊 Análisis de Hojas de Cálculo")
    st.markdown("Sube tus archivos `.xlsx` para visualizar tablas y gráficos sin abrir Excel.")
    
    archivo = st.file_uploader("Arrastra tu Excel aquí", type=["xlsx"])
    
    if archivo:
        try:
            df = pd.read_excel(archivo)
            st.success("Archivo procesado con éxito.")
            
            with st.expander("🔍 Ver Tabla Completa", expanded=True):
                st.dataframe(df, use_container_width=True)
            
            st.subheader("📈 Análisis Rápido")
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Estadísticas:**")
                st.write(df.describe())
            with col2:
                st.write("**Gráfico de Tendencias:**")
                st.line_chart(df.select_dtypes(include=['float', 'int']))
                
        except Exception as e:
            st.error(f"Error leyendo el archivo: {e}")

# --- PÁGINA: CALCULADORA ---
elif opcion == "🧮 Calculadora Estructural":
    st.title("🧮 Calculadora de Vigas")
    st.write("Cálculo rápido para viga simplemente apoyada con carga distribuida.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Beam_UDL.svg/1200px-Beam_UDL.svg.png", caption="Esquema de Carga")
    with col2:
        w = st.number_input("Carga Distribuida (w) [kg/m]", value=1500.0, step=100.0)
        L = st.number_input("Longitud de la Viga (L) [m]", value=6.0, step=0.5)
        st.markdown("### Resultados:")
        
        if st.button("Calcular Esfuerzos"):
            M_max = (w * L**2) / 8
            V_max = (w * L) / 2
            
            st.success(f"🔹 Momento Máximo (+): **{M_max:,.2f} kg·m**")
            st.info(f"🔹 Cortante Máximo (V): **{V_max:,.2f} kg**")
            
            # Mostrar fórmula usada
            st.latex(r"M_{max} = \frac{w \cdot L^2}{8}")

# --- PÁGINA: REPOSITORIO ---
elif opcion == "☁️ Repositorio":
    st.title("☁️ Nube Privada F.I.T.A.")
    st.markdown("Gestión de archivos PDF, DWG y Planos.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📤 Subir Documento")
        up = st.file_uploader("Selecciona archivo", type=["pdf", "dwg", "docx"])
        if up:
            barra = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                barra.progress(i + 1)
            st.success(f"¡{up.name} subido a la nube segura!")
            
    with col2:
        st.subheader("📥 Descargas Disponibles")
        st.write("Archivos recientes:")
        st.download_button("📄 Plan_Sprint_30Dias.pdf", data="Simulacion", file_name="Plan.pdf")
        st.download_button("🏗️ Detalle_Viga_V101.dwg", data="Simulacion", file_name="Plano.dwg")

# --- PIE DE PÁGINA ---
st.markdown("---")
st.markdown("© 2026 F.I.T.A. Construction S.A.C. | Desarrollado por Ing. Luigi")
