# Caracterización de las Fuentes de Datos

Como alistamiento para desarrollar la canalización ETL propuesta en este proyecto, se presenta esta caracterización de las fuentes de datos en términos estructurales y de calidad. Se aclara que se hace sobre las fuentes originales, sin ninguna transformación hecha o cambio de formato de recepción. Complementariamente, la caracterización aplicada combina elementos metodológicos del estándar de facto Data Profiling, de DAMA-DMBOK, y de la ISO 25012.

## 1. "COMISIONES AÑO 2025.xlsx"

Esta fuente registra comisiones bancarias y gastos de impuesto 4x1000 de la empresa objetivo durante el año 2025. Contiene múltiples hojas, incluyendo tablas dinámicas y una hoja de datos transaccionales principal. Su caracterización es la siguiente:

| **Atributo**              | **Descripción**                                                                                                                      |
|---------------------------|--------------------------------------------------------------------------------------------------------------------------------------|
| **Nombre del archivo**    | COMISIONES AÑO 2025.xlsx.                                                                                                            |
| **Temática**              | Comisiones bancarias y gastos financieros (impuesto 4x1000).                                                                         |
| **Número de hojas**       | 7 hojas: TD, TD (espacio), COMISIONES ENERO-MARZO 2025, COMISIONES ENERO-MARZO 2025 (2), COMISIONES, 4 x 1000, datos.                |
| **Hoja principal**        | COMISIONES --- 283 registros × 24 columnas.                                                                                          |
| **Cobertura temporal**    | Enero -- junio de 2025.                                                                                                              |
| **Variables clave**       | CUENTA, Auxiliar, Desc. auxiliar, Neto, Fecha, Docto., Razón social tercero movto., Mes, Nombre Mes, Débitos, Créditos.              |
| **Tipos de datos**        | Texto (str), numérico (int/float), fecha (datetime).                                                                                 |
| **Valores nulos**         | Columnas C.Costo, Desc. C.Costo, SECCION y Referencias 1/2/3 presentan 100% de nulos. El resto de las columnas está bien completado. |
| **Rango del campo: Neto** | Mínimo: -\$67.603.541 / Máximo: \$67.603.541 / Suma total: \$628.873.629.                                                            |
| **Calidad general**       | Aceptable. Contiene hojas duplicadas o auxiliares y varias columnas completamente vacías que deben depurarse.                        |
| **Formato**               | Excel (.xlsx) con tablas dinámicas en hojas TD.                                                                                      |

## 2. "Intereses Sobregiro.xlsx"

Esta fuente consigna los registros contables de movimientos asociados a intereses por sobregiro bancario. Contiene una sola hoja con datos transaccionales de todos los meses del año.

| **Atributo**                             | **Descripción**                                                                                                                   |
|------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| **Nombre del archivo**                   | Intereses Sobregiro.xlsx.                                                                                                         |
| **Temática**                             | Movimientos contables de intereses por sobregiro bancario.                                                                        |
| **Número de hojas**                      | 1 hoja: Intereses.                                                                                                                |
| **Cantidad total de registros y campos** | 768 filas × 25 columnas (757 contienen datos reales).                                                                             |
| **Cobertura temporal**                   | Enero -- diciembre (todos los meses); registros hasta enero 2026.                                                                 |
| **Variables clave**                      | CUENTA, Auxiliar, Desc. auxiliar, Neto, Fecha, Docto., Razón social tercero movto., Mes, Nombre Mes.                              |
| **Tipos de datos**                       | Texto (str), numérico (float), fecha (object/datetime --- tipo inconsistente).                                                    |
| **Valores nulos**                        | C.Costo, Desc. C.Costo y columnas Unnamed (16--22) con 100% de nulos. Aproximadamente 11 filas sin datos en campos clave.         |
| **Rango del campo Neto**                 | Mínimo: -\$791.082 / Máximo: \$633.099 / Suma total: \$16.317.744.                                                                |
| **Calidad general**                      | Buena en los registros válidos. Presenta columnas residuales sin nombre (Unnamed) y tipo de dato inconsistente en el campo Fecha. |
| **Formato**                              | Excel (.xlsx) con una sola hoja de datos.                                                                                         |

## 3. "tasas sobregiro.xlsx"

Esta fuente consolida los cupos de crédito y las tasas de sobregiro vigentes por entidad bancaria. A diferencia de las otras fuentes, no-registra datos transaccional sino un documento de consulta con estructura semiestructurada.

| **Atributo**                             | **Descripción**                                                                                                                            |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| **Nombre del archivo**                   | tasas sobregiro.xlsx.                                                                                                                      |
| **Temática**                             | Tasas de sobregiro y cupos de crédito por entidad bancaria.                                                                                |
| **Número de hojas**                      | 1 hoja: Creditos.                                                                                                                          |
| **Cantidad total de registros y campos** | 42 filas × 6 columnas (estructura semiestructurada, no tabular estándar).                                                                  |
| **Cobertura temporal**                   | Sin fechas explícitas; datos de referencia estáticos con algunas notas de vigencia.                                                        |
| **Entidades bancarias**                  | Bancolombia, Davivienda, Banco Bogotá, Banco Popular, Itaú, Banco de Occidente, Serfinanzas, BBVA.                                         |
| **Variables clave**                      | Entidad, Valor del cupo (\$), Tasa de sobregiro (decimal), Tasa equivalente, Notas y condiciones.                                          |
| **Tipos de datos**                       | Texto (str) y numérico (float); sin encabezados formales en el archivo.                                                                    |
| **Valores nulos**                        | Alto porcentaje de nulos de forma estructural, producto del diseño no tabular de la hoja.                                                  |
| **Secciones identificadas**              | 1\) Cupos de crédito por banco 2) Tasas de sobregiro anual y mensual por entidad.                                                          |
| **Calidad general**                      | Baja estructuración. Los datos son válidos, pero están dispersos en celdas sin encabezados formales. Requiere limpieza para uso analítico. |
| **Formato**                              | Excel (.xlsx) utilizado como documento de referencia más que como registro tabular.                                                        |

En general, la tres fuentes están relacionadas con la gestión financiera y bancaria de la empresa objetivo. "COMISIONES AÑO 2025.xlsx" e "Intereses Sobregiro.xlsx" albergan registros transaccionales con buena estructuración para análisis, aunque sometibles a transformación, mientras que "tasas sobregiro.xlsx" es un documento de referencia que requeriría normalización previa para ser cruzado con las otras fuentes.
