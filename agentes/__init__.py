"""
Pacote de Agentes - Secretaria Universitária Virtual
"""

from .agente_assistente import AgenteAssistente
from .agente_academico import AgenteAcademico
from .agente_horarios import AgenteHorarios
from .agente_regulamentos import AgenteRegulamentos
from .agente_financeiro import AgenteFinanceiro

__all__ = [
    'AgenteAssistente',
    'AgenteAcademico',
    'AgenteHorarios',
    'AgenteRegulamentos',
    'AgenteFinanceiro'
]
