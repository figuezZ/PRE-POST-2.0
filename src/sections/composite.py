"""Áreas compuestas y teorema de ejes paralelos; docs/formulas.md."""
from dataclasses import dataclass
from math import isfinite
from src.models.project import Component
from src.sections.rectangular import SectionProperties


@dataclass(frozen=True)
class ComponentRow:
    name: str
    sign: int
    b: float
    h: float
    y: float
    area: float
    centroid: float
    d: float
    own: float
    parallel: float


@dataclass
class CompositeProperties(SectionProperties):
    gross_area_m2: float
    gross_inertia_m4: float
    gross_centroid_m: float
    width_m: float
    components: tuple[Component, ...]
    rows: tuple[ComponentRow, ...]


def template(name: str, b: float, h: float) -> tuple[Component, ...]:
    """Mismas proporciones de plantilla que el taller HTML 0.7."""
    shapes = {
        'Rectangular': [('Rectángulo', 1, b, h, 0)],
        'T': [('Alma', 1, .3*b, .8*h, 0), ('Ala superior', 1, b, .2*h, .8*h)],
        'I': [('Ala inferior', 1, .8*b, .18*h, 0), ('Alma', 1, .25*b, .6*h, .18*h),
              ('Ala superior', 1, b, .22*h, .78*h)],
        'Hueca': [('Exterior', 1, b, h, 0), ('Vacío', -1, .5*b, .6*h, .2*h)],
    }
    if name not in shapes:
        raise ValueError('Plantilla desconocida.')
    return tuple(Component(name=n, sign=s, b=w, h=t, y=y) for n, s, w, t, y in shapes[name])


def component_properties(components, gamma: float) -> CompositeProperties:
    if not isfinite(gamma) or gamma <= 0:
        raise ValueError('El peso específico debe ser positivo y finito.')
    parts = tuple(Component.model_validate(p) for p in components)
    if not 1 <= len(parts) <= 24:
        raise ValueError('Use entre 1 y 24 componentes.')
    solids = sorted((p for p in parts if p.sign == 1), key=lambda p: p.y)
    holes = [p for p in parts if p.sign == -1]
    if not solids or abs(solids[0].y) > 1e-10:
        raise ValueError('El primer sólido debe comenzar en Y = 0.')
    for a, b in zip(solids, solids[1:]):
        if abs(b.y - a.y - a.h) > 1e-9:
            raise ValueError('Los sólidos deben tocarse, sin superposición ni separación.')
    for j, p in enumerate(holes):
        if not any(p.b < s.b and p.y >= s.y-1e-10 and p.y+p.h <= s.y+s.h+1e-10 for s in solids):
            raise ValueError('Cada vacío debe quedar dentro de un sólido y ser más estrecho.')
        if any(min(p.y+p.h, q.y+q.h)-max(p.y, q.y) > 1e-10 for q in holes[:j]):
            raise ValueError('Los vacíos no pueden superponerse.')
    height = max(p.y+p.h for p in solids)
    covered = 0.0
    for p in sorted(holes, key=lambda p: p.y):
        if p.y <= covered+1e-10:
            covered = max(covered, p.y+p.h)
    if covered >= height-1e-10:
        raise ValueError('Los vacíos separan completamente la sección en dos piezas.')
    area = sum(p.sign*p.b*p.h for p in parts)
    if area <= 0 or not isfinite(area):
        raise ValueError('Área de hormigón inválida.')
    cy = sum(p.sign*p.b*p.h*(p.y+p.h/2) for p in parts)/area
    rows = tuple(ComponentRow(**p.model_dump(), area=p.sign*p.b*p.h,
        centroid=p.y+p.h/2, d=p.y+p.h/2-cy, own=p.sign*p.b*p.h**3/12,
        parallel=p.sign*p.b*p.h*(p.y+p.h/2-cy)**2) for p in parts)
    inertia = sum(r.own+r.parallel for r in rows)
    gross_area = sum(p.b*p.h for p in solids)
    gross_cy = sum(p.b*p.h*(p.y+p.h/2) for p in solids)/gross_area
    gross_i = sum(p.b*p.h**3/12+p.b*p.h*(p.y+p.h/2-gross_cy)**2 for p in solids)
    if not all(isfinite(v) and v > 0 for v in (inertia, cy, height-cy, gross_i, area*gamma)):
        raise ValueError('Propiedades fuera del rango numérico. Revise las unidades.')
    return CompositeProperties(area, cy, inertia, inertia/(height-cy), inertia/cy,
        area*gamma, height, gross_area, gross_i, gross_cy, max(p.b for p in solids), parts, rows)


def contains_concrete(parts, x: float, y: float) -> bool:
    height = max(p.y+p.h for p in parts if p.sign == 1)
    return (0 < y < height
        and any(p.sign == 1 and abs(x) < p.b/2 and p.y <= y <= p.y+p.h for p in parts)
        and not any(p.sign == -1 and abs(x) <= p.b/2 and p.y <= y <= p.y+p.h for p in parts))


def tendon_eccentricity(section: CompositeProperties, relative_height: float = .1) -> float:
    """Posición inicial de plantilla: 10 % del alto desde la base."""
    return section.height_m*relative_height-section.centroid_from_bottom_m


def append_component(parts, kind: str, gamma: float):
    """Atajos geométricos del editor HTML; dimensiones editables después."""
    sec = component_properties(parts,gamma)
    if kind == 'solid':
        new = Component(name='Sólido añadido',b=sec.width_m,h=.15*sec.height_m,y=sec.height_m)
    elif kind == 'hole':
        solid = next(p for p in sec.components if p.sign == 1)
        new = Component(name='Vacío añadido',sign=-1,b=.3*solid.b,h=.3*solid.h,y=solid.y+.35*solid.h)
    else:
        raise ValueError('Tipo de componente inválido.')
    updated = (*sec.components,new)
    component_properties(updated,gamma)
    return updated
