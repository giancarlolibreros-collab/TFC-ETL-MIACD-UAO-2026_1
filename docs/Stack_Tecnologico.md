# 4. Stack Tecnológico de la Canalización ETL

La definición del stack tecnológico responde a tres criterios fundamentales: alineación con el currículo del curso de ETL[^1] (Python, SQL y herramientas ETL especializadas), viabilidad técnica en el entorno académico disponible (UAO[^2], equipos propios), y coherencia con las capacidades técnicas del equipo de trabajo. El stack tecnológico propuesto cubre las tres fases de la canalización: Extracción, Transformación, Carga, además de la Visualización y Reportes.

## 4.1 Visión General del Stack Tecnológico y su Justificación {#visión-general-del-stack-tecnológico-y-su-justificación}

El panorama del stack tecnológico queda definida como se muestra a continuación:

| **Fase**       | **Herramienta**          | **Tecnología** | **Descripción**                                                      |
|----------------|--------------------------|----------------|----------------------------------------------------------------------|
| Extracción     | openpyxl y pandas        | Python         | Lectura de archivos .xlsx y construcción de data frames.             |
| Transformación | pandas                   | Python         | Limpieza, filtrado, cálculo de indicadores.                          |
| Carga          | SQLite / MySQL           | SQL            | Almacenamiento en base de datos analítica local.                     |
| Visualización  | Matplotlib y Seaborn     | Python         | Generación de reportes y gráficas señalando indicadores por periodo. |
| Orquestación   | Scripts modulares Python | Python         | Ejecución de la canalización completa.                               |
| Versionamiento | Git y GitHub             | GitHub         | Control de versiones y entregable final del curso.                   |

Las justificaciones de las elecciones tecnológicas se expresan en los siguientes términos:

**Python:** es el lenguaje principal de la canalización por tres razones: está explícitamente contemplado en el currículo del curso como herramienta para extracción y transformación de datos; el equipo de trabajo lo maneja actualmente; y su ecosistema de librerías (por ejemplo, openpyxl, pandas, matplotlib, seaborn, entre otras) cubre todas las fases de la canalización, incluso las relacionada con visualización y reportes.

**SQL:** SQLite como base de datos local para el entorno de desarrollo académico tiene la capacidad de migración a MySQL en un entorno productivo. SQLite no-requiere servidor, es portable y se integra nativamente con Python.

**Git y GitHub:** con estas tecnologías la gestión de versiones y de la colaboración garantiza la trazabilidad del desarrollo del trabajo de final de curso.

## 4.2 Arquitectura de la Canalización ETL y su Viabilidad Técnica {#arquitectura-de-la-canalización-etl-y-su-viabilidad-técnica}

La arquitectura de la canalización ETL queda definida por el siguiente flujo de datos:

| **Fase**          | **Actividad**                                                        | **Salida**                                         |
|-------------------|----------------------------------------------------------------------|----------------------------------------------------|
| 1: Extracción     | Lectura de archivos .xlsx y filtrado por subcuenta contable.         | Data frames por: sobregiro, factoring, y tasas.    |
| 2: Transformación | Limpieza, tipado, normalización, cálculo de indicadores por periodo. | Data frames limpios y tabla de hechos consolidada. |
| 3: Carga          | Inserción en base de datos analítica.                                | Base de datos analítica.                           |
| 4: Visualización  | Generación de reportes con base en indicadores por periodo.          | Reportes ejecutivos para los clientes o usuarios.  |

La viabilidad técnica de las tecnologías y herramientas asociadas con la arquitectura expuesta queda determinada por los siguientes factores: son de código abierto, gratuitas e instalables mediante **pip**[^3] sin licencias de pago; el stack es compatible con los entornos Windows disponibles en las salas de sistemas de la UAO y en los equipos personales del equipo de trabajo; y, la curva de aprendizaje incremental necesaria es coherente con el nivel del programa de maestría y el tiempo disponible para cumplir con la entrega del trabajo de final de curso.

[^1]: Extract, Transform, Load.

[^2]: Universidad Autónoma de Occidente.

[^3]: Python Package Index.
