# Base para continuar el informe de Entrega 2

## Decisión del equipo

Se dejó exclusivamente el ejercicio 1 del set en la app y el repositorio vigente. Se retiraron otros ejemplos y los informes anteriores para evitar resultados mezclados. Fecha de entrega: 27 de octubre de 2026.

## Caso que debe describir el informe

Sección b=0.4 m, h=0.9 m y dp=0.8 m; fc=30 MPa, Ms=1000 kN m, fpe=1150 MPa y fpy=1700 MPa. Adopciones: fpu=1860 MPa, Mu=1.6 Ms y fuerza por exceso en incrementos de 10 kN.

| Resultado | Valor |
|---|---:|
| P efectiva | 1410 kN |
| Ap teórica | 1226.086957 mm² |
| Tensión superior | -13.296296 MPa |
| Tensión inferior | 5.462963 MPa |
| Mu | 1600 kN m |
| phi Mn | 1318.544420 kN m |

La fibra inferior satisface el intervalo de clase T; la resistencia a flexión NO CUMPLE. No cambiar datos para ocultar ese resultado.

## Evidencias que deben distinguirse

1. `docs/Ejercicio1_Comparacion_Manual_Software.pdf`: desarrollo de referencia para estudiar y resolver a mano.
2. `outputs/set_ejercicio_1.pdf`: exportación directa del software, sin reconstruirla como una memoria externa.
3. Manuscrito original de los integrantes: aún no incorporado; debe mostrar datos, unidades, pasos y conclusión.
4. Comparación de resultados: ingresar valores reales del manuscrito en la app y conservar el cotejo.
5. `outputs/validation_summary.json`: pruebas automáticas del alcance actual, no certificación estructural.

## Observaciones técnicas para la discusión

La guía publica P=1403 kN, que produce una tensión inferior de 5.527778 MPa, superior a sqrt(30). La resolución revisada adopta 1410 kN y recalcula Ap. La resistencia utiliza CIRSOC 201-2005 y difiere de la simplificación de la fuente. Ratificar con el profesor la norma aplicable, sin afirmar concordancia normativa ya resuelta.

No se calculan pérdidas, transferencia, corte ni flechas: faltan datos para esas comprobaciones. Contrastar este alcance reducido con la pauta; no declarar cumplidos todos sus requisitos por haber limpiado el repositorio.

## Estructura sugerida del informe

Objetivo y alcance; presentación del ejercicio; decisiones y método; funcionamiento de la app; desarrollo manuscrito; tabla manual/software; discusión del incumplimiento y de la guía; conclusiones; anexos.

Registrar aportes y revisión reales de Estefanía, Rocío, Pedro y José. No asignar autorías ficticias ni reemplazar el manuscrito por el desarrollo generado. Número de grupo y evidencias personales pendientes de confirmar.
