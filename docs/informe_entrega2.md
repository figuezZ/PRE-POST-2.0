# PRE/POST 2.0 — Informe de Entrega 2

Borrador para revisión | 27-10-2026 | v2.1.0-rc1 | Grupo XX pendiente

## 1. Introducción y objetivos del Avance 2

PRE/POST 2.0 es una herramienta académica para analizar vigas de hormigón pretensado. Este borrador documenta la evolución desde la entrega del 10 de septiembre y prepara el hito del 27 de octubre de 2026, fecha corregida por el equipo respecto de la pauta. Grupo: XX, pendiente de confirmar. Integrantes: Estefanía, Rocío, Pedro y José.

El objetivo de esta versión es hacer comprensible y reproducible el recorrido desde geometría, cargas y fuerza inicial hasta pérdidas, tensiones y verificaciones. Se conserva el cálculo elástico ya probado y se añade una extensión limitada al rectángulo pretesado recto. La simplificación consiste en organizar la interacción en cuatro etapas y concentrar las ecuaciones en un núcleo único.

Estado de emisión: borrador técnico para revisión del equipo. Se han ejecutado pruebas automáticas; no se han incorporado cálculos manuscritos, firmas de revisión ni evidencias de aportes personales. Los criterios de CIRSOC y el método histórico FHWA están identificados, pero su adopción para el curso no está ratificada. No corresponde declarar cumplimiento integral de la entrega ni certificación estructural.

## 2. Antecedentes del Avance 1 y retroalimentación

Se revisaron la pauta oficial, el informe realmente entregado en septiembre, las dos imágenes de observaciones del profesor y la guía de ejercicios de 24 páginas. También se recuperaron las cuatro guías complementarias de clases sobre momento nominal, resolución de Clase 4 y cargas equivalentes. El ejemplo resuelto utiliza ACI 318-19, mientras otras guías remiten a ediciones posteriores. Es necesario confirmar qué edición y procedimiento exige el docente para esta aplicación.

El Avance 1 presentaba migración a Python/Streamlit, geometría rectangular y taller compuesto, estática, superposición elástica, memoria y exportaciones. La pérdida era un porcentaje ingresado. No calculaba mecanismos diferidos ni verificaba resistencia o flecha. El análisis de vacíos no equivalía a una sección transformada con acero.

La observación principal exige resolución física en papel y lápiz de todos los procedimientos estructurales, con unidades, sustitución, interpretación y revisión. Se responde con doce fichas y una matriz función–ecuación–ficha–prueba. Este material prepara el trabajo; no satisface por sí solo la exigencia de manuscritos.

La exigencia de participación se aborda con una bitácora verificable y revisión cruzada propuesta. Se evita atribuir al equipo decisiones o hallazgos producidos durante la asistencia automatizada. Cada afirmación de trabajo humano deberá vincularse a una evidencia original.

## 3. Evolución del proyecto

El HEAD consultado al inicio era d59181bcd2a3e111d2d0692dd53a2572aad2169e, la misma referencia del informe de septiembre. No existían cambios posteriores en la rama examinada. La auditoría ejecutó 70 pruebas aprobadas y 15 controles analíticos antes de modificar el código. Por tanto, los desarrollos aquí descritos corresponden a esta nueva intervención, no a trabajo previo supuesto.

Los archivos originales inputs.py, rectangular.py y elastic.py permanecen sin cambios. La extensión agrega opciones explícitas, pérdidas, propiedades auxiliares y verificaciones; el pipeline mantiene una sola fuente de resultados para pantalla y exportación. La tabla resume las acciones y su evidencia.

| Avance 1 | Acción en Avance 2 | Evidencia |

| --- | --- | --- |

| Geometría, ejes paralelos y taller | Sección neta/transformada auxiliar añadida | F01–F03; tests/test_sections.py y test_design.py |

| Estática y superposición elástica | Mantener signos; fuerzas de etapas actualizadas | F04–F05; regresión contra JS |

| Pérdida global declarada | Modo FHWA acotado y opción histórica | F06; compatibilidad y sensibilidad |

| Ausencia de criterios resistentes | Añadir criterios preliminares con guardas | F07–F11; equilibrio, integración, referencia externa |

| Cinco pestañas de resultados | Dos pestañas; cuatro etapas; expansores | AppTest; preservación SI/USCS |

| Caso base/15 controles | Caso B adaptado y B2 corte; prueba fuente crítica | JSON de validación y auditoría de guía |

