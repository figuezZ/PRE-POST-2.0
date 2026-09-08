# Fórmulas, convenciones y controles

Fuente de implementación: código entregado en `orden preypost.txt` y núcleo del
HTML PRE-POST 0.7. Las referencias a Clase 3 USS (2026) son las ya documentadas
en el proyecto original; esta migración no introduce nuevos criterios normativos.

## Geometría

Rectángulo: A=bh, Yc=h/2, I=bh³/12, W=I/(h/2), wpp=gamma A.

Componentes: signo s=+1 para sólidos y -1 para vacíos; Yi=Y inferior+hi/2.

$$A=\sum_i s_i b_i h_i,\quad \bar Y=\frac{\sum_i A_iY_i}{A}$$

$$I=\sum_i\left(\frac{s_i b_i h_i^3}{12}+A_i(Y_i-\bar Y)^2\right)$$

$$c_s=h-\bar Y,\quad c_i=\bar Y,\quad W_s=I/c_s,\quad W_i=I/c_i$$

Las propiedades brutas se obtienen con los sólidos, respecto de su propio
centroide. Las del hormigón se calculan después de restar vacíos. El acero no
aporta rigidez en esta versión: Ap se utiliza para calcular la tensión del acero.

## Cargas y tensiones

$$P_e=(1-r)P_i,\qquad w_t=w_{pp},\qquad w_s=w_{pp}+g+q$$

$$R=wL/2,\quad V(x)=R-wx,\quad M(x)=Rx-wx^2/2,\quad M(L/2)=wL^2/8$$

$$\sigma(y)=-\frac{P}{A}-\frac{(P\cdot e+M(x))y}{I}$$

En esta última fórmula **P·e es el producto de fuerza por excentricidad**.
La fuerza efectiva se denota P_e. En código y memoria se escribe `P * e` o `P e`.
P es Pi en transferencia o P_e en servicio. y se mide desde el centroide hacia
arriba: y superior=cs e y inferior=-ci. La excentricidad de un tendón inferior
es negativa. Compresión negativa; momento externo sagante positivo.

La pendiente de tensiones es k=-(P e+M)/I. Si k es distinto de cero, la coordenada
de tensión cero es y0=-sigmaN/k. El mapa usa el máximo absoluto de las tensiones
extremas en apoyos y centro de luz de ambas etapas como escala común; bajo carga
uniforme esas posiciones contienen los extremos del momento externo.

## Caso rectangular independiente

b=0.4 m; h=0.8 m; L=10 m; gamma=25000 N/m³; Pi=1000000 N;
e=-0.2 m; Ap=0.0007 m²; r=0.15; g=0; q=5000 N/m.

| Resultado | Valor SI |
|---|---:|
| A | 0.32 m² |
| I | 0.017066666666666667 m⁴ |
| Peso propio | 8000 N/m |
| Reacción de transferencia | 40000 N |
| Momento de transferencia | 100000 N·m |
| Tensión superior de transferencia | -781250 Pa |
| Tensión inferior de transferencia | -5468750 Pa |
| Pe servicio | 850000 N |
| Carga de servicio | 13000 N/m |
| Momento de servicio | 162500 N·m |
| Tensión superior de servicio | -2480468.75 Pa |
| Tensión inferior de servicio | -2832031.25 Pa |

Control T: alma 0.12×0.64 m desde Y=0 y ala 0.4×0.16 m desde Y=0.64 m.
A=0.1408 m², Yc=0.5018181818181818 m, I=0.008343427878787879 m⁴.
Estos 15 valores se comparan en `src.validation` con tolerancia relativa 1e-10.

## Unidades

Conversiones heredadas de `src/units.py` del proyecto original: pie=0.3048 m,
pulgada=0.0254 m, libra masa=0.45359237 kg y gravedad estándar=9.80665 m/s².
Libra fuerza=4.4482216152605 N; kip=1000 lbf. El símbolo pcf se usa como lbf/ft³.
La luz se presenta en ft y las dimensiones de sección en in en USCS; cargas en
kip/ft, fuerzas en kip, tensiones en psi y momentos en kip·ft.
