# PRE-POST 2.0 · Ejercicio 1 del set

Aplicación académica dedicada únicamente al ejercicio 1 de `SET DE EJERCICIOS PARA AVANCE 2.pdf`, pp. 1–3. Entrega 2: 27 de octubre de 2026.

## Ejecutar

Python 3.12:

```bash
python -m venv .venv
python -m pip install -r requirements-dev.txt
python -m streamlit run app/main.py
```

Activar antes el entorno: `source .venv/bin/activate` en Linux/macOS o `.venv\Scripts\Activate.ps1` en Windows PowerShell. Abrir la dirección que indique Streamlit.

La app muestra directamente el ejercicio 1. Pulsar **Restablecer ejercicio del set** y **Calcular ejercicio 1**. Permite cambiar parámetros de este mismo modelo, ingresar resultados manuscritos, comparar y descargar PDF/JSON.

## Reproducir resultados y verificar

```bash
python -m src.run_case examples/set_ejercicio_1.json --output outputs/set_ejercicio_1
python scripts/verify.py
```

Solo existe un archivo de ejemplo. El programa rechaza las entradas del antiguo modelo de viga completa. Las pruebas y el resumen de validación corresponden exclusivamente al alcance actual.

## Documentos vigentes

- [Base para redactar el informe de Entrega 2](docs/base_informe_entrega2.md).
- [Ejercicio y procedimiento de uso](docs/ejercicio_principal.md).
- [Desarrollo manual PDF](docs/Ejercicio1_Comparacion_Manual_Software.pdf) y [LaTeX](docs/latex/Ejercicio1_Comparacion_Manual_Software.tex).
- [Exportación directa del programa](outputs/set_ejercicio_1.pdf).
- [Alcance](docs/alcance.md) y [matriz de evidencia](docs/matriz_requisitos.md).

El informe de la entrega debe redactarse de nuevo con esta base. Se retiraron del árbol actual los casos anteriores y sus informes, ejemplos, memorias y validaciones; son recuperables en el historial de Git.

## Resultado e interpretación

P efectiva adoptada = 1410 kN; Ap teórica = 1226.086957 mm²; tensiones superior/inferior = -13.296296 / 5.462963 MPa; Mu = 1600 kN m; phi Mn = 1318.544420 kN m. Clase T en fibra inferior según el criterio del set; **NO CUMPLE a flexión**.

No se inventan luz, carga distribuida, fuerza inicial ni pérdidas. No se verifican transferencia, pérdidas, corte ni flechas. Referencia resistente preliminar CIRSOC 201-2005: requiere ratificación y unificación con el material del curso. Coincidencia numérica no acredita autoría manuscrita ni cumplimiento integral de la pauta.
