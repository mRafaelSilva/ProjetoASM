"""
Agente Horários - Gestão de Conflitos de Horário
Este agente detecta conflitos de horário entre disciplinas.
"""

import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from datetime import datetime


class HorariosBehaviour(CyclicBehaviour):
    """Comportamento principal do Agente Horários"""
    
    async def on_start(self):
        print("✅ Agente Horários iniciado.")
        await self.carregar_dados()
    
    async def carregar_dados(self):
        """Carrega dados de cursos e estudantes"""
        try:
            with open('/home/runner/work/ProjetoASM/ProjetoASM/data/cursos.json', 'r', encoding='utf-8') as f:
                self.cursos_data = json.load(f)
            
            with open('/home/runner/work/ProjetoASM/ProjetoASM/data/estudantes.json', 'r', encoding='utf-8') as f:
                self.estudantes_data = json.load(f)
            
            print("📅 Dados de horários carregados com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            self.cursos_data = {"cursos": []}
            self.estudantes_data = {"estudantes": []}
    
    async def run(self):
        """Processa pedidos relacionados com horários"""
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                content = json.loads(msg.body)
                tipo = content.get("tipo")
                
                if tipo == "verificar_conflito":
                    resposta = await self.verificar_conflito(content)
                elif tipo == "consultar_horario":
                    resposta = await self.consultar_horario(content)
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
                print(f"❌ Erro no Agente Horários: {e}")
    
    async def verificar_conflito(self, content):
        """Verifica se há conflito de horário"""
        estudante_id = content.get("estudante_id")
        disciplina_codigo = content.get("disciplina")
        
        print(f"⏰ Verificando conflitos de horário: {estudante_id} -> {disciplina_codigo}")
        
        # Buscar estudante
        estudante = self.buscar_estudante(estudante_id)
        if not estudante:
            return {
                "sem_conflito": False,
                "mensagem": "Estudante não encontrado"
            }
        
        # Buscar horário da nova disciplina
        curso_novo = self.buscar_curso(disciplina_codigo)
        if not curso_novo:
            return {
                "sem_conflito": False,
                "mensagem": "Disciplina não encontrada"
            }
        
        horario_novo = self.parsear_horario(curso_novo.get("horario", ""))
        
        # Verificar conflitos com disciplinas já inscritas
        for disc_inscrita in estudante.get("disciplinas_inscritas", []):
            curso_inscrito = self.buscar_curso(disc_inscrita)
            if curso_inscrito:
                horario_inscrito = self.parsear_horario(curso_inscrito.get("horario", ""))
                
                conflito = self.detectar_conflito(horario_novo, horario_inscrito)
                if conflito:
                    return {
                        "sem_conflito": False,
                        "mensagem": f"Conflito com {curso_inscrito.get('nome')} ({disc_inscrita})"
                    }
        
        return {
            "sem_conflito": True,
            "mensagem": "Sem conflitos de horário"
        }
    
    async def consultar_horario(self, content):
        """Consulta o horário completo do estudante"""
        estudante_id = content.get("estudante_id")
        
        print(f"📋 Consultando horário: {estudante_id}")
        
        estudante = self.buscar_estudante(estudante_id)
        if not estudante:
            return {
                "status": "erro",
                "mensagem": "Estudante não encontrado"
            }
        
        horarios = []
        for disc_codigo in estudante.get("disciplinas_inscritas", []):
            curso = self.buscar_curso(disc_codigo)
            if curso:
                horarios.append({
                    "codigo": disc_codigo,
                    "nome": curso.get("nome"),
                    "horario": curso.get("horario")
                })
        
        if not horarios:
            return {
                "status": "sucesso",
                "mensagem": "Sem disciplinas inscritas",
                "horarios": []
            }
        
        return {
            "status": "sucesso",
            "horarios": horarios
        }
    
    def parsear_horario(self, horario_str):
        """
        Parseia string de horário para formato estruturado
        Exemplo: "Segunda 14:00-16:00, Quarta 14:00-16:00"
        """
        dias_map = {
            "Segunda": 1, "Terça": 2, "Quarta": 3,
            "Quinta": 4, "Sexta": 5, "Sábado": 6
        }
        
        slots = []
        if not horario_str:
            return slots
        
        partes = horario_str.split(",")
        for parte in partes:
            parte = parte.strip()
            tokens = parte.split()
            if len(tokens) >= 2:
                dia_nome = tokens[0]
                horario_range = tokens[1]
                
                if dia_nome in dias_map and "-" in horario_range:
                    dia = dias_map[dia_nome]
                    inicio, fim = horario_range.split("-")
                    slots.append({
                        "dia": dia,
                        "inicio": inicio,
                        "fim": fim
                    })
        
        return slots
    
    def detectar_conflito(self, horario1, horario2):
        """Detecta se há sobreposição entre dois horários"""
        for slot1 in horario1:
            for slot2 in horario2:
                # Mesmo dia
                if slot1["dia"] == slot2["dia"]:
                    # Verificar sobreposição de horários
                    inicio1 = self.hora_para_minutos(slot1["inicio"])
                    fim1 = self.hora_para_minutos(slot1["fim"])
                    inicio2 = self.hora_para_minutos(slot2["inicio"])
                    fim2 = self.hora_para_minutos(slot2["fim"])
                    
                    # Há conflito se os intervalos se sobrepõem
                    if not (fim1 <= inicio2 or fim2 <= inicio1):
                        return True
        
        return False
    
    def hora_para_minutos(self, hora_str):
        """Converte hora (HH:MM) para minutos desde meia-noite"""
        try:
            partes = hora_str.split(":")
            horas = int(partes[0])
            minutos = int(partes[1])
            return horas * 60 + minutos
        except:
            return 0
    
    def buscar_estudante(self, estudante_id):
        """Busca estudante por ID"""
        for estudante in self.estudantes_data.get("estudantes", []):
            if estudante.get("id") == estudante_id:
                return estudante
        return None
    
    def buscar_curso(self, codigo):
        """Busca curso por código"""
        for curso in self.cursos_data.get("cursos", []):
            if curso.get("codigo") == codigo:
                return curso
        return None


class AgenteHorarios(Agent):
    """Agente Horários - Gestão de conflitos de horário"""
    
    async def setup(self):
        """Configuração inicial do agente"""
        print("🚀 Configurando Agente Horários...")
        comportamento = HorariosBehaviour()
        self.add_behaviour(comportamento)
