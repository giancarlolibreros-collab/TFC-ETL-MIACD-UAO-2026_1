# Definición del Problema

El objetivo de este documento es definir el **Contexto** y el **Problema** por enfrentar 
como trabajo final del curso de **ETL** (extracción, transformación y carga).

Los proponentes son **Brayan Valencia Sánchez**: contador público de la Universidad del Valle
y especialista en finanzas de la Universidad Autónoma de Occidente; actualmente se desempeña
como analista de crédito y riesgo del Ingenio Carmelita S.A. Y, **Giancarlo Libreros Londoño**:
Ingeniero Industrial de la Universidad del Valle y especialista en estadística aplicada
de la Fundación Universitaria Los Libertadores; a la fecha se desempeña como docente auxiliar
del Sistema de Regionalización de la Universidad del Valle en las áreas de matemáticas, física,
estadística y gestión de datos.

Bajo compromiso previo de trabajo, los proponentes decidieron desarrollar entre ambos, y mientras
sea posible, los trabajos exigidos en los cursos de la maestría para aprovechar el acceso de primera
mano a fuentes de datos financieras sobre la empresa azucarera que es reconocida como una de las de tipo
agroindustriales más importantes del suroccidente colombiano, que aporta, en sus mejores temporadas
productivas, hasta un 5 % de la producción colombiana de azúcar y alrededor de 800.000 toneladas de caña
molida al año, y que exporta azúcar y mieles a más de 25 países, con crecimiento reciente en el mercado
ecuatoriano, chileno y de Estados Unidos de Norteamérica.

Así, las siguientes especificaciones de **Contexto** y **Problema** están relacionados con aspectos
de dicho sector productivo.

## 1.  **Contexto** (dónde ocurre la necesidad o problema identificado)

El aspecto problemático por enfrentar se sitúa en el Ingenio Carmelita S.A., empresa del sector azucarero
del Valle del Cauca, cuya operación requiere altos niveles de capital de trabajo y una gestión cuidadosa
de la liquidez. Para sostener el volumen de ventas, especialmente con grandes superficies y clientes
de alto cupo, el ingenio utiliza instrumentos financieros como el **factoring**[^1] y los **sobregiros**[^2] bancarios
con entidades como Bancolombia, Davivienda y Banco de Bogotá, para lo cual asume gastos financieros, pero,
con posibilidades de optimizar la elección de bancos, productos y condiciones de uso de los esos instrumentos.

A través del factoring, el ingenio cede sus facturas a varias entidades financieras para obtener
liquidez inmediata, mientras que el cliente les paga a los bancos en plazos de 30 a 60 días. Esta práctica, necesaria
para evitar cuellos de botella comerciales y liberar cupos de crédito a clientes, ha generado gastos financieros
anuales estimados entre 1.500 y 2.000 millones de pesos solo por intereses financieros asociados al factoring y sobregiros.

## 2.  **Caracterización del usuario** (perfil del usuario o cliente)

El usuario principal es el área de **planeación financiera** del Ingenio Carmelita S.A., en particular
el **analista de crédito y riesgo** responsable del análisis de los gastos financieros. Este rol requiere
balancear la necesidad de liquidez inmediata con la presión por mantener la rentabilidad de la compañía
y controlar el nivel de gastos financieros, dentro de los límites de cupos de crédito definidos
para cada cliente.

Asimismo, se identifican los siguiente usuarios vinculados con las responsabilidades directas
de la toma de decisiones mencionadas: **dirección financiera** (que es el nivel organizacional
con el que está en situación de dependencia jerárquica **planeación financiera**). Esta dirección funge
por la disminución de gastos financieros y sus impactos sobre el resultado neto anual. También, está el **área comercial**
que se responsabiliza de la venta cuando aún en situaciones de copamiento de los cupos de crédito
de los clientes, y por negociar precios que incorporen parte del costo financiero en el precio de los productos
ofertados por la compañía. Y, la **gerencia general** que demanda una visión integral de los escenarios
de uso de factoring y sobregiros, para definir políticas comerciales y financieras de mediano plazo.

