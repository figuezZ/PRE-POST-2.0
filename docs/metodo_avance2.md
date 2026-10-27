# Fundamento, fuentes y dominio de la extensión

## Contrato físico

Viga prismática simplemente apoyada, carga uniforme no negativa, sección rectangular y un nivel de cordones rectos adherentes de baja relajación, inferior o centrado. Hormigón normal, flexión positiva, sin acero longitudinal pasivo, torsión, cargas concentradas ni construcción por etapas. SI interno: m, N, Pa. Compresión negativa; e/y hacia arriba; momento sagante positivo. Desplazamiento positivo hacia abajo.

P0 es la fuerza inmediatamente antes de liberar el pretensado: no la fuerza máxima histórica del gato. Pt se usa en transferencia con peso propio; Pe en servicio con peso propio, carga muerta adicional y carga viva. Los mapas del módulo histórico usan fuerza constante y no resuelven la zona de transferencia. Fuera de lt=50 diámetros de cordón se evalúa la envolvente de tensiones.

Las constantes por defecto Ep=195 GPa, Eci=30 GPa, Ec=34 GPa, H=70%, fpu=1860 MPa, fpy=1674 MPa, fy=420 MPa, dos ramas de 8 mm cada 200 mm y cordón 12.7 mm son datos de demostración, no ensayos ni especificaciones confirmadas. Deben reemplazarse con antecedentes trazables del caso real. El divisor 360 es un criterio configurable pendiente de acuerdo según uso.

## Pérdidas

Fuente primaria: FHWA, Prestressed Concrete Bridge Design Example, publicación FHWA-NHI-04-043 (2003), Design Step 5.4, referencias históricas S5.9.5.2.3a y S5.9.5.4.2–4. https://www.fhwa.dot.gov/bridge/lrfd/pscus054.cfm

ES se resuelve implícitamente para que la tensión de hormigón corresponda a Pt, sin descontar dos veces el acortamiento. fcgp=Pt(1/A+e²/I)+Mg e/I, positivo en compresión. fcdp=−Mpermanente_adicional e/I es el alivio de compresión posterior. SH se convierte desde ksi; CR y RE se limitan a cero. Las pérdidas diferidas se restan como Ap(SH+CR+RE). La humedad afecta retracción; no se modelan edades, tamaño equivalente ni historia temporal completa. No usar fricción, asiento de anclajes o secuencias de tesado propias de postensado.

El modelo es una estimación histórica simplificada; no afirma vigencia AASHTO actual ni adopción chilena. Si se elige pérdida declarada, el porcentaje reconstruye fuerzas, pero no constituye validación de mecanismos.

## Verificaciones

Referencia primaria: INTI, Reglamento CIRSOC 201-2005, texto oficial: https://app.inti.gob.ar/greenstone3/biblio/collection/works/document/ReglamentoCIRSOC201-2005_pdf

Se utiliza como referencia académica explícita. La pauta no fija una edición única para el proyecto. El material complementario recuperado incluye un ejemplo con ACI 318-19 y guías que remiten a otras ediciones; ver contraste_material_docente.md. La extensión CIRSOC no equivale a adoptar ACI. Se requiere ratificación del profesor antes de afirmar cumplimiento normativo. No mezclar estos límites con ACI sin comparar ediciones.

- Tensiones: 18.3.3 (clases U/T/C), 18.4.1 y 18.4.2; límites de acero 18.5.1. Se usa el límite general de tracción de transferencia, sin excepción de extremos. Fuerza máxima del gato/fabricante permanece pendiente.
- Combinaciones 9.2: máximo 1.4D y 1.2D+1.6L bajo este conjunto de cargas. No se incluyen viento, sismo ni otras acciones.
- Flexión: 18.7.2(a), 10.2.7 y 9.3.2.1. fps aproximado solo para fpe≥0.5fpu; γp=.28/.40/.55 para fpy/fpu≥.90/.85/.80. Se verifica dominio controlado por tracción; no se extrapola cuando falla. φ=.90. Resistencia mínima 18.8.2: φMn≥1.2Mcr, sin exención.
- Corte: 11.4.2, 11.4.4, 11.5.5–7 y 9.3.2.3. Requiere Pe≥0.4Ap fpu. d=max(dp,.8h), sección crítica x=d medida desde apoyo ideal; presupone reacción que comprime el extremo y carga superior. Cerca del extremo, Vc se limita con Vcw calculado usando fpc reducido a h/2 y sin componente vertical del tendón. Reducción min(1,h/(2lt)). Vcw=(.3√fc+fpc) b dp, magnitudes de tensión en MPa. Límite Vs=(2/3)√fc bd. Mínimo conservador de 11-13, sin aprovechar la alternativa menor 11-14. Si Vs>√fc bd/3 se reduce a la mitad el máximo de separación. Esto no diseña la transferencia ni el anclaje.
- Servicio: integración de curvatura no fisurada y comparación de flecha viva con L/divisor. Clase T/C exige modelo fisurado no implementado. Estimar pérdidas diferidas NO calcula la flecha diferida: faltan historia de cargas, rigidez, edad y evolución de contraflecha.

Todas las raíces √fc usan MPa y todos los resultados se convierten a SI antes de comparar. Las propiedades neta/transformada son auxiliares mediante acero concentrado y ejes paralelos; no reemplazan Ig en las comprobaciones de sección bruta. Peso propio calculado con área bruta equivalente: no incluye corrección por densidad del acero.

## Validación y límites

La matriz docs/cobertura_manual.md relaciona cada procedimiento con ficha y test. Equilibrio, integración independiente, comparación con valores fijos y regresión cubren aspectos distintos. Ninguno sustituye revisión manual ni confirma validez normativa. No usar esta herramienta para proyecto ejecutivo. No hay validación integral para postensado ni sección variable.
