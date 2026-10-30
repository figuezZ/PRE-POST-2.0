"""Entrada única de producción: ejercicio 1 del set."""
from src.models.exercise1 import Exercise1Input
from src.exercises.exercise1 import solve_exercise1

def analyze(data: Exercise1Input | dict) -> dict:
    return solve_exercise1(Exercise1Input.model_validate(data))
