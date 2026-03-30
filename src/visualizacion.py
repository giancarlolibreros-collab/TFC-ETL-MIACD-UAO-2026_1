# =============================================================================
# FASE de VISUALIZACIÓN [TFC-ETL-MIACD-UAO-2026_1]
# Autores: Brayan Valencia Sánchez | Giancarlo Libreros Londoño
# Maestría en IA y Ciencia de Datos - UAO | Curso ETL | 2026-1
# =============================================================================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import warnings
import os
from sqlalchemy import create_engine
from datetime import datetime
warnings.filterwarnings('ignore')

# -----------------------------------------------------------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------------------------------------------------------
RUTA_BD         = "data/processed/CARMELITA_ETL.db"
RUTA_REPORTES   = "docs/reportes"
TABLA_HECHOS    = "hechos_financieros"

# Estilo general de gráficos
sns.set_theme(style="whitegrid", palette="Blues_d")
plt.rcParams.update({
    'font.family'  : 'Arial',
    'font.size'    : 10,
    'axes.titlesize': 12,
    'axes.titleweight': 'bold',
    'figure.dpi'   : 150
})

COLORES_INSTRUMENTO = {
    'FACTORING' : '#1F4E79',
    'SOBREGIRO' : '#2E75B6',
    'OTRO'      : '#BDD7EE'
}

# =============================================================================
# UTILIDAD: CREAR CARPETA DE REPORTES
# =============================================================================

def crear_carpeta_reportes(ruta: str):
    os.makedirs(ruta, exist_ok=True)
    print(f"  Carpeta de reportes: {ruta}")

# =============================================================================
# UTILIDAD: CARGAR DATOS DESDE LA BASE DE DATOS
# =============================================================================

def cargar_datos(ruta_bd: str) -> pd.DataFrame:
    engine = create_engine(f"sqlite:///{ruta_bd}")
    df = pd.read_sql(f"SELECT * FROM {TABLA_HECHOS}", engine)
    df['Fecha_Transaccion'] = pd.to_datetime(df['Fecha_Transaccion'])
    return df

# =============================================================================
# UTILIDAD: FORMATO DE PESOS COLOMBIANOS
# =============================================================================

def formato_cop(valor, pos=None):
    if valor >= 1_000_000_000:
        return f"${valor/1_000_000_000:.1f}B"
    elif valor >= 1_000_000:
        return f"${valor/1_000_000:.0f}M"
    else:
        return f"${valor/1_000:.0f}K"

# =============================================================================
# KPI 1: GASTO ANUAL TOTAL POR INSTRUMENTO
# =============================================================================

def grafico_kpi1_gasto_por_instrumento(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(8, 5))

    datos = df.groupby('Tipo_Instrumento')['Valor_Neto_Pesos'].sum().reset_index()
    datos = datos[datos['Tipo_Instrumento'] != 'OTRO']
    colores = [COLORES_INSTRUMENTO.get(i, '#BDD7EE') for i in datos['Tipo_Instrumento']]

    barras = ax.bar(datos['Tipo_Instrumento'], datos['Valor_Neto_Pesos'],
                    color=colores, edgecolor='white', width=0.5)

    for barra in barras:
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() * 1.02,
                formato_cop(barra.get_height()),
                ha='center', va='bottom', fontweight='bold', fontsize=11)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('KPI 1 — Gasto Financiero Anual por Instrumento')
    ax.set_xlabel('Instrumento Financiero')
    ax.set_ylabel('Gasto Total (COP)')
    plt.tight_layout()
    plt.savefig(f"{ruta}/KPI1_gasto_por_instrumento.png")
    plt.close()
    print("  ✓ KPI 1 — Gasto anual por instrumento")

# =============================================================================
# KPI 2: GASTO MENSUAL POR INSTRUMENTO (LÍNEAS)
# =============================================================================

