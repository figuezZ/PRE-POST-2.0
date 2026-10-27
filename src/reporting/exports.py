"""Exportaciones directas de la instantánea del ejercicio 1."""
import json
from src.reporting.exercise1 import exercise_pdf

def json_bytes(result, report) -> bytes:
    return json.dumps({'schema_version':'exercise1-1.0','input_si':result['input_si'],
        'report':report},ensure_ascii=False,indent=2,allow_nan=False).encode('utf-8')

def pdf_bytes(report) -> bytes:
    return exercise_pdf(report)
