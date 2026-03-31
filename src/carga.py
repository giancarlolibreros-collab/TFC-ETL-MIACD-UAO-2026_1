# =============================================================================
# FASE de CARGA [TFC-ETL-MIACD-UAO-2026_1]
# Autores: Brayan Valencia Sánchez | Giancarlo Libreros Londoño
# Maestría en IA y Ciencia de Datos - UAO | Curso ETL | 2026-1
# =============================================================================

import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')
from src.utils.timer import registrar

# -----------------------------------------------------------------------------
# CONFIGURACIÓN DE LA BASE DE DATOS
# -----------------------------------------------------------------------------
RUTA_BD     = "data/processed/CARMELITA_ETL.db"
TABLA_HECHOS = "hechos_financieros"

# =============================================================================
# UTILIDAD: CREAR CONEXIÓN A LA BASE DE DATOS
# =============================================================================

def crear_conexion(ruta_bd: str):
    """
    Crea y retorna un engine de SQLAlchemy para SQLite.
    """
    engine = create_engine(f"sqlite:///{ruta_bd}")
    print(f"  Conexión establecida: {ruta_bd}")
    return engine

# =============================================================================
# CARGA: TABLA DE HECHOS FINANCIERA
# =============================================================================

@registrar(fase="CARGA", componente="Tabla Hechos → SQLite")
def cargar_tabla_hechos(df: pd.DataFrame, engine, tabla: str = TABLA_HECHOS):
    """
    Carga la tabla de hechos transformada en la base de datos SQLite.
    Estrategia: replace — reemplaza la tabla completa en cada ejecución
    para garantizar consistencia con los datos más recientes.
    """
    print("=" * 60)
    print("CARGA - Tabla de Hechos Financiera")
    print("=" * 60)

    # Convertir fecha a string para compatibilidad con SQLite
    df = df.copy()
    df['Fecha_Transaccion'] = df['Fecha_Transaccion'].dt.strftime('%Y-%m-%d')

    # Carga a la base de datos
    df.to_sql(
        name      = tabla,
        con       = engine,
        if_exists = 'replace',
        index     = True,
        index_label = 'id'
    )

    print(f"  Tabla cargada          : {tabla}")
    print(f"  Registros cargados     : {len(df)}")
    print(f"  Base de datos          : {RUTA_BD}")
    print()

# =============================================================================
# VERIFICACIÓN: CONSULTAS DE VALIDACIÓN POST-CARGA
# =============================================================================

@registrar(fase="CARGA", componente="Verificación Post-Carga")
def verificar_carga(engine, tabla: str = TABLA_HECHOS):
    """
    Ejecuta consultas de validación para verificar que la carga
    fue exitosa y los datos son consistentes.
    """
    print("=" * 60)
    print("VERIFICACIÓN - Validación post-carga")
    print("=" * 60)

    with engine.connect() as conn:

        # Total de registros
        total = conn.execute(
            text(f"SELECT COUNT(*) FROM {tabla}")
        ).scalar()
        print(f"  Total registros en BD       : {total}")

        # Total por instrumento
        print(f"\n  Gasto por tipo de instrumento:")
        resultado = conn.execute(text(f"""
            SELECT Tipo_Instrumento,
                   COUNT(*)              AS registros,
                   SUM(Valor_Neto_Pesos) AS total_cop
            FROM {tabla}
            GROUP BY Tipo_Instrumento
            ORDER BY total_cop DESC
        """))
        for row in resultado:
            print(f"    {row[0]:<12} : {row[1]:>5} registros | ${row[2]:>18,.0f} COP")

        # Total por entidad financiera
        print(f"\n  Gasto por entidad financiera:")
        resultado = conn.execute(text(f"""
            SELECT Entidad_Financiera,
                   COUNT(*)              AS registros,
                   SUM(Valor_Neto_Pesos) AS total_cop
            FROM {tabla}
            GROUP BY Entidad_Financiera
            ORDER BY total_cop DESC
        """))
        for row in resultado:
            print(f"    {row[0]:<35} : {row[1]:>5} registros | ${row[2]:>18,.0f} COP")

        # Total por mes y año
        print(f"\n  Gasto por periodo (Año - Mes):")
        resultado = conn.execute(text(f"""
            SELECT Anio, Nombre_Mes, Mes,
                   SUM(Valor_Neto_Pesos) AS total_cop
            FROM {tabla}
            GROUP BY Anio, Mes, Nombre_Mes
            ORDER BY Anio, Mes
        """))
        for row in resultado:
            print(f"    {row[0]} - {row[1]:<12} : ${row[3]:>18,.0f} COP")

    print()

# =============================================================================
# RESUMEN GENERAL DE CARGA
# =============================================================================

def resumen_carga(engine, tabla: str = TABLA_HECHOS):
    """
    Imprime un resumen final del proceso de carga.
    """
    print("=" * 60)
    print("RESUMEN CONSOLIDADO DE CARGA")
    print("=" * 60)

    with engine.connect() as conn:
        total = conn.execute(
            text(f"SELECT COUNT(*) FROM {tabla}")
        ).scalar()
        total_cop = conn.execute(
            text(f"SELECT SUM(Valor_Neto_Pesos) FROM {tabla}")
        ).scalar()
        fecha_min = conn.execute(
            text(f"SELECT MIN(Fecha_Transaccion) FROM {tabla}")
        ).scalar()
        fecha_max = conn.execute(
            text(f"SELECT MAX(Fecha_Transaccion) FROM {tabla}")
        ).scalar()

    print(f"  Base de datos          : {RUTA_BD}")
    print(f"  Tabla cargada          : {tabla}")
    print(f"  Total registros        : {total}")
    print(f"  Total gasto (COP)      : ${total_cop:,.0f}")
    print(f"  Período cubierto       : {fecha_min} → {fecha_max}")
    print(f"  Motor de base de datos : SQLite")
    print(f"  Conector               : SQLAlchemy")
    print(f"  Fecha de ejecución     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
    from src.transformacion import (
        transformar_intereses_sobregiro,
        transformar_comisiones_factoring,
        consolidar_tabla_hechos
    )

    print()
    print("  PRUEBA UNITARIA - MÓDULO DE CARGA")
    print("  Ejecución directa de carga.py")
    print()

    # Extracción
    renombrar_archivos(CARPETA_RAW)
    df_sob_raw = extraer_intereses_sobregiro(RUTA_SOBREGIRO)
    df_fac_raw = extraer_comisiones_factoring(RUTA_COMISIONES)

    # Transformación
    df_sob_t  = transformar_intereses_sobregiro(df_sob_raw)
    df_fac_t  = transformar_comisiones_factoring(df_fac_raw)
    df_hechos = consolidar_tabla_hechos(df_sob_t, df_fac_t)

    # Carga
    engine = crear_conexion(RUTA_BD)
    cargar_tabla_hechos(df_hechos, engine)
    verificar_carga(engine)
    resumen_carga(engine)

    print("Base de datos generada: data/processed/CARMELITA_ETL.db")
    print()