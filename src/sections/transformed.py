"""Sección rectangular con acero concentrado en un nivel, perfectamente adherente.
Teorema de ejes paralelos. Se desprecia inercia propia de los cordones.
Propiedades auxiliares: no sustituyen Ig en verificaciones de sección bruta.
"""
def transformed_rectangular(b,h,ap,yp,ep,ec):
    if not (b>0 and h>0 and 0<ap<b*h and 0<yp<h and ep>0 and ec>0):
        raise ValueError('Datos incompatibles para sección neta/transformada.')
    ag=b*h;yg=h/2;ig=b*h**3/12;n=ep/ec
    def properties(delta):
        area=ag+delta
        y=(ag*yg+delta*yp)/area
        inertia=ig+ag*(yg-y)**2+delta*(yp-y)**2
        if inertia<=0:raise ValueError('Inercia no positiva; aproximación de acero concentrado inaplicable.')
        return dict(area_m2=area,centroid_m=y,inertia_m4=inertia)
    return dict(net=properties(-ap),transformed=properties((n-1)*ap),modular_ratio=n,
                note='Acero concentrado; sin ductos ni inercia propia. Propiedades auxiliares; análisis de clase U conserva sección bruta.')
