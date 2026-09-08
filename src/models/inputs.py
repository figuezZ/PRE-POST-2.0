from pydantic import BaseModel, Field, model_validator

class BeamInput(BaseModel):
    span_m: float = Field(..., gt=0)
    width_m: float = Field(..., gt=0)
    height_m: float = Field(..., gt=0)
    unit_weight_n_m3: float = Field(..., gt=0)
    fci_pa: float = Field(..., gt=0)
    fc_pa: float = Field(..., gt=0)
    dead_load_n_m: float = Field(default=0.0, ge=0)
    live_load_n_m: float = Field(default=0.0, ge=0)
    initial_force_n: float = Field(..., gt=0)
    eccentricity_m: float = Field(...)
    steel_area_m2: float = Field(..., gt=0)
    loss_ratio: float = Field(..., ge=0, lt=1)

    @model_validator(mode='after')
    def validate_physics(self) -> 'BeamInput':
        if self.fc_pa < self.fci_pa: raise ValueError("f'c no puede ser menor que f'ci.")
        if abs(self.eccentricity_m) >= self.height_m / 2: raise ValueError("El tendón debe estar dentro de la sección bruta.")
        if (self.initial_force_n / self.steel_area_m2) > 1860e6: raise ValueError("La tensión inicial del acero supera 1860 MPa.")
        return self
