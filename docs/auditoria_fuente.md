# Auditoría de la guía UNaM
Fuente: Dávalos, Rubén y Fraticelli, Lucas, Verificación de secciones de hormigón pretensado, 24 páginas, archivo 3b00fcbd75cedfac.pdf. Sin fecha de edición visible. Referencias bibliográficas internas: Larsson, 2.ª edición; Hernández Balat y Cisaruk. El ejercicio 3 cita CIRSOC 201-2005. Esto no confirma que USS haya adoptado ese reglamento.

## Ejercicio 1: adaptable como caso elástico, no patrón resistente literal
Datos: b=0.40 m, h=0.90 m, dp=0.80 m, e=-0.35 m en nuestra convención; fc=30 MPa; Ms=1000 kN m; fpe=1150 MPa; fpy=1700 MPa; Mu=1.6 Ms.
- A=0.36 m2; I=0.0243 m4; W=0.054 m3. La fuente etiqueta W en m4: error dimensional.
- Publica P=1403 kN, Ap=12.20 cm2 y tensión objetivo sqrt(30)=5.477225575 MPa.
- Sustitución independiente exacta con P publicado: sigma_inf=1000000/0.054-1403000*(1/0.36+0.35/0.054)=49750000/9 Pa=5.527777778 MPa. Diferencia contra 5.48 MPa: 0.047777778 MPa (0.871857%). No atribuible solo al redondeo habitual.
- Despeje independiente: P=(1000000/0.054-sqrt(30)*1000000)/(1/0.36+0.35/0.054)=1408459.637894 N. Ap=P/1150e6=1224.747511 mm2. No se altera el dato publicado; se conserva la discrepancia.
- Publica a=0.173 m empleando fc b, sin 0.85; toma fps=fpy sin verificar compatibilidad. Su 2074*0.7135=1479.799 kN m, distinto de 1473 kN m. La extensión aplica 18.7.2(a), no fuerza coincidencia con esa capacidad.
- Caso B adaptado: luz 15 m tomada del ejercicio 2 y carga uniforme equivalente 35.5555556 kN/m para Ms=1000 kN m. Descuento de peso propio 9 kN/m. Se adopta pérdida declarada 15% SOLO para reconstruir Pe=1403 kN; no valida pérdidas FHWA. El caso conserva los 1220 mm2 publicados: Pe/Ap=1150 MPa exactos.

## Ejercicio 2: compatible como comprobación local de corte
Datos: L=15 m, Mu_max=1512 kN m, x=dp=0.80 m, b=0.40 m, h=0.90 m, fc=30 MPa, fy=420 MPa; phi=0.75.
- wu=8*1512/15²=53.76 kN/m.
- Vu=53.76*(7.5-0.8)=360.192 kN; M(x)=53.76*0.8*(15-0.8)/2=305.3568 kN m.
- Cap Vc=400 sqrt(30)*0.4*0.8=701.084873607 kN, consistente con 701.10 kN redondeado.
- Mínimo conservador Av/s=max(sqrt(30)/16,0.33)*400/420=0.326025332 mm2/mm =326.025332 mm2/m=3.26025332 cm2/m. La fuente escribe mm2/m donde corresponde mm2/mm.
- Dos ramas de diámetro 8 mm a 0.25 m proporcionan 402.12386 mm2/m. No se usa una cuantía negativa: se separan requerimiento resistente y mínimo.
- La frase de separación «mínima s<=3/8 h» no constituye regla general. Verificar 11.5.5: máximo min(3h/4,400 mm), reducido si corresponde por Vs.
- Caso local B2 evalúa d=0.80 m. No sustituye la combinación de cargas del caso B: son solicitaciones distintas.

## Ejercicio 3: fuera del alcance integral, útil para revisión crítica
Postensado a 7 días, sección variable (apoyos rectangulares 1.04 m2, centro doble T 0.51 m2), carga permanente adicional 6.5 kN/m, viva 21.3 kN/m, fc=35 MPa, fpu=1864 MPa, fpy=1682 MPa; 21 cordones y Ap=2072.70 mm2. Publica Pe=2601.19 kN y Pi=2841.02 kN. No se incorporan estos valores como patrón de pretesado.
- El promedio de peso propio emplea 27.80 m; la tabla usa x=L/2=13.60 m (L=27.20 m). Debe fijarse una luz antes de comparar.
- La tabla publica M total=4414.56 kN m pero tensión 19.03 MPa con W=0.211 m3: el cociente de esos datos es 20.922085 MPa.
- Fricción enumera lpx=13.30 m pero sustituye 13.60 m. El resultado 0.05986 corresponde a 13.60 m y alpha=0.1633.
- Pérdidas tienen ecuaciones incrustadas como imágenes. La ficha RE muestra Kre=25 MPa, J=0.04 y C=1.05: con pérdidas no negativas, [25-0.04(SH+CR+ES)]*1.05 no puede dar 33.29 MPa (>26.25). Requiere aclaración del dato o resultado.
- Al añadir acero pasivo obtiene a=0.2736 m>hf=0.25 m y lo trata aproximadamente como ala completa: no se acepta; debe incluirse el alma en el equilibrio.
- Confunde a y c=a/beta1 al comprobar deformación. No usar su conclusión resistente sin recalcular.
No se amplía el programa a postensado variable para adaptar este ejemplo artificialmente.
