# =============================================================================
# PIPELINE ETL [TFC-ETL-MIACD-UAO-2026_1]
# Autores: Brayan Valencia Sánchez | Giancarlo Libreros Londoño
# Maestría en IA y Ciencia de Datos - UAO | Curso ETL | 2026-1
# =============================================================================

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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
# from src.transformacion import (...)  # Se habilitará en la siguiente fase
# from src.carga import (...)           # Se habilitará en la siguiente fase

import pandas as pd

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

def fase_transformacion(df_sobregiro, df_factoring, df_tasas, df_cupos):
    """Ejecuta la fase de transformación. Se habilitará en la siguiente fase."""
    pass  # TODO: invocar funciones de transformacion.py

# =============================================================================
# FASE 3 - CARGA
# =============================================================================

def fase_carga():
    """Ejecuta la fase de carga. Se habilitará en la siguiente fase."""
    pass  # TODO: invocar funciones de carga.py


# =============================================================================
# EJECUCIÓN PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    print()
    print("  PIPELINE ETL - EMPRESA")
    print("  Ejecución completa de la canalización")
    print()

    # Fase 1
    df_sobregiro, df_factoring, df_tasas, df_cupos = fase_extraccion()

    # Fase 2 — se habilitará en la siguiente fase
    # fase_transformacion(df_sobregiro, df_factoring, df_tasas, df_cupos)

    # Fase 3 — se habilitará en la siguiente fase
    # fase_carga()