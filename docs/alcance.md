# Alcance vigente — Avance 2

La extensión opcional implementa pérdidas por mecanismo, comprobaciones preliminares y propiedades auxiliares neta/transformada para rectángulo pretesado recto. El modo histórico sigue disponible. Consulte [método y restricciones](metodo_avance2.md), [matriz vigente](matriz_avance2.md) y [cobertura manual](cobertura_manual.md).

Estado: validación numérica ejecutada; manuscritos, contribuciones personales y ratificación del criterio normativo pendientes. Servicio es parcial: solo flecha instantánea no fisurada.

## Antecedente histórico al commit d59181b (no describe la extensión nueva)

# Alcance de PRE-POST 2.0

El alcance base de `CLAUDE.md` es una viga simplemente apoyada rectangular.
El taller opcional conserva las secciones compuestas de la versión HTML anterior.
Ambos usan el mismo flujo Python y se presentan en una sola interfaz.

- Viga prismática, estática lineal, carga uniforme, un tendón recto equivalente.
- Transferencia: Pi y peso propio. Servicio: Pe y peso propio + muerta adicional + viva.
- Pe = (1 - pérdida declarada) Pi. No se estiman mecanismos de pérdida.
- Hormigón elástico no fisurado. Compresión negativa y tracción positiva.
- Núcleo SI. Presentación SI/USCS. Memoria y componentes siempre en SI base.
- No se han implementado límites normativos ni se declara cumplimiento de ACI.

## Geometría del taller

Entre 1 y 24 componentes rectangulares centrados en un eje vertical. Los sólidos
se apilan desde Y=0, sin superposición ni separación. Los vacíos restan área e
inercia, quedan dentro de un sólido y deben ser más estrechos. No pueden
superponerse ni formar una abertura continua que separe la sección en dos piezas.
Un vacío puede llegar al borde superior/inferior como rebaje dentro de ese sólido.

Se calcula la geometría bruta antes de vacíos y la del hormigón descontando los
vacíos. No se descuenta automáticamente el área del acero. No hay polígonos
libres, excentricidad horizontal ni flexión biaxial. El tendón es un punto
equivalente, sin verificación de recubrimiento o distribución de armaduras.

La línea de tensión cero no es el centroide cuando existe fuerza axial. Si la
fibra seleccionada sobre el eje central cae en un vacío o borde, se identifica
como prolongación del campo elástico y no como tensión en un punto de hormigón.

## Pendiente para ampliar la entrega

Sección neta que contemple explícitamente desplazamiento por acero/ductos según
el procedimiento del curso; sección transformada con Es/Ec; selección de perfiles
de proveedores; pérdidas por mecanismo; límites normativos; fisuración, flechas,
resistencia y anclajes. Se debe acordar el procedimiento y la edición normativa
antes de incorporar estas verificaciones.
