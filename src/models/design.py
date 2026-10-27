"""Opciones explícitas de la extensión académica; SI: m, N, Pa."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, model_validator

class DesignOptions(BaseModel):
    model_config = ConfigDict(allow_inf_nan=False, extra='forbid', frozen=True)
    system: Literal['pretensado_recto_adherente'] = 'pretensado_recto_adherente'
    loss_method: Literal['declarada', 'fhwa_2003'] = 'fhwa_2003'
    ep_pa: float = Field(default=195e9, gt=0)
    eci_pa: float = Field(default=30e9, gt=0)
    ec_pa: float = Field(default=34e9, gt=0)
    humidity_percent: float = Field(default=70, ge=0, le=100)
    fpu_pa: float = Field(default=1860e6, gt=0)
    fpy_pa: float = Field(default=1674e6, gt=0)
    stirrup_fy_pa: float = Field(default=420e6, gt=0, le=420e6)
    stirrup_diameter_m: float = Field(default=.008, gt=0)
    stirrup_legs: int = Field(default=2, ge=2, le=8)
    stirrup_spacing_m: float = Field(default=.2, gt=0)
    strand_diameter_m: float = Field(default=.0127, gt=0)
    live_deflection_divisor: float = Field(default=360, gt=0)
    criterion_note: str = Field(default='CIRSOC 201-2005 como referencia académica; adopción USS pendiente.', min_length=10)

    @model_validator(mode='after')
    def valid_material(self):
        if self.fpy_pa > self.fpu_pa or self.fpy_pa < .8*self.fpu_pa:
            raise ValueError('Se requiere 0.8 fpu <= fpy <= fpu para la aproximación adoptada.')
        return self
