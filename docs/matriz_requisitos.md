# Matriz de trazabilidad del Avance 1

| Requisito | Módulo / evidencia | Estado |
|---|---|---|
| Arquitectura modular; interfaz sin ecuaciones | `src/`, `app/`, prueba de dependencias | Hecho |
| Datos tipados y validación física | `models/`, pruebas de entradas inválidas | Hecho |
| Área bruta | `sections/`, rectángulo y sólidos antes de vacíos | Hecho |
| Inercia bruta | `sections/`, integrales y ejes paralelos | Hecho |
| Propiedades de hormigón / sección neta | Descuento de vacíos dibujados; acero no descontado automáticamente | Parcial |
| Sección transformada incorporando acero | Falta Es/Ec y contribución geométrica del acero | Pendiente |
| Peso propio | `sections/`, caso analítico | Hecho |
| Momento por peso propio | `analysis/`, equilibrio de viga simplemente apoyada | Hecho |
| Tensiones en distintas fibras | `analysis/pipeline.py`, pruebas de equilibrio y migración JS | Hecho para modelo elástico no fisurado |
| Secciones de proveedores locales | Plantillas geométricas, sin catálogo identificado | Pendiente |
| Entradas y resultados organizados | Streamlit, tablas, editor, explorador y gráficos | Hecho |
| Memoria reproducible y exportación | `analysis/memory.py`, `reporting/`, pruebas de archivos | Hecho |
| Pruebas y autovalidación | `tests/`, `src/validation.py`, GitHub Actions | Implementado |
| Pérdidas detalladas, resistencia y norma | Solo porcentaje global declarado; sin límites ACI | Pendiente |

La migración de arquitectura no significa que todos los requisitos estructurales
de la entrega estén resueltos. Esta tabla debe acompañar cualquier presentación.


Actualización: esta matriz conserva el estado de septiembre; ver matriz_avance2.md para la extensión del 27-10-2026.