## 3.  **Problema identificado** (explicación de la situación anómala detectada)

Para comprender mejor la situación problemática se presenta un paralelo de causas y efectos relacionados
con ella en donde las causas se subclasifican, pero los efectos se generalizan:

<table>
<colgroup>
<col style="width: 49%" />
<col style="width: 50%" />
</colgroup>
<thead>
<tr class="header">
<th colspan="2">Causas</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><p>Por la gestión financiera:</p>
<ul>
<li><p>Uso intensivo de factoring, dada una estructura de cupos de crédito internos, para evitar
la detención de ventas cuando los clientes los copan y pagan entre 30 a 60 días, es decir, mantener
la necesidad imperiosa de liquidez.</p></li>
<li><p>Dependencia de sobregiros bancarios para cumplir pagos a proveedores cuando no se recurre al factoring.</p></li>
<li><p>Negociaciones comerciales que frecuentemente obvian incorporar explícitamente el costo financiero
en el precio final de los productos ofertados por la empresa.</p></li>
</ul></td>
<td><p><strong>Por el manejo de la información</strong>:</p>
<ul>
<li><p>Existencia de información dispersa en distintas fuentes (facturación, cupos, tasas, cuentas bancarias,
condiciones comerciales), sin un proceso formal de ETL que consolide y limpie los datos para análisis riguroso.</p></li>
<li><p>Falta de un análisis sistemático de datos que identifique el punto de equilibrio entre factoring,
sobregiros y alternativas como la posibilidad de implementar programas de pronto pago.</p></li>
<li><p>Ausencia de modelos de escenarios que cuantifiquen el impacto de las políticas de uso del factoring
y los sobregiros en los gastos financieros y las ventas.</p></li>
</ul></td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>Efectos</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><ul>
<li><p>Gastos financieros anuales entre 1.500 y 2.000 millones de pesos solo por el rubro de gastos financieros
asociados a factoring y sobregiros.</p></li>
<li><p>Disminución de la rentabilidad al cierre del periodo y menor capacidad para invertir en otros proyectos
estratégicos.</p></li>
<li><p>Riesgo de decisiones subóptimas, por ejemplo, usar factoring por costumbre sin evidencia del punto
de equilibrio con sobregiro.</p></li>
<li><p>Conflicto de objetivos entre el área comercial (mantener ventas) y el área financiera
(reducir gastos financieros), sin un marco de datos unificado para negociar decisiones.</p></li>
</ul></td>
</tr>
</tbody>
</table>

Con base en lo expuesto se puede identificar un problema de gestión financiera manifestado por la existencia
de gastos financieros elevados relacionados con el uso combinado de los instrumentos financieros conocidos
como factoring y sobregiros, que reducen significativamente la rentabilidad anual del Ingenio Carmelita S.A.

## 4.  **Fuentes de datos** (especificación de las posibles fuentes de datos)

