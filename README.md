# Instalación y ejecución — PRE/POST 2.0

Requiere Python 3.12. Desde esta carpeta:

```bash
python -m venv .venv
```

Activar en Linux/macOS: `source .venv/bin/activate`. En Windows PowerShell: `.venv\Scripts\Activate.ps1`.

```bash
python -m pip install -r requirements-dev.txt
python -m streamlit run app/main.py
```

Abrir la dirección de Streamlit (normalmente http://localhost:8501). En Codespaces, abrir el puerto 8501. El servidor Python debe estar en ejecución. Para reproducir exactamente las versiones usadas en Linux/Python 3.12 puede instalarse requirements-lock.txt en lugar de requirements-dev.txt; el archivo lock registra el entorno probado, no garantiza todas las plataformas.

## Avance 2 — 27 de octubre de 2026

Versión candidata 2.1.0-rc1. La fecha indicada por el equipo corrige el 29 de octubre de la pauta. Grupo XX es un marcador pendiente de reemplazar antes de entregar. No se atribuyen revisiones ni cálculos manuales todavía no aportados.

## Flujo de uso

1. Ingreso de datos: elegir SI/USCS, geometría, materiales, cargas y tendón. Carga muerta adicional excluye peso propio.
2. Activar la extensión de Entrega 2 para pérdidas y criterios preliminares. Los parámetros nuevos muestran unidades SI explícitas aun con presentación USCS. Sin extensión se conserva el caso histórico.
3. Calcular etapas y revisar Resultados: métricas, pérdidas, verificaciones y diagramas esenciales. Explorador y taller están conservados en expansores.
4. Validación y reportes: referencias automáticas, memoria y exportación PDF/Excel/JSON. Toda modificación de datos exige recalcular; cambiar unidades conserva la viga.

Pérdidas FHWA solo para rectángulo simple y tendón recto inferior/centrado. El taller T/I/hueca conserva geometría y tensiones históricas; no dispone de verificación resistente nueva. La opción de pérdida declarada no desglosa mecanismos.

## Reproducir casos y pruebas

```bash
python -m src.run_case examples/caso_criterios_satisfechos.json --output outputs/memoria_calculo
python -m src.run_case examples/caso_A_ampliado.json --output outputs/caso_A
python -m src.run_case examples/caso_B_externo.json --output outputs/caso_B
python scripts/verify.py
```

Para regresión contra JavaScript se necesita Node.js (se probó v24; CI usa v22). Sin Node esas pruebas se omiten; revisar el contador skipped. Node no es necesario para la aplicación. El script guarda test_run.txt, pytest_results.xml y validation_summary.json con pruebas, 15 controles legado y 15 comparaciones A/B/B2. Varios controles se superponen; no presentarlos como 30 fenómenos independientes.

Control legado individual: `python -m src.validation --all --output outputs/validation_legacy.json`. Control nuevo individual: `python -m src.validation_avance2 --output outputs/references_only.json`. No sobreescribir el resumen conjunto si se desea conservar sus metadatos.

Ver [demostración](docs/demostracion.md), [auditoría de guía](docs/auditoria_fuente.md), [ocho requisitos](docs/matriz_avance2.md), [método y fuentes](docs/metodo_avance2.md) y [cobertura manual](docs/cobertura_manual.md).

## Estructura

- src/: modelos, geometría, estática, pérdidas, comprobaciones y exportaciones; SI interno m,N,Pa.
- app/: entrada y presentación; ecuaciones exclusivamente en src/.
- tests/: pruebas de equilibrio, referencias, guardas, archivos, unidades e interfaz.
- examples/: entradas JSON en SI y resultados esperados independientes.
- docs/: informe fuente, método, auditoría, fichas y trazabilidad.
- outputs/: evidencia de ejecución y memoria preliminar.
- contribuciones.md: asignaciones propuestas y bitácora por completar.

Los tres archivos literales originales permanecen sin cambios. No hay catálogo de proveedores ni importación JSON desde la interfaz: los ejemplos se ejecutan con la CLI.

## Interpretar los estados

CUMPLE CRITERIO significa que satisface una comparación implementada. NO CUMPLE señala el criterio excedido. PENDIENTE señala que no se ha verificado. Ninguno equivale a certificación normativa. El caso A ampliado original incumple tensión del acero; el ejemplo de 950 kN permite demostrar criterios satisfechos sin ocultar el incumplimiento original.

Faltan manuscritos originales, evidencia de los cuatro integrantes y ratificación docente de norma/edición/criterios. Servicio no incluye flecha diferida; tampoco están resueltos anclaje/desarrollo, transferencia local, postensado o resistencia de secciones compuestas. Las propiedades transformadas son auxiliares. Consultar docs/alcance.md.
