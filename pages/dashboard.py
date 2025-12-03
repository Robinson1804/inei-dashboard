import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.units import inch
import xlsxwriter
import sys
import os

# Agregar el directorio raíz al path para importar componentes
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components import init_page, render_navbar, render_footer, render_metric_inei, get_global_styles
from database import SessionLocal, UnidadEjecutora
from db_operations import (
    inicializar_datos_ejemplo,
    obtener_programacion_df,
    obtener_adquisiciones_df,
    obtener_detalle_adquisicion,
    procesar_archivo_programacion,
    obtener_alertas,
    crear_alerta,
    eliminar_alerta
)
from database import SessionLocal as DirectSessionLocal

# Inicializar página con componentes
init_page("Dashboard de Adquisiciones", initial_sidebar_state="collapsed")

# Renderizar Navbar
render_navbar(
    title="Dashboard de Adquisiciones",
    show_buttons=True,
    active_page="dashboard"
)

# ============================================================
# CONFIGURACIÓN DE GRÁFICOS - Textos grandes para pantalla completa
# ============================================================
CHART_CONFIG = {
    'displayModeBar': True,
    'displaylogo': False,
    'modeBarButtonsToAdd': ['fullscreen'],
    'toImageButtonOptions': {
        'format': 'png',
        'filename': 'grafico_inei',
        'height': 800,
        'width': 1200,
        'scale': 2
    }
}

def get_chart_layout(title: str, height: int = 450) -> dict:
    """Retorna configuración de layout para gráficos con textos grandes"""
    return {
        'title': {
            'text': title,
            'font': {'size': 20, 'color': '#1f2937', 'family': 'Inter, sans-serif'},
            'x': 0.5,
            'xanchor': 'center'
        },
        'font': {'size': 14, 'family': 'Inter, sans-serif'},
        'height': height,
        'margin': {'t': 60, 'b': 60, 'l': 60, 'r': 40},
        'legend': {
            'font': {'size': 13},
            'orientation': 'h',
            'yanchor': 'bottom',
            'y': -0.2,
            'xanchor': 'center',
            'x': 0.5
        },
        'xaxis': {
            'tickfont': {'size': 12},
            'titlefont': {'size': 14}
        },
        'yaxis': {
            'tickfont': {'size': 12},
            'titlefont': {'size': 14}
        }
    }

@st.cache_data(ttl=60)
def cargar_datos_adquisiciones():
    """Carga datos de adquisiciones desde la base de datos"""
    return obtener_adquisiciones_df()

