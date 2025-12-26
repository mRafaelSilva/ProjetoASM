"""
Exemplo de Uso - Sistema de Secretaria Universitária Virtual

Este arquivo demonstra como usar o sistema programaticamente para fazer
pedidos específicos.
"""

import json
from colorama import init, Fore, Style

init()


def exemplo_inscricao():
    """Exemplo de pedido de inscrição"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print("📝 EXEMPLO: Pedido de Inscrição em Disciplina")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    pedido = {
        "tipo": "inscricao",
        "estudante_id": "20230001",
        "disciplina": "IA201"
    }
    
    print("Pedido a enviar ao Agente Assistente:")
    print(json.dumps(pedido, indent=2, ensure_ascii=False))
    
    print(f"\n{Fore.GREEN}Processamento esperado:")
    print("1. Agente Financeiro verifica propinas")
    print("2. Agente Horários verifica conflitos de horário")
    print("3. Agente Académico verifica:")
    print("   • Pré-requisitos (IA201 requer ASM101)")
    print("   • Vagas disponíveis")
    print("   • Limite de créditos do estudante")
    print("4. Resposta final: Aprovado/Recusado")
    print(f"{Style.RESET_ALL}")


def exemplo_equivalencia():
    """Exemplo de pedido de equivalência"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print("🔄 EXEMPLO: Pedido de Equivalência")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    pedido = {
        "tipo": "equivalencia",
        "estudante_id": "20230003",
        "disciplina_origem": "BD101",
        "disciplina_destino": "RC301"
    }
    
    print("Pedido a enviar ao Agente Assistente:")
    print(json.dumps(pedido, indent=2, ensure_ascii=False))
    
    print(f"\n{Fore.GREEN}Processamento esperado:")
    print("1. Agente Académico verifica:")
    print("   • Se o estudante completou a disciplina de origem")
    print("   • Se os créditos são compatíveis (mínimo 80%)")
    print("2. Resposta final: Aprovado/Recusado")
    print(f"{Style.RESET_ALL}")