| Informe septiembre y memoria | Informe nuevo, fichas y bitácora pendiente | Documentos editables; contribuciones.md |

## 4. Fundamentos y modelo estructural

La viga es prismática y simplemente apoyada; recibe cargas uniformes gravitatorias y un tendón equivalente recto. Se asumen pequeñas deformaciones, hormigón normal y adherencia perfecta. La extensión resistente se limita a sección rectangular, tendón inferior o centrado, sin acero pasivo longitudinal. No se extrapola a secciones T/I, postensado o cargas concentradas.

El núcleo usa m, N y Pa. La compresión es negativa; y y e son positivos hacia arriba desde el centroide; el momento externo sagante es positivo. Un tendón inferior tiene e<0. Con A=bh, I=bh³/12 y W=I/c, la tensión resulta σ(y)=−P/A−(Pe+M)y/I. En esta ecuación Pe representa el producto P·e; la fuerza efectiva se escribe Pef cuando se necesita evitar ambigüedad.

Para carga w: R=wL/2, V(x)=R−wx y M(x)=Rx−wx²/2. Transferencia utiliza peso propio g=γA y fuerza Pt después de ES; servicio utiliza g+qD+qL y fuerza efectiva. La tensión de servicio no se obtiene restando simplemente un porcentaje a la tensión de transferencia: también cambia la carga externa.

En el taller, Ai tiene signo positivo para sólido y negativo para vacío; Y=ΣAiYi/ΣAi e I=Σ[Ii+Ai(Yi−Y)²]. Se conservan guardas geométricas y se identifica el campo prolongado en vacíos. Las propiedades neta y transformada nuevas descuentan acero concentrado y agregan nAp, con n=Ep/Ec. Se informan como auxiliares: el análisis de clase U conserva propiedades brutas.

El caso A usa L=10 m, b=.4 m, h=.8 m, γ=25 kN/m³, fci=35 MPa, fc=45 MPa, P0=1000 kN, e=−.2 m, Ap=700 mm² y qL=5 kN/m. Los nuevos valores de demostración son Ep=195 GPa, Eci=30 GPa, Ec=34 GPa, humedad 70%, fpu=1860 MPa, fpy=1674 MPa, estribos de dos ramas de 8 mm cada 200 mm y cordón de 12.7 mm. No son propiedades ensayadas ni decisiones humanas confirmadas.

## 5. Desarrollo de nuevas funcionalidades

Pérdidas. Se implementó FHWA-NHI-04-043, Design Step 5.4, método histórico para pretesado de baja relajación. Con n=Ep/Eci y k=1/A+e²/I, ES=n(P0k+Mg e/I)/(1+nApk). Esta forma satisface compatibilidad usando la fuerza posterior al acortamiento: Pt=P0−ApES. Se evita descontar ES dos veces.

La retracción se estima SH=(17−.15H) ksi; 1 ksi=6 894 757.293168 Pa. La fluencia es CR=max(0,12fcgp−7fcdp), donde fcgp es compresión en el tendón al transferir y fcdp el alivio por carga permanente posterior. La relajación es RE=max(0,.3[20ksi−.4ES−.2(SH+CR)]). Pef=Pt−Ap(SH+CR+RE). No se suma la pérdida porcentual histórica. Se rechazan fuerza efectiva no positiva y dominio incompatible.

Tensiones. La envolvente desarrollada se obtiene en lt, L/2 y L−lt, con lt=50 diámetros. CIRSOC 201-2005, 18.4: compresión ≤.6fci en transferencia, ≤.6fc en servicio total y ≤.45fc bajo cargas permanentes. La tracción general de transferencia se limita a .25√fci MPa. La clasificación U/T/C de 18.3.3 usa .7√fc y √fc; el objetivo de la extensión es clase U. El acero después de transferencia se compara con min(.74fpu,.82fpy). El máximo del gato y sus condiciones permanecen pendientes.

Flexión. La demanda es Mu=max(1.4D,1.2D+1.6L)·Luz²/8. Se adopta la aproximación de 18.7.2(a): fps=fpu[1−(γp/β1)ρp fpu/fc], ρp=Ap/(b dp), a=Ap fps/(.85fc b), c=a/β1 y Mn=Ap fps(dp−a/2). β1 se reduce desde .85 para fc>30 MPa, a razón .05 por 7 MPa, con mínimo .65. γp depende de fpy/fpu. Se exige fpe≥.5fpu y dominio controlado por tracción para aplicar φ=.9. La resistencia mínima se compara con 1.2Mcr. No se asume fps=fpy.

