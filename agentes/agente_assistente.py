"""
Agente Assistente - Interface e Diálogo
Este agente é o ponto de entrada do sistema, dialogando com o estudante
e coordenando os pedidos com os outros agentes especializados.
"""

import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from spade.template import Template
import asyncio


class AssistenteBehaviour(CyclicBehaviour):
    """Comportamento principal do Agente Assistente"""
    
    async def on_start(self):
        print("✅ Agente Assistente iniciado e pronto para receber pedidos.")
        self.pending_requests = {}
        self.request_counter = 0
    
    async def run(self):
        """Processa mensagens dos estudantes e coordena com outros agentes"""
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                content = json.loads(msg.body)
                tipo_pedido = content.get("tipo")
                estudante_id = content.get("estudante_id")
                
                print(f"\n📩 Pedido recebido de {estudante_id}: {tipo_pedido}")
                
                if tipo_pedido == "inscricao":
                    await self.processar_inscricao(content, msg.sender)
                elif tipo_pedido == "equivalencia":
                    await self.processar_equivalencia(content, msg.sender)
                elif tipo_pedido == "estatuto":
                    await self.processar_estatuto(content, msg.sender)
                elif tipo_pedido == "consulta_horario":
                    await self.consultar_horario(content, msg.sender)
                else:
                    await self.enviar_resposta(msg.sender, {
                        "status": "erro",
                        "mensagem": "Tipo de pedido desconhecido"
                    })
            except Exception as e:
                print(f"❌ Erro ao processar mensagem: {e}")
    
    async def processar_inscricao(self, content, sender):
        """Processa pedido de inscrição em disciplina"""
        print("🔄 Processando inscrição...")
        
        # Verificar propinas com Agente Financeiro
        msg_financeiro = Message(to=str(self.agent.agente_financeiro))
        msg_financeiro.set_metadata("performative", "request")
        msg_financeiro.body = json.dumps({
            "tipo": "verificar_propinas",
            "estudante_id": content["estudante_id"]
        })
        await self.send(msg_financeiro)
        
        # Aguardar resposta do Agente Financeiro
        resp_financeiro = await self.receive(timeout=10)
        if resp_financeiro:
            resp_fin_data = json.loads(resp_financeiro.body)
            if not resp_fin_data.get("aprovado"):
                await self.enviar_resposta(sender, {
                    "status": "recusado",
                    "mensagem": "Propinas em atraso. Regularize a situação antes de se inscrever."
                })
                return
        
        # Verificar horários com Agente Horários
        msg_horarios = Message(to=str(self.agent.agente_horarios))
        msg_horarios.set_metadata("performative", "request")
        msg_horarios.body = json.dumps({
            "tipo": "verificar_conflito",
            "estudante_id": content["estudante_id"],
            "disciplina": content["disciplina"]
        })
        await self.send(msg_horarios)
        
        # Aguardar resposta do Agente Horários
        resp_horarios = await self.receive(timeout=10)
        if resp_horarios:
            resp_hor_data = json.loads(resp_horarios.body)
            if not resp_hor_data.get("sem_conflito"):
                await self.enviar_resposta(sender, {
                    "status": "recusado",
                    "mensagem": f"Conflito de horário: {resp_hor_data.get('mensagem')}"
                })
                return
        
        # Verificar regras académicas com Agente Académico
        msg_academico = Message(to=str(self.agent.agente_academico))
        msg_academico.set_metadata("performative", "request")
        msg_academico.body = json.dumps({
            "tipo": "verificar_inscricao",
            "estudante_id": content["estudante_id"],
            "disciplina": content["disciplina"]
        })
        await self.send(msg_academico)
        
        # Aguardar resposta do Agente Académico
        resp_academico = await self.receive(timeout=10)
        if resp_academico:
            resp_acad_data = json.loads(resp_academico.body)
            if resp_acad_data.get("aprovado"):
                await self.enviar_resposta(sender, {
                    "status": "aprovado",
                    "mensagem": resp_acad_data.get("mensagem", "Inscrição aprovada!")
                })
            else:
                await self.enviar_resposta(sender, {
                    "status": "recusado",
                    "mensagem": resp_acad_data.get("mensagem", "Inscrição recusada")
                })
    
    async def processar_equivalencia(self, content, sender):
        """Processa pedido de equivalência"""
        print("🔄 Processando equivalência...")
        
        msg_academico = Message(to=str(self.agent.agente_academico))
        msg_academico.set_metadata("performative", "request")
        msg_academico.body = json.dumps({
            "tipo": "verificar_equivalencia",
            "estudante_id": content["estudante_id"],
            "disciplina_origem": content.get("disciplina_origem"),
            "disciplina_destino": content.get("disciplina_destino")
        })
        await self.send(msg_academico)
        
        resp = await self.receive(timeout=10)
        if resp:
            resp_data = json.loads(resp.body)
            await self.enviar_resposta(sender, resp_data)
    
    async def processar_estatuto(self, content, sender):
        """Processa pedido de estatuto especial"""
        print("🔄 Processando pedido de estatuto...")
        
        msg_regulamentos = Message(to=str(self.agent.agente_regulamentos))
        msg_regulamentos.set_metadata("performative", "request")
        msg_regulamentos.body = json.dumps({
            "tipo": "verificar_estatuto",
            "estudante_id": content["estudante_id"],
            "tipo_estatuto": content.get("tipo_estatuto"),
            "documentos": content.get("documentos", [])
        })
        await self.send(msg_regulamentos)
        
        resp = await self.receive(timeout=10)
        if resp:
            resp_data = json.loads(resp.body)
            await self.enviar_resposta(sender, resp_data)
    
    async def consultar_horario(self, content, sender):
        """Consulta horário e possíveis conflitos"""
        print("🔄 Consultando horários...")
        
        msg_horarios = Message(to=str(self.agent.agente_horarios))
        msg_horarios.set_metadata("performative", "request")
        msg_horarios.body = json.dumps({
            "tipo": "consultar_horario",
            "estudante_id": content["estudante_id"]
        })
        await self.send(msg_horarios)
        
        resp = await self.receive(timeout=10)
        if resp:
            resp_data = json.loads(resp.body)
            await self.enviar_resposta(sender, resp_data)
    
    async def enviar_resposta(self, destinatario, dados):
        """Envia resposta ao estudante"""
        msg = Message(to=str(destinatario))
        msg.set_metadata("performative", "inform")
        msg.body = json.dumps(dados)
        await self.send(msg)
        print(f"✉️ Resposta enviada: {dados['status']}")


class AgenteAssistente(Agent):
    """Agente Assistente - Coordenador principal do sistema"""
    
    def __init__(self, jid, password, agente_academico, agente_horarios, 
                 agente_regulamentos, agente_financeiro):
        super().__init__(jid, password)
        self.agente_academico = agente_academico
        self.agente_horarios = agente_horarios
        self.agente_regulamentos = agente_regulamentos
        self.agente_financeiro = agente_financeiro
    
    async def setup(self):
        """Configuração inicial do agente"""
        print("🚀 Configurando Agente Assistente...")
        comportamento = AssistenteBehaviour()
        self.add_behaviour(comportamento)
