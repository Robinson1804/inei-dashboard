import streamlit as st
from PIL import Image
import base64

st.set_page_config(
    page_title="Presupuesto General - INEI",
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

# CSS para el navbar y el iframe
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
        padding-bottom: 0;
        max-width: 100%;
    }

    /* ====== NAVBAR CORREGIDO ====== */
    .navbar-custom {
        background: linear-gradient(135deg, #003a7a 0%, #00264d 100%);
        padding: 0.75rem 2rem;
        margin: -1rem -5rem 1rem -5rem;
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

    .navbar-buttons {
        display: flex;
        gap: 0.5rem;
        align-items: center;
    }

    .nav-btn {
        display: inline-flex;
        align-items: center;
        gap: 0.3rem;
        background: rgba(255,255,255,0.15);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 6px;
        text-decoration: none;
        font-size: 0.95rem;
        font-weight: 500;
        transition: all 0.3s;
        border: 1px solid rgba(255,255,255,0.2);
    }

    .nav-btn:hover {
        background: rgba(255,255,255,0.25);
        transform: translateY(-1px);
        color: white;
        text-decoration: none;
    }

    /* Contenedor del iframe */
    .powerbi-container {
        width: 100%;
        height: calc(100vh - 120px);
        border: none;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin-top: 1rem;
    }

    iframe {
        width: 100%;
        height: 100%;
        border: none;
    }

    /* Responsive */
    @media (max-width: 768px) {
        .navbar-custom {
            padding: 0.5rem 1rem;
            margin: -1rem -1rem 1rem -1rem;
        }
        .navbar-title {
            font-size: 1rem;
        }
        .navbar-logo {
            width: 45px;
        }
        .nav-btn {
            padding: 0.4rem 0.8rem;
            font-size: 0.85rem;
        }
        .powerbi-container {
            height: calc(100vh - 100px);
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
    <span class="navbar-title">Presupuesto General - Sistema de Seguimiento Administrativo</span>
    <div class="navbar-buttons">
        <a href="/" target="_self" class="nav-btn" title="Inicio">
            🏠 Inicio
        </a>
        <a href="/dashboard" target="_self" class="nav-btn" title="Ver Detalle">
            📊 Detalle
        </a>
    </div>
</div>
""", unsafe_allow_html=True)

# ====== IFRAME DE POWER BI ======
powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNmYxMjNhMzktNmZhYi00OTZhLTlkOTMtZDY2OTM1YzhmNWRhIiwidCI6ImM0MWJjOWY2LTVlNDAtNDA5Yy1iOWNjLWRiNjhmYjVhMzU1NCIsImMiOjR9&pageName=9bc2ee5dc610211c9bc2"

st.markdown(f"""
<div class="powerbi-container">
    <iframe
        src="{powerbi_url}"
        frameborder="0"
        allowFullScreen="true"
        loading="lazy">
    </iframe>
</div>
""", unsafe_allow_html=True)
