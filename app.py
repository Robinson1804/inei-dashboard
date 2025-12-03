import streamlit as st
from PIL import Image
from components import (
    init_page,
    render_navbar,
    render_footer,
    get_global_styles,
    get_landing_styles,
    get_image_base64
)

# Inicializar página
init_page("Sistema Presupuestal", initial_sidebar_state="collapsed")

# Aplicar estilos adicionales para landing
st.markdown(get_landing_styles(), unsafe_allow_html=True)

# Renderizar Navbar
render_navbar(
    title="Sistema de Seguimiento Administrativo",
    show_buttons=True,
    active_page="home"
)

# ====== TÍTULO PRINCIPAL ======
st.markdown('<h1 class="main-title">Bienvenido al <span class="highlight">TABLERO PRESUPUESTAL</span></h1>', unsafe_allow_html=True)

# ====== CONTENIDO PRINCIPAL ======
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    try:
        icon = Image.open("img/iconprincipal.png")
        st.image(icon, use_container_width=True)
    except:
        st.info("📊 Imagen del sistema")

with col2:
    st.markdown('<p class="landing-description">Este sistema es la <strong>herramienta clave</strong> para la gestión transparente y eficiente de nuestros recursos financieros, diseñada para optimizar cada proceso administrativo y presupuestal de la institución.</p>', unsafe_allow_html=True)

    st.markdown('<p class="landing-subtitle">A través de esta plataforma intuitiva, usted podrá:</p>', unsafe_allow_html=True)

    st.markdown('<ul class="landing-list"><li><strong>Visualizar y dar seguimiento</strong> a las ejecuciones presupuestales conforme a los créditos autorizados, con información actualizada en tiempo real.</li><li><strong>Gestionar y registrar</strong> las adquisiciones de bienes y/o servicios de manera ágil, controlada y con total trazabilidad.</li><li><strong>Asegurar que cada inversión</strong> esté alineada con los objetivos institucionales y la disponibilidad presupuestaria vigente.</li></ul>', unsafe_allow_html=True)

    st.markdown('<p class="landing-description">Nuestro objetivo primordial es <strong>garantizar la rendición de cuentas</strong> y el uso óptimo del presupuesto en cada etapa del ciclo administrativo, promoviendo la transparencia y eficiencia institucional.</p>', unsafe_allow_html=True)

    # Botón centrado con HTML
    st.markdown('<div class="btn-container"><a href="/presupuesto-general" target="_self" class="btn-primary">🚀 INICIAR</a></div>', unsafe_allow_html=True)

# ====== FOOTER ======
st.markdown("<br><br>", unsafe_allow_html=True)
render_footer()