La especificación de las posibles fuentes de datos se describe en tres categorías, como muestra el siguiente
esquema:

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr class="header">
<th>Fuentes Internas Estructuradas</th>
</tr>
</thead>
<tbody>
<tr class="odd">
<td><ul>
<li><p>Sistema de facturación y cartera: facturas emitidas (fecha, cliente, monto, plazo, tasa implícita
si la hay). Estados de cuenta de clientes, cupos asignados, cupo utilizado, cupo disponible. Información
sobre facturas cedidas en factoring (fecha de cesión, tasa, entidad financiera, valor anticipado).</p></li>
<li><p>Sistema contable y financiero: registro de gastos financieros por factoring y sobregiros por periodo
(mensual, anual). Tasas de interés pactadas con cada banco para sobregiros y factoring. Estados de sobregiros
por banco, cupos autorizados y utilizados.</p></li>
<li><p>Sistema de compras y proveedores: calendario de pagos a proveedores, montos y fechas. Historial de uso
de sobregiros para cubrir pagos a proveedores.</p></li>
<li><p>Información comercial: condiciones comerciales por cliente (precios por quintal, descuentos, acuerdos
de pronto pago). Historial de negociaciones donde se haya intentado incorporar el costo financiero al precio
de venta.</p></li>
</ul></td>
</tr>
<tr class="even">
<td>Fuentes Internas Semi-estructuradas o No-estructuradas</td>
</tr>
<tr class="odd">
<td><ul>
<li><p>Correos, memorandos o minutas de reuniones de tesorería y comercial donde se discuten políticas
de factoring, sobregiros y pronto pago.</p></li>
<li><p>Plantillas Excel usadas por analistas para cálculos ad hoc<a href="#fn1" class="footnote-ref" id="fnref1" role="doc-noteref"><sup>1</sup></a> de gastos financieros.</p></li>
</ul></td>
</tr>
<tr class="even">
<td>Fuentes Externas</td>
</tr>
<tr class="odd">
<td><ul>
<li><p>Información de mercado sobre tasas promedio de factoring y sobregiro en el sector.</p></li>
<li><p>Referencias normativas o regulatorias sobre factoring en Colombia.</p></li>
</ul></td>
</tr>
</tbody>
</table>
<aside id="footnotes" class="footnotes footnotes-end-of-document" role="doc-endnotes">
<hr />
<ol>
<li id="fn1"><p>Vocablo en latín que se refiere a: “para este fin”.<a href="#fnref1" class="footnote-back" role="doc-backlink">↩︎</a></p></li>
</ol>
</aside>

Con lo expuesto en el esquema se entiende que el problema identificado es susceptible de ser enfrentado
con datos.

## 5.  **Definición de los OKR y KPIs** (especificación de los Objetivos y Resultados Clave e Indicadores Clave de Rendimiento)

Los objetivos y resultados clave (OKR) por alcanzar al enfrentar el problema quedan propuestos así:

> **OKR1**: Reducir el peso de los gastos financieros asociados a factoring y sobregiros en la operación
del ingenio, sin sacrificar el nivel de ventas.
>
> ***OKR1.1***: Disminuir el gasto financiero anual por factoring y sobregiros comprendido
entre 1.500 y 2.000 millones de pesos a un rango entre 800 y 1.200 millones en un horizonte de 1 a 2 años.
>
> ***OKR1.2***: Mantener o incrementar en al menos un 3 % a 5 % el volumen de ventas a clientes
de grandes superficies durante el mismo periodo.
>
> **OKR2**: Optimizar la mezcla de instrumentos financieros (factoring y sobregiros) a partir de evidencia
basada en datos.
>
> ***OKR2.1***: Definir y documentar un punto de equilibrio cuantitativo entre el uso de factoring
y sobregiro para los principales clientes según plazos.
>
> ***OKR2.2***: Diseñar al menos un escenario de programa de pronto pago que redireccione parte
de los gastos financieros hacia descuentos por pronto pago.
>
> **OKR3**: Consolidar un pipeline ETL (o canalización ETL) automatizado que soporte el análisis recurrente
de decisiones financieras y comerciales.
>
> ***OKR3.1***: Implementar un flujo ETL que integre fuentes de datos (por ejemplo, de facturación, 
contabilidad y bancos) y lo cargue en una base de datos analítica o smart-data[^3] financiero.
>
> ***OKR3.2***: Generar reportes periódicos (mensuales) con indicadores clave para las direcciones financiera
y comercial, que responden a la gerencia general.

Ahora, los indicadores claves de rendimiento (KPIs) se proponen a través de la siguiente lista:

- Gasto financiero anual total por factoring (en pesos).

- Gasto financiero anual total por sobregiro (en pesos).

- Gasto financiero total como porcentaje de la facturación anual.

- Días promedio de cartera por segmento de cliente (con y sin factoring).