def grafico_kpi2_gasto_mensual(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(12, 5))

    datos = df[df['Tipo_Instrumento'] != 'OTRO'].copy()
    datos['Periodo'] = datos['Anio'].astype(str) + '-' + datos['Mes'].astype(str).str.zfill(2)
    datos = datos.groupby(['Periodo', 'Tipo_Instrumento'])['Valor_Neto_Pesos'].sum().reset_index()

    for instrumento, color in COLORES_INSTRUMENTO.items():
        if instrumento == 'OTRO':
            continue
        subset = datos[datos['Tipo_Instrumento'] == instrumento]
        ax.plot(subset['Periodo'], subset['Valor_Neto_Pesos'],
                marker='o', label=instrumento, color=color, linewidth=2)

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('KPI 2 — Evolución Mensual del Gasto Financiero por Instrumento')
    ax.set_xlabel('Período (Año-Mes)')
    ax.set_ylabel('Gasto Total (COP)')
    ax.legend()
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(f"{ruta}/KPI2_gasto_mensual.png")
    plt.close()
    print("  ✓ KPI 2 — Evolución mensual por instrumento")

# =============================================================================
# KPI 3: PARTICIPACIÓN PORCENTUAL POR INSTRUMENTO (TORTA)
# =============================================================================

def grafico_kpi3_participacion(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(7, 7))

    datos = df[df['Tipo_Instrumento'] != 'OTRO'].groupby(
        'Tipo_Instrumento')['Valor_Neto_Pesos'].sum()
    colores = [COLORES_INSTRUMENTO.get(i, '#BDD7EE') for i in datos.index]

    wedges, texts, autotexts = ax.pie(
        datos, labels=datos.index, autopct='%1.1f%%',
        colors=colores, startangle=90,
        wedgeprops={'edgecolor': 'white', 'linewidth': 2}
    )
    for at in autotexts:
        at.set_fontweight('bold')
        at.set_fontsize(12)

    ax.set_title('KPI 3 — Participación Porcentual del Gasto por Instrumento')
    plt.tight_layout()
    plt.savefig(f"{ruta}/KPI3_participacion_porcentual.png")
    plt.close()
    print("  ✓ KPI 3 — Participación porcentual por instrumento")

# =============================================================================
# KPI 4: GASTO POR ENTIDAD FINANCIERA (BARRAS HORIZONTALES)
# =============================================================================

def grafico_kpi4_gasto_por_entidad(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(10, 6))

    datos = df.groupby('Entidad_Financiera')['Valor_Neto_Pesos'].sum().sort_values()
    colores = ['#1F4E79' if v == datos.max() else '#2E75B6' for v in datos]

    barras = ax.barh(datos.index, datos.values, color=colores, edgecolor='white')

    for barra in barras:
        ax.text(barra.get_width() * 1.01, barra.get_y() + barra.get_height() / 2,
                formato_cop(barra.get_width()),
                va='center', fontsize=9)

    ax.xaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('KPI 4 — Gasto Financiero por Entidad Financiera')
    ax.set_xlabel('Gasto Total (COP)')
    ax.set_ylabel('Entidad Financiera')
    plt.tight_layout()
    plt.savefig(f"{ruta}/KPI4_gasto_por_entidad.png")
    plt.close()
    print("  ✓ KPI 4 — Gasto por entidad financiera")

# =============================================================================
# KPI 5: TASA EA POR ENTIDAD FINANCIERA
# =============================================================================

def grafico_kpi5_tasas_ea(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(9, 5))

    datos = df[df['Tasa_EA_Entidad'].notna()].groupby(
        'Entidad_Financiera')['Tasa_EA_Entidad'].mean().sort_values(ascending=False).reset_index()

    barras = ax.bar(datos['Entidad_Financiera'], datos['Tasa_EA_Entidad'] * 100,
                    color='#2E75B6', edgecolor='white', width=0.5)

    for barra in barras:
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() * 1.02,
                f"{barra.get_height():.2f}%",
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.set_title('KPI 5 — Tasa Efectiva Anual (EA) por Entidad Financiera')
    ax.set_xlabel('Entidad Financiera')
    ax.set_ylabel('Tasa EA (%)')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(f"{ruta}/KPI5_tasas_ea_por_entidad.png")
    plt.close()
    print("  ✓ KPI 5 — Tasa EA por entidad financiera")

