"""
Script para crear una plantilla SIMPLE de Excel de UNA SOLA HOJA
para importar datos de adquisiciones al Dashboard
"""

import pandas as pd
import xlsxwriter
from datetime import datetime

def crear_plantilla_simple(nombre_archivo='Plantilla_Adquisiciones_Simple.xlsx'):
    """Crea una plantilla simple de una sola hoja con todas las columnas necesarias"""

    # Crear el archivo Excel
    workbook = xlsxwriter.Workbook(nombre_archivo)
    worksheet = workbook.add_worksheet('Adquisiciones')

    # ========== FORMATOS ==========
    # Formato para encabezados principales
    header_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'align': 'center',
        'fg_color': '#1f4e78',
        'font_color': 'white',
        'border': 1,
        'font_size': 11
    })

    # Formato para encabezados obligatorios (rojo)
    header_obligatorio_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'align': 'center',
        'fg_color': '#c00000',
        'font_color': 'white',
        'border': 1,
        'font_size': 11
    })

    # Formato para encabezados opcionales (azul claro)
    header_opcional_format = workbook.add_format({
        'bold': True,
        'text_wrap': True,
        'valign': 'vcenter',
        'align': 'center',
        'fg_color': '#4472c4',
        'font_color': 'white',
        'border': 1,
        'font_size': 11
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
        'valign': 'top',
        'bold': True,
        'font_size': 10,
        'fg_color': '#fff2cc'
    })

    # ========== INSTRUCCIONES EN LAS PRIMERAS FILAS ==========
    worksheet.set_row(0, 30)
    worksheet.merge_range('A1:T1',
        'PLANTILLA DE ADQUISICIONES - Complete las filas debajo con sus datos. Las columnas en ROJO son OBLIGATORIAS. Puede eliminar los ejemplos.',
        instruction_format)

    worksheet.set_row(1, 20)
    worksheet.merge_range('A2:F2', 'VALORES PERMITIDOS: Estado: EN PROCESO | CULMINADO | CANCELADO | HISTORICO | NO INICIADO', instruction_format)
    worksheet.merge_range('G2:J2', 'Tipo_Servicio: BIEN | SERVICIO', instruction_format)
    worksheet.merge_range('K2:N2', 'Fechas: DD/MM/YYYY', instruction_format)
    worksheet.merge_range('O2:T2', 'Montos: Numeros sin simbolos (ej: 150000.00)', instruction_format)

    # ========== DEFINIR COLUMNAS ==========
    # Estructura: (nombre, ancho, obligatorio, formato_encabezado)
    columnas = [
        # OBLIGATORIAS
        ('Anio', 8, True),
        ('UE', 10, True),
        ('Meta', 35, True),
        ('Descripcion', 45, True),
        ('Estado', 15, True),
        ('Monto_Referencial', 18, True),

        # OPCIONALES - Datos básicos
        ('Codigo', 15, False),
        ('Cantidad', 10, False),
        ('Tipo_Servicio', 15, False),
        ('Tipo_Proceso', 22, False),
        ('Monto_Adjudicado', 18, False),
        ('Proveedor', 30, False),
        ('Fecha_Convocatoria', 18, False),
        ('Fecha_Adjudicacion', 18, False),

        # OPCIONALES - Detalle adicional
        ('PIM_Asignado', 15, False),
        ('Requerimientos_Total', 18, False),
        ('Requerimientos_Adquiridos', 20, False),
        ('Unidad_Responsable', 28, False),
        ('Observaciones', 40, False),
        ('Notas', 40, False),
    ]

    # Fila de encabezados (fila 3, índice 2)
    row_header = 2
    for col, (nombre, ancho, obligatorio) in enumerate(columnas):
        # Usar formato según si es obligatorio u opcional
        formato = header_obligatorio_format if obligatorio else header_opcional_format
        worksheet.write(row_header, col, nombre, formato)
        worksheet.set_column(col, col, ancho)

    # ========== DATOS DE EJEMPLO ==========
    ejemplos = [
        # Ejemplo 1: Adquisición en proceso
        [
            2025,                                           # Anio
            'CIDE',                                         # UE
            '0001 - Administracion y Planeamiento',        # Meta
            'Adquisicion de equipos de computo para personal tecnico', # Descripcion
            'EN PROCESO',                                   # Estado
            125000.00,                                      # Monto_Referencial
            'ADQ-2025-001',                                 # Codigo
            25,                                             # Cantidad
            'BIEN',                                         # Tipo_Servicio
            'Adjudicacion Simplificada',                   # Tipo_Proceso
            0.00,                                           # Monto_Adjudicado
            '',                                             # Proveedor
            datetime(2025, 2, 15),                         # Fecha_Convocatoria
            None,                                           # Fecha_Adjudicacion
            125000.00,                                      # PIM_Asignado
            1,                                              # Requerimientos_Total
            0,                                              # Requerimientos_Adquiridos
            'Oficina de Tecnologias de la Informacion',   # Unidad_Responsable
            'Proceso en evaluacion tecnica',               # Observaciones
            '',                                             # Notas
        ],

        # Ejemplo 2: Adquisición culminada
        [
            2025,
            'DNCE',
            '0002 - Censos y Encuestas',
            'Servicio de impresion de cuestionarios para encuesta nacional',
            'CULMINADO',
            450000.00,
            'ADQ-2025-002',
            500000,
            'SERVICIO',
            'Licitacion Publica',
            420000.00,
            'Imprenta Nacional S.A.',
            datetime(2025, 1, 10),
            datetime(2025, 3, 15),
            450000.00,
            5,
            5,
            'Direccion Nacional de Censos y Encuestas',
            'Proceso culminado exitosamente',
            'Se realizaron 6 hitos: TDR, Revision Legal, Publicacion SEACE, Recepcion Ofertas, Evaluacion, Adjudicacion',
        ],

        # Ejemplo 3: Adquisición culminada - Software
        [
            2025,
            'DNCN',
            '0003 - Cuentas Nacionales',
            'Licencias de software estadistico especializado',
            'CULMINADO',
            85000.00,
            'ADQ-2025-003',
            50,
            'SERVICIO',
            'Comparacion de Precios',
            82000.00,
            'Software Analytics Peru',
            datetime(2025, 1, 5),
            datetime(2025, 2, 20),
            85000.00,
            1,
            1,
            'Direccion de Cuentas Nacionales',
            'Licencias instaladas y operativas',
            '',
        ],

        # Ejemplo 4: No iniciado
        [
            2025,
            'CIDE',
            '0001 - Administracion y Planeamiento',
            'Servicio de mantenimiento de infraestructura informatica',
            'NO INICIADO',
            180000.00,
            'ADQ-2025-004',
            12,
            'SERVICIO',
            'Adjudicacion Simplificada',
            0.00,
            '',
            None,
            None,
            180000.00,
            1,
            0,
            'Oficina de Tecnologias de la Informacion',
            'Pendiente elaboracion de TDR',
            'Inicio programado para Q2 2025',
        ],

        # Ejemplo 5: Histórico
        [
            2024,
            'DNCE',
            '0002 - Censos y Encuestas',
            'Tablets para trabajo de campo en zonas rurales',
            'HISTORICO',
            1250000.00,
            'ADQ-2024-005',
            350,
            'BIEN',
            'Licitacion Publica',
            1180000.00,
            'Tecnologia Movil S.A.C.',
            datetime(2024, 8, 1),
            datetime(2024, 11, 15),
            1250000.00,
            1,
            1,
            'Direccion Nacional de Censos y Encuestas',
            'Tablets entregadas y en uso',
            'Proceso de 2024 completado exitosamente',
        ],
    ]

    # Escribir ejemplos (empezando en fila 4, índice 3)
    start_row = 3
    for row_num, ejemplo in enumerate(ejemplos, start=start_row):
        for col_num, valor in enumerate(ejemplo):
            if isinstance(valor, datetime):
                worksheet.write_datetime(row_num, col_num, valor, date_format)
            elif isinstance(valor, (int, float)) and col_num in [5, 10, 14]:  # Columnas de monto
                worksheet.write_number(row_num, col_num, valor, number_format)
            elif isinstance(valor, int) and col_num in [7, 15, 16]:  # Cantidad y requerimientos
                worksheet.write(row_num, col_num, valor, text_format)
            elif valor is None or valor == '':
                worksheet.write_blank(row_num, col_num, '', text_format)
            else:
                worksheet.write(row_num, col_num, valor, text_format)

    # Freeze panes: congelar las 3 primeras filas
    worksheet.freeze_panes(3, 0)

    # Cerrar el archivo
    workbook.close()

    print(f"[OK] Plantilla SIMPLE creada exitosamente: {nombre_archivo}")
    print(f"\nCaracteristicas:")
    print(f"  - UNA SOLA HOJA con todas las columnas necesarias")
    print(f"  - {len([c for c in columnas if c[2]])} columnas OBLIGATORIAS (fondo rojo)")
    print(f"  - {len([c for c in columnas if not c[2]])} columnas OPCIONALES (fondo azul)")
    print(f"  - {len(ejemplos)} ejemplos de adquisiciones incluidos")
    print(f"  - Instrucciones claras en las primeras 2 filas")
    print(f"\nColumnas OBLIGATORIAS:")
    for nombre, _, obligatorio in columnas:
        if obligatorio:
            print(f"    - {nombre}")
    print(f"\nSolo complete los datos y guarde. Listo para importar!")

if __name__ == "__main__":
    crear_plantilla_simple()
