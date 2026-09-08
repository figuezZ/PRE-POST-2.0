# Aplicación de orden preypost.txt

Destino autorizado: `figuezZ/PRE-POST-2.0`, inicialmente vacío.
Origen funcional: `figuezZ/PRE-POST` versión 0.7.0, commit
`a2251344e17ba75cedc6639bbdbaed4043b72726`.

## Aplicación del documento

1. El commit de inicialización incorpora los seis paquetes pedidos, `CLAUDE.md`,
   las carpetas y todos los archivos Python del texto literalmente.
2. El commit de migración sustituye la interfaz de ejemplo y añade módulos para
   conservar las capacidades que el ejemplo no cubría. Los tres archivos base
   `inputs.py`, `rectangular.py` y `elastic.py`, el test rectangular y `CLAUDE.md`
   permanecen como en el documento. Los `__init__.py` solicitados están vacíos.

## Correcciones al ejemplo de interfaz

| Problema detectado | Solución |
|---|---|
| Pi, pérdida y cargas se combinaban dentro de `app/main.py` | Orquestación y ecuaciones en `src/analysis/pipeline.py` |
| USCS convertía solo longitudes y usaba un factor redondeado | `src/units.py` convierte todas las magnitudes con factores definidos |
| Faltaba la entrada de carga muerta adicional | Se incorpora y se suma solo en servicio |
| Solo se mostraban algunas métricas | Tablas completas, ambas fibras y aportes de tensión |
| Resultados dentro de `if st.button` desaparecían al interactuar | Estado de sesión, invalidación al editar y conversiones sin perder el cálculo |
| El ejemplo no incluía el taller 0.7 | Geometría compuesta, explorador y memoria migrados a Python |
| Excel contenía cinco valores | Informe de ocho hojas, PDF tabulado y JSON de datos |
| No estaba contemplada la dependencia PDF | ReportLab añadido a los seis paquetes requeridos |

El límite geométrico `abs(e) < h/2` y las fibras a `±h/2` del código literal son
válidos para la sección rectangular. Para T/I se usan las distancias al centroide
real y se verifica que el tendón esté dentro del hormigón. `ProjectInput` extiende
el contrato base y valida valores finitos; la aplicación siempre entra por
`analyze`. Los auxiliares literales de `elastic.py` presuponen entradas válidas.

## Equivalencia funcional y diferencias de distribución

| Función anterior | Ubicación nueva | Evidencia |
|---|---|---|
| Sección rectangular y etapas | `sections/rectangular.py`, `analysis/pipeline.py` | Caso analítico y comparación JS |
| Editor T/I/hueca y filas | `sections/composite.py`, `app/main.py` | Cuatro plantillas, geometrías inválidas, AppTest |
| Agregar sólido/vacío y restablecer | Geometría en `src/`, controles en `app/` | Pruebas de atajos y estado |
| SI/USCS | `src/units.py` | 11 magnitudes, ida/vuelta, entradas y gráficos |
| V(x), M(x), perfil | Muestreo en `src/`, Plotly en `app/plots.py` | Extremos y centro, igualdad con núcleo |
| Mapa de tensiones y fibra | `analysis/pipeline.py`, `app/plots.py` | Equilibrio, vacíos, escala, línea cero |
| Memoria de 19 pasos | `analysis/memory.py` | Comparación de valores con JavaScript |
| Tablas y Excel | `reporting/` | Tipos numéricos, contenido y unidades |
| Guardar/Imprimir PDF | Descarga directa de PDF tabulado | Apertura, contenido y revisión de páginas |

La interfaz es una adaptación a controles nativos Streamlit, no una copia visual
píxel por píxel del HTML. La impresión del HTML anterior incluía sus gráficos;
el nuevo PDF descarga tablas y memoria. Los gráficos siguen disponibles en la
plataforma. La ejecución por doble clic sin Python se sustituye por un servidor
Python local o Streamlit Cloud, como exige esta migración de arquitectura.

No se incorpora el ejemplo externo eliminado anteriormente. Tampoco se cambia
el repositorio PRE-POST original ni la configuración de su aplicación desplegada.

## Prueba de migración

`tests/reference/prepost_v0_7_core.js` es el núcleo original extraído del HTML
del commit indicado. Solo lo ejecutan las pruebas con Node, nunca la aplicación.
Se compara área, inercia, centroides, módulos, peso, cargas, tensiones, fibras y
los 19 resultados de memoria para cuatro geometrías, dos etapas y cuatro
posiciones. Esa equivalencia se complementa con integrales independientes para
evitar depender únicamente de que dos implementaciones compartan un error.

La prueba de Streamlit usa AppTest y no sustituye una revisión visual en todos los
navegadores. El estado de GitHub Actions debe consultarse en la pestaña Actions;
las pruebas locales no se presentan como una ejecución remota.
