# Fichas manuales — guía editable

Todas pendientes. Imprimir docs/Fichas_manuales.pdf o editar su DOCX. Resolver en papel y anexar evidencia original; ver contribuciones.md.

## F01 Rectángulo, peso y módulos

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: A=bh; I=bh³/12; W=I/c; g=γA

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A: A=.32 m²; I=.017066666667 m⁴; W=.042666666667 m³; g=8 kN/m

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.sections.rectangular.calculate_rectangular_properties; pruebas: test_rectangular_properties

## F02 Secciones T/I/hueca, centroide y vacíos

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: A=ΣAi; Y=ΣAiYi/A; I=Σ(Ii+Ai di²)

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: T: A=.1408 m²; Y=.501818181818 m; I=.008343427879 m⁴. Repetir I y hueca con las plantillas de la app.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.sections.composite.component_properties; template; contains_concrete; tendon_eccentricity; pruebas: test_equilibrium; test_invalid_components; test_void_and_loads_and_selection

## F03 Sección neta y transformada

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: An=Ag−Ap; At=Ag+(n−1)Ap; n=Ep/Ec; Y=ΣAiYi/A; I=Σ(Ii+Ai di²)

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A: An=.3193 m²; n=195/34. Acero concentrado; propiedades auxiliares.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.sections.transformed.transformed_rectangular; pruebas: test_transformed_concentrated_steel

## F04 Reacciones, corte y momento

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: R=wL/2; V=R−wx; M=Rx−wx²/2; Mmax=wL²/8

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A histórico: Rtr=40 kN; Mtr=100 kN m; Rs=65 kN; Ms=162.5 kN m.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.analysis.elastic.uniform_load_effects; generate_beam_diagram; pipeline.stage_at; diagrams; pruebas: test_equilibrium; test_manual_validation

## F05 Superposición y campo de tensiones

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: σ=−P/A−(Pe+M)y/I; y0=−(−P/A)/(−(Pe+M)/I)

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A histórico centro: transferencia sup/inf −.78125/−5.46875 MPa; servicio −2.48046875/−2.83203125 MPa. Contrastar tres x y tres fibras.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.analysis.elastic.calculate_elastic_stresses; pipeline.stresses; fiber_at; stress_profile; stress_field; stress_scale; selected_coordinates; pruebas: test_equilibrium; test_void_and_loads_and_selection; test_migration_against_original_javascript

## F06 Fuerzas y pérdidas por mecanismo

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: Pe=(1−r)P0 en modo declarado; ES=n[P0 k+Mg e/I]/(1+nAp k); k=1/A+e²/I; SH=(17−.15H) ksi; CR=max(0,12fcgp−7fcdp); RE=max(0,.3[20ksi−.4ES−.2(SH+CR)]); Pt=P0−Ap ES; Pe=Pt−Ap(SH+CR+RE)

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A ampliado ES=27.251591264; SH=44.815922406; CR=50.310630026; RE=32.390759661 MPa; Pt=980.923886 kN; Pe=891.661768 kN. No aplicar 15% adicional.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.analysis.pipeline.effective_force; prestress.losses.calculate_losses; pruebas: test_loss_equilibrium_and_no_double_counting; test_centered_tendon_closed_form; test_humidity_sensitivity

## F07 Envolvente y límites de tensiones

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: Evaluar x=lt,L/2,L−lt; lt=50db. Compresión ≤.6fci transferencia; ≤.6fc total; ≤.45fc permanente. Tracción ≤.25√fci transferencia; objetivo U ≤.7√fc; acero ≤min(.74fpu,.82fpy)

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A ampliado: acero 1401.319837 MPa frente a 1372.68 MPa: NO CUMPLE. Raíces con fc en MPa. Extremos no verificados.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.checks.engineering.evaluate; pruebas: test_no_global_pass_and_real_noncompliance; test_reports_use_real_losses_and_states

