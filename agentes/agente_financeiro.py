"""
Agente Financeiro - Verificação de Propinas
Este agente verifica se o estudante tem propinas em atraso.
"""

import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class FinanceiroBehaviour(CyclicBehaviour):
    """Comportamento principal do Agente Financeiro"""
    
    async def on_start(self):
        print("✅ Agente Financeiro iniciado.")
        await self.carregar_dados()
    
    async def carregar_dados(self):
        """Carrega dados de estudantes"""
        try:
            with open('/home/runner/work/ProjetoASM/ProjetoASM/data/estudantes.json', 'r', encoding='utf-8') as f:
                self.estudantes_data = json.load(f)
            
            print("💰 Dados financeiros carregados com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            self.estudantes_data = {"estudantes": []}
    
    async def run(self):
        """Processa pedidos relacionados com situação financeira"""
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                content = json.loads(msg.body)
                tipo = content.get("tipo")
                
                if tipo == "verificar_propinas":
                    resposta = await self.verificar_propinas(content)
                elif tipo == "consultar_dividas":
                    resposta = await self.consultar_dividas(content)
                else:
                    resposta = {
                        "status": "erro",
                        "mensagem": "Tipo de pedido desconhecido"
                    }
                
                # Enviar resposta
                reply = Message(to=str(msg.sender))
                reply.set_metadata("performative", "inform")
                reply.body = json.dumps(resposta)
                await self.send(reply)
                
            except Exception as e:
                print(f"❌ Erro no Agente Financeiro: {e}")
    
    async def verificar_propinas(self, content):
        """Verifica se estudante tem propinas em atraso"""
        estudante_id = content.get("estudante_id")
        
        print(f"💳 Verificando situação financeira: {estudante_id}")
        
        # Buscar estudante
        estudante = self.buscar_estudante(estudante_id)
        if not estudante:
            return {
                "aprovado": False,
                "mensagem": "Estudante não encontrado"
            }
        
        # Verificar se tem propinas em atraso
        propinas_em_atraso = estudante.get("propinas_em_atraso", False)
        
        if propinas_em_atraso:
            return {
                "aprovado": False,
                "mensagem": "Estudante tem propinas em atraso. Deve regularizar a situação."
            }
        
        return {
            "aprovado": True,
            "mensagem": "Situação financeira regularizada"
        }
    
    async def consultar_dividas(self, content):
        """Consulta detalhes de dívidas do estudante"""
        estudante_id = content.get("estudante_id")
        
        print(f"📊 Consultando dívidas: {estudante_id}")
        
        estudante = self.buscar_estudante(estudante_id)
        if not estudante:
            return {
                "status": "erro",
                "mensagem": "Estudante não encontrado"
            }
        
        propinas_em_atraso = estudante.get("propinas_em_atraso", False)
        
        if propinas_em_atraso:
            return {
                "status": "sucesso",
                "tem_dividas": True,
                "mensagem": "Estudante tem propinas em atraso",
                "detalhes": {
                    "tipo": "propinas",
                    "status": "em atraso"
                }
            }
        
        return {
            "status": "sucesso",
            "tem_dividas": False,
            "mensagem": "Sem dívidas pendentes"
        }
    
    def buscar_estudante(self, estudante_id):
        """Busca estudante por ID"""
        for estudante in self.estudantes_data.get("estudantes", []):
            if estudante.get("id") == estudante_id:
                return estudante
        return None


class AgenteFinanceiro(Agent):
    """Agente Financeiro - Gestão de propinas e situação financeira"""
    
    async def setup(self):
        """Configuração inicial do agente"""
        print("🚀 Configurando Agente Financeiro...")
        comportamento = FinanceiroBehaviour()
        self.add_behaviour(comportamento)
