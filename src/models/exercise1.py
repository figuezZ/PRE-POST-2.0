"""Ejercicio 1: datos seccionales del set, sin inventar luz ni pérdidas."""
from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,model_validator

class Exercise1Input(BaseModel):
    model_config=ConfigDict(extra='forbid',allow_inf_nan=False,frozen=True)
    case_type: Literal['set_ejercicio_1']='set_ejercicio_1'
    width_m: float=Field(default=.4,gt=0)
    height_m: float=Field(default=.9,gt=0)
    steel_depth_m: float=Field(default=.8,gt=0)
    fc_pa: float=Field(default=30e6,gt=0)
    service_moment_n_m: float=Field(default=1e6,gt=0)
    effective_steel_stress_pa: float=Field(default=1150e6,gt=0)
    fpu_pa: float=Field(default=1860e6,gt=0)
    fpy_pa: float=Field(default=1700e6,gt=0)
    moment_factor: float=Field(default=1.6,gt=0)
    force_rounding_n: float=Field(default=10000,gt=0)

    @model_validator(mode='after')
    def domain(self):
        if not self.height_m/2 < self.steel_depth_m < self.height_m:
            raise ValueError('Se requiere tendón inferior dentro de la sección: h/2 < dp < h.')
        if not .8*self.fpu_pa <= self.fpy_pa <= self.fpu_pa:
            raise ValueError('Se requiere 0.8 fpu <= fpy <= fpu.')
        if not .5*self.fpu_pa <= self.effective_steel_stress_pa < self.fpu_pa:
            raise ValueError('Se requiere 0.5 fpu <= fpe < fpu para la aproximación resistente.')
        return self
