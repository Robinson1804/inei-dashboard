"""
Script para crear una plantilla de Excel para importar datos de adquisiciones
al Dashboard de Adquisiciones
"""

import pandas as pd
import xlsxwriter
from datetime import datetime, timedelta

def crear_plantilla_excel(nombre_archivo='Plantilla_Adquisiciones.xlsx'):
    """Crea una plantilla de Excel con estructura y ejemplos para importar adquisiciones"""

    # Crear el archivo Excel
    workbook = xlsxwriter.Workbook(nombre_archivo)

    # ========== FORMATOS ==========
    # Formato para encabezados
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'align': 'center',
        'fg_color': '#1f4e78',
        'font_color': 'white',
        'border': 1
    })

    # Formato para texto
    text_format = workbook.add_format({
        'text_wrap': True,
        'valign': 'vcenter',
        'border': 1
    })

    # Formato para números
    number_format = workbook.add_format({
        'num_format': '#,##0.00',
        'valign': 'vcenter',
        'border': 1
    })

    # Formato para fechas
    date_format = workbook.add_format({
        'num_format': 'dd/mm/yyyy',
        'valign': 'vcenter',
        'border': 1
    })

    # Formato para instrucciones
    instruction_format = workbook.add_format({
        'text_wrap': True,
        'valign': 'top'
    })

    title_format = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'fg_color': '#1f4e78',
        'font_color': 'white'
    })

    # ========== HOJA 1: INSTRUCCIONES ==========
    ws_instrucciones = workbook.add_worksheet('Instrucciones')
    ws_instrucciones.set_column('A:A', 80)

    row = 0
    ws_instrucciones.write(row, 0, 'PLANTILLA DE IMPORTACIÓN DE ADQUISICIONES', title_format)
    row += 2

    instrucciones = [
        ['DESCRIPCIÓN GENERAL', ''],
        ['Esta plantilla permite importar datos de adquisiciones al Dashboard de Adquisiciones.', ''],
        ['Complete la hoja "Adquisiciones" con los datos de sus procesos de adquisición.', ''],
        ['', ''],
        ['HOJAS INCLUIDAS', ''],
        ['1. Instrucciones: Esta hoja con información de uso', ''],
        ['2. Adquisiciones: Hoja principal para completar con datos de adquisiciones', ''],
        ['3. Detalle_Adquisicion (Opcional): Información adicional de cada adquisición', ''],
        ['4. Proceso_Timeline (Opcional): Hitos y pasos del proceso de cada adquisición', ''],
        ['5. Valores_Permitidos: Lista de valores válidos para cada campo', ''],
        ['', ''],
        ['CAMPOS OBLIGATORIOS', ''],
        ['- Anio: Anio de la adquisicion (formato: 2024, 2025, etc.)', ''],
        ['- UE: Codigo de la Unidad Ejecutora / DDNNTT (ej: CIDE, DNCE, DNCN)', ''],
        ['- Meta: Descripcion de la Meta Presupuestal', ''],
        ['- Descripcion: Descripcion completa del bien o servicio a adquirir', ''],
        ['- Estado: Estado actual de la adquisicion', ''],
        ['- Monto_Referencial: Presupuesto asignado (PIM) en Soles', ''],
        ['', ''],
        ['CAMPOS OPCIONALES', ''],
        ['- Codigo: Codigo unico de la adquisicion (si no se proporciona, se generara automaticamente)', ''],
        ['- Cantidad: Cantidad de unidades a adquirir (default: 1)', ''],
        ['- Tipo_Servicio: BIEN o SERVICIO', ''],
        ['- Tipo_Proceso: Tipo de proceso (ej: Adjudicacion Simplificada, Licitacion Publica)', ''],
        ['- Monto_Adjudicado: Monto adjudicado o ejecutado en Soles', ''],
        ['- Proveedor: Nombre del proveedor adjudicado', ''],
        ['- Fecha_Convocatoria: Fecha de convocatoria del proceso', ''],
        ['- Fecha_Adjudicacion: Fecha de adjudicacion o certificacion', ''],
        ['', ''],
        ['VALORES PERMITIDOS PARA CAMPOS ESPECIFICOS', ''],
        ['Estado: EN PROCESO | CULMINADO | CANCELADO | HISTORICO | NO INICIADO', ''],
        ['Tipo_Servicio: BIEN | SERVICIO', ''],
        ['', ''],
        ['FORMATO DE FECHAS', ''],
        ['Las fechas deben estar en formato DD/MM/YYYY (ej: 15/03/2024)', ''],
        ['', ''],
        ['FORMATO NUMERICO', ''],
        ['Los montos deben ser numeros sin simbolos (ej: 150000.00 en lugar de S/ 150,000.00)', ''],
        ['', ''],
        ['NOTAS IMPORTANTES', ''],
        ['IMPORTANTE: No modifique los nombres de las columnas en la hoja "Adquisiciones"', ''],
        ['IMPORTANTE: Asegurese de que las Unidades Ejecutoras (UE) y Metas existan en el sistema', ''],
        ['IMPORTANTE: El campo Avance_% se calculara automaticamente', ''],
        ['IMPORTANTE: Las hojas "Detalle_Adquisicion" y "Proceso_Timeline" son opcionales pero enriquecen la informacion', ''],
    ]

    for inst in instrucciones:
        ws_instrucciones.write(row, 0, inst[0], instruction_format)
        row += 1

    # ========== HOJA 2: ADQUISICIONES (Principal) ==========
    ws_adquisiciones = workbook.add_worksheet('Adquisiciones')

    # Definir columnas
    columnas = [
        ('Año', 8),
        ('UE', 8),
        ('Meta', 40),
        ('Código', 15),
        ('Descripción', 50),
        ('Tipo_Servicio', 12),
        ('Cantidad', 10),
        ('Tipo_Proceso', 25),
        ('Estado', 15),
        ('Monto_Referencial', 18),
        ('Monto_Adjudicado', 18),
        ('Proveedor', 30),
        ('Fecha_Convocatoria', 18),
        ('Fecha_Adjudicacion', 18)
    ]

    # Escribir encabezados y configurar anchos
    for col, (nombre, ancho) in enumerate(columnas):
        ws_adquisiciones.write(0, col, nombre, header_format)
        ws_adquisiciones.set_column(col, col, ancho)

    # Datos de ejemplo
    ejemplos = [
        [
            2025,
            'CIDE',
            '0001 - Administración y Planeamiento',
            'ADQ-2025-001',
            'Adquisición de equipos de cómputo para personal técnico',
            'BIEN',
            25,
            'Adjudicación Simplificada',
            'EN PROCESO',
            125000.00,
            0.00,
            '',
            datetime(2025, 2, 15),
            None
        ],
        [
            2025,
            'DNCE',
            '0002 - Censos y Encuestas',
            'ADQ-2025-002',
            'Servicio de impresión de cuestionarios para encuesta nacional',
            'SERVICIO',
            500000,
            'Licitación Pública',
            'CULMINADO',
            450000.00,
            420000.00,
            'Imprenta Nacional S.A.',
            datetime(2025, 1, 10),
            datetime(2025, 3, 15)
        ],
        [
            2025,
            'DNCN',
            '0003 - Cuentas Nacionales',
            'ADQ-2025-003',
            'Licencias de software estadístico especializado',
            'SERVICIO',
            50,
            'Comparación de Precios',
            'CULMINADO',
            85000.00,
            82000.00,
            'Software Analytics Peru',
            datetime(2025, 1, 5),
            datetime(2025, 2, 20)
        ],
        [
            2025,
            'CIDE',
            '0001 - Administración y Planeamiento',
            'ADQ-2025-004',
            'Servicio de mantenimiento de infraestructura informática',
            'SERVICIO',
            12,
            'Adjudicación Simplificada',
            'NO INICIADO',
            180000.00,
            0.00,
            '',
            None,
            None
        ],
        [
            2024,
            'DNCE',
            '0002 - Censos y Encuestas',
            'ADQ-2024-005',
            'Tablets para trabajo de campo en zonas rurales',
            'BIEN',
            350,
            'Licitación Pública',
            'HISTORICO',
            1250000.00,
            1180000.00,
            'Tecnología Móvil S.A.C.',
            datetime(2024, 8, 1),
            datetime(2024, 11, 15)
        ]
    ]

    # Escribir ejemplos
    for row_num, ejemplo in enumerate(ejemplos, start=1):
        for col_num, valor in enumerate(ejemplo):
            if isinstance(valor, datetime):
                ws_adquisiciones.write_datetime(row_num, col_num, valor, date_format)
            elif isinstance(valor, (int, float)) and col_num in [9, 10]:  # Columnas de monto
                ws_adquisiciones.write_number(row_num, col_num, valor, number_format)
            elif valor is None or valor == '':
                ws_adquisiciones.write_blank(row_num, col_num, '', text_format)
            else:
                ws_adquisiciones.write(row_num, col_num, valor, text_format)

    # ========== HOJA 3: DETALLE_ADQUISICION (Opcional) ==========
    ws_detalle = workbook.add_worksheet('Detalle_Adquisicion')

    columnas_detalle = [
        ('Código_Adquisicion', 15),
        ('PIM_Asignado', 18),
        ('Requerimientos_Total', 18),
        ('Requerimientos_Adquiridos', 22),
        ('Unidad_Responsable', 30),
        ('Observaciones', 50)
    ]

    for col, (nombre, ancho) in enumerate(columnas_detalle):
        ws_detalle.write(0, col, nombre, header_format)
        ws_detalle.set_column(col, col, ancho)

    ejemplos_detalle = [
        ['ADQ-2025-001', 125000.00, 1, 0, 'Oficina de Tecnologías de la Información', 'Proceso en evaluación técnica'],
        ['ADQ-2025-002', 450000.00, 5, 5, 'Dirección Nacional de Censos y Encuestas', 'Proceso culminado exitosamente'],
        ['ADQ-2025-003', 85000.00, 1, 1, 'Dirección de Cuentas Nacionales', 'Licencias instaladas y operativas'],
    ]

    for row_num, ejemplo in enumerate(ejemplos_detalle, start=1):
        for col_num, valor in enumerate(ejemplo):
            if isinstance(valor, (int, float)) and col_num in [1]:
                ws_detalle.write_number(row_num, col_num, valor, number_format)
            else:
                ws_detalle.write(row_num, col_num, valor, text_format)

    # ========== HOJA 4: PROCESO_TIMELINE (Opcional) ==========
    ws_proceso = workbook.add_worksheet('Proceso_Timeline')

    columnas_proceso = [
        ('Código_Adquisicion', 15),
        ('Orden', 8),
        ('Hito', 40),
        ('Tipo_Flujo', 12),
        ('Responsable_Area', 25),
        ('Responsable_Correo', 30),
        ('Fecha_Inicio', 15),
        ('Fecha_Fin', 15),
        ('Dias_Transcurridos', 18),
        ('Comentarios', 40)
    ]

    for col, (nombre, ancho) in enumerate(columnas_proceso):
        ws_proceso.write(0, col, nombre, header_format)
        ws_proceso.set_column(col, col, ancho)

    ejemplos_proceso = [
        ['ADQ-2025-002', 1, 'Elaboración de TDR', 'OTIN', 'Unidad Solicitante', 'usuario@inei.gob.pe', datetime(2025, 1, 10), datetime(2025, 1, 17), 7, 'TDR aprobados'],
        ['ADQ-2025-002', 2, 'Revisión Legal', 'OTA', 'Oficina Técnica de Administración', 'ota@inei.gob.pe', datetime(2025, 1, 18), datetime(2025, 1, 25), 7, 'Conformidad legal'],
        ['ADQ-2025-002', 3, 'Publicación en SEACE', 'OTA', 'Oficina Técnica de Administración', 'ota@inei.gob.pe', datetime(2025, 1, 26), datetime(2025, 2, 5), 10, 'Convocatoria publicada'],
        ['ADQ-2025-002', 4, 'Recepción de Ofertas', 'OTA', 'Comité de Selección', 'comite@inei.gob.pe', datetime(2025, 2, 6), datetime(2025, 2, 25), 19, '5 ofertas recibidas'],
        ['ADQ-2025-002', 5, 'Evaluación Técnica', 'OTIN', 'Comité Técnico', 'tecnico@inei.gob.pe', datetime(2025, 2, 26), datetime(2025, 3, 5), 7, 'Evaluación completada'],
        ['ADQ-2025-002', 6, 'Adjudicación', 'OTA', 'Oficina Técnica de Administración', 'ota@inei.gob.pe', datetime(2025, 3, 6), datetime(2025, 3, 15), 9, 'Adjudicado'],
    ]

    for row_num, ejemplo in enumerate(ejemplos_proceso, start=1):
        for col_num, valor in enumerate(ejemplo):
            if isinstance(valor, datetime):
                ws_proceso.write_datetime(row_num, col_num, valor, date_format)
            elif isinstance(valor, int) and col_num in [1, 8]:
                ws_proceso.write_number(row_num, col_num, valor, text_format)
            else:
                ws_proceso.write(row_num, col_num, valor, text_format)

    # ========== HOJA 5: VALORES PERMITIDOS ==========
    ws_valores = workbook.add_worksheet('Valores_Permitidos')
    ws_valores.set_column('A:A', 20)
    ws_valores.set_column('B:B', 50)

    ws_valores.write(0, 0, 'Campo', header_format)
    ws_valores.write(0, 1, 'Valores Permitidos', header_format)

    valores_permitidos = [
        ['Estado', 'EN PROCESO, CULMINADO, CANCELADO, HISTORICO, NO INICIADO'],
        ['Tipo_Servicio', 'BIEN, SERVICIO'],
        ['Tipo_Flujo', 'OTIN, OTA'],
        ['UE (ejemplos)', 'CIDE, DNCE, DNCN, DNPD, DNIA'],
    ]

    for row_num, (campo, valores) in enumerate(valores_permitidos, start=1):
        ws_valores.write(row_num, 0, campo, text_format)
        ws_valores.write(row_num, 1, valores, text_format)

    # Cerrar el archivo
    workbook.close()

    print(f"[OK] Plantilla creada exitosamente: {nombre_archivo}")
    print(f"\nEstructura de la plantilla:")
    print(f"  Hoja 1: Instrucciones - Guia completa de uso")
    print(f"  Hoja 2: Adquisiciones - Datos principales (OBLIGATORIO)")
    print(f"  Hoja 3: Detalle_Adquisicion - Informacion adicional (OPCIONAL)")
    print(f"  Hoja 4: Proceso_Timeline - Hitos del proceso (OPCIONAL)")
    print(f"  Hoja 5: Valores_Permitidos - Referencia de valores validos")
    print(f"\nLa plantilla incluye {len(ejemplos)} ejemplos de adquisiciones para guiarlo")

if __name__ == "__main__":
    crear_plantilla_excel()
