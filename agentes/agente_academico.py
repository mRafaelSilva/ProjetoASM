"""
Agente Académico - Regras de Inscrição
Este agente verifica regras académicas como pré-requisitos, 
limites de créditos, e processa equivalências.
"""

import json
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class AcademicoBehaviour(CyclicBehaviour):
    """Comportamento principal do Agente Académico"""
    
    async def on_start(self):
        print("✅ Agente Académico iniciado.")
        await self.carregar_dados()
    
    async def carregar_dados(self):
        """Carrega dados de cursos e estudantes"""
        try:
            with open('/home/runner/work/ProjetoASM/ProjetoASM/data/cursos.json', 'r', encoding='utf-8') as f:
                self.cursos_data = json.load(f)
            
            with open('/home/runner/work/ProjetoASM/ProjetoASM/data/estudantes.json', 'r', encoding='utf-8') as f:
                self.estudantes_data = json.load(f)
            
            print("📚 Dados académicos carregados com sucesso.")
        except Exception as e:
            print(f"❌ Erro ao carregar dados: {e}")
            self.cursos_data = {"cursos": []}
            self.estudantes_data = {"estudantes": []}
    
    async def run(self):
        """Processa pedidos relacionados com regras académicas"""
        msg = await self.receive(timeout=10)
        
        if msg:
            try:
                content = json.loads(msg.body)
                tipo = content.get("tipo")
                
                if tipo == "verificar_inscricao":
                    resposta = await self.verificar_inscricao(content)
                elif tipo == "verificar_equivalencia":
                    resposta = await self.verificar_equivalencia(content)
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
                print(f"❌ Erro no Agente Académico: {e}")
    
    async def verificar_inscricao(self, content):
        """Verifica se estudante pode se inscrever na disciplina"""
        estudante_id = content.get("estudante_id")
        disciplina_codigo = content.get("disciplina")
        
        print(f"🎓 Verificando inscrição: {estudante_id} -> {disciplina_codigo}")
        
        # Buscar estudante
        estudante = self.buscar_estudante(estudante_id)
        if not estudante:
            return {
                "aprovado": False,
                "mensagem": "Estudante não encontrado"
            }
        
        # Buscar curso
        curso = self.buscar_curso(disciplina_codigo)
        if not curso:
            return {
                "aprovado": False,
                "mensagem": "Disciplina não encontrada"
            }
        
        # Verificar se já está inscrito
        if disciplina_codigo in estudante.get("disciplinas_inscritas", []):
            return {
                "aprovado": False,
                "mensagem": "Já está inscrito nesta disciplina"
            }
        
        # Verificar se já completou
        if disciplina_codigo in estudante.get("disciplinas_completas", []):
            return {
                "aprovado": False,
                "mensagem": "Já completou esta disciplina"
            }
        
        # Verificar pré-requisitos
        prerequisitos = curso.get("prerequisitos", [])
        disciplinas_completas = estudante.get("disciplinas_completas", [])
        
        prerequisitos_faltantes = [p for p in prerequisitos if p not in disciplinas_completas]
        
        if prerequisitos_faltantes:
            return {
                "aprovado": False,
                "mensagem": f"Faltam pré-requisitos: {', '.join(prerequisitos_faltantes)}"
            }
        
        # Verificar vagas
        vagas = curso.get("vagas", 0)
        if vagas <= 0:
            return {
                "aprovado": False,
                "mensagem": "Não há vagas disponíveis"
            }
        
        # Verificar limite de créditos (máximo 30 créditos por semestre)
        creditos_atuais = sum([
            self.buscar_curso(d).get("creditos", 0) 
            for d in estudante.get("disciplinas_inscritas", [])
            if self.buscar_curso(d)
        ])
        novos_creditos = curso.get("creditos", 0)
        
        if creditos_atuais + novos_creditos > 30:
            return {
                "aprovado": False,
                "mensagem": f"Excede o limite de 30 créditos por semestre (atual: {creditos_atuais}, novo: {novos_creditos})"
            }
        
        return {
            "aprovado": True,
            "mensagem": f"Inscrição aprovada em {curso.get('nome')} ({novos_creditos} créditos)"
        }
    
    async def verificar_equivalencia(self, content):
        """Verifica se pode conceder equivalência entre disciplinas"""
        estudante_id = content.get("estudante_id")
        disciplina_origem = content.get("disciplina_origem")
        disciplina_destino = content.get("disciplina_destino")
        
        print(f"🔄 Verificando equivalência: {disciplina_origem} -> {disciplina_destino}")
        
        # Buscar estudante
        estudante = self.buscar_estudante(estudante_id)
        if not estudante:
            return {
                "status": "recusado",
                "mensagem": "Estudante não encontrado"
            }
        
        # Verificar se completou a disciplina de origem
        if disciplina_origem not in estudante.get("disciplinas_completas", []):
            return {
                "status": "recusado",
                "mensagem": f"Não completou a disciplina {disciplina_origem}"
            }
        
        # Buscar cursos
        curso_origem = self.buscar_curso(disciplina_origem)
        curso_destino = self.buscar_curso(disciplina_destino)
        
        if not curso_origem or not curso_destino:
            return {
                "status": "recusado",
                "mensagem": "Uma das disciplinas não foi encontrada"
            }
        
        # Verificar créditos (deve ter pelo menos 80% dos créditos)
        creditos_origem = curso_origem.get("creditos", 0)
        creditos_destino = curso_destino.get("creditos", 0)
        
        if creditos_origem < creditos_destino * 0.8:
            return {
                "status": "recusado",
                "mensagem": f"Créditos insuficientes (origem: {creditos_origem}, necessário: {creditos_destino * 0.8})"
            }
        
        return {
            "status": "aprovado",
            "mensagem": f"Equivalência aprovada: {curso_origem.get('nome')} ≈ {curso_destino.get('nome')}"
        }
    
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


class AgenteAcademico(Agent):
    """Agente Académico - Gestão de regras de inscrição"""
    
    async def setup(self):
        """Configuração inicial do agente"""
        print("🚀 Configurando Agente Académico...")
        comportamento = AcademicoBehaviour()
        self.add_behaviour(comportamento)
