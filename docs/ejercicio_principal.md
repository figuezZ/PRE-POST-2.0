# Caso principal para Entrega 2: ejercicio 1 del set

Es el único caso disponible. Se retiraron los demás ejemplos, modos y controles del árbol vigente.

Fuente: `SET DE EJERCICIOS PARA AVANCE 2.pdf`, pp. 1–3. Datos: b=0.4 m, h=0.9 m, dp=0.8 m, fc=30 MPa, Ms=1000 kN m, fpe=1150 MPa, fpy=1700 MPa, grado 270 y Mu=1.6 Ms. Adopciones revisadas: fpu=1860 MPa y P por exceso en incrementos de 10 kN. No se inventan luz, cargas distribuidas, P0 ni pérdidas de 15%.

## Flujo reproducible

1. Ejecutar `python -m streamlit run app/main.py`.
2. La app abre directamente el ejercicio 1, sin selector de casos.
3. Pulsar **Restablecer ejercicio del set** y **Calcular ejercicio 1**.
4. Desarrollar a mano `latex/Ejercicio1_Comparacion_Manual_Software.tex` (PDF en esta carpeta).
5. Introducir los valores propios en **Comparar con tu desarrollo manuscrito** y pulsar **Comparar resultados**.
6. Descargar cotejo JSON y memoria PDF; adjuntar el manuscrito real. La referencia calculada no acredita autoría humana.

Por consola: `python -m src.run_case examples/set_ejercicio_1.json --output outputs/set_ejercicio_1`.

## Valores de control

| Magnitud | Referencia revisada |
|---|---:|
| P efectiva adoptada (kN) | 1410 |
| Ap teórica (mm²) | 1226.086956522 |
| Tensión superior (MPa) | -13.296296296 |
| Tensión inferior (MPa) | 5.462962963 |
| Mu (kN m) | 1600 |
| phi Mn (kN m) | 1318.544419616 |

La fibra inferior satisface el intervalo abierto de clase T; **la resistencia a flexión NO CUMPLE**. El área es teórica, no una selección comercial de torones.

## Diferencias con el impreso

P=1403 kN, publicado en la fuente, conduce a 5.527777778 MPa, superior a sqrt(30)=5.477225575 MPa. El intervalo recalculado es 1408.459637894 < P < 1585.921746526 kN. Se adopta 1410 y se recalcula Ap; no se altera la tolerancia para hacer pasar el dato impreso.

La resistencia revisada usa CIRSOC 201-2005, 18.7.2(a) y 9.3.2.1, ya implementado en el proyecto. Difiere de la simplificación de la guía. La unificación con el material ACI del curso requiere ratificación docente. No se afirma cumplimiento normativo integral.

## Cobertura actual

Solo propiedades, fuerza efectiva, área activa, tensiones de servicio y resistencia seccional. Pérdidas, transferencia, corte y flechas quedan fuera del alcance. Ver base_informe_entrega2.md para continuar la redacción del informe.

La entrada de producción `src.analysis.pipeline.analyze` acepta exclusivamente Exercise1Input o su representación JSON. Las ecuaciones se mantienen en src/.
