# Contraste con material complementario de clases

Se recuperaron y revisaron cuatro documentos disponibles del proyecto: Guia_Didactica_Momento_Nominal_Vigas_Pretensadas.pdf, Anexo_Clase_4_Resolucion_Detallada.pdf, Guia_Cargas_Equivalentes_Momentos_Secundarios.pdf y Ejemplo_Resuelto_Cargas_Equivalentes_Momentos_Secundarios.pdf. Son antecedentes complementarios; no se presume por su título que sustituyan la pauta o confirmen por sí solos la edición exigida para este repositorio.

## Hallazgos que afectan la entrega

- La guía didáctica desarrolla compatibilidad adherente: deformación efectiva del acero + descompresión + incremento por curvatura. Deben incluirse las cargas presentes en el estado de referencia al calcular descompresión. No se suma Pe otra vez al equilibrio resistente Ap fps.
- Su ejemplo da aproximadamente fps=254.30 ksi y Mn=317.40 kip ft con una curva de cordón definida. El anexo de Clase 4 usa otra lectura/curva y obtiene aproximadamente 220 ksi y 267.45 kip ft. No mezclar esos resultados como si fueran un único patrón; sus relaciones constitutivas son distintas.
- El programa de esta entrega utiliza fps aproximado CIRSOC 18.7.2(a); no implementa ni valida aún la iteración de compatibilidad de esas guías. F09 debe identificar esta diferencia. La ecuación de equilibrio C=T y el brazo son comunes, pero eso no prueba igualdad de capacidades.
- El ejemplo resuelto de viga continua usa ACI 318-19, 20.3.2.3, para fps; 24.5 para tensiones y 5.3.11 para incorporar el momento secundario con factor 1.0. Su β1=.85−.05(35−28)/7=.80 a fc=35 MPa difiere del β1=.8142857 del criterio CIRSOC implementado, cuyo umbral es 30 MPa. Debe ratificarse y unificarse la base normativa antes de declarar cumplimiento del curso. No se etiqueta el cálculo actual como ACI.
- La guía general menciona ediciones ACI posteriores, pero el ejemplo fija ACI 318-19 para sus operaciones. Esa coexistencia no permite seleccionar silenciosamente una edición para el proyecto.
- Las cargas equivalentes y momentos secundarios corresponden a trazados curvos y estructuras hiperestáticas. Para el tendón recto de esta app no hay carga transversal distribuida por curvatura y para la viga simplemente apoyada no hay momento secundario. Permanece el efecto excéntrico P·e. La guía mide e hacia abajo; el programa hacia arriba: convertir el signo antes de comparar.

## Acción académica pendiente

Confirmar con el docente si la Entrega 2 debe utilizar ACI 318-19 u otra edición, y si exige compatibilidad iterativa o admite fps aproximado en su dominio. Después actualizar coherentemente todos los límites, β1, φ, cláusulas y casos; no cambiar solo una constante y afirmar adopción completa. Hasta entonces, todas las verificaciones nuevas siguen siendo preliminares y el requisito 3 se mantiene parcial.