Corte. Se evalúa x=d con d=max(dp,.8h), bajo reacción que comprime el extremo y carga superior. La expresión simplificada 11.4.2 tiene Vc=[√fc/20+5min(Vu dp/M,1)]bd, entre √fc bd/6 y .4√fc bd. En SI, los coeficientes de tensión se convierten desde MPa. Cerca del extremo se aplica el límite Vcw con compresión reducida según 11.4.4. Vs=Av fy d/s; se verifican φ=.75, cuantía mínima, límite de Vs y separación máxima. El procedimiento requiere Pef≥.4Ap fpu y no resuelve anclaje ni desarrollo.

Servicio. La flecha instantánea central no fisurada se obtiene por integración: δ=5wL⁴/(384EcI)+Pef e L²/(8EcI), positiva hacia abajo. La parte viva se compara con L/360 como criterio de demostración configurable. Se bloquea esa conclusión para clases T/C. La flecha diferida requiere edades, rigidez e historia temporal: permanece pendiente aunque existan pérdidas diferidas calculadas.

Los límites se usan como referencia académica CIRSOC 201-2005 y no como norma del curso ya confirmada. Las fuentes y cláusulas completas están en docs/metodo_avance2.md. Los valores por defecto son hipótesis editables de demostración.

Contraste docente. La guía de momento nominal propone compatibilidad iterativa con la curva del acero; este módulo implementa una aproximación y no reproduce esa iteración. El ejemplo docente de cargas equivalentes utiliza ACI 318-19 y β1=.80 para fc=35 MPa; CIRSOC en esta versión produce .8142857. No son bases intercambiables. La unificación normativa y el procedimiento requerido permanecen pendientes; ver docs/contraste_material_docente.md.

## 6. Metodología de cálculo y validación manual

El respaldo manual debe elaborarse antes de comparar con la aplicación. Cada integrante imprimirá las fichas asignadas, identificará fuente y unidades, dibujará el sistema y resolverá las operaciones físicamente. Después registrará el resultado del programa y calculará diferencia absoluta y relativa. Si el valor manual es cero, se informará diferencia absoluta y no se dividirá por cero.

Las doce fichas cubren geometría, ejes paralelos y vacíos, sección transformada, estática, campo de tensiones, pérdidas, límites, fisuración/cargas, flexión, corte, flecha y reproducción de unidades/etapas. Para F02 se deben repetir T, I y hueca; F05 debe revisar varias posiciones y fibras. Una tabla final generada no reemplaza esos desarrollos.

El revisor debe trabajar con ecuaciones y datos de fuente, sin copiar resultados del programa. Debe examinar signo, orden de magnitud, equilibrio y restricciones. Las diferencias se investigan antes de cambiar tolerancias. En el caso externo se conserva por separado el valor publicado incorrecto y su recomputación independiente.

Anexo manual M: PENDIENTE. Incorporar fotografías o escaneos originales con nombre Fxx_integrante_fecha, sin simular manuscritos. La ficha impresa, el informe y la memoria automática son guías, no evidencia de autoría ni resolución física. La matriz de cobertura mantiene todos los procedimientos pendientes hasta que exista evidencia revisada.

## 7. Casos de referencia

Caso A histórico. Conserva los datos del Avance 1 y pérdida declarada 15%; Pef=850 kN. Contrasta propiedades, momentos y tensiones con valores analíticos fijos del informe previo. Este caso prueba continuidad y regresión, no el nuevo modelo de pérdidas. El caso A ampliado activa mecanismos sin modificar artificialmente sus entradas para obtener aprobación.

Caso B externo adaptado. El ejercicio 1 aporta b=.4 m, h=.9 m, dp=.8 m, fc=30 MPa, Ms=1000 kN m, Ap=1220 mm² y Pef=1403 kN. Para conectarlo a la viga uniforme se toma L=15 m del ejercicio 2 y w=35.5555556 kN/m. Se descuenta g=9 kN/m para obtener qL=26.5555556 kN/m. La pérdida declarada 15% solo permite reconstruir la fuerza efectiva; no es un resultado de la guía ni valida pérdidas.

