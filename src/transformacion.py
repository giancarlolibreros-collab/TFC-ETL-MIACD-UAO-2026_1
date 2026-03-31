# =============================================================================
# FASE de TRANSFORMACIÓN [TFC-ETL-MIACD-UAO-2026_1]
# Autores: Brayan Valencia Sánchez | Giancarlo Libreros Londoño
# Maestría en IA y Ciencia de Datos - UAO | Curso ETL | 2026-1
# =============================================================================

import pandas as pd
import warnings
warnings.filterwarnings('ignore')
from src.utils.timer import registrar

# =============================================================================
# MAPEO DE TASAS EA POR ENTIDAD
# Fuente: tasas_sobregiro.xlsx (extraído en fase de extracción)
# =============================================================================

TASAS_EA = {
    'BANCOLOMBIA'      : 0.22419735,
    'DAVIVIENDA'       : 0.195,
    'BANCO DE BOGOTÁ'  : 0.189,
    'BANCO DE BOGOTA'  : 0.189,
    'BANCO POPULAR'    : None,
    'BANCO ITAÚ'       : 0.1362,
    'BANCO ITAU'       : 0.1362,
    'BANCO DE OCCIDENTE': None,
    'SERFINANZAS'      : None,
    'BBVA'             : None,
}

# =============================================================================
# UTILIDAD: CLASIFICAR TIPO DE INSTRUMENTO
# =============================================================================

def clasificar_instrumento(descripcion: str) -> str:
    """
    Clasifica cada registro según el tipo de instrumento financiero.
    """
    if pd.isna(descripcion):
        return 'OTRO'
    desc = descripcion.upper()
    if 'SOBREGIRO' in desc:
        return 'SOBREGIRO'
    elif 'FACTORING' in desc or 'COMISION' in desc or 'COMISIÓN' in desc:
        return 'FACTORING'
    else:
        return 'OTRO'

# =============================================================================
# UTILIDAD: CALCULAR COSTO DIARIO ESTIMADO
# Fórmula: Costo_Diario = Valor * ((1 + Tasa_EA)^(1/365) - 1)
# =============================================================================

def calcular_costo_diario(valor: float, tasa_ea: float) -> float:
    """
    Estima el costo diario de un instrumento financiero dado su valor y tasa EA.
    """
    if pd.isna(valor) or pd.isna(tasa_ea):
        return None
    return valor * ((1 + tasa_ea) ** (1 / 365) - 1)

# =============================================================================
# TRANSFORMACIÓN - FUENTE 1: Intereses por Sobregiro
# =============================================================================

