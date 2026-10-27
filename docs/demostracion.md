# Demostración y efecto esperado

1. Ejecutar `python -m src.run_case examples/caso_criterios_satisfechos.json --output outputs/demo_correcto`. P0=950 kN satisface los criterios implementados, conservando tres pendientes: gato, diferida y extremos. No decir que la viga está certificada.
2. En interfaz, ingresar caso A ampliado con H=70%; anticipar que al bajar H a 60% aumentará SH y bajará Pe. Calcular y verificar ambos cambios. Cambiar una entrada invalida resultados; recalcular. Explicar ES por compatibilidad en F06.
3. Ejecutar `python -m src.run_case examples/caso_no_cumple.json --output outputs/demo_no_cumple`. Carga viva 90 kN/m: sube Mu y aumenta tracción. Explicar comparación de demanda/capacidad en F07–F10. El caso A ampliado original ya incumple el límite de acero tras transferencia; no ocultarlo.
4. Ejecutar `python -m src.run_case examples/caso_invalido.json --output outputs/demo_invalido`. Altura negativa: entrada rechazada, código de salida 2, sin informe nuevo. Mantener nombres de salida distintos para no confundir archivos antiguos.
5. Abrir src/checks/engineering.py y F09, identificar ecuación de fps, bloque comprimido, brazo y φMn. Revisar además cálculo de corte B2 y conversión mm²/mm a mm²/m.
6. Ejecutar `python scripts/verify.py`. Explicar que PASS compara números; no acredita manuscritos ni norma. Mostrar outputs/validation_summary.json y docs/auditoria_fuente.md.

Para la defensa, cada integrante debe ejecutar el recorrido completo y explicar al menos un procedimiento ajeno. Registrar ensayos reales en contribuciones.md.