La fuente publica tensión objetivo 5.48 MPa. Con sus datos P=1403 kN, la sustitución independiente da 1000000/.054−1403000(1/.36+.35/.054)=5.527777778 MPa, diferencia .047777778 MPa, aproximadamente .871857%. Resolver para √30 MPa exige P=1408.459638 kN. No se aumenta la tolerancia para aceptar el valor publicado: se documenta la discrepancia y se conserva el número original como antecedente.

El ejercicio 1 es adaptable para geometría y tensiones; su resistencia literal no se acepta como patrón porque omite el factor .85 en el bloque, supone fps=fpy y presenta una multiplicación inconsistente. La comparación resistente del programa utiliza su propia referencia normativa explícita y controles de equilibrio independientes.

El ejercicio 2 es compatible como control local B2 de corte: wu=53.76 kN/m, x=.8 m, Vu=360.192 kN y M(x)=305.3568 kN m. Vc=701.084874 kN coincide con 701.10 kN redondeado. El mínimo Av/s es .326025332 mm²/mm, equivalente a 326.025332 mm²/m; la unidad de la guía está mal rotulada. B2 no reemplaza la combinación de cargas del caso B.

El ejercicio 3 queda fuera del alcance integral: postensado y sección variable. Además presenta luces 27.8/27.2 m, discrepancia M/W, datos incompatibles de relajación y bloque comprimido que supera el ala sin resolver el alma. No se incorporan fricción ni resultados de ese sistema al modelo de pretesado. El detalle por ejercicio está en docs/auditoria_fuente.md.

Las 15 comparaciones nuevas usan tolerancia max(atol,rtol·|referencia|), con rtol=10⁻⁹ y atol=10⁻⁸ en A/B; B2 usa 0.01 N. Las tolerancias son numéricas, no tolerancias de aceptación normativa ni de lectura redondeada. Los valores siguientes están en SI (m, N, Pa y potencias correspondientes).

| Caso / magnitud | Referencia independiente | Aplicación | Diferencia absoluta |

| --- | --- | --- | --- |

| A histórico / section.area_m2 | 0.32 | 0.32 | 5.55e-17 |

| A histórico / section.inertia_m4 | 0.01706666667 | 0.01706666667 | 3.47e-18 |

| A histórico / section.self_weight_n_m | 8000 | 8000 | 1.82e-12 |

| A histórico / transfer.stress.top_pa | -781250 | -781250 | 4.66e-10 |

| A histórico / transfer.stress.bottom_pa | -5468750 | -5468750 | 1.86e-09 |

| A histórico / service.force_n | 850000 | 850000 | 0 |

| A histórico / service.midspan_moment_n_m | 162500 | 162500 | 2.91e-11 |

| A histórico / service.stress.top_pa | -2480468.75 | -2480468.75 | 0 |

| A histórico / service.stress.bottom_pa | -2832031.25 | -2832031.25 | 9.31e-10 |

| B guía ejercicio 1 adaptado / section.area_m2 | 0.36 | 0.36 | 5.55e-17 |

| B guía ejercicio 1 adaptado / section.section_modulus_bottom_m3 | 0.054 | 0.054 | 6.94e-18 |

| B guía ejercicio 1 adaptado / service.force_n | 1403000 | 1403000 | 0 |

| B guía ejercicio 1 adaptado / service.midspan_moment_n_m | 1000000 | 1000000 | 0 |

| B guía ejercicio 1 adaptado / service.stress.bottom_pa | 5527777.778 | 5527777.778 | 0 |

| B2 Corte de guía, cálculo local / Vc N | 701084.8736 | 701084.8736 | 2.33e-10 |

## 8. Arquitectura y modificaciones de software

ProjectInput mantiene los datos históricos e incorpora DesignOptions opcional. analyze valida entradas, obtiene propiedades, calcula pérdidas, construye ambas etapas y evalúa criterios. La interfaz recoge datos y presenta la instantánea; reporting genera tablas y exportaciones desde los mismos resultados. No existen ecuaciones estructurales duplicadas en Streamlit.

Los módulos nuevos son prestress/losses.py, checks/engineering.py, sections/transformed.py y reporting/design.py. La CLI run_case permite ejecutar entradas JSON; validation_avance2 compara referencias fijas. scripts/verify.py conserva resultados de pytest y validadores. tests/test_design.py incorpora compatibilidad, equilibrio, integración, límites del dominio, exportaciones e interacción.

La aplicación se organiza en Ingreso de datos, Cálculo, Resultados y Validación/reportes. Las cinco pestañas de salida anteriores se reducen a dos, conservando taller, explorador, unidades y exportaciones mediante expansores. Cambiar entradas invalida resultados; cambiar SI/USCS conserva la viga. Los parámetros nuevos exhiben unidades SI explícitas.

