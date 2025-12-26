"""
Agente Regulamentos - Gestão de Estatutos Especiais
Este agente processa pedidos de estatutos especiais (estudante-trabalhador, atleta, etc.)
"""

import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class RegulamentosBehaviour(CyclicBehaviour):
    """Comportamento principal do Agente Regulamentos"""
    
    async def on_start(self):
        print("✅ Agente Regulamentos iniciado.")
        await self.carregar_dados()
    
    async def carregar_dados(self):
        """Carrega dados de estatutos e estudantes"""
        try:
            with open('/home/runner/work/ProjetoASM/ProjetoASM/data/estatutos.json', 'r', encoding='utf-8') as f:
                self.estatutos_data = json.load(f)
            
            with open('/home/runner/work/ProjetoASM/ProjetoASM/data/estudantes.json', 'r', encoding='utf-8') as f:
                self.estudantes_data = json.load(f)
            
            print("📜 Dados de regulamentos carregados com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            self.estatutos_data = {"estatutos": []}
            self.estudantes_data = {"estudantes": []}
    
    async def run(self):
        """Processa pedidos relacionados com estatutos"""
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                content = json.loads(msg.body)
                tipo = content.get("tipo")
                
                if tipo == "verificar_estatuto":
                    resposta = await self.verificar_estatuto(content)
                elif tipo == "consultar_estatuto":
                    resposta = await self.consultar_estatuto(content)
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
                print(f"❌ Erro no Agente Regulamentos: {e}")
    
    async def verificar_estatuto(self, content):
        """Verifica e processa pedido de estatuto especial"""
        estudante_id = content.get("estudante_id")
        tipo_estatuto = content.get("tipo_estatuto")
        documentos = content.get("documentos", [])
        
        print(f"📋 Verificando pedido de estatuto: {estudante_id} -> {tipo_estatuto}")
        
        # Buscar estudante
        estudante = self.buscar_estudante(estudante_id)
        if not estudante:
            return {
                "status": "recusado",
                "mensagem": "Estudante não encontrado"
            }
        
        # Verificar se já tem estatuto
        estatuto_atual = estudante.get("estatuto")
        if estatuto_atual and estatuto_atual != tipo_estatuto:
            return {
                "status": "recusado",
                "mensagem": f"Estudante já tem estatuto de {estatuto_atual}. Deve cancelar antes de solicitar novo."
            }
        
        if estatuto_atual == tipo_estatuto:
            return {
                "status": "aprovado",
                "mensagem": f"Estudante já tem estatuto de {tipo_estatuto}"
            }
        
        # Buscar informações do estatuto
        info_estatuto = self.buscar_estatuto(tipo_estatuto)
        if not info_estatuto:
            return {
                "status": "recusado",
                "mensagem": f"Tipo de estatuto '{tipo_estatuto}' não encontrado"
            }
        
        # Verificar documentos necessários
        requisitos = info_estatuto.get("requisitos", [])
        documentos_faltantes = []
        
        for requisito in requisitos:
            # Simplificação: verificar se documento está na lista
            encontrado = any(requisito.lower() in doc.lower() for doc in documentos)
            if not encontrado:
                documentos_faltantes.append(requisito)
        
        if documentos_faltantes:
            return {
                "status": "pendente",
                "mensagem": f"Documentos em falta: {', '.join(documentos_faltantes)}",
                "requisitos_faltantes": documentos_faltantes
            }
        
        # Estatuto aprovado
        beneficios = info_estatuto.get("beneficios", [])
        
        return {
            "status": "aprovado",
            "mensagem": f"Estatuto de {tipo_estatuto} aprovado!",
            "beneficios": beneficios
        }
    
    async def consultar_estatuto(self, content):
        """Consulta informações sobre um tipo de estatuto"""
        tipo_estatuto = content.get("tipo_estatuto")
        
        print(f"ℹ️ Consultando informações do estatuto: {tipo_estatuto}")
        
        if not tipo_estatuto:
            # Listar todos os estatutos disponíveis
            estatutos = []
            for estatuto in self.estatutos_data.get("estatutos", []):
                estatutos.append({
                    "tipo": estatuto.get("tipo"),
                    "requisitos": estatuto.get("requisitos", []),
                    "beneficios": estatuto.get("beneficios", [])
                })
            
            return {
                "status": "sucesso",
                "estatutos": estatutos
            }
        
        # Buscar estatuto específico
        info_estatuto = self.buscar_estatuto(tipo_estatuto)
        if not info_estatuto:
            return {
                "status": "erro",
                "mensagem": f"Estatuto '{tipo_estatuto}' não encontrado"
            }
        
        return {
            "status": "sucesso",
            "tipo": info_estatuto.get("tipo"),
            "requisitos": info_estatuto.get("requisitos", []),
            "beneficios": info_estatuto.get("beneficios", [])
        }
    
    def buscar_estudante(self, estudante_id):
        """Busca estudante por ID"""
        for estudante in self.estudantes_data.get("estudantes", []):
            if estudante.get("id") == estudante_id:
                return estudante
        return None
    
    def buscar_estatuto(self, tipo):
        """Busca estatuto por tipo"""
        for estatuto in self.estatutos_data.get("estatutos", []):
            if estatuto.get("tipo") == tipo:
                return estatuto
        return None


class AgenteRegulamentos(Agent):
    """Agente Regulamentos - Gestão de estatutos especiais"""
    
    async def setup(self):
        """Configuração inicial do agente"""
        print("🚀 Configurando Agente Regulamentos...")
        comportamento = RegulamentosBehaviour()
        self.add_behaviour(comportamento)
