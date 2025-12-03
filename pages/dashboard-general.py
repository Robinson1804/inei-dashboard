import streamlit as st
import sys
import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Agregar el directorio raíz al path para importar componentes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import (
    init_page,
    render_navbar,
    render_footer,
    get_global_styles,
    render_metric_inei
)

# ============================================================
# CONFIGURACIÓN DE PÁGINA
# ============================================================
init_page("Dashboard General", initial_sidebar_state="collapsed")

# Estilos adicionales para dashboard general
st.markdown("""
<style>
    /* ====== KPI CARDS ====== */
    .kpi-container {
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        margin-bottom: 1.5rem;
    }

    .kpi-card {
        background: linear-gradient(135deg, #1f4e78 0%, #163d5c 100%);
        padding: 16px 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        flex: 1;
        min-width: 140px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }

    .kpi-label {
        font-size: 11px;
        font-weight: 500;
        opacity: 0.9;
        margin-bottom: 6px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-value {
        font-size: 20px;
        font-weight: 700;
    }

    .kpi-value-small {
        font-size: 16px;
        font-weight: 700;
    }

    /* ====== FILTROS ====== */
    .filter-section {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e5e7eb;
    }

    /* ====== TABLA ====== */
    .dataframe-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    /* ====== SECCIÓN GRÁFICOS ====== */
    .chart-section {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #1c64f2;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# NAVBAR
# ============================================================
render_navbar(
    title="Dashboard General - Sistema de Seguimiento Administrativo",
    show_buttons=True,
    active_page="dashboard-general"
)

# ============================================================
# DATOS SIMULADOS REALISTAS
# ============================================================
@st.cache_data
def generar_datos_simulados():
    """Genera datos simulados realistas de programación presupuestal"""
    np.random.seed(42)

    # Unidades Ejecutoras (DDNNTT)
    unidades = ['CIDE', 'DNCE', 'DNCN', 'DNPC', 'DNES', 'OGA', 'OPP', 'OTIC', 'RRHH', 'LEGAL']

    # Metas Presupuestales
    metas = [
        '0001 - Gestión Administrativa',
        '0002 - Censos y Encuestas',
        '0003 - Estadísticas Económicas',
        '0004 - Estadísticas Sociales',
        '0005 - Cuentas Nacionales',
        '0006 - Infraestructura Tecnológica',
        '0007 - Capacitación y Desarrollo',
        '0008 - Difusión Estadística',
        '0009 - Cartografía y Geodesia',
        '0010 - Coordinación Regional'
    ]

    # Clasificadores presupuestales
    clasificadores = [
        '2.3.1 - Compra de Bienes',
        '2.3.2 - Contratación de Servicios',
        '2.3.3 - Servicios Básicos',
        '2.4.1 - Donaciones y Transferencias',
        '2.5.1 - Otros Gastos',
        '2.6.1 - Adquisición de Activos',
        '2.6.2 - Construcción de Edificios',
        '2.3.4 - Consultorías',
        '2.3.5 - Alquileres',
        '2.3.6 - Viáticos y Asignaciones'
    ]

    # Descripciones de gastos
    descripciones = [
        'Adquisición de equipos de cómputo para procesamiento estadístico',
        'Servicio de mantenimiento de infraestructura tecnológica',
        'Contratación de personal temporal para censos',
        'Compra de materiales de oficina y papelería',
        'Servicio de telecomunicaciones y conectividad',
        'Alquiler de locales para operativos de campo',
        'Viáticos para supervisores regionales',
        'Consultoría en metodología estadística',
        'Servicio de transporte para operativos',
        'Adquisición de licencias de software',
        'Impresión de cuestionarios y manuales',
        'Servicio de seguridad y vigilancia',
        'Mantenimiento de vehículos institucionales',
        'Capacitación del personal técnico',
        'Servicio de difusión en medios',
        'Equipamiento de sedes regionales',
        'Desarrollo de sistemas informáticos',
        'Servicio de limpieza institucional',
        'Adquisición de mobiliario de oficina',
        'Gastos de representación institucional'
    ]

    registros = []

    for año in [2024, 2025]:
        for ue in unidades:
            # Cada UE tiene diferentes metas y montos
            num_registros = np.random.randint(8, 15)

            for _ in range(num_registros):
                meta = np.random.choice(metas)
                clasificador = np.random.choice(clasificadores)
                descripcion = np.random.choice(descripciones)

                # Generar montos realistas
                pim = np.random.randint(50000, 2500000)

                # Certificado entre 60% y 95% del PIM
                porcentaje_cert = np.random.uniform(0.60, 0.95)
                certificado = int(pim * porcentaje_cert)

                pim_por_certificar = pim - certificado

                # Compromiso Anual entre 90% y 100% del certificado
                porcentaje_comp = np.random.uniform(0.90, 1.0)
                compromiso_anual = int(certificado * porcentaje_comp)

                # Devengado entre 70% y 95% del compromiso
                porcentaje_dev = np.random.uniform(0.70, 0.95)
                devengado = int(compromiso_anual * porcentaje_dev)

                compromiso_por_devengar = compromiso_anual - devengado
                pim_por_devengar = pim - devengado

                registros.append({
                    'Año': año,
                    'UE': ue,
                    'Meta': meta,
                    'Clasificador': clasificador.split(' - ')[0],
                    'Descripción': descripcion,
                    'PIM': pim,
                    'Certificado': certificado,
                    'PIM_Por_Certificar': pim_por_certificar,
                    'Compromiso_Anual': compromiso_anual,
                    'Devengado': devengado,
                    'Compromiso_Por_Devengar': compromiso_por_devengar,
                    'PIM_Por_Devengar': pim_por_devengar,
                    'Saldo': pim - certificado,
                    'Ejecución_%': round((devengado / pim * 100) if pim > 0 else 0, 1)
                })

    return pd.DataFrame(registros)

# Cargar datos simulados
df = generar_datos_simulados()

# ============================================================
# FILTROS SUPERIORES
# ============================================================
with st.expander("🔍 **Filtros de Búsqueda**", expanded=True):
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        años_disponibles = sorted(df['Año'].unique(), reverse=True)
        año_seleccionado = st.selectbox(
            "AÑO",
            options=años_disponibles,
            index=0
        )

    with col2:
        ddnntt_opciones = ["Todos"] + sorted(df['UE'].unique().tolist())
        ddnntt_seleccionado = st.selectbox(
            "DDNNTT",
            options=ddnntt_opciones,
            index=0
        )

    with col3:
        meta_opciones = ["Todos"] + sorted(df['Meta'].unique().tolist())
        meta_seleccionada = st.selectbox(
            "META",
            options=meta_opciones,
            index=0
        )

    with col4:
        clasificador_opciones = ["Todos"] + sorted(df['Clasificador'].unique().tolist())
        clasificador_seleccionado = st.selectbox(
            "CLASIFICADOR",
            options=clasificador_opciones,
            index=0
        )

    with col5:
        buscar_detalle = st.text_input(
            "DETALLE",
            placeholder="Buscar..."
        )

# ============================================================
# APLICAR FILTROS
# ============================================================
df_filtrado = df[df['Año'] == año_seleccionado].copy()

if ddnntt_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['UE'] == ddnntt_seleccionado]

if meta_seleccionada != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Meta'] == meta_seleccionada]

if clasificador_seleccionado != "Todos":
    df_filtrado = df_filtrado[df_filtrado['Clasificador'] == clasificador_seleccionado]

if buscar_detalle:
    df_filtrado = df_filtrado[df_filtrado['Descripción'].str.contains(buscar_detalle, case=False, na=False)]

# ============================================================
# CALCULAR KPIs
# ============================================================
total_pim = df_filtrado['PIM'].sum()
total_certificado = df_filtrado['Certificado'].sum()
pim_por_certificar = df_filtrado['PIM_Por_Certificar'].sum()
compromiso_anual = df_filtrado['Compromiso_Anual'].sum()
total_devengado = df_filtrado['Devengado'].sum()
compromiso_por_devengar = df_filtrado['Compromiso_Por_Devengar'].sum()

# Calcular porcentaje de avance
porcentaje_avance = (total_devengado / total_pim * 100) if total_pim > 0 else 0

# ============================================================
# KPI CARDS
# ============================================================
st.markdown("### 📊 Resumen Ejecutivo")

kpi_html = f'''
<div class="kpi-container">
    <div class="kpi-card">
        <div class="kpi-label">PIM</div>
        <div class="kpi-value-small">S/ {total_pim:,.0f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">CERTIFICADO</div>
        <div class="kpi-value-small">S/ {total_certificado:,.0f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">PIM POR CERTIFICAR</div>
        <div class="kpi-value-small">S/ {pim_por_certificar:,.0f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">COMPROMISO ANUAL</div>
        <div class="kpi-value-small">S/ {compromiso_anual:,.0f}</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">DEVENGADO ACUMULADO</div>
        <div class="kpi-value-small">S/ {total_devengado:,.0f}</div>
    </div>
    <div class="kpi-card" style="background: linear-gradient(135deg, #059669 0%, #047857 100%);">
        <div class="kpi-label">% AVANCE</div>
        <div class="kpi-value">{porcentaje_avance:.1f}%</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">COMP. POR DEVENGAR</div>
        <div class="kpi-value-small">S/ {compromiso_por_devengar:,.0f}</div>
    </div>
</div>
'''
st.markdown(kpi_html, unsafe_allow_html=True)

# ============================================================
# GRÁFICOS Y TABLA
# ============================================================
col_grafico, col_tabla = st.columns([1, 1.5])

# Configuración común de gráficos
CHART_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'grafico_presupuestal',
        'height': 800,
        'width': 1200,
        'scale': 2
    }
}

with col_grafico:
    st.markdown('<div class="section-title">% AVANCE DE EJECUCIÓN PRESUPUESTAL POR DDNNTT</div>', unsafe_allow_html=True)

    # Agrupar por DDNNTT
    df_agrupado = df_filtrado.groupby('UE').agg({
        'PIM': 'sum',
        'Certificado': 'sum',
        'Devengado': 'sum'
    }).reset_index()

    df_agrupado['Avance_%'] = (df_agrupado['Devengado'] / df_agrupado['PIM'] * 100).round(1)
    df_agrupado = df_agrupado.sort_values('Avance_%', ascending=True)

    # Crear gráfico de barras horizontales
    fig_avance = go.Figure()

    # Definir colores basados en el porcentaje
    colors = []
    for val in df_agrupado['Avance_%']:
        if val >= 80:
            colors.append('#10b981')  # Verde
        elif val >= 60:
            colors.append('#f59e0b')  # Amarillo
        else:
            colors.append('#ef4444')  # Rojo

    # Agregar barras
    fig_avance.add_trace(go.Bar(
        y=df_agrupado['UE'],
        x=df_agrupado['Avance_%'],
        orientation='h',
        marker=dict(color=colors),
        text=[f'{v:.1f}%' for v in df_agrupado['Avance_%']],
        textposition='outside',
        textfont=dict(size=12, color='#1f2937', family='Inter'),
        hovertemplate='<b>%{y}</b><br>Avance: %{x:.1f}%<br>PIM: S/ %{customdata[0]:,.0f}<br>Devengado: S/ %{customdata[1]:,.0f}<extra></extra>',
        customdata=df_agrupado[['PIM', 'Devengado']].values
    ))

    fig_avance.update_layout(
        height=400,
        margin=dict(l=20, r=80, t=20, b=20),
        xaxis=dict(
            title=dict(text='% Avance', font=dict(size=12, family='Inter')),
            tickfont=dict(size=11, family='Inter'),
            range=[0, max(df_agrupado['Avance_%'].max() * 1.15, 100)],
            gridcolor='#e5e7eb',
            showgrid=True
        ),
        yaxis=dict(
            title=dict(text='', font=dict(size=12, family='Inter')),
            tickfont=dict(size=12, family='Inter')
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        showlegend=False
    )

    st.plotly_chart(fig_avance, use_container_width=True, config=CHART_CONFIG)

    # Sección adicional: Meta Proyectada / Ejecución del Mes
    st.markdown('<div class="section-title" style="margin-top: 1rem;">META PROYECTADA / EJECUCIÓN DEL MES</div>', unsafe_allow_html=True)

    # Crear gráfico de comparación por meta
    df_por_meta = df_filtrado.groupby('Meta').agg({
        'PIM': 'sum',
        'Certificado': 'sum',
        'Devengado': 'sum'
    }).reset_index()
    df_por_meta = df_por_meta.nlargest(5, 'PIM')  # Top 5 metas por PIM

    fig_meta = go.Figure()

    fig_meta.add_trace(go.Bar(
        name='PIM',
        x=df_por_meta['Meta'].str[:25] + '...',
        y=df_por_meta['PIM'],
        marker_color='#1f4e78',
        text=[f'S/ {v/1000000:.1f}M' if v >= 1000000 else f'S/ {v/1000:.0f}K' for v in df_por_meta['PIM']],
        textposition='outside',
        textfont=dict(size=9, family='Inter')
    ))

    fig_meta.add_trace(go.Bar(
        name='Devengado',
        x=df_por_meta['Meta'].str[:25] + '...',
        y=df_por_meta['Devengado'],
        marker_color='#059669',
        text=[f'S/ {v/1000000:.1f}M' if v >= 1000000 else f'S/ {v/1000:.0f}K' for v in df_por_meta['Devengado']],
        textposition='outside',
        textfont=dict(size=9, family='Inter')
    ))

    fig_meta.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=30, b=80),
        barmode='group',
        xaxis=dict(
            title=dict(text='', font=dict(size=10, family='Inter')),
            tickfont=dict(size=8, family='Inter'),
            tickangle=-35
        ),
        yaxis=dict(
            title=dict(text='Monto (S/)', font=dict(size=10, family='Inter')),
            tickfont=dict(size=9, family='Inter'),
            gridcolor='#e5e7eb'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1,
            font=dict(size=10, family='Inter')
        )
    )

    st.plotly_chart(fig_meta, use_container_width=True, config=CHART_CONFIG)

with col_tabla:
    st.markdown('<div class="section-title">DETALLE DE EJECUCIÓN PRESUPUESTAL</div>', unsafe_allow_html=True)

    # Preparar datos para la tabla
    df_tabla = df_filtrado[['UE', 'Meta', 'Clasificador', 'Descripción', 'PIM', 'Certificado', 'PIM_Por_Certificar', 'Devengado', 'Ejecución_%']].copy()

    # Renombrar columnas para mejor visualización
    df_tabla.columns = ['DDNNTT', 'Meta', 'Clasif.', 'Descripción', 'PIM', 'Certificado', 'PIM x Certif.', 'Devengado', '% Ejec.']

    # Crear versión formateada para mostrar
    df_display = df_tabla.copy()

    # Formatear montos
    for col in ['PIM', 'Certificado', 'PIM x Certif.', 'Devengado']:
        df_display[col] = df_display[col].apply(lambda x: f"S/ {x:,.0f}")

    df_display['% Ejec.'] = df_display['% Ejec.'].apply(lambda x: f"{x:.1f}%")

    # Limitar descripción
    df_display['Descripción'] = df_display['Descripción'].str[:35] + '...'
    df_display['Meta'] = df_display['Meta'].str[:20] + '...'

    # Mostrar tabla con scroll
    st.dataframe(
        df_display,
        use_container_width=True,
        height=650,
        hide_index=True,
        column_config={
            "DDNNTT": st.column_config.TextColumn("DDNNTT", width="small"),
            "Meta": st.column_config.TextColumn("Meta", width="medium"),
            "Clasif.": st.column_config.TextColumn("Clasif.", width="small"),
            "Descripción": st.column_config.TextColumn("Descripción", width="medium"),
            "PIM": st.column_config.TextColumn("PIM", width="small"),
            "Certificado": st.column_config.TextColumn("Certificado", width="small"),
            "PIM x Certif.": st.column_config.TextColumn("PIM x Certif.", width="small"),
            "Devengado": st.column_config.TextColumn("Devengado", width="small"),
            "% Ejec.": st.column_config.TextColumn("% Ejec.", width="small")
        }
    )

# ============================================================
# RESUMEN INFERIOR
# ============================================================
st.markdown("---")

# Totales por DDNNTT
st.markdown("### 📈 Resumen por Unidad Ejecutora")

df_resumen = df_filtrado.groupby('UE').agg({
    'PIM': 'sum',
    'Certificado': 'sum',
    'PIM_Por_Certificar': 'sum',
    'Compromiso_Anual': 'sum',
    'Devengado': 'sum',
    'Compromiso_Por_Devengar': 'sum'
}).reset_index()

df_resumen['Avance_%'] = (df_resumen['Devengado'] / df_resumen['PIM'] * 100).round(1)
df_resumen = df_resumen.sort_values('PIM', ascending=False)

# Formatear para visualización
df_resumen_display = df_resumen.copy()
for col in ['PIM', 'Certificado', 'PIM_Por_Certificar', 'Compromiso_Anual', 'Devengado', 'Compromiso_Por_Devengar']:
    df_resumen_display[col] = df_resumen_display[col].apply(lambda x: f"S/ {x:,.0f}")
df_resumen_display['Avance_%'] = df_resumen_display['Avance_%'].apply(lambda x: f"{x:.1f}%")

df_resumen_display.columns = ['DDNNTT', 'PIM', 'Certificado', 'PIM por Certificar', 'Compromiso Anual', 'Devengado', 'Comp. por Devengar', '% Avance']

st.dataframe(
    df_resumen_display,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# FOOTER
# ============================================================
st.markdown("<br>", unsafe_allow_html=True)
render_footer()