# =============================================================================
# KPI 6: COSTO DIARIO ESTIMADO POR ENTIDAD
# =============================================================================

def grafico_kpi6_costo_diario(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(10, 5))

    datos = df[df['Costo_Diario_Estimado'].notna()].groupby(
        'Entidad_Financiera')['Costo_Diario_Estimado'].mean().sort_values(ascending=False).reset_index()

    barras = ax.bar(datos['Entidad_Financiera'], datos['Costo_Diario_Estimado'],
                    color='#1F4E79', edgecolor='white', width=0.5)

    for barra in barras:
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() * 1.02,
                formato_cop(barra.get_height()),
                ha='center', va='bottom', fontsize=9, fontweight='bold')

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('KPI 6 — Costo Diario Estimado Promedio por Entidad Financiera')
    ax.set_xlabel('Entidad Financiera')
    ax.set_ylabel('Costo Diario Estimado (COP)')
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(f"{ruta}/KPI6_costo_diario_por_entidad.png")
    plt.close()
    print("  ✓ KPI 6 — Costo diario estimado por entidad")

# =============================================================================
# KPI 7: GASTO TRIMESTRAL ACUMULADO (BARRAS APILADAS)
# =============================================================================

def grafico_kpi7_gasto_trimestral(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(10, 5))

    datos = df[df['Tipo_Instrumento'] != 'OTRO'].groupby(
        ['Anio', 'Trimestre', 'Tipo_Instrumento'])['Valor_Neto_Pesos'].sum().unstack(
        fill_value=0).reset_index()
    datos['Periodo'] = 'Q' + datos['Trimestre'].astype(str) + '-' + datos['Anio'].astype(str)

    bottom = np.zeros(len(datos))
    for instrumento, color in COLORES_INSTRUMENTO.items():
        if instrumento not in datos.columns:
            continue
        ax.bar(datos['Periodo'], datos[instrumento],
               bottom=bottom, label=instrumento, color=color, edgecolor='white')
        bottom += datos[instrumento].values

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('KPI 7 — Gasto Financiero Trimestral Acumulado por Instrumento')
    ax.set_xlabel('Trimestre')
    ax.set_ylabel('Gasto Total (COP)')
    ax.legend()
    plt.xticks(rotation=30, ha='right')
    plt.tight_layout()
    plt.savefig(f"{ruta}/KPI7_gasto_trimestral.png")
    plt.close()
    print("  ✓ KPI 7 — Gasto trimestral acumulado")

# =============================================================================
# PE 8: COSTO PROMEDIO POR PESO: FACTORING VS SOBREGIRO
# =============================================================================

def grafico_pe8_costo_por_peso(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(8, 5))

    datos = df[df['Tipo_Instrumento'] != 'OTRO'].copy()
    datos['Costo_Por_Peso'] = datos['Costo_Diario_Estimado'] / datos['Valor_Neto_Pesos']
    resumen = datos.groupby('Tipo_Instrumento')['Costo_Por_Peso'].mean().reset_index()
    colores = [COLORES_INSTRUMENTO.get(i, '#BDD7EE') for i in resumen['Tipo_Instrumento']]

    barras = ax.bar(resumen['Tipo_Instrumento'], resumen['Costo_Por_Peso'] * 1000,
                    color=colores, edgecolor='white', width=0.5)

    for barra in barras:
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() * 1.02,
                f"${barra.get_height():.4f} x $1.000",
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_title('PE 8 — Costo Financiero Promedio por Cada $1.000 Pesos\nFactoring vs Sobregiro')
    ax.set_xlabel('Instrumento Financiero')
    ax.set_ylabel('Costo por $1.000 COP')
    plt.tight_layout()
    plt.savefig(f"{ruta}/PE8_costo_por_peso.png")
    plt.close()
    print("  ✓ PE 8 — Costo promedio por peso: factoring vs sobregiro")