La extensión puede desactivarse para reproducir septiembre. Se preservaron los tres archivos literales base. Las ecuaciones siguen trazables mediante nombres de función, referencias y memoria. No se agrega catálogo, optimización ni postensado variable para forzar la compatibilidad de la guía.

## 9. Participación y decisiones del equipo

No se dispone de evidencias suficientes para atribuir contribuciones individuales nuevas. Las responsabilidades de la tabla son propuestas del usuario pendientes de confirmar; no deben redactarse en pasado como trabajo ya realizado.

La bitácora contribuciones.md solicita tarea, cálculo desarrollado y revisado, problema detectado, alternativa descartada, decisión y fundamento, ecuación contrastada, fecha y evidencia. Cada integrante debe revisar al menos un procedimiento de otro integrante y comprender el recorrido completo.

La auditoría, las modificaciones programadas, los controles ejecutados y este borrador se prepararon con asistencia de IA. El equipo deberá verificar las fuentes, decidir criterios, desarrollar manuscritos y asumir la revisión académica. No se han fabricado firmas, fotografías, cálculos personales o decisiones del grupo.

| Integrante | Responsabilidad propuesta | Evidencia actual |

| --- | --- | --- |

| Estefanía | Geometría, secciones y caso de flexión | Pendiente de confirmar y aportar |

| Rocío | Pérdidas y tensiones | Pendiente de confirmar y aportar |

| José | Resistencia a flexión y corte | Pendiente de confirmar y aportar |

| Pedro | Integración, pruebas, trazabilidad y memoria | Pendiente de confirmar y aportar |

## 10. Pruebas y control de calidad

La instalación se realizó en un entorno virtual nuevo con Python 3.12 y las dependencias del repositorio; requirements-lock.txt registra las versiones instaladas. Node se utiliza solo para contrastar la migración con JavaScript, no para ejecutar el cálculo de la app.

La ejecución conjunta registrada contiene 88 pruebas, 0 fallos, 0 errores y 0 omitidas. Los 15 controles históricos y las 15 comparaciones A/B/B2 resultaron PASS. Algunos controles se superponen: no equivalen a 30 casos estructurales independientes. Archivos: outputs/test_run.txt, pytest_results.xml y validation_summary.json.

La compatibilidad de ES se contrasta con deformación de hormigón; las pérdidas con conservación de fuerza; la flexión con equilibrio C=T; la flecha mediante integración numérica de trabajo virtual independiente; el corte con la referencia local auditada. AppTest verifica ejecución, cambios de unidades e invalidación de resultados. Las exportaciones se abren y contrastan en pruebas. No se afirma revisión visual en todos los navegadores.

El caso A ampliado arroja ES=27.251591 MPa, SH=44.815922 MPa, CR=50.310630 MPa y RE=32.390760 MPa; Pt=980.923886 kN y Pef=891.661768 kN. La pérdida total es 10.833823%. Su tensión de acero tras transferencia es 1401.319837 MPa y supera 1372.68 MPa: NO CUMPLE ese criterio. La capacidad φMn=625.701232 kN m supera Mu=220 kN m, pero ello no anula el incumplimiento del acero.

El ejemplo de demostración con P0=950 kN satisface los criterios calculados y conserva tres estados pendientes. Cambiar humedad permite anticipar y comprobar sensibilidad; el ejemplo de 90 kN/m produce incumplimiento; la altura negativa se rechaza antes de calcular. Estos casos están separados para evitar presentar el caso modificado como si fuera el original.

La suite registra una advertencia de deprecación de pandas emitida desde Streamlit al editar filas. No afecta al resultado de esta ejecución; deberá revisarse al actualizar dependencias. El resumen automático separa aprobación numérica, revisión normativa pendiente y respaldo manual pendiente.

## 11. Limitaciones y trabajo pendiente

Antes de la entrega deben completarse los manuscritos originales y su revisión cruzada, confirmar número de grupo, registrar aportes verificables y obtener el criterio docente de norma/edición y límites aplicables. No puede declararse cumplido el requisito 8 con la tabla de responsabilidades sola.

El servicio es parcial: faltan flecha diferida, efectos de historia temporal y modelo fisurado para clases T/C. También faltan comprobaciones locales de transferencia, desarrollo y anclaje, y trazabilidad del límite del gato/fabricante. El método FHWA empleado es histórico y simplificado; sus parámetros de demostración requieren fundamento en el caso real.

