import streamlit as st
import sys
import os

# Agregar el directorio raíz al path para importar componentes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import (
    init_page,
    render_navbar,
    render_footer,
    get_global_styles,
    get_powerbi_styles
)

# Inicializar página
init_page("Presupuesto General", initial_sidebar_state="collapsed")

# Aplicar estilos adicionales para Power BI
st.markdown(get_powerbi_styles(), unsafe_allow_html=True)

# Renderizar Navbar
render_navbar(
    title="Presupuesto General - Sistema de Seguimiento Administrativo",
    show_buttons=True,
    active_page="general"
)

# ====== IFRAME DE POWER BI ======
powerbi_url = "https://app.powerbi.com/view?r=eyJrIjoiNmYxMjNhMzktNmZhYi00OTZhLTlkOTMtZDY2OTM1YzhmNWRhIiwidCI6ImM0MWJjOWY2LTVlNDAtNDA5Yy1iOWNjLWRiNjhmYjVhMzU1NCIsImMiOjR9&pageName=9bc2ee5dc610211c9bc2"

powerbi_html = f'<div class="powerbi-container"><iframe src="{powerbi_url}" frameborder="0" allowFullScreen="true" loading="lazy"></iframe></div>'
st.markdown(powerbi_html, unsafe_allow_html=True)