@st.dialog("Detalle de Adquisición", width="large")
def mostrar_detalle_adquisicion(codigo_adquisicion):
    """Modal para mostrar el detalle completo de una adquisición con timeline"""
    db = DirectSessionLocal()
    try:
        detalle_completo = obtener_detalle_adquisicion(db, codigo_adquisicion)

        if not detalle_completo:
            st.error("No se encontró la adquisición")
            return

        adq = detalle_completo['adquisicion']
        detalle = detalle_completo['detalle']
        procesos = detalle_completo['procesos']

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader(f"{codigo_adquisicion}")
            st.write(f"**{adq.descripcion}**")

        with col2:
            if detalle:
                st.metric("PIM Asignado", f"S/ {detalle.pim_asignado:,.0f}")

        col_a, col_b, col_c, col_d = st.columns(4)

        with col_a:
            if detalle:
                st.metric("Entregables", f"{detalle.requerimientos_adquiridos}/{detalle.requerimientos_total}")

        with col_b:
            st.metric("Estado", adq.estado)

        with col_c:
            st.metric("Monto Referencial", f"S/ {adq.monto_referencial:,.0f}")

        with col_d:
            st.metric("Monto Adjudicado", f"S/ {adq.monto_adjudicado:,.0f}")

        if detalle:
            st.info(f"**Unidad Responsable:** {detalle.unidad_responsable} | **Tipo:** {detalle.tipo_servicio}")

        st.divider()

        if procesos:
            # Header con toggle de expandir
            col_title, col_expand = st.columns([4, 1])
            with col_title:
                st.subheader("Timeline del Proceso")
            with col_expand:
                expand_timeline = st.toggle("Ampliar", key="toggle_expand_timeline", help="Expandir gráfico")

            df_procesos = pd.DataFrame([{
                'Orden': p.orden,
                'Hito': p.hito,
                'Area': p.tipo_flujo,
                'Fecha_Inicio': p.fecha_inicio,
                'Fecha_Fin': p.fecha_fin if p.fecha_fin else p.fecha_inicio,
                'Dias': p.dias_transcurridos,
                'Responsable': p.responsable_correo
            } for p in procesos])

            # Configuración según si está expandido o no
            if expand_timeline:
                chart_height = 650
                title_size = 22
                font_size = 15
                tick_size = 14
                axis_title_size = 16
                legend_size = 14
                text_size = 13
            else:
                chart_height = 420
                title_size = 18
                font_size = 13
                tick_size = 12
                axis_title_size = 14
                legend_size = 12
                text_size = 11

            fig_timeline = px.timeline(
                df_procesos,
                x_start='Fecha_Inicio',
                x_end='Fecha_Fin',
                y='Hito',
                color='Area',
                hover_data=['Dias', 'Responsable'],
                color_discrete_map={'OTIN': '#FFB84D', 'OTA': '#90EE90'}
            )

            fig_timeline.update_layout(
                title={
                    'text': 'Flujo de Proceso de Adquisición',
                    'font': {'size': title_size, 'color': '#1f2937', 'family': 'Inter, sans-serif'},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                font={'size': font_size, 'family': 'Inter, sans-serif'},
                height=chart_height,
                margin={'t': 60, 'b': 100, 'l': 30, 'r': 30},
                yaxis={
                    'categoryorder': 'array',
                    'categoryarray': df_procesos['Hito'].tolist()[::-1],
                    'tickfont': {'size': tick_size}
                },
                xaxis={
                    'title': {'text': 'Fecha', 'font': {'size': axis_title_size}},
                    'tickfont': {'size': tick_size - 1}
                },
                legend={
                    'font': {'size': legend_size},
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': -0.18,
                    'xanchor': 'center',
                    'x': 0.5
                },
                showlegend=True
            )

            # Actualizar tamaño de texto en las barras del timeline
            fig_timeline.update_traces(
                textfont_size=text_size
            )

            # Configuración para la barra de herramientas de Plotly
            modal_chart_config = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': 'timeline_proceso',
                    'height': 800,
                    'width': 1400,
                    'scale': 2
                }
            }

            st.plotly_chart(fig_timeline, use_container_width=True, config=modal_chart_config)

            total_dias = sum(p.dias_transcurridos for p in procesos)
            st.metric("**Total de Días del Proceso**", f"{total_dias} días")

            st.divider()
            st.subheader("Detalle de Pasos del Proceso")

            df_procesos_tabla = pd.DataFrame([{
                'Orden': p.orden,
                'Hito': p.hito,
                'Área': p.tipo_flujo,
                'Días': p.dias_transcurridos,
                'Fecha Inicio': p.fecha_inicio.strftime('%d/%m/%Y') if p.fecha_inicio else '',
                'Responsable': p.responsable_correo if p.responsable_correo else '',
                'Comentarios': p.comentarios if p.comentarios else ''
            } for p in procesos])

            st.dataframe(df_procesos_tabla, use_container_width=True, hide_index=True)

        else:
            st.info("No hay información de proceso disponible para esta adquisición")

    finally:
        db.close()

# Cargar datos
df_adquisiciones = cargar_datos_adquisiciones()

# Verificar si hay un código de adquisición en la URL (query param)
query_params = st.query_params
codigo_adq_url = query_params.get("adq", None)

# Si hay un código en la URL, mostrar el modal automáticamente
if codigo_adq_url:
    mostrar_detalle_adquisicion(codigo_adq_url)

# ============================================================
# FILTROS EN LA PARTE SUPERIOR
# ============================================================

# Inicializar variables de filtros
año_seleccionado = "Todos"
meta_seleccionada = []
ue_seleccionada = []
tipo_servicio_seleccionado = []
estado_seleccionado = []

if len(df_adquisiciones) == 0:
    st.warning("⚠️ No hay datos cargados. Por favor, importe un archivo de programación en la pestaña 'Importar/Exportar'")