def exemplo_estatuto():
    """Exemplo de pedido de estatuto especial"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print("📋 EXEMPLO: Pedido de Estatuto Especial")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    pedido = {
        "tipo": "estatuto",
        "estudante_id": "20230001",
        "tipo_estatuto": "estudante-trabalhador",
        "documentos": [
            "Contrato de trabalho válido",
            "Declaração da entidade empregadora"
        ]
    }
    
    print("Pedido a enviar ao Agente Assistente:")
    print(json.dumps(pedido, indent=2, ensure_ascii=False))
    
    print(f"\n{Fore.GREEN}Processamento esperado:")
    print("1. Agente Regulamentos verifica:")
    print("   • Se já tem outro estatuto")
    print("   • Se apresentou todos os documentos necessários")
    print("2. Resposta final inclui benefícios do estatuto")
    print(f"{Style.RESET_ALL}")
    
    print(f"\n{Fore.YELLOW}Estatutos disponíveis:")
    estatutos = [
        "estudante-trabalhador",
        "atleta",
        "dirigente-associativo",
        "necessidades-especiais"
    ]
    for e in estatutos:
        print(f"   • {e}")
    print(f"{Style.RESET_ALL}")


def exemplo_consulta_horario():
    """Exemplo de consulta de horário"""
    print(f"\n{Fore.CYAN}{'='*70}")
    print("⏰ EXEMPLO: Consulta de Horário")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    pedido = {
        "tipo": "consulta_horario",
        "estudante_id": "20230001"
    }
    
    print("Pedido a enviar ao Agente Assistente:")
    print(json.dumps(pedido, indent=2, ensure_ascii=False))
    
    print(f"\n{Fore.GREEN}Processamento esperado:")
    print("1. Agente Horários consulta disciplinas inscritas")
    print("2. Retorna lista completa de horários organizados por dia")
    print(f"{Style.RESET_ALL}")


def estrutura_resposta():
    """Mostra estrutura de respostas"""
    print(f"\n{Fore.MAGENTA}{'='*70}")
    print("📤 ESTRUTURA DE RESPOSTAS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Resposta de Inscrição (Aprovada):")
    resposta_aprovada = {
        "status": "aprovado",
        "mensagem": "Inscrição aprovada em Inteligência Artificial (6 créditos)"
    }
    print(json.dumps(resposta_aprovada, indent=2, ensure_ascii=False))
    
    print("\nResposta de Inscrição (Recusada):")
    resposta_recusada = {
        "status": "recusado",
        "mensagem": "Propinas em atraso. Regularize a situação antes de se inscrever."
    }
    print(json.dumps(resposta_recusada, indent=2, ensure_ascii=False))
    
    print("\nResposta de Estatuto (Aprovada):")
    resposta_estatuto = {
        "status": "aprovado",
        "mensagem": "Estatuto de estudante-trabalhador aprovado!",
        "beneficios": [
            "Horário flexível",
            "Prioridade em inscrições noturnas",
            "Regime de avaliação contínua adaptado"
        ]
    }
    print(json.dumps(resposta_estatuto, indent=2, ensure_ascii=False))


def cenarios_comuns():
    """Descreve cenários comuns"""
    print(f"\n{Fore.BLUE}{'='*70}")
    print("🎯 CENÁRIOS COMUNS")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    cenarios = [
        {
            "titulo": "Estudante quer se inscrever em disciplina",
            "passos": [
                "1. Verificar se não tem propinas em atraso",
                "2. Verificar se há conflito de horário",
                "3. Verificar pré-requisitos e vagas",
                "4. Processar inscrição"
            ]
        },
        {
            "titulo": "Estudante trabalhador pede estatuto",
            "passos": [
                "1. Submeter documentos (contrato, declaração)",
                "2. Agente Regulamentos valida documentação",
                "3. Estatuto concedido com benefícios"
            ]
        },
        {
            "titulo": "Estudante com conflito de horário",
            "passos": [
                "1. Sistema detecta sobreposição de horários",
                "2. Inscrição é bloqueada",
                "3. Estudante pode consultar horário atual",
                "4. Estudante escolhe outra disciplina"
            ]
        },
        {
            "titulo": "Pedido de equivalência",
            "passos": [
                "1. Verificar se completou disciplina de origem",
                "2. Comparar créditos (mínimo 80%)",
                "3. Aprovar ou recusar equivalência"
            ]
        }
    ]
    
    for i, cenario in enumerate(cenarios, 1):
        print(f"{Fore.YELLOW}{i}. {cenario['titulo']}{Style.RESET_ALL}")
        for passo in cenario['passos']:
            print(f"   {passo}")
        print()


def main():
    """Função principal"""
    print(f"\n{Fore.GREEN}{'='*70}")
    print("📚 EXEMPLOS DE USO - SISTEMA DE SECRETARIA UNIVERSITÁRIA")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    
    print("Este arquivo demonstra como interagir com o sistema.")
    print("Os exemplos mostram os diferentes tipos de pedidos disponíveis.\n")
    
    # Mostrar exemplos
    exemplo_inscricao()
    exemplo_equivalencia()
    exemplo_estatuto()
    exemplo_consulta_horario()
    
    # Mostrar estrutura de respostas
    estrutura_resposta()
    
    # Cenários comuns
    cenarios_comuns()
    
    # Informações finais
    print(f"{Fore.CYAN}{'='*70}")
    print("💡 DICAS DE USO")
    print(f"{'='*70}{Style.RESET_ALL}\n")
    print("1. Sempre use o Agente Assistente como ponto de entrada")
    print("2. O Agente Assistente coordena automaticamente com outros agentes")
    print("3. Verifique os dados em data/*.json para entender as regras")
    print("4. Para uso em produção, configure um servidor XMPP")
    print("5. Adapte os JIDs dos agentes às suas necessidades\n")
    
    print(f"{Fore.GREEN}Para executar o sistema completo:")
    print(f"   python main.py{Style.RESET_ALL}\n")


if __name__ == "__main__":
    main()