# =============================================================================
# PE 9: PUNTO DE EQUILIBRIO FACTORING VS SOBREGIRO
# =============================================================================

def grafico_pe9_punto_equilibrio(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Tasas promedio por instrumento
    tasas = df[df['Tipo_Instrumento'] != 'OTRO'].groupby(
        'Tipo_Instrumento')['Tasa_EA_Entidad'].mean()

    montos = np.linspace(1_000_000, 500_000_000, 500)

    for instrumento, color in COLORES_INSTRUMENTO.items():
        if instrumento == 'OTRO' or instrumento not in tasas.index:
            continue
        tasa = tasas[instrumento]
        costo_diario = montos * ((1 + tasa) ** (1 / 365) - 1)
        ax.plot(montos / 1_000_000, costo_diario / 1_000,
                label=f"{instrumento} (EA: {tasa:.2%})",
                color=color, linewidth=2)

    # Punto de equilibrio
    if 'FACTORING' in tasas.index and 'SOBREGIRO' in tasas.index:
        tasa_f = tasas['FACTORING']
        tasa_s = tasas['SOBREGIRO']
        if abs(tasa_f - tasa_s) > 0:
            monto_eq = 0
            costo_eq  = 0
            ax.axvline(x=monto_eq / 1_000_000, color='red',
                       linestyle='--', linewidth=1.5, label='Punto de equilibrio')

    ax.set_title('PE 9 — Punto de Equilibrio: Costo Diario Factoring vs Sobregiro\npor Monto de Operación')
    ax.set_xlabel('Monto de Operación (Millones COP)')
    ax.set_ylabel('Costo Diario Estimado (Miles COP)')
    ax.legend()
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:.0f}M"))
    plt.tight_layout()
    plt.savefig(f"{ruta}/PE9_punto_equilibrio.png")
    plt.close()
    print("  ✓ PE 9 — Punto de equilibrio factoring vs sobregiro")

# =============================================================================
# PE 10: SIMULACIÓN ESCENARIO PRONTO PAGO VS SITUACIÓN ACTUAL
# =============================================================================