else:
    # Contenedor de filtros usando expander de Streamlit
    with st.expander("🔍 **Filtros de Búsqueda**", expanded=True):
        # Primera fila de filtros
        col_f1, col_f2, col_f3 = st.columns([1, 2, 2])

        with col_f1:
            años_disponibles = sorted(df_adquisiciones['Año'].unique())
            opciones_año = ["Todos"] + list(años_disponibles)
            indice_default = opciones_año.index(2025) if 2025 in años_disponibles else 0
            año_seleccionado = st.selectbox(
                "Año",
                options=opciones_año,
                index=indice_default,
                key="filtro_año"
            )

        with col_f2:
            ues_disponibles = sorted(df_adquisiciones['UE'].unique())
            ue_seleccionada = st.multiselect(
                "DDNNTT (Unidad Ejecutora)",
                options=ues_disponibles,
                default=ues_disponibles,
                key="filtro_ue"
            )

        with col_f3:
            metas_disponibles = sorted(df_adquisiciones['Meta'].unique())
            meta_seleccionada = st.multiselect(
                "Meta Presupuestal",
                options=metas_disponibles,
                default=metas_disponibles[:5] if len(metas_disponibles) > 5 else metas_disponibles,
                key="filtro_meta"
            )

        # Segunda fila de filtros
        col_f4, col_f5 = st.columns(2)

        with col_f4:
            tipos_permitidos = ['BIEN', 'SERVICIO']
            tipos_en_datos = [t for t in tipos_permitidos if t in df_adquisiciones['Tipo_Servicio'].values]
            tipo_servicio_seleccionado = st.multiselect(
                "Tipo (Bien/Servicio)",
                options=tipos_permitidos,
                default=tipos_en_datos,
                key="filtro_tipo"
            )

        with col_f5:
            estados_permitidos = ['EN PROCESO', 'CULMINADO', 'CANCELADO', 'HISTORICO', 'NO INICIADO']
            estados_en_datos = [e for e in estados_permitidos if e in df_adquisiciones['Estado'].values]
            estado_seleccionado = st.multiselect(
                "Estado",
                options=estados_permitidos,
                default=estados_en_datos,
                key="filtro_estado"
            )

# ============================================================
# TABS PRINCIPALES
# ============================================================

tabs = st.tabs([
    "🛒 Adquisiciones",
    "📤 Importar/Exportar",
])

