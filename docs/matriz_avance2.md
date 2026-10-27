# Avance 1 → Entrega 2

Base real auditada: d59181bcd2a3e111d2d0692dd53a2572aad2169e. El HEAD remoto consultado coincidía con esa base: no había avances posteriores que atribuir a octubre. Se ejecutaron 70 pruebas de base, todas aprobadas, y 15 controles analíticos.

| Avance 1 | Estado al auditar | Exigencia Avance 2 | Acción efectuada | Evidencia |
|---|---|---|---|---|
| Geometría, ejes paralelos y taller | Probado en septiembre; conservado | Reproducibilidad y alcance claro | Sección neta/transformada auxiliar añadida | F01–F03; tests/test_sections.py y test_design.py |
| Estática y superposición elástica | Probado; sin cambios en archivos literales | Tensiones transferencia/servicio | Mantener signos; fuerzas de etapas actualizadas | F04–F05; regresión contra JS |
| Pérdida global declarada | Solo porcentaje; no mecanismos | Pérdidas inmediatas/diferidas | Modo FHWA acotado y opción histórica | F06; compatibilidad y sensibilidad |
| Ausencia de criterios resistentes | No implementados al inicio | Servicio/flexión/corte | Añadir criterios preliminares con guardas | F07–F11; equilibrio, integración, referencia externa |
| Cinco pestañas de resultados | Funcionales pero dispersas | Interfaz simple conectada | Dos pestañas; cuatro etapas; expansores | AppTest; preservación SI/USCS |
| Caso base/15 controles | 70 pruebas ejecutadas inicialmente | Dos casos y suite ampliada | Caso B adaptado y B2 corte; prueba fuente crítica | JSON de validación y auditoría de guía |
| Informe septiembre y memoria | Memoria elástica; sin evidencia manual nueva | Memoria de Avance 2 y trabajo humano | Informe nuevo, fichas y bitácora pendiente | Documentos editables; contribuciones.md |

## Ocho requisitos oficiales

| Nº | Requisito | Estado | Evidencia y límite |
|---|---|---|---|
| 1 | MVP desde entorno limpio | Implementado y ejecutado | venv nuevo, requirements-dev, prueba AppTest; README |
| 2 | Pérdidas inmediatas y diferidas | Implementado con alcance acotado | ES/SH/CR/RE para pretensado recto; método histórico pendiente de adopción docente |
| 3 | Tensiones, servicio, flexión y corte | Parcial | Límites, clase U, flecha instantánea y resistencias; falta flecha diferida, desarrollo y criterios ratificados |
| 4 | Interfaz conectada al núcleo | Implementado y probado | Cuatro etapas; ecuaciones solo en src; prueba de dependencias |
| 5 | Dos casos y tolerancias | Implementado numéricamente | A histórico y B externo adaptado; B2 control local; manuscritos pendientes |
| 6 | Pruebas unitarias e integración | Ejecutado | outputs/test_run.txt y pytest_results.xml; control adicional legado |
| 7 | Memoria preliminar | Generada | Entradas, hipótesis, resultados y estados; no certificación normativa |
| 8 | Evidencia de cuatro integrantes | Pendiente | Registro preparado; no se recibieron manuscritos ni evidencias personales verificables |
