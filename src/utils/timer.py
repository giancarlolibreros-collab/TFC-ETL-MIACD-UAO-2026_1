# =============================================================================
# UTILIDAD: MEDIDOR DE TIEMPOS DE EJECUCIÓN [TFC-ETL-MIACD-UAO-2026_1]
# Autores: Brayan Valencia Sánchez | Giancarlo Libreros Londoño
# Maestría en IA y Ciencia de Datos - UAO | Curso ETL | 2026-1
# =============================================================================

import time
import functools
from datetime import datetime
import pandas as pd

# -----------------------------------------------------------------------------
# REGISTRO GLOBAL DE MÉTRICAS
# -----------------------------------------------------------------------------
_metricas = []

def registrar(fase: str, componente: str):
    """
    Decorador que mide el tiempo de ejecución de una función
    y registra la métrica en el log global.

    Uso:
        @registrar(fase="EXTRACCIÓN", componente="Intereses Sobregiro")
        def extraer_intereses_sobregiro(ruta):
            ...
    """
    def decorador(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            inicio    = time.perf_counter()
            resultado = func(*args, **kwargs)
            fin       = time.perf_counter()
            duracion  = fin - inicio

            _metricas.append({
                'Fase'        : fase,
                'Componente'  : componente,
                'Función'     : func.__name__,
                'Inicio'      : datetime.fromtimestamp(inicio).strftime('%H:%M:%S'),
                'Fin'         : datetime.fromtimestamp(fin).strftime('%H:%M:%S'),
                'Duración (s)': round(duracion, 4),
            })
            return resultado
        return wrapper
    return decorador

def obtener_metricas() -> pd.DataFrame:
    """Retorna el DataFrame con todas las métricas registradas."""
    return pd.DataFrame(_metricas)

def limpiar_metricas():
    """Limpia el registro global de métricas."""
    _metricas.clear()

def imprimir_tabla_metricas():
    """Imprime la tabla de métricas de desempeño en consola."""
    df = obtener_metricas()
    if df.empty:
        print("  No hay métricas registradas.")
        return

    total = df['Duración (s)'].sum()

    print("=" * 70)
    print("MÉTRICAS DE DESEMPEÑO — PIPELINE ETL")
    print("=" * 70)
    print(f"  {'Fase':<18} {'Componente':<30} {'Duración (s)':>12} {'% del Total':>12}")
    print(f"  {'─'*18} {'─'*30} {'─'*12} {'─'*12}")

    for _, row in df.iterrows():
        pct = (row['Duración (s)'] / total) * 100
        print(f"  {row['Fase']:<18} {row['Componente']:<30} "
              f"{row['Duración (s)']:>12.4f} {pct:>11.1f}%")

    print(f"  {'─'*18} {'─'*30} {'─'*12} {'─'*12}")
    print(f"  {'TOTAL':<18} {'':<30} {total:>12.4f} {'100.0%':>12}")
    print("=" * 70)

def exportar_metricas(ruta: str = "docs/reportes/METRICAS_DESEMPENO.xlsx"):
    """
    Exporta la tabla de métricas a un archivo Excel.
    """
    df = obtener_metricas()
    if df.empty:
        print("  No hay métricas para exportar.")
        return

    total = df['Duración (s)'].sum()
    df['% del Total'] = (df['Duración (s)'] / total * 100).round(2)

    df.to_excel(ruta, index=False, engine='openpyxl')
    print(f"  Métricas exportadas: {ruta}")