## F08 Descompresión, fisuración y carga última

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: Mdec=Pe(W/A−e); Mcr=Mdec+.7√fc W; wu=max(1.4D,1.2D+1.6L); Mu=wu L²/8

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A ampliado Mu=220 kN m; Mcr=497.57228 kN m; φMn≥1.2Mcr.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.checks.engineering.evaluate; pruebas: test_reports_use_real_losses_and_states; test_no_global_pass_and_real_noncompliance

## F09 Flexión resistente

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: β1=max(.65,.85−.05max(fc−30,0)/7); ρ=Ap/(b dp); fps=fpu[1−(γp/β1)ρ fpu/fc]; a=Ap fps/(.85fc b); c=a/β1; ε=.003(dp−c)/c; Mn=Ap fps(dp−a/2)

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A ampliado: fps=1775.481282 MPa; a=.08123117 m; c=.10934965 m; φMn=625.701232 kN m. φ=.9; ε≥.005 y fpe≥.5fpu.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.checks.engineering.rectangular_flexure; pruebas: test_flexure_independent_equilibrium; test_limits_not_silently_accepted

## F10 Corte y armadura transversal

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: d=max(dp,.8h); Vu=wu(L/2−d); Vc=[√fc/20+5 min(Vu dp/M,1)]bd; límites √fc bd/6 y .4√fc bd; Vs=Av fy d/s; φVn=.75(Vc+Vs); mínimo Av/s=max(√fc/16,.33)b/fy; smax=min(.75h,.4m)

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: B2: Vu=360.192 kN; M=.3053568 MN m; Vc=701.084874 kN; Av/s mínimo=326.025332 mm²/m. Revisar cap Vcw y reducción en extremo.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.checks.engineering.shear_capacity; evaluate; pruebas: test_source_shear_control; test_limits_not_silently_accepted

## F11 Flecha instantánea y contraflecha

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: δg=5wL⁴/(384EcI); δp=Pe e L²/(8EcI); δ=δg+δp; δL≤L/divisor

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: A ampliado: δtr=−2.755162 mm; δs=−.924482 mm; δL=1.121970 mm. Positivo abajo; contraflecha negativa. Diferida pendiente.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.checks.engineering.elastic_deflections; evaluate; pruebas: test_deflection_independent_curvature_integral; test_no_global_pass_and_real_noncompliance

## F12 Unidades, etapas y reproducción

Objetivo: desarrollar y contrastar este procedimiento.

Esquema: dibujar viga/sección con cotas, apoyos, cargas y tendón.

Datos y procedencia: caso A o B2 especificado en el cuaderno; anotar unidades y fuente.

Hipótesis: modelo no fisurado, recto y prismático; agregar restricciones aplicables.

Signos: compresión negativa; e/y arriba; M sagante positivo.

Ecuaciones: SI: m,N,Pa; 1 MPa=10⁶ Pa; 1 mm²=10⁻⁶ m²; 1 kN m=1000 N m. Δ=|manual−app|; εr=Δ/|manual| si no nulo

Sustitución paso a paso: PENDIENTE EN PAPEL.

Operaciones con unidades: PENDIENTE EN PAPEL.

Resultado e interpretación: PENDIENTE.

Contraste impreso: Misma viga SI/USCS; resultados físicos invariantes. Repetir memoria en x=L/2 y x=L/4; firmas y archivos de evidencia pendientes.

Diferencia absoluta/relativa: PENDIENTE.

Conclusión y discrepancias: PENDIENTE.

Desarrolló / revisó / fecha / evidencia: PENDIENTE.

Función: src.units.to_si; from_si; analysis.pipeline.analyze; analysis.memory.calculation_memory; reporting.design.design_memory; pruebas: test_conversion_roundtrip; test_units_known_and_bad_inputs; test_new_interface_and_invalidation; test_exports_numeric_and_readable

Nota F09: la compatibilidad iterativa del material docente todavía no está implementada. Ver contraste_material_docente.md; no confundir con fps aproximado CIRSOC.