with tabs[0]:
    if len(df_adquisiciones) == 0:
        st.info("⚠️ No hay datos de adquisiciones disponibles")
    else:
        df_adq_filtrado = df_adquisiciones.copy()

        if año_seleccionado != "Todos":
            df_adq_filtrado = df_adq_filtrado[df_adq_filtrado['Año'] == año_seleccionado]

        if ue_seleccionada:
            df_adq_filtrado = df_adq_filtrado[df_adq_filtrado['UE'].isin(ue_seleccionada)]

        if meta_seleccionada:
            df_adq_filtrado = df_adq_filtrado[df_adq_filtrado['Meta'].isin(meta_seleccionada)]

        if tipo_servicio_seleccionado:
            df_adq_filtrado = df_adq_filtrado[df_adq_filtrado['Tipo_Servicio'].isin(tipo_servicio_seleccionado)]

        if estado_seleccionado:
            df_adq_filtrado = df_adq_filtrado[df_adq_filtrado['Estado'].isin(estado_seleccionado)]

        # ============================================================
        # RESUMEN EJECUTIVO
        # ============================================================
        st.subheader("Resumen Ejecutivo")

        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            total_adquisiciones = len(df_adq_filtrado)
            render_metric_inei("Total<br>Requerimientos", f"{total_adquisiciones:,}")

        with col2:
            total_culminados = len(df_adq_filtrado[df_adq_filtrado['Estado'] == 'CULMINADO'])
            render_metric_inei("Total Adquiridos<br>(Culminados)", f"{total_culminados:,}")

        with col3:
            total_referencial = df_adq_filtrado['Monto_Referencial'].sum()
            render_metric_inei("Monto Total<br>(PIM)", f"S/ {total_referencial:,.2f}")

        with col4:
            monto_culminados = df_adq_filtrado[df_adq_filtrado['Estado'] == 'CULMINADO']['Monto_Adjudicado'].sum()
            render_metric_inei("Monto Adquiridos<br>(Culminados)", f"S/ {monto_culminados:,.2f}")

        with col5:
            pct_avance = (monto_culminados / total_referencial * 100) if total_referencial > 0 else 0
            render_metric_inei("% Avance<br>(Adqui. / PIM)", f"{pct_avance:.1f}%")

        st.markdown("---")

        # ============================================================
        # GRÁFICOS
        # ============================================================
        col1, col2 = st.columns(2)

        with col1:
            # Gráfico de Distribución por Estado
            adq_por_estado = df_adq_filtrado.groupby('Estado').size().reset_index(name='Cantidad')

            fig_estado = px.pie(
                adq_por_estado,
                values='Cantidad',
                names='Estado'
            )
            fig_estado.update_layout(
                title={
                    'text': 'Distribución por Estado',
                    'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter, sans-serif'},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                font={'size': 14, 'family': 'Inter, sans-serif'},
                height=450,
                margin={'t': 60, 'b': 60, 'l': 40, 'r': 40},
                legend={
                    'font': {'size': 13},
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': -0.15,
                    'xanchor': 'center',
                    'x': 0.5
                }
            )
            fig_estado.update_traces(
                textposition='inside',
                textinfo='percent+label',
                textfont_size=13
            )
            st.plotly_chart(fig_estado, use_container_width=True, config=CHART_CONFIG)

        with col2:
            # Gráfico de Montos por DDNNTT
            montos_por_ue = df_adq_filtrado.groupby('UE').agg({
                'Monto_Referencial': 'sum',
                'Monto_Adjudicado': 'sum'
            }).reset_index()

            fig_montos = go.Figure()

            fig_montos.add_trace(go.Bar(
                name='PIM',
                x=montos_por_ue['UE'],
                y=montos_por_ue['Monto_Referencial'],
                marker_color='#f87171',
                texttemplate='%{y:,.0f}',
                textposition='outside',
                textfont_size=11
            ))

            fig_montos.add_trace(go.Bar(
                name='Monto Adquiridos',
                x=montos_por_ue['UE'],
                y=montos_por_ue['Monto_Adjudicado'],
                marker_color='#991b1b',
                texttemplate='%{y:,.0f}',
                textposition='outside',
                textfont_size=11
            ))

            fig_montos.update_layout(
                title={
                    'text': 'Montos por DDNNTT',
                    'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter, sans-serif'},
                    'x': 0.5,
                    'xanchor': 'center'
                },
                font={'size': 14, 'family': 'Inter, sans-serif'},
                xaxis={
                    'title': {'text': 'DDNNTT', 'font': {'size': 14}},
                    'tickfont': {'size': 12}
                },
                yaxis={
                    'title': {'text': 'Monto (S/)', 'font': {'size': 14}},
                    'tickfont': {'size': 12}
                },
                barmode='group',
                height=450,
                margin={'t': 60, 'b': 60, 'l': 80, 'r': 40},
                legend={
                    'font': {'size': 13},
                    'orientation': 'h',
                    'yanchor': 'bottom',
                    'y': -0.2,
                    'xanchor': 'center',
                    'x': 0.5
                }
            )

            st.plotly_chart(fig_montos, use_container_width=True, config=CHART_CONFIG)

        st.markdown("---")

        col3, col4 = st.columns(2)

        with col3:
            # Gráfico de Certificado por Mes
            meses_español = {
                1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
                5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
                9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
            }

            df_con_fecha = df_adq_filtrado[df_adq_filtrado['Fecha_Adjudicacion'].notna()].copy()

            if len(df_con_fecha) > 0:
                df_con_fecha['Mes'] = pd.to_datetime(df_con_fecha['Fecha_Adjudicacion']).dt.month
                df_con_fecha['Mes_Nombre'] = df_con_fecha['Mes'].map(meses_español)

                gastos_por_mes = df_con_fecha.groupby(['Mes', 'Mes_Nombre'])['Monto_Adjudicado'].sum().reset_index()
                gastos_por_mes = gastos_por_mes.sort_values('Mes')

                fig_meses = px.bar(
                    gastos_por_mes,
                    x='Mes_Nombre',
                    y='Monto_Adjudicado',
                    text='Monto_Adjudicado'
                )
                fig_meses.update_traces(
                    marker_color='#3b82f6',
                    texttemplate='S/ %{text:,.0f}',
                    textposition='outside',
                    textfont_size=11
                )
                fig_meses.update_layout(
                    title={
                        'text': 'Certificado por Mes',
                        'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter, sans-serif'},
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    font={'size': 14, 'family': 'Inter, sans-serif'},
                    xaxis={
                        'title': {'text': 'Mes', 'font': {'size': 14}},
                        'tickfont': {'size': 11}
                    },
                    yaxis={
                        'title': {'text': 'Monto Adquirido (S/)', 'font': {'size': 14}},
                        'tickfont': {'size': 12}
                    },
                    height=450,
                    margin={'t': 60, 'b': 60, 'l': 80, 'r': 40},
                    showlegend=False
                )
                st.plotly_chart(fig_meses, use_container_width=True, config=CHART_CONFIG)
            else:
                st.info("No hay adquisiciones con fecha de adjudicación para mostrar")

        with col4:
            # Gráfico de % Avance por DDNNTT
            avance_por_ue = df_adq_filtrado.groupby('UE').agg({
                'Monto_Referencial': 'sum',
                'Monto_Adjudicado': 'sum'
            }).reset_index()
            avance_por_ue['Avance_%'] = (avance_por_ue['Monto_Adjudicado'] / avance_por_ue['Monto_Referencial'] * 100).round(1)
            avance_por_ue = avance_por_ue.sort_values('Avance_%', ascending=True)

            if len(avance_por_ue) > 0:
                fig_avance = px.bar(
                    avance_por_ue,
                    x='Avance_%',
                    y='UE',
                    orientation='h',
                    text='Avance_%'
                )
                fig_avance.update_traces(
                    marker_color='#1e40af',
                    texttemplate='%{text:.1f}%',
                    textposition='outside',
                    textfont_size=12
                )
                fig_avance.update_layout(
                    title={
                        'text': '% Avance por DDNNTT',
                        'font': {'size': 18, 'color': '#1f2937', 'family': 'Inter, sans-serif'},
                        'x': 0.5,
                        'xanchor': 'center'
                    },
                    font={'size': 14, 'family': 'Inter, sans-serif'},
                    xaxis={
                        'title': {'text': '% Avance', 'font': {'size': 14}},
                        'tickfont': {'size': 12},
                        'range': [0, max(avance_por_ue['Avance_%'].max() * 1.15, 100)]
                    },
                    yaxis={
                        'title': {'text': 'Unidad Ejecutora', 'font': {'size': 14}},
                        'tickfont': {'size': 12}
                    },
                    height=450,
                    margin={'t': 60, 'b': 60, 'l': 100, 'r': 60},
                    showlegend=False
                )
                st.plotly_chart(fig_avance, use_container_width=True, config=CHART_CONFIG)
            else:
                st.info("No hay datos suficientes para mostrar avance por UE")

        st.markdown("---")

        # ============================================================
        # TABLA DETALLADA
        # ============================================================
        st.subheader("Tabla Detallada de Adquisiciones")

        col_busq, col_sel = st.columns([2, 3])

        with col_busq:
            busqueda_adq = st.text_input("🔎 Buscar en descripción:", "")

        with col_sel:
            adquisiciones_disponibles = df_adq_filtrado['Descripción'].unique().tolist()
            adquisiciones_seleccionadas = st.multiselect(
                "Filtrar por Adquisición:",
                options=adquisiciones_disponibles,
                default=[],
                placeholder="Seleccionar adquisiciones..."
            )

        df_adq_tabla = df_adq_filtrado.copy()

        if adquisiciones_seleccionadas:
            df_adq_tabla = df_adq_tabla[df_adq_tabla['Descripción'].isin(adquisiciones_seleccionadas)]

        if busqueda_adq:
            df_adq_tabla = df_adq_tabla[
                df_adq_tabla['Descripción'].str.contains(busqueda_adq, case=False, na=False) |
                df_adq_tabla['Proveedor'].str.contains(busqueda_adq, case=False, na=False)
            ]

        df_adq_display = df_adq_tabla[['Año', 'UE', 'Meta', 'Código', 'Descripción', 'Tipo_Servicio', 'Cantidad','Tipo_Proceso', 'Estado', 'Monto_Referencial', 'Monto_Adjudicado', 'Proveedor', 'Avance_%']].copy()
        df_adq_display['Monto_Referencial'] = df_adq_display['Monto_Referencial'].apply(lambda x: f"S/ {x:,.0f}")
        df_adq_display['Monto_Adjudicado'] = df_adq_display['Monto_Adjudicado'].apply(lambda x: f"S/ {x:,.0f}")

        seleccion = st.dataframe(
            df_adq_display,
            use_container_width=True,
            hide_index=True,
            height=400,
            on_select="rerun",
            selection_mode="single-row",
            key="tabla_adquisiciones"
        )

        if seleccion and seleccion.selection and seleccion.selection.rows:
            fila_seleccionada = seleccion.selection.rows[0]
            codigo_seleccionado_tabla = df_adq_display.iloc[fila_seleccionada]['Código']
            mostrar_detalle_adquisicion(codigo_seleccionado_tabla)

        st.caption(f"Mostrando {len(df_adq_tabla)} de {len(df_adquisiciones)} adquisiciones totales")