Para diciembre se propone priorizar cierre de esos vacíos antes de ampliar geometría resistente o postensado. La sección transformada está disponible como propiedad auxiliar, sin integrar redistribución por acero en todo el análisis. No hay catálogo de proveedores ni tercer caso integral validado. Esas capacidades no deben mostrarse como implementadas.

El paquete usa GrupoXX por ausencia del número confirmado. Los documentos son borradores editables; deben incorporar anexos manuales y contribuciones reales antes de presentarse como producto revisado por los cuatro integrantes.

| Nº | Requisito | Estado |

| --- | --- | --- |

| 1 | MVP desde entorno limpio | Implementado y ejecutado |

| 2 | Pérdidas inmediatas y diferidas | Implementado con alcance acotado |

| 3 | Tensiones, servicio, flexión y corte | Parcial |

| 4 | Interfaz conectada al núcleo | Implementado y probado |

| 5 | Dos casos y tolerancias | Implementado numéricamente |

| 6 | Pruebas unitarias e integración | Ejecutado |

| 7 | Memoria preliminar | Generada |

| 8 | Evidencia de cuatro integrantes | Pendiente |

## 12. Conclusiones

La evolución comprobada añade pérdidas por mecanismo, criterios preliminares de tensiones, flexión y corte, y flecha instantánea a un núcleo elástico previamente probado. Se preserva la trazabilidad del caso de septiembre y se reduce la dispersión de la interfaz sin eliminar sus herramientas correctas.

La referencia externa aporta contraste útil después de auditar unidades e hipótesis. Su discrepancia de tensión demuestra la necesidad de comprobar las fuentes antes de convertirlas en resultados esperados. Las pruebas automáticas acreditan consistencia numérica en el dominio ensayado; no sustituyen la revisión humana ni prueban cumplimiento normativo.

El siguiente paso académico es resolver y revisar las fichas en papel, justificar los datos y criterios y registrar decisiones reales. La entrega queda técnicamente preparada para esa revisión, con pendientes visibles. Solo al incorporar esa evidencia podrá sostenerse que el equipo ha comprendido y contrastado los procedimientos.

## Anexos y bibliografía

Anexo A: docs/matriz_avance2.md, auditoría de evolución y ocho requisitos. Anexo B: docs/cobertura_manual.md y Fichas_manuales.docx/PDF. Anexo M: manuscritos originales PENDIENTES. Anexo C: contribuciones.md, evidencia humana PENDIENTE. Anexo D: outputs/validation_summary.json, test_run.txt, pytest_results.xml y memoria_calculo.pdf.

Fuentes del proyecto: pauta Proyecto_curso_pretensado-2(1).pdf, sección 7.2 y formato de entrega; informe Proyecto PRE-POST 2.0(1).pdf de 10-09-2026; dos capturas de observaciones del profesor suministradas por el equipo. Fecha de entrega corregida por instrucción del usuario a 27-10-2026.

Dávalos, R. y Fraticelli, L., Verificación de secciones de hormigón pretensado, guía UNaM de 24 páginas, archivo 3b00fcbd75cedfac.pdf, sin fecha de edición visible. Ejercicios 1 y 2: revisión dimensional y adaptación; ejercicio 3: excluido como caso integral.

FHWA, Prestressed Concrete Bridge Design Example, FHWA-NHI-04-043, 2003, Design Step 5.4. https://www.fhwa.dot.gov/bridge/lrfd/pscus054.cfm . Método histórico consultado para pérdidas; no se afirma normativa vigente.

INTI, Reglamento CIRSOC 201-2005, capítulos 9, 10, 11 y 18. Texto oficial: https://app.inti.gob.ar/greenstone3/biblio/collection/works/document/ReglamentoCIRSOC201-2005_pdf . Edición identificada; adopción para el curso pendiente.

Material complementario recuperado: Guia_Didactica_Momento_Nominal_Vigas_Pretensadas.pdf; Anexo_Clase_4_Resolucion_Detallada.pdf; Guia_Cargas_Equivalentes_Momentos_Secundarios.pdf; Ejemplo_Resuelto_Cargas_Equivalentes_Momentos_Secundarios.pdf. Se distingue compatibilidad iterativa de aproximación resistente, se convierten los signos y se documenta la diferencia ACI/CIRSOC. No se usa la viga continua postensada como caso integral de la app.
