import streamlit as st
from PIL import Image
import base64

st.set_page_config(
    page_title="Sistema Presupuestal - INEI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Función para convertir imagen a base64
def get_image_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None

# CSS Corregido
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    /* Reset Streamlit */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}

    .stApp {
        font-family: 'Inter', sans-serif;
        background: #f9fafb;
    }

    .block-container {
        padding-top: 0 !important;
        max-width: 1200px;
    }

    /* ====== NAVBAR CORREGIDO ====== */
    .navbar-custom {
        background: linear-gradient(135deg, #003a7a 0%, #00264d 100%);
        padding: 0.75rem 2rem;
        margin: -1rem -5rem 2rem -5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .navbar-logo {
        width: 60px;
        height: auto;
        border-radius: 4px;
    }

    .navbar-title {
        font-size: 1.2rem;
        font-weight: 500;
        color: white;
        margin: 0;
        flex-grow: 1;
        text-align: center;
    }

    /* ====== TÍTULO PRINCIPAL ====== */
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        color: #1f2937;
        margin: 2rem 0;
    }

    .highlight {
        color: #1c64f2;
    }

    /* ====== DESCRIPCIÓN ====== */
    .description {
        font-size: 1.05rem;
        line-height: 1.8;
        color: #4b5563;
        margin-bottom: 1.5rem;
        text-align: justify;
    }

    .description strong {
        color: #1c64f2;
        font-weight: 600;
    }

    /* ====== LISTA PERSONALIZADA ====== */
    .custom-list {
        list-style: none;
        padding-left: 0;
        margin: 1.5rem 0;
    }

    .custom-list li {
        padding: 0.75rem 0;
        padding-left: 2rem;
        position: relative;
        color: #4b5563;
        line-height: 1.7;
        text-align: justify;
    }

    .custom-list li:before {
        content: "✅";
        position: absolute;
        left: 0;
        font-size: 1.2rem;
    }

    /* ====== BOTÓN ====== */
    .btn-iniciar {
        display: inline-block;
        background: linear-gradient(135deg, #1c64f2 0%, #1752c4 100%);
        color: white !important;
        padding: 0.85rem 3rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(28, 100, 242, 0.3);
        text-decoration: none;
        text-align: center;
        transition: all 0.3s ease;
        border: none;
        cursor: pointer;
    }

    .btn-iniciar:hover {
        background: linear-gradient(135deg, #1752c4 0%, #1443a3 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(28, 100, 242, 0.4);
        color: white !important;
        text-decoration: none;
    }

    .btn-container {
        display: flex;
        justify-content: center;
        margin-top: 2rem;
    }

    /* ====== IMAGEN CENTRADA ====== */
    .centered-image {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 1rem 0;
    }

    /* ====== FOOTER ====== */
    .footer-text {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        padding: 1rem 0;
    }

    /* ====== RESPONSIVE ====== */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
        .description {
            font-size: 1rem;
        }
        .navbar-custom {
            padding: 0.5rem 1rem;
            margin: -1rem -1rem 1.5rem -1rem;
        }
        .navbar-title {
            font-size: 1rem;
        }
        .navbar-logo {
            width: 45px;
        }
    }
</style>
""", unsafe_allow_html=True)

# ====== NAVBAR COMO HTML PURO ======
logo_base64 = get_image_base64("img/logo.png")

if logo_base64:
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="navbar-logo" alt="INEI Logo">'
else:
    logo_html = '<span style="color: white; font-weight: bold; font-size: 1.5rem;">INEI</span>'

st.markdown(f"""
<div class="navbar-custom">
    {logo_html}
    <span class="navbar-title">Sistema de Seguimiento Administrativo</span>
</div>
""", unsafe_allow_html=True)

# ====== TÍTULO PRINCIPAL ======
st.markdown('<h1 class="main-title">Bienvenido al <span class="highlight">TABLERO PRESUPUESTAL</span></h1>', unsafe_allow_html=True)

# ====== CONTENIDO PRINCIPAL ======
col1, col2 = st.columns([1, 1.2], gap="large")

with col1:
    st.markdown('<div class="centered-image">', unsafe_allow_html=True)
    try:
        icon = Image.open("img/iconprincipal.png")
        st.image(icon, use_container_width=True)
    except:
        st.info("📊 Imagen del sistema")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="description">
        Este sistema es la <strong>herramienta clave</strong> para la gestión transparente
        y eficiente de nuestros recursos financieros, diseñada para optimizar cada proceso.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**A través de esta plataforma intuitiva, usted podrá:**")

    st.markdown("""
    <ul class="custom-list">
        <li><strong>Visualizar y dar seguimiento</strong> a las ejecuciones presupuestales conforme a los créditos autorizados.</li>
        <li><strong>Gestionar y registrar</strong> las adquisiciones de bienes y/o servicios de manera ágil y controlada.</li>
        <li>Asegurar que cada inversión esté <strong>alineada con los objetivos</strong> y la disponibilidad presupuestaria.</li>
    </ul>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="description">
        Nuestro objetivo primordial es <strong>garantizar la rendición de cuentas</strong>
        y el uso óptimo del presupuesto en cada etapa del ciclo administrativo.
    </div>
    """, unsafe_allow_html=True)

    # Botón centrado con HTML
    st.markdown("""
    <div class="btn-container">
        <a href="/presupuesto-general" target="_self" class="btn-iniciar">
            🚀 INICIAR
        </a>
    </div>
    """, unsafe_allow_html=True)

# ====== FOOTER ======
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div class="footer-text">
    <strong>Sistema Presupuestal INEI</strong><br>
    Instituto Nacional de Estadística e Informática<br>
    <small style='opacity: 0.7;'>© 2025 - Todos los derechos reservados</small>
</div>
""", unsafe_allow_html=True)