def grafico_pe10_escenario_pronto_pago(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(9, 6))

    total_actual    = df['Valor_Neto_Pesos'].sum()
    meta_okr        = 800_000_000
    descuento_pp    = total_actual * 0.15
    escenario_pp    = total_actual - descuento_pp

    escenarios = {
        'Situación\nActual'        : total_actual,
        'Escenario\nPronto Pago'   : escenario_pp,
        'Meta OKR1.1\n(800M)'      : meta_okr
    }
    colores = ['#1F4E79', '#2E75B6', '#70AD47']

    barras = ax.bar(escenarios.keys(), escenarios.values(),
                    color=colores, edgecolor='white', width=0.5)

    for barra in barras:
        ax.text(barra.get_x() + barra.get_width() / 2,
                barra.get_height() * 1.02,
                formato_cop(barra.get_height()),
                ha='center', va='bottom', fontsize=11, fontweight='bold')

    ax.axhline(y=meta_okr, color='red', linestyle='--',
               linewidth=1.5, label=f'Meta OKR1.1: {formato_cop(meta_okr)}')
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('PE 10 — Simulación: Impacto del Programa de Pronto Pago\nsobre el Gasto Financiero')
    ax.set_ylabel('Gasto Financiero Total (COP)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{ruta}/PE10_escenario_pronto_pago.png")
    plt.close()
    print("  ✓ PE 10 — Simulación escenario pronto pago")

# =============================================================================
# PE 11: COMBINACIÓN ÓPTIMA DE INSTRUMENTOS
# =============================================================================

def grafico_pe11_combinacion_optima(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(9, 6))

    total = df[df['Tipo_Instrumento'] != 'OTRO']['Valor_Neto_Pesos'].sum()
    datos_actual = df[df['Tipo_Instrumento'] != 'OTRO'].groupby(
        'Tipo_Instrumento')['Valor_Neto_Pesos'].sum()

    # Escenario optimizado: reducir factoring 30%, aumentar sobregiro 10%
    datos_optimo = datos_actual.copy()
    if 'FACTORING' in datos_optimo.index:
        datos_optimo['FACTORING'] *= 0.70
    if 'SOBREGIRO' in datos_optimo.index:
        datos_optimo['SOBREGIRO'] *= 1.10

    x      = np.arange(len(datos_actual))
    ancho  = 0.35

    ax.bar(x - ancho/2, datos_actual.values, ancho,
           label='Situación Actual', color='#1F4E79', edgecolor='white')
    ax.bar(x + ancho/2, datos_optimo.values, ancho,
           label='Escenario Optimizado', color='#70AD47', edgecolor='white')

    ax.set_xticks(x)
    ax.set_xticklabels(datos_actual.index)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('PE 11 — Combinación Óptima de Instrumentos\nSituación Actual vs Escenario Optimizado')
    ax.set_ylabel('Gasto Financiero Total (COP)')
    ax.legend()
    plt.tight_layout()
    plt.savefig(f"{ruta}/PE11_combinacion_optima.png")
    plt.close()
    print("  ✓ PE 11 — Combinación óptima de instrumentos")

# =============================================================================
# PE 12: GASTO POR ENTIDAD VS TASA EA (SCATTER)
# =============================================================================

def grafico_pe12_gasto_vs_tasa(df: pd.DataFrame, ruta: str):
    fig, ax = plt.subplots(figsize=(10, 6))

    datos = df[df['Tasa_EA_Entidad'].notna()].groupby('Entidad_Financiera').agg(
        Gasto_Total=('Valor_Neto_Pesos', 'sum'),
        Tasa_EA=('Tasa_EA_Entidad', 'mean')
    ).reset_index()

    scatter = ax.scatter(
        datos['Tasa_EA'] * 100,
        datos['Gasto_Total'],
        s=datos['Gasto_Total'] / datos['Gasto_Total'].max() * 1000,
        color='#1F4E79', alpha=0.7, edgecolors='white', linewidth=1.5
    )

    for _, row in datos.iterrows():
        ax.annotate(
            row['Entidad_Financiera'],
            (row['Tasa_EA'] * 100, row['Gasto_Total']),
            textcoords="offset points", xytext=(8, 4), fontsize=8
        )

    ax.yaxis.set_major_formatter(mticker.FuncFormatter(formato_cop))
    ax.set_title('PE 12 — Relación entre Tasa EA y Gasto Financiero por Entidad\n'
                 '(Tamaño del punto proporcional al gasto total)')
    ax.set_xlabel('Tasa Efectiva Anual (%)')
    ax.set_ylabel('Gasto Financiero Total (COP)')
    plt.tight_layout()
    plt.savefig(f"{ruta}/PE12_gasto_vs_tasa_ea.png")
    plt.close()
    print("  ✓ PE 12 — Gasto por entidad vs tasa EA")

# =============================================================================
# RESUMEN GENERAL DE VISUALIZACIÓN
# =============================================================================

def resumen_visualizacion(ruta: str):
    archivos = [f for f in os.listdir(ruta) if f.endswith('.png')]
    print("=" * 60)
    print("RESUMEN CONSOLIDADO DE VISUALIZACIÓN")
    print("=" * 60)
    print(f"  Gráficos generados     : {len(archivos)}")
    print(f"  Carpeta de reportes    : {ruta}")
    print(f"  Fecha de ejecución     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    for archivo in sorted(archivos):
        print(f"    → {archivo}")
    print("=" * 60)

# =============================================================================
# EJECUCIÓN DIRECTA - PRUEBA UNITARIA DEL MÓDULO
# =============================================================================

if __name__ == "__main__":
    print()
    print("  PRUEBA UNITARIA - MÓDULO DE VISUALIZACIÓN")
    print("  Ejecución directa de visualizacion.py")
    print()

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
    print()