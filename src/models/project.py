"""Contrato extendido para conservar el taller de la versión HTML 0.7.

El BeamInput solicitado se conserva literalmente en inputs.py.
"""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator
from src.models.inputs import BeamInput
from src.models.design import DesignOptions


class Component(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False, extra='forbid', frozen=True)
    name: str = Field(default='Componente', min_length=1, max_length=80)
    sign: Literal[1, -1] = 1
    b: float = Field(gt=0)
    h: float = Field(gt=0)
    y: float = Field(ge=0)


class ProjectInput(BeamInput):
    model_config = ConfigDict(allow_inf_nan=False, extra='forbid', frozen=True)
    project: str = Field(default='PRE-POST', max_length=160)
    author: str = Field(default='', max_length=160)
    design: DesignOptions | None = None
    components: tuple[Component, ...] = Field(default=(), max_length=24)

    @model_validator(mode='after')
    def validate_physics(self) -> 'ProjectInput':
        if self.fc_pa < self.fci_pa:
            raise ValueError("f'c no puede ser menor que f'ci.")
        if self.initial_force_n / self.steel_area_m2 > 1860e6:
            raise ValueError('La tensión inicial del acero supera 1860 MPa.')
        if not self.components and abs(self.eccentricity_m) >= self.height_m / 2:
            raise ValueError('El tendón debe estar dentro de la sección bruta.')
        # En secciones compuestas, analysis.pipeline comprueba el centroide real
        # y excluye los vacíos; la regla h/2 solo corresponde al rectángulo.
        return self


DEFAULT_INPUT = dict(
    span_m=10.0, width_m=0.4, height_m=0.8, unit_weight_n_m3=25000.0,
    fci_pa=35e6, fc_pa=45e6, dead_load_n_m=0.0, live_load_n_m=5000.0,
    initial_force_n=1e6, eccentricity_m=-0.2, steel_area_m2=0.0007,
    loss_ratio=0.15,
)
