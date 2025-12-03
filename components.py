"""
Módulo de componentes reutilizables para el Dashboard INEI
Incluye: Navbar, estilos globales, filtros y footer
"""
import streamlit as st
import base64
from typing import List, Optional, Dict, Any

# ============================================================
# FUNCIONES UTILITARIAS
# ============================================================

def get_image_base64(image_path: str) -> Optional[str]:
    """Convierte una imagen a base64 para uso en HTML"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except:
        return None


# ============================================================
# ESTILOS CSS GLOBALES
# ============================================================

def get_global_styles() -> str:
    """Retorna los estilos CSS globales compartidos"""
    return """
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
            padding-left: 3rem !important;
            padding-right: 3rem !important;
            max-width: 100% !important;
        }

        [data-testid="stAppViewContainer"] {
            max-width: 100% !important;
        }

        [data-testid="stMain"] {
            max-width: 100% !important;
        }

        /* ====== NAVBAR ====== */
        .navbar-custom {
            background: linear-gradient(135deg, #003a7a 0%, #00264d 100%);
            padding: 0.75rem 2rem;
            margin: -1rem -3rem 0.5rem -3rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .navbar-logo {
            width: 50px;
            height: auto;
            border-radius: 4px;
        }

        .navbar-title {
            font-size: 1.1rem;
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
            color: white !important;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            text-decoration: none !important;
            font-size: 0.9rem;
            font-weight: 500;
            transition: all 0.3s;
            border: 1px solid rgba(255,255,255,0.2);
        }

        .nav-btn:hover {
            background: rgba(255,255,255,0.25);
            transform: translateY(-1px);
            color: white !important;
            text-decoration: none !important;
        }

        .nav-btn.active {
            background: rgba(255,255,255,0.3);
            border-color: rgba(255,255,255,0.4);
        }

        /* ====== FILTROS SUPERIORES (EXPANDER) ====== */
        .stExpander {
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            margin-bottom: 1rem;
            border: 1px solid #e5e7eb;
        }

        .stExpander > div:first-child {
            background: #f8fafc;
            border-radius: 10px 10px 0 0;
        }

        .stExpander[data-expanded="true"] > div:first-child {
            border-bottom: 1px solid #e5e7eb;
        }

        /* ====== MÉTRICAS INEI ====== */
        .metric-inei {
            background: #1f4e78;
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 10px;
        }

        .metric-inei .metric-label {
            font-size: 14px;
            font-weight: 500;
            opacity: 0.9;
            margin-bottom: 8px;
        }

        .metric-inei .metric-value {
            font-size: 28px;
            font-weight: 700;
        }

        /* ====== FOOTER ====== */
        .footer-text {
            text-align: center;
            color: #6b7280;
            font-size: 0.85rem;
            padding: 1rem 0;
        }

        /* ====== ESTILOS ADICIONALES ====== */
        .highlight {
            color: #1c64f2;
        }

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

        .btn-primary {
            display: inline-block;
            background: linear-gradient(135deg, #1c64f2 0%, #1752c4 100%);
            color: white !important;
            padding: 0.85rem 3rem;
            font-size: 1.1rem;
            font-weight: 600;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(28, 100, 242, 0.3);
            text-decoration: none !important;
            text-align: center;
            transition: all 0.3s ease;
            border: none;
            cursor: pointer;
        }

        .btn-primary:hover {
            background: linear-gradient(135deg, #1752c4 0%, #1443a3 100%);
            transform: translateY(-2px);
            box-shadow: 0 6px 16px rgba(28, 100, 242, 0.4);
            color: white !important;
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

        /* ====== RESPONSIVE ====== */
        @media (max-width: 768px) {
            .block-container {
                padding-left: 1rem !important;
                padding-right: 1rem !important;
            }
            .navbar-custom {
                padding: 0.5rem 1rem;
                margin: -1rem -1rem 0.5rem -1rem;
                flex-wrap: wrap;
            }
            .navbar-title {
                font-size: 0.95rem;
                order: 1;
                width: 100%;
                text-align: center;
                margin-top: 0.5rem;
            }
            .navbar-logo {
                width: 40px;
            }
            .nav-btn {
                padding: 0.4rem 0.7rem;
                font-size: 0.8rem;
            }
        }
    </style>
    """


def get_powerbi_styles() -> str:
    """Estilos adicionales para la página de Power BI"""
    return """
    <style>
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
    </style>
    """


def get_landing_styles() -> str:
    """Estilos adicionales para la landing page"""
    return """
    <style>
        .main-title {
            font-size: 2.8rem;
            font-weight: 700;
            text-align: center;
            color: #1f2937;
            margin: 2.5rem 0;
        }

        .landing-description {
            font-size: 1.25rem;
            line-height: 2;
            color: #4b5563;
            margin-bottom: 1.5rem;
        }

        .landing-description strong {
            color: #1c64f2;
            font-weight: 600;
        }

        .landing-subtitle {
            font-size: 1.3rem;
            font-weight: 600;
            color: #1f2937;
            margin: 1.5rem 0 1rem 0;
        }

        .landing-list {
            list-style: none;
            padding-left: 0;
            margin: 1.5rem 0;
        }

        .landing-list li {
            padding: 1rem 0;
            padding-left: 2.5rem;
            position: relative;
            color: #4b5563;
            line-height: 1.8;
            font-size: 1.15rem;
        }

        .landing-list li:before {
            content: "✅";
            position: absolute;
            left: 0;
            font-size: 1.3rem;
        }

        .landing-list li strong {
            color: #1c64f2;
            font-weight: 600;
        }

        .btn-container {
            display: flex;
            justify-content: center;
            margin-top: 2.5rem;
        }

        .btn-primary {
            padding: 1rem 3.5rem;
            font-size: 1.2rem;
        }

        @media (max-width: 768px) {
            .main-title {
                font-size: 2rem;
            }
            .landing-description {
                font-size: 1.1rem;
            }
            .landing-list li {
                font-size: 1rem;
            }
        }
    </style>
    """


# ============================================================
# COMPONENTES DE UI
# ============================================================

def render_navbar(
    title: str = "Sistema de Seguimiento Administrativo",
    show_buttons: bool = True,
    active_page: str = None,
    buttons: List[Dict[str, str]] = None
):
    """
    Renderiza el navbar del sistema

    Args:
        title: Título a mostrar en el navbar
        show_buttons: Si se muestran los botones de navegación
        active_page: Página activa para resaltar el botón correspondiente
        buttons: Lista de diccionarios con {href, icon, label} para botones personalizados
    """
    logo_base64 = get_image_base64("img/logo.png")

    if logo_base64:
        logo_html = f'<img src="data:image/png;base64,{logo_base64}" class="navbar-logo" alt="INEI Logo">'
    else:
        logo_html = '<span style="color: white; font-weight: bold; font-size: 1.2rem;">INEI</span>'

    # Botones por defecto
    if buttons is None:
        buttons = [
            {"href": "/", "icon": "🏠", "label": "Inicio", "id": "home"},
            {"href": "/presupuesto-general", "icon": "📈", "label": "General", "id": "general"},
            {"href": "/dashboard-general", "icon": "📋", "label": "Dashboard", "id": "dashboard-general"},
            {"href": "/dashboard", "icon": "📊", "label": "Adquisiciones", "id": "dashboard"},
        ]

    buttons_html = ""
    if show_buttons:
        for btn in buttons:
            active_class = "active" if active_page == btn.get("id") else ""
            buttons_html += f'<a href="{btn["href"]}" target="_self" class="nav-btn {active_class}" title="{btn["label"]}">{btn["icon"]} {btn["label"]}</a>'

    navbar_html = f'<div class="navbar-custom">{logo_html}<span class="navbar-title">{title}</span><div class="navbar-buttons">{buttons_html}</div></div>'

    st.markdown(navbar_html, unsafe_allow_html=True)


def render_footer():
    """Renderiza el footer del sistema"""
    st.markdown("---")
    footer_html = '<div class="footer-text"><strong>Sistema Presupuestal INEI</strong><br>Instituto Nacional de Estadística e Informática<br><small style="opacity: 0.7;">© 2025 - Todos los derechos reservados</small></div>'
    st.markdown(footer_html, unsafe_allow_html=True)


def render_metric_inei(label: str, value: str):
    """Renderiza una métrica con estilo INEI"""
    metric_html = f'<div class="metric-inei"><div class="metric-label">{label}</div><div class="metric-value">{value}</div></div>'
    st.markdown(metric_html, unsafe_allow_html=True)


# ============================================================
# INICIALIZACIÓN DE PÁGINA
# ============================================================

def init_page(
    page_title: str,
    layout: str = "wide",
    initial_sidebar_state: str = "collapsed"
):
    """
    Inicializa una página con la configuración estándar

    Args:
        page_title: Título de la página
        layout: Layout de Streamlit ("wide" o "centered")
        initial_sidebar_state: Estado inicial del sidebar
    """
    st.set_page_config(
        page_title=f"{page_title} - INEI",
        layout=layout,
        initial_sidebar_state=initial_sidebar_state
    )

    # Aplicar estilos globales
    st.markdown(get_global_styles(), unsafe_allow_html=True)