- Porcentaje de facturación cedida a factoring (sobre ventas totales).

- Porcentaje de uso de cupos de sobregiro por entidad financiera.

- Margen neto por unidades de medida de los productos ofertados por la empresa vendidos a clientes clave,
antes y después de incorporar el costo financiero en el precio.

- Monto anual de descuentos otorgados por programas de pronto pago (si se implementan) y su efecto
sobre gastos financieros (en términos absolutos y relativos).

Estos OKR y KPIs propuestos se entiende que están alineados con las posibilidades de que las fuentes de datos
provean lo que corresponda.

## 6.  **Formulación de las preguntas estratégicas o de negocio para responder con el Pipeline**[^4] **ETL** (canalización ETL)

Son propuestas las siguientes preguntas para que con el soporte de la canalización ETL se puedan ayudar
a responder como apoyo para la toma de decisiones en referencia al problema de gestión financiera planteado
en el inciso 3 de este documento:

> ¿Cuál es el costo financiero promedio efectivo (por peso facturado) de utilizar factoring
frente al de utilizar sobregiros, por periodo?
>
> ¿Cuál es el punto de equilibrio (en volumen de facturas o monto) a partir del cual conviene más
el factoring que el sobregiro, o viceversa, bajo las tasas actuales de los bancos?
>
> ¿Qué impacto tendría reducir el gasto financiero, actualmente entre 1.500 y 2.000 millones, a 800 millones
aplicando un plan de descuento por pronto pago (si la gerencia general y la dirección financiera
toman la decisión de implementarlo), sobre la rentabilidad y el flujo de caja?
>
> ¿Cómo cambian los días promedio de cartera y el uso de cupos de crédito internos si se aplica
un plan de descuento por pronto pago?
>
> ¿Qué combinación de instrumentos (porcentaje de facturas con factoring, nivel de sobregiro, 
porcentaje de clientes en pronto pago) minimiza el gasto financiero manteniendo o mejorando el nivel de ventas?
>
> ¿En qué medida las decisiones comerciales de precio final aplicado a los productos ofertado
por la empresa compensan el costo financiero sin perder competitividad?

Las preguntas formuladas muestran que se captura la lógica causal necesaria para enfrentar un problema
basado en datos que requiere una canalización ETL como apoyo para la toma de decisiones, en este caso
de gestión financiera, que faciliten acceder de manera efectiva a los datos generados por la empresa
y por terceros en el contexto indicado.

[^1]: El **factoring** es un instrumento financiero de corto plazo mediante el cual una empresa vende
o cede sus facturas pendientes de cobro (cuentas por cobrar) a una entidad financiera o empresa especializada
(llamada "factor"), a cambio de liquidez inmediata, aunque con un descuento. El factoring permite
que una empresa adelante el cobro de sus ventas a crédito, a cambio de una comisión para el factor, así: 
en lugar de esperar los 30, 60 o 90 días que fijó el cliente, la empresa de manos del factor
recibe un porcentaje del valor de las facturas en efectivo de forma rápida, mientras el factor
asume la gestión de cobro y, en algunos casos, el riesgo de impago.

[^2]: Un **sobregiro** bancario es una situación en la que una cuenta corriente, de ahorros o similar
queda con saldo negativo porque el cliente efectúa pagos o retiros que exceden el dinero disponible
en la cuenta y el banco acepta de igual manera la operación.

[^3]: Smart-data financiero hace referencia a la aplicación de datos inteligentes en el ámbito financiero,
es decir, datos financieros que han sido filtrados, procesados y analizados para que sean relevantes,
precisos y usables en la toma de decisiones financieras, económicas y de negocio.

[^4]: Un Pipeline ETL o Canalización ETL es un flujo de trabajo automatizado que extrae datos de una o varias
fuentes, los transforma; es decir, limpia, integra y adapta, y luego los carga en un sistema de destino,
por ejemplo, un almacén de datos, un lago de datos o una base de datos analítica.
