# Trabajo de Final de Curso (TFC) "ETL (Extract, Transform and Load)"

Este repositorio se usa para alojar y permitir el desarrollo colaborativo, y con control de versiones, del trabajo de final de curso (TFC) "ETL (Extract, Transform and Load)" de la Maestría en Inteligencia Artificial y Ciencias de Datos (MIACD) de la Universidad Autónoma de Occidente (UAO) en el periodo 2026-1 (repositorio: TFC-ETL-MIACD-UAO-2026_1). Este repositorio tendrá la siguiente estructura:
```
TFC-ETL-MIACD-UAO-2026_1/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── src/
│   ├── extraccion.py
│   ├── transformacion.py
│   └── carga.py
│
├── dags/
│   └── pipeline.py
│
├── docs/
│   ├── Caracterizacion_Fuentes_de_Datos.md
│   ├── Definicion_del_Problema.md
│   ├── Estado_del_Arte.md
│   └── Stack_Tecnologico.md
│
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```
NOTA: por confidencialidad la carpeta `data/` carece de versionado.
## What the project does :: ¿Qué hace el proyecto?

Los procesos de ETL (Extract, Transform and Load) son fundamentales para obtener valor y tomar decisiones basadas en datos, en el sentido de que preparan los datos para análisis avanzados y la toma de decisiones informadas. Así, extraer datos de diversas fuentes, limpiar y transformar estos en formatos adecuados para el análisis, y finalmente cargarlos en bases de datos facilitan su exploración y modelado. Con base en lo dicho, el TFC respaldado por este repositorio muestra cómo afrontar las fases ETL para un problema basado en datos en el ámbito financiero relacionado con un ingenio azucarero del Valle del Cauca.

## Why the project is useful :: ¿Por qué es útil el proyecto?

El proyecto captura la lógica causal necesaria para enfrentar un problema basado en datos que requiere una canalización ETL como apoyo para la toma de decisiones, en este caso de gestión financiera, que facilite acceder de manera efectiva a los datos generados por la empresa y por terceros en el contexto indicado. El problema estudiado de gestión financiera se manifiesta por la existencia de gastos financieros elevados relacionados con el uso combinado de instrumentos financieros conocidos como factoring y sobregiros, que reducen significativamente la rentabilidad anual de la empresa objeto de estudio.

## How users can get started with the project :: ¿Cómo pueden los usuarios empezar a usar el proyecto?

Es fundamental leer, en el orden siguiente, la documentación asociada con los archivos: Definicion_del_Problema, Estado_del_Arte, Stack_Tecnologico y Caracterizacion_Fuentes_de_Datos, hospedados en la carpeta `docs`. 

En el primero, se consignan el contexto del problema basado en datos, las caracterizaciones de los usuarios::clientes, la formulación del problema identificado, las fuentes de datos asociadas con el problema, la definición de los objetivos y resultados clave (OKR) y los indicadores clave de rendimiento (KPI), y las preguntas estratégicas (o de negocio) soportadas por la canalización (pipeline) ETL. 

En el segundo, se exponen fuentes bibliográficas relevantes, verificables y actualizadas sobre las decisiones técnicas de canalización de datos relacionadas con el problema abordado de gestión financiera en torno a tres ejes temáticos: canalizaciones ETL en el sector financiero; factoring en Colombia y Latinoamérica; y la gestión del capital de trabajo y los costos financieros en empresas agroindustriales.

En el tercero, se registra la caracterización de las fuentes de datos en términos estructurales y de calidad combinando elementos metodológicos del estándar de facto Data Profiling, de DAMA-DMBOK, y de la ISO 25012.

En el cuarto, se muestra la definición del stack tecnológico definido con base en tres criterios fundamentales: alineación con el currículo del curso de ETL  (Python, SQL y herramientas ETL especializadas), viabilidad técnica en el entorno académico disponible (UAO , equipos propios), y coherencia con las capacidades técnicas del equipo de trabajo. El stack tecnológico propuesto cubre las tres fases de la canalización: Extracción, Transformación, Carga, además de la Visualización y Reportes.

Luego de las lecturas contextuales puede se puede proceder con la ejecución de la canalización ETL, o de sus componentes, así:

### 1. Clonar el repositorio:
```bash
git clone https://github.com//TFC-ETL-MIACD-UAO-2026_1.git
cd TFC-ETL-MIACD-UAO-2026_1
```
### 2. Crear y activar el entorno virtual:
```bash
python -m venv venv
venv\Scripts\Activate.ps1
```
### 3. Instalar las dependencias:
```bash
pip install -r requirements.txt
```
### 4. Colocar los archivos de datos en la carpeta `data/raw/`:
```
data/raw/Intereses Sobregiro.xlsx
data/raw/tasas sobregiro.xlsx
data/raw/COMISIONES AÑO 2025.xlsx
```
> Los archivos de datos carecen de versionamiento, por esto se debe contactar al equipo de trabajo para obetener acceso a ellos. 
> La normalización de nombres se aplica automáticamente al ejecutar la canalización.
---
### 5.1 Cada módulo puede ejecutarse de forma independiente como prueba unitaria:
```bash
# Módulo de extracción
python src/extraccion.py

# Módulo de transformación (próximamente)
# python src/transformacion.py

# Módulo de carga (próximamente)
# python src/carga.py
```
### 5.2 Para ejecutar la canalización ETL completa:
```bash
python dags/pipeline.py
```

## Where users can get help with your project :: ¿Dónde pueden los usuarios obtener ayuda con el proyecto?

Quienes estén interesados o requieran orientación o ayuda pueden contactar a los formuladores principales: CP. Esp. Brayan Valencia Sánchez (brayan.valencia_san@uao.edu.co) y el Ing. Esp. Giancarlo Libreros Londoño (giancarlo.libreros@uao.edu.co), a través de los correos electrónicos indicados.

## Who maintains and contributes to the project :: ¿Quién(es) mantiene(n) y contribuye(n) al proyecto?

En principio estas labores son hechas por el CP. Esp. Brayan Valencia Sánchez y el Ing. Esp. Giancarlo Libreros Londoño, quienes al momento de escribir la primera versión de este README son estudiantes de la maestría en Inteligencia Artificial y Ciencias de Datos de la Universidad Autónoma de Occidente (2026-1).
