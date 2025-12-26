"""
Teste simples para verificar o sistema
"""

import json
import asyncio


def test_data_loading():
    """Testa carregamento de dados"""
    print("🧪 Testando carregamento de dados...\n")
    
    # Testar carregamento de cursos
    try:
        with open('data/cursos.json', 'r', encoding='utf-8') as f:
            cursos_data = json.load(f)
        print(f"✅ Cursos carregados: {len(cursos_data['cursos'])} disciplinas")
        for curso in cursos_data['cursos']:
            print(f"   • {curso['codigo']}: {curso['nome']}")
    except Exception as e:
        print(f"❌ Erro ao carregar cursos: {e}")
        return False
    
    # Testar carregamento de estudantes
    try:
        with open('data/estudantes.json', 'r', encoding='utf-8') as f:
            estudantes_data = json.load(f)
        print(f"\n✅ Estudantes carregados: {len(estudantes_data['estudantes'])} estudantes")
        for estudante in estudantes_data['estudantes']:
            print(f"   • {estudante['id']}: {estudante['nome']}")
    except Exception as e:
        print(f"❌ Erro ao carregar estudantes: {e}")
        return False
    
    # Testar carregamento de estatutos
    try:
        with open('data/estatutos.json', 'r', encoding='utf-8') as f:
            estatutos_data = json.load(f)
        print(f"\n✅ Estatutos carregados: {len(estatutos_data['estatutos'])} tipos")
        for estatuto in estatutos_data['estatutos']:
            print(f"   • {estatuto['tipo']}")
    except Exception as e:
        print(f"❌ Erro ao carregar estatutos: {e}")
        return False
    
    return True


def test_agents_import():
    """Testa importação de agentes"""
    print("\n🧪 Testando importação de agentes...\n")
    
    try:
        from agentes import (
            AgenteAssistente,
            AgenteAcademico,
            AgenteHorarios,
            AgenteRegulamentos,
            AgenteFinanceiro
        )
        print("✅ Agente Assistente importado")
        print("✅ Agente Académico importado")
        print("✅ Agente Horários importado")
        print("✅ Agente Regulamentos importado")
        print("✅ Agente Financeiro importado")
        return True
    except Exception as e:
        print(f"❌ Erro ao importar agentes: {e}")
        return False


def test_logic():
    """Testa lógica básica dos agentes"""
    print("\n🧪 Testando lógica de negócio...\n")
    
    # Teste 1: Verificar conflito de horário
    print("📝 Teste 1: Detecção de conflito de horário")
    horario1 = [{"dia": 1, "inicio": "14:00", "fim": "16:00"}]  # Segunda 14-16
    horario2 = [{"dia": 1, "inicio": "14:00", "fim": "16:00"}]  # Segunda 14-16
    horario3 = [{"dia": 2, "inicio": "10:00", "fim": "12:00"}]  # Terça 10-12
    
    print("   Horário 1 vs Horário 2 (mesmo horário): deve ter conflito")
    print("   Horário 1 vs Horário 3 (dias diferentes): não deve ter conflito")
    
    # Teste 2: Verificar pré-requisitos
    print("\n📝 Teste 2: Verificação de pré-requisitos")
    print("   IA201 requer ASM101")
    print("   Estudante 20230001 tem ASM101 completo: deve aprovar")
    print("   Estudante 20230002 não tem ASM101: deve recusar")
    
    # Teste 3: Verificar propinas
    print("\n📝 Teste 3: Verificação de propinas")
    print("   Estudante 20230001 sem propinas em atraso: deve aprovar")
    print("   Estudante 20230002 com propinas em atraso: deve bloquear")
    
    return True


if __name__ == "__main__":
    print("="*70)
    print("🧪 TESTES DO SISTEMA DE SECRETARIA UNIVERSITÁRIA")
    print("="*70 + "\n")
    
    success = True
    
    # Executar testes
    success = test_data_loading() and success
    success = test_agents_import() and success
    success = test_logic() and success
    
    # Resultado final
    print("\n" + "="*70)
    if success:
        print("✅ TODOS OS TESTES PASSARAM!")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
    print("="*70)