@registrar(fase="TRANSFORMACIÓN", componente="Intereses Sobregiro")
def transformar_intereses_sobregiro(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma el dataframe de intereses por sobregiro a la estructura
    consolidada definida para el análisis financiero.
    """
    print("=" * 60)
    print("TRANSFORMACIÓN - FUENTE 1: Intereses por Sobregiro")
    print("=" * 60)

    df = df.copy()

    # Renombrar columnas a estructura objetivo
    df.rename(columns={
        'tipo_gasto'      : 'Descripcion_Cuenta_Auxiliar',
        'valor_cop'       : 'Valor_Neto_Pesos',
        'documento'       : 'Documento',
        'Fecha'           : 'Fecha_Transaccion',
        'descripcion'     : 'Notas_Documento',
        'entidad_bancaria': 'Entidad_Financiera',
        'Mes'             : 'Mes',
        'nombre_mes'      : 'Nombre_Mes'
    }, inplace=True)

    # Agregar campos fijos de cuenta
    df['Cuenta_Principal']      = '5501 - COSTO DE LA DEUDA'
    df['Cuenta_Auxiliar']       = 53052004

    # Agregar campos calculados
    df['Tipo_Instrumento']      = df['Descripcion_Cuenta_Auxiliar'].apply(clasificar_instrumento)
    df['Anio']                  = df['Fecha_Transaccion'].dt.year
    df['Trimestre']             = df['Fecha_Transaccion'].dt.quarter
    df['Tasa_EA_Entidad']       = df['Entidad_Financiera'].str.upper().map(
                                    lambda e: TASAS_EA.get(e.strip(), None) if pd.notna(e) else None
                                  )
    df['Costo_Diario_Estimado'] = df.apply(
                                    lambda r: calcular_costo_diario(r['Valor_Neto_Pesos'], r['Tasa_EA_Entidad']),
                                    axis=1
                                  )

    # Limpieza
    df['Valor_Neto_Pesos']      = pd.to_numeric(df['Valor_Neto_Pesos'], errors='coerce')
    df['Entidad_Financiera']    = df['Entidad_Financiera'].str.strip().str.upper()
    df                          = df[df['Valor_Neto_Pesos'] > 0].copy()
    df                          = df.dropna(subset=['Fecha_Transaccion'])

    # Orden de columnas estructura objetivo
    df = df[[
        'Cuenta_Principal', 'Cuenta_Auxiliar', 'Descripcion_Cuenta_Auxiliar',
        'Valor_Neto_Pesos', 'Documento', 'Fecha_Transaccion', 'Notas_Documento',
        'Entidad_Financiera', 'Tipo_Instrumento', 'Mes', 'Nombre_Mes',
        'Anio', 'Trimestre', 'Tasa_EA_Entidad', 'Costo_Diario_Estimado'
    ]]

    print(f"  Registros transformados : {len(df)}")
    print(f"  Tipo instrumento        : {df['Tipo_Instrumento'].unique()}")
    print(f"  Entidades               : {sorted(df['Entidad_Financiera'].unique())}")
    print(f"  Total valor (COP)       : ${df['Valor_Neto_Pesos'].sum():,.0f}")
    print()
    return df

# =============================================================================
# TRANSFORMACIÓN - FUENTE 2: Comisiones por Factoring
# =============================================================================

@registrar(fase="TRANSFORMACIÓN", componente="Comisiones Factoring")
def transformar_comisiones_factoring(df: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma el dataframe de comisiones por factoring a la estructura
    consolidada definida para el análisis financiero.
    """
    print("=" * 60)
    print("TRANSFORMACIÓN - FUENTE 2: Comisiones por Factoring")
    print("=" * 60)

    df = df.copy()

    # Renombrar columnas a estructura objetivo
    df.rename(columns={
        'tipo_gasto'    : 'Descripcion_Cuenta_Auxiliar',
        'valor_cop'     : 'Valor_Neto_Pesos',
        'documento'     : 'Documento',
        'Fecha'         : 'Fecha_Transaccion',
        'descripcion'   : 'Notas_Documento',
        'entidad_factor': 'Entidad_Financiera',
        'Mes'           : 'Mes',
        'nombre_mes'    : 'Nombre_Mes'
    }, inplace=True)

    # Agregar campos fijos de cuenta
    df['Cuenta_Principal'] = '5502 - COMISIONES'
    df['Cuenta_Auxiliar']  = 53051502

    # Agregar campos calculados
    df['Tipo_Instrumento']      = df['Descripcion_Cuenta_Auxiliar'].apply(clasificar_instrumento)
    df['Anio']                  = df['Fecha_Transaccion'].dt.year
    df['Trimestre']             = df['Fecha_Transaccion'].dt.quarter
    df['Tasa_EA_Entidad']       = df['Entidad_Financiera'].str.upper().map(
                                    lambda e: TASAS_EA.get(e.strip(), None) if pd.notna(e) else None
                                  )
    df['Costo_Diario_Estimado'] = df.apply(
                                    lambda r: calcular_costo_diario(r['Valor_Neto_Pesos'], r['Tasa_EA_Entidad']),
                                    axis=1
                                  )

    # Limpieza
    df['Valor_Neto_Pesos']   = pd.to_numeric(df['Valor_Neto_Pesos'], errors='coerce')
    df['Entidad_Financiera'] = df['Entidad_Financiera'].str.strip().str.upper()
    df                       = df[df['Valor_Neto_Pesos'] > 0].copy()
    df                       = df.dropna(subset=['Fecha_Transaccion'])

    # Orden de columnas estructura objetivo
    df = df[[
        'Cuenta_Principal', 'Cuenta_Auxiliar', 'Descripcion_Cuenta_Auxiliar',
        'Valor_Neto_Pesos', 'Documento', 'Fecha_Transaccion', 'Notas_Documento',
        'Entidad_Financiera', 'Tipo_Instrumento', 'Mes', 'Nombre_Mes',
        'Anio', 'Trimestre', 'Tasa_EA_Entidad', 'Costo_Diario_Estimado'
    ]]

    print(f"  Registros transformados : {len(df)}")
    print(f"  Tipo instrumento        : {df['Tipo_Instrumento'].unique()}")
    print(f"  Entidades               : {sorted(df['Entidad_Financiera'].unique())}")
    print(f"  Total valor (COP)       : ${df['Valor_Neto_Pesos'].sum():,.0f}")
    print()
    return df

# =============================================================================
# CONSOLIDACIÓN: TABLA DE HECHOS FINAL
# =============================================================================

@registrar(fase="TRANSFORMACIÓN", componente="Consolidación Hechos")
def consolidar_tabla_hechos(df_sobregiro: pd.DataFrame,
                             df_factoring: pd.DataFrame) -> pd.DataFrame:
    """
    Consolida los dataframes transformados en una única tabla de hechos
    lista para la fase de carga.
    """
    print("=" * 60)
    print("CONSOLIDACIÓN - Tabla de Hechos Financiera")
    print("=" * 60)

    df_consolidado = pd.concat([df_sobregiro, df_factoring], ignore_index=True)
    df_consolidado = df_consolidado.sort_values(
                        ['Anio', 'Mes', 'Entidad_Financiera']
                     ).reset_index(drop=True)

    print(f"  Total registros consolidados : {len(df_consolidado)}")
    print(f"  Instrumentos identificados   : {sorted(df_consolidado['Tipo_Instrumento'].unique())}")
    print(f"  Entidades financieras        : {sorted(df_consolidado['Entidad_Financiera'].unique())}")
    print(f"  Período cubierto             : {df_consolidado['Fecha_Transaccion'].min().date()} → "
          f"{df_consolidado['Fecha_Transaccion'].max().date()}")
    print(f"  Total gasto financiero (COP) : ${df_consolidado['Valor_Neto_Pesos'].sum():,.0f}")
    print()
    return df_consolidado

# =============================================================================
# RESUMEN GENERAL DE LA TRANSFORMACIÓN
# =============================================================================

def resumen_transformacion(df: pd.DataFrame):
    """
    Imprime un resumen consolidado de la tabla de hechos transformada.
    """
    print("=" * 60)
    print("RESUMEN CONSOLIDADO DE TRANSFORMACIÓN")
    print("=" * 60)

    por_instrumento = df.groupby('Tipo_Instrumento')['Valor_Neto_Pesos'].agg(['sum', 'count'])
    total           = df['Valor_Neto_Pesos'].sum()

    for instrumento, row in por_instrumento.iterrows():
        pct = (row['sum'] / total) * 100
        print(f"  {instrumento:<12} : {int(row['count']):>5} registros | "
              f"${row['sum']:>18,.0f} COP | {pct:>5.1f}%")

    print(f"  {'─'*54}")
    print(f"  TOTAL        : {len(df):>5} registros | ${total:>18,.0f} COP | 100.0%")
    print()
    print(f"  Costo diario estimado promedio : "
          f"${df['Costo_Diario_Estimado'].mean():,.0f} COP/día")
    print(f"  Tasa EA promedio ponderada     : "
          f"{(df['Tasa_EA_Entidad'] * df['Valor_Neto_Pesos']).sum() / df['Valor_Neto_Pesos'].sum():.2%}")
    print(f"  Método de transformación       : pandas")
    print("=" * 60)

# =============================================================================
# EJECUCIÓN DIRECTA - PRUEBA UNITARIA DEL MÓDULO
# =============================================================================

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from src.extraccion import (
        renombrar_archivos,
        extraer_intereses_sobregiro,
        extraer_comisiones_factoring,
        CARPETA_RAW,
        RUTA_SOBREGIRO,
        RUTA_COMISIONES
    )

    print()
    print("  PRUEBA UNITARIA - MÓDULO DE TRANSFORMACIÓN")
    print("  Ejecución directa de transformacion.py")
    print()

    # Extracción previa necesaria para la prueba
    renombrar_archivos(CARPETA_RAW)
    df_sob_raw = extraer_intereses_sobregiro(RUTA_SOBREGIRO)
    df_fac_raw = extraer_comisiones_factoring(RUTA_COMISIONES)

    # Transformación
    df_sob_t   = transformar_intereses_sobregiro(df_sob_raw)
    df_fac_t   = transformar_comisiones_factoring(df_fac_raw)
    df_hechos  = consolidar_tabla_hechos(df_sob_t, df_fac_t)

    resumen_transformacion(df_hechos)

    # Exportar tabla de hechos transformada
    df_hechos.to_excel(
        "data/processed/TABLA_HECHOS_FINANCIERA.xlsx",
        index=False,
        engine='openpyxl'
    )
    print("Archivo exportado: data/processed/TABLA_HECHOS_FINANCIERA.xlsx")
    print()