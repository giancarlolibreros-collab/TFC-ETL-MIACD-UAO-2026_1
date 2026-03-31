# =============================================================================
# PIPELINE ETL [TFC-ETL-MIACD-UAO-2026_1]
# Autores: Brayan Valencia Sánchez | Giancarlo Libreros Londoño
# Maestría en IA y Ciencia de Datos - UAO | Curso ETL | 2026-1
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.timer import imprimir_tabla_metricas, exportar_metricas

from src.extraccion import (
    renombrar_archivos,
    extraer_intereses_sobregiro,
    extraer_comisiones_factoring,
    extraer_tasas_sobregiro,
    resumen_extraccion,
    CARPETA_RAW,
    RUTA_SOBREGIRO,
    RUTA_TASAS,
    RUTA_COMISIONES
)
from src.transformacion import (
    transformar_intereses_sobregiro,
    transformar_comisiones_factoring,
    consolidar_tabla_hechos,
    resumen_transformacion
)
from src.carga import (
    crear_conexion,
    cargar_tabla_hechos,
    verificar_carga,
    resumen_carga,
    RUTA_BD,
    TABLA_HECHOS
)
from src.visualizacion import (
    crear_carpeta_reportes,
    cargar_datos,
    grafico_kpi1_gasto_por_instrumento,
    grafico_kpi2_gasto_mensual,
    grafico_kpi3_participacion,
    grafico_kpi4_gasto_por_entidad,
    grafico_kpi5_tasas_ea,
    grafico_kpi6_costo_diario,
    grafico_kpi7_gasto_trimestral,
    grafico_pe8_costo_por_peso,
    grafico_pe9_punto_equilibrio,
    grafico_pe10_escenario_pronto_pago,
    grafico_pe11_combinacion_optima,
    grafico_pe12_gasto_vs_tasa,
    resumen_visualizacion,
    RUTA_REPORTES
)

# =============================================================================
# FASE 1 - EXTRACCIÓN
# =============================================================================

def fase_extraccion():
    """Ejecuta la fase de extracción y retorna los dataframes extraídos."""
    renombrar_archivos(CARPETA_RAW)
    df_sobregiro       = extraer_intereses_sobregiro(RUTA_SOBREGIRO)
    df_factoring       = extraer_comisiones_factoring(RUTA_COMISIONES)
    df_tasas, df_cupos = extraer_tasas_sobregiro(RUTA_TASAS)
    resumen_extraccion(df_sobregiro, df_factoring, df_tasas)
    return df_sobregiro, df_factoring, df_tasas, df_cupos

# =============================================================================
# FASE 2 - TRANSFORMACIÓN
# =============================================================================

def fase_transformacion(df_sobregiro, df_factoring):
    """Ejecuta la fase de transformación y retorna la tabla de hechos."""
    df_sob_t  = transformar_intereses_sobregiro(df_sobregiro)
    df_fac_t  = transformar_comisiones_factoring(df_factoring)
    df_hechos = consolidar_tabla_hechos(df_sob_t, df_fac_t)
    resumen_transformacion(df_hechos)
    return df_hechos

# =============================================================================
# FASE 3 - CARGA
# =============================================================================

def fase_carga(df_hechos):
    """Ejecuta la fase de carga en la base de datos SQLite."""
    engine = crear_conexion(RUTA_BD)
    cargar_tabla_hechos(df_hechos, engine)
    verificar_carga(engine)
    resumen_carga(engine)

# =============================================================================
# FASE 4 - VISUALIZACIÓN
# =============================================================================

def fase_visualizacion():
    """Ejecuta la fase de visualización y genera los reportes."""
    crear_carpeta_reportes(RUTA_REPORTES)
    df = cargar_datos(RUTA_BD)

    print("\n  Generando KPIs:")
    grafico_kpi1_gasto_por_instrumento(df, RUTA_REPORTES)
    grafico_kpi2_gasto_mensual(df, RUTA_REPORTES)
    grafico_kpi3_participacion(df, RUTA_REPORTES)
    grafico_kpi4_gasto_por_entidad(df, RUTA_REPORTES)
    grafico_kpi5_tasas_ea(df, RUTA_REPORTES)
    grafico_kpi6_costo_diario(df, RUTA_REPORTES)
    grafico_kpi7_gasto_trimestral(df, RUTA_REPORTES)

    print("\n  Generando preguntas estratégicas:")
    grafico_pe8_costo_por_peso(df, RUTA_REPORTES)
    grafico_pe9_punto_equilibrio(df, RUTA_REPORTES)
    grafico_pe10_escenario_pronto_pago(df, RUTA_REPORTES)
    grafico_pe11_combinacion_optima(df, RUTA_REPORTES)
    grafico_pe12_gasto_vs_tasa(df, RUTA_REPORTES)

    resumen_visualizacion(RUTA_REPORTES)

# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print()
    print("  PIPELINE ETL - INGENIO CARMELITA S.A.")
    print("  Ejecución completa de la canalización")
    print()

    df_sobregiro, df_factoring, df_tasas, df_cupos = fase_extraccion()
    df_hechos = fase_transformacion(df_sobregiro, df_factoring)
    fase_carga(df_hechos)
    fase_visualizacion()

    # Métricas de desempeño
    imprimir_tabla_metricas()
    exportar_metricas()