# ============================================================
# TAB IMPORTAR/EXPORTAR
# ============================================================
with tabs[1]:
    st.header("Importar y Exportar Datos")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Importar Programación Anual")

        año_importacion = st.number_input(
            "Año de la programación",
            min_value=2020,
            max_value=2030,
            value=2024,
            step=1
        )

        st.info("""
        **Formato requerido:**

        - Archivo Excel (.xlsx) con estructura de Programación Anual
        - Columnas: PIM, CERTIFICADO, PIM POR CERTIFICAR, TOTAL ANUAL, etc.
        - El archivo debe incluir las Unidades Ejecutoras y Metas
        """)

        archivo_carga = st.file_uploader(
            "Cargar archivo Excel de Programación Anual",
            type=['xlsx'],
            key="file_uploader"
        )

        if archivo_carga and st.button("Importar Datos"):
            with st.spinner("Procesando archivo..."):
                db = SessionLocal()
                try:
                    exito, mensaje = procesar_archivo_programacion(db, archivo_carga, año_importacion)

                    if exito:
                        st.success(f"✅ {mensaje}")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"❌ {mensaje}")
                finally:
                    db.close()

    with col2:
        st.subheader("Exportar Reportes")

        formato_exportacion = st.selectbox(
            "Formato de exportación",
            ["Excel", "PDF"]
        )

        if st.button("Generar Reporte"):
            if formato_exportacion == "Excel":
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    if len(df_adquisiciones) > 0:
                        df_adquisiciones.to_excel(writer, sheet_name='Adquisiciones', index=False)

                output.seek(0)
                st.download_button(
                    label="⬇️ Descargar Reporte Excel",
                    data=output,
                    file_name=f"adquisiciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )

            elif formato_exportacion == "PDF":
                buffer = io.BytesIO()
                doc = SimpleDocTemplate(buffer, pagesize=A4)
                story = []
                styles = getSampleStyleSheet()

                story.append(Paragraph("Reporte de Adquisiciones", styles['Title']))
                story.append(Spacer(1, 0.3*inch))
                story.append(Paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
                story.append(Spacer(1, 0.2*inch))

                story.append(Paragraph("Resumen Ejecutivo", styles['Heading1']))
                data_resumen = [
                    ['Métrica', 'Valor'],
                    ['Total Adquisiciones', f"{len(df_adquisiciones):,}"],
                    ['Monto Referencial Total', f"S/ {df_adquisiciones['Monto_Referencial'].sum():,.0f}"],
                    ['Monto Adjudicado Total', f"S/ {df_adquisiciones['Monto_Adjudicado'].sum():,.0f}"],
                ]

                tabla_resumen = Table(data_resumen)
                tabla_resumen.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                story.append(tabla_resumen)

                doc.build(story)
                buffer.seek(0)

                st.download_button(
                    label="⬇️ Descargar Reporte PDF",
                    data=buffer,
                    file_name=f"adquisiciones_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf"
                )

# Footer
render_footer()
