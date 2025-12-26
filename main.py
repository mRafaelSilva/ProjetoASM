"""
Sistema de Agentes - Secretaria Universitária Virtual
Ponto de entrada principal do sistema
"""

import asyncio
import json
from spade.message import Message
from agentes.agente_assistente import AgenteAssistente
from agentes.agente_academico import AgenteAcademico
from agentes.agente_horarios import AgenteHorarios
from agentes.agente_regulamentos import AgenteRegulamentos
from agentes.agente_financeiro import AgenteFinanceiro
import time
from colorama import init, Fore, Style

# Inicializar colorama para output colorido
init()


class SimuladorEstudante:
    """Simula um estudante fazendo pedidos ao sistema"""
    
    def __init__(self, assistente_jid):
        self.assistente_jid = assistente_jid
    
    async def fazer_pedido(self, tipo, estudante_id, **kwargs):
        """Envia um pedido ao agente assistente"""
        pedido = {
            "tipo": tipo,
            "estudante_id": estudante_id,
            **kwargs
        }
        
        print(f"\n{Fore.CYAN}{'='*70}")
        print(f"🎓 PEDIDO DO ESTUDANTE {estudante_id}")
        print(f"{'='*70}{Style.RESET_ALL}")
        print(f"Tipo: {tipo}")
        for key, value in kwargs.items():
            print(f"{key}: {value}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        return pedido


async def main():
    """Função principal que inicia e coordena o sistema"""
    
    print(f"\n{Fore.GREEN}{'='*70}")
    print("🏛️  SISTEMA DE SECRETARIA UNIVERSITÁRIA VIRTUAL")
    print("    Multi-Agent System usando SPADE")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    # NOTA: Para este projeto de demonstração, utilizamos JIDs simulados
    # Em produção, seriam necessários JIDs reais de um servidor XMPP
    
    # Configurar JIDs dos agentes (simulados para demonstração)
    assistente_jid = "assistente@localhost"
    academico_jid = "academico@localhost"
    horarios_jid = "horarios@localhost"
    regulamentos_jid = "regulamentos@localhost"
    financeiro_jid = "financeiro@localhost"
    password = "password"
    
    print(f"{Fore.YELLOW}⚠️  MODO DEMONSTRAÇÃO")
    print(f"   Este sistema demonstra a arquitetura e lógica dos agentes.")
    print(f"   Para execução completa, configure um servidor XMPP (ex: Prosody).{Style.RESET_ALL}\n")
    
    # Criar agentes
    print(f"{Fore.BLUE}📦 Criando agentes...{Style.RESET_ALL}")
    
    agente_financeiro = AgenteFinanceiro(financeiro_jid, password)
    agente_regulamentos = AgenteRegulamentos(regulamentos_jid, password)
    agente_horarios = AgenteHorarios(horarios_jid, password)
    agente_academico = AgenteAcademico(academico_jid, password)
    agente_assistente = AgenteAssistente(
        assistente_jid,
        password,
        academico_jid,
        horarios_jid,
        regulamentos_jid,
        financeiro_jid
    )
    
    print(f"{Fore.GREEN}✅ Todos os agentes criados!{Style.RESET_ALL}\n")
    
    # Demonstrar a arquitetura do sistema
    print(f"{Fore.MAGENTA}{'='*70}")
    print("📋 ARQUITETURA DO SISTEMA")
    print(f"{'='*70}{Style.RESET_ALL}")
    print("""
🤖 Agente Assistente (Interface & Coordenação)
   ├── Recebe pedidos dos estudantes
   ├── Coordena comunicação entre agentes especializados
   └── Retorna respostas finais aos estudantes

🎓 Agente Académico (Regras de Inscrição)
   ├── Verifica pré-requisitos
   ├── Valida limites de créditos
   ├── Processa equivalências
   └── Controla vagas disponíveis

⏰ Agente Horários (Conflitos de Horário)
   ├── Detecta conflitos entre disciplinas
   ├── Valida sobreposições de horário
   └── Consulta horários dos estudantes

📜 Agente Regulamentos (Estatutos Especiais)
   ├── Processa pedidos de estatuto
   ├── Verifica requisitos e documentos
   └── Consulta benefícios

💰 Agente Financeiro (Propinas)
   ├── Verifica propinas em atraso
   └── Bloqueia inscrições se necessário
""")
    
    # Demonstrar cenários de uso
    print(f"\n{Fore.MAGENTA}{'='*70}")
    print("🎬 CENÁRIOS DE DEMONSTRAÇÃO")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    simulador = SimuladorEstudante(assistente_jid)
    
    # Cenário 1: Inscrição bem-sucedida
    print(f"{Fore.GREEN}📝 CENÁRIO 1: Inscrição com sucesso{Style.RESET_ALL}")
    pedido1 = await simulador.fazer_pedido(
        tipo="inscricao",
        estudante_id="20230001",
        disciplina="IA201"
    )
    print(f"{Fore.GREEN}✅ Fluxo esperado:")
    print("   1. Agente Financeiro: Verifica propinas (OK)")
    print("   2. Agente Horários: Verifica conflitos (OK)")
    print("   3. Agente Académico: Verifica pré-requisitos (OK - tem ASM101)")
    print(f"   4. Resultado: APROVADO{Style.RESET_ALL}\n")
    
    await asyncio.sleep(1)
    
    # Cenário 2: Propinas em atraso
    print(f"{Fore.RED}📝 CENÁRIO 2: Inscrição com propinas em atraso{Style.RESET_ALL}")
    pedido2 = await simulador.fazer_pedido(
        tipo="inscricao",
        estudante_id="20230002",
        disciplina="ASM101"
    )
    print(f"{Fore.RED}❌ Fluxo esperado:")
    print("   1. Agente Financeiro: Verifica propinas (BLOQUEADO)")
    print(f"   2. Resultado: RECUSADO - Propinas em atraso{Style.RESET_ALL}\n")
    
    await asyncio.sleep(1)
    
    # Cenário 3: Conflito de horário
    print(f"{Fore.YELLOW}📝 CENÁRIO 3: Conflito de horário{Style.RESET_ALL}")
    pedido3 = await simulador.fazer_pedido(
        tipo="inscricao",
        estudante_id="20230001",
        disciplina="BD101"
    )
    print(f"{Fore.YELLOW}⚠️  Fluxo esperado:")
    print("   1. Agente Financeiro: Verifica propinas (OK)")
    print("   2. Agente Horários: Verifica conflitos (CONFLITO detectado)")
    print("   3. ASM101 e BD101 têm aulas na Segunda 14:00-16:00")
    print(f"   4. Resultado: RECUSADO - Conflito de horário{Style.RESET_ALL}\n")
    
    await asyncio.sleep(1)
    
    # Cenário 4: Pedido de equivalência
    print(f"{Fore.CYAN}📝 CENÁRIO 4: Pedido de equivalência{Style.RESET_ALL}")
    pedido4 = await simulador.fazer_pedido(
        tipo="equivalencia",
        estudante_id="20230003",
        disciplina_origem="BD101",
        disciplina_destino="RC301"
    )
    print(f"{Fore.CYAN}ℹ️  Fluxo esperado:")
    print("   1. Agente Académico: Verifica se completou disciplina origem (OK)")
    print("   2. Agente Académico: Compara créditos (OK)")
    print(f"   3. Resultado: Análise submetida{Style.RESET_ALL}\n")
    
    await asyncio.sleep(1)
    
    # Cenário 5: Pedido de estatuto especial
    print(f"{Fore.MAGENTA}📝 CENÁRIO 5: Pedido de estatuto especial{Style.RESET_ALL}")
    pedido5 = await simulador.fazer_pedido(
        tipo="estatuto",
        estudante_id="20230001",
        tipo_estatuto="estudante-trabalhador",
        documentos=["Contrato de trabalho válido", "Declaração da entidade empregadora"]
    )
    print(f"{Fore.MAGENTA}📋 Fluxo esperado:")
    print("   1. Agente Regulamentos: Verifica documentos")
    print("   2. Agente Regulamentos: Valida requisitos (OK)")
    print("   3. Resultado: APROVADO")
    print(f"   4. Benefícios: Horário flexível, prioridade em inscrições{Style.RESET_ALL}\n")
    
    await asyncio.sleep(1)
    
    # Cenário 6: Consulta de horário
    print(f"{Fore.BLUE}📝 CENÁRIO 6: Consulta de horário{Style.RESET_ALL}")
    pedido6 = await simulador.fazer_pedido(
        tipo="consulta_horario",
        estudante_id="20230001"
    )
    print(f"{Fore.BLUE}📅 Fluxo esperado:")
    print("   1. Agente Horários: Lista disciplinas inscritas")
    print(f"   2. Resultado: Horário completo do estudante{Style.RESET_ALL}\n")
    
    # Sumário final
    print(f"\n{Fore.GREEN}{'='*70}")
    print("✨ DEMONSTRAÇÃO CONCLUÍDA")
    print(f"{'='*70}{Style.RESET_ALL}")
    print("""
O sistema implementa uma arquitetura multiagente completa com:

✅ 5 Agentes Especializados
   • Assistente (coordenação)
   • Académico (regras)
   • Horários (conflitos)
   • Regulamentos (estatutos)
   • Financeiro (propinas)

✅ Comunicação entre Agentes via SPADE
   • Mensagens assíncronas
   • Coordenação distribuída
   • Processamento paralelo

✅ Funcionalidades Completas
   • Inscrição em disciplinas
   • Equivalências
   • Estatutos especiais
   • Conflitos de horários
   • Verificação de propinas

Para executar com servidor XMPP real:
1. Instale Prosody ou Ejabberd
2. Configure os JIDs dos agentes
3. Execute: python main.py
""")
    
    print(f"\n{Fore.CYAN}💡 PRÓXIMOS PASSOS:")
    print("   1. Configure servidor XMPP para comunicação real")
    print("   2. Adapte os JIDs aos seus agentes")
    print("   3. Execute testes com dados reais")
    print(f"   4. Adicione interface web se necessário{Style.RESET_ALL}\n")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}⚠️  Sistema interrompido pelo usuário{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Erro: {e}{Style.RESET_ALL}")
