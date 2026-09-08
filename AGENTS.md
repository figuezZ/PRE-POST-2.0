# Trabajo en PRE-POST 2.0

- Leer `CLAUDE.md`, `docs/alcance.md` y `docs/matriz_requisitos.md` antes de ampliar el modelo.
- Núcleo en m, N y Pa; compresión negativa; y/e positivos hacia arriba; M sagante positivo.
- `app/` recoge entradas y presenta resultados. Ecuaciones estructurales y muestreo en `src/`.
- La entrada de producción es `src.analysis.pipeline.analyze` con `ProjectInput` validado.
- Mantener los tres archivos literales del documento como base trazable; documentar cambios futuros.
- Cada cálculo nuevo debe tener referencia y prueba independiente.
- No declarar cumplimiento normativo sin norma, edición, artículo y criterio ratificados.
- Verificar con `python -m pytest` y `python -m src.validation --all --output outputs/validation_summary.json`.
- No requiere Node para ejecutar la aplicación; Node solo se usa en pruebas de migración.
