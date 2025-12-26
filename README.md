# ProjetoASM - Sistema de Secretaria Universitária Virtual

Sistema multiagente utilizando o framework **SPADE** (Smart Python Agent Development Environment) para simular uma secretaria universitária virtual.

## 🎯 Objetivo

Simular uma secretaria universitária onde estudantes podem fazer diversos tipos de pedidos:
- 📝 Inscrição em disciplinas
- 🔄 Pedidos de equivalências
- 📋 Pedidos de estatuto especial
- ⏰ Resolução de conflitos de horários
- 💰 Verificação de propinas

## 🤖 Arquitetura de Agentes

O sistema é composto por 5 agentes especializados que trabalham de forma coordenada:

### 1. **Agente Assistente** (`agente_assistente.py`)
- Interface principal com o estudante
- Coordena a comunicação entre os agentes especializados
- Processa pedidos e retorna respostas finais

### 2. **Agente Académico** (`agente_academico.py`)
- Verifica regras de inscrição
- Valida pré-requisitos das disciplinas
- Controla limites de créditos por semestre
- Processa pedidos de equivalência
- Verifica disponibilidade de vagas

### 3. **Agente Horários** (`agente_horarios.py`)
- Detecta conflitos de horário entre disciplinas
- Valida sobreposições de tempo
- Consulta horários dos estudantes
- Gera visualizações de horários

### 4. **Agente Regulamentos** (`agente_regulamentos.py`)
- Processa pedidos de estatutos especiais:
  - Estudante-trabalhador
  - Atleta
  - Dirigente associativo
  - Necessidades especiais
- Verifica requisitos e documentação necessária
- Informa benefícios de cada estatuto

### 5. **Agente Financeiro** (`agente_financeiro.py`)
- Verifica situação de propinas
- Bloqueia inscrições em caso de propinas em atraso
- Consulta dívidas pendentes

## 📁 Estrutura do Projeto

```
ProjetoASM/
├── agentes/
│   ├── __init__.py
│   ├── agente_assistente.py
│   ├── agente_academico.py
│   ├── agente_horarios.py
│   ├── agente_regulamentos.py
│   └── agente_financeiro.py
├── data/
│   ├── cursos.json          # Base de dados de disciplinas
│   ├── estatutos.json       # Tipos de estatutos disponíveis
│   └── estudantes.json      # Base de dados de estudantes
├── main.py                  # Ponto de entrada do sistema
├── requirements.txt         # Dependências do projeto
└── README.md               # Documentação
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos

1. **Clone o repositório:**
```bash
git clone https://github.com/mRafaelSilva/ProjetoASM.git
cd ProjetoASM
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

3. **Execute o sistema:**
```bash
python main.py
```

## 📊 Base de Dados

### Disciplinas (`data/cursos.json`)
Contém informações sobre disciplinas disponíveis:
- Código da disciplina
- Nome
- Créditos
- Horário
- Vagas disponíveis
- Pré-requisitos

### Estudantes (`data/estudantes.json`)
Perfis dos estudantes:
- ID do estudante
- Nome
- Curso
- Ano
- Disciplinas completadas
- Disciplinas inscritas
- Estatuto especial
- Situação de propinas

### Estatutos (`data/estatutos.json`)
Tipos de estatutos especiais disponíveis com requisitos e benefícios.

## 🎬 Cenários de Uso

### Cenário 1: Inscrição em Disciplina
```python
pedido = {
    "tipo": "inscricao",
    "estudante_id": "20230001",
    "disciplina": "IA201"
}
```
**Fluxo:**
1. Agente Financeiro verifica propinas
2. Agente Horários verifica conflitos
3. Agente Académico verifica pré-requisitos e vagas
4. Resposta final ao estudante

### Cenário 2: Pedido de Equivalência
```python
pedido = {
    "tipo": "equivalencia",
    "estudante_id": "20230003",
    "disciplina_origem": "BD101",
    "disciplina_destino": "RC301"
}
```

### Cenário 3: Pedido de Estatuto Especial
```python
pedido = {
    "tipo": "estatuto",
    "estudante_id": "20230001",
    "tipo_estatuto": "estudante-trabalhador",
    "documentos": ["Contrato de trabalho", "Declaração"]
}
```

### Cenário 4: Consulta de Horário
```python
pedido = {
    "tipo": "consulta_horario",
    "estudante_id": "20230001"
}
```

## 🔧 Configuração Avançada

### Usar com Servidor XMPP Real

Para comunicação real entre agentes, você precisa de um servidor XMPP:

1. **Instale Prosody ou Ejabberd:**
```bash
# Ubuntu/Debian
sudo apt-get install prosody

# Ou usando Docker
docker run -d -p 5222:5222 -p 5269:5269 prosody/prosody
```

2. **Crie contas para os agentes:**
```bash
prosodyctl adduser assistente@localhost
prosodyctl adduser academico@localhost
prosodyctl adduser horarios@localhost
prosodyctl adduser regulamentos@localhost
prosodyctl adduser financeiro@localhost
```

3. **Atualize as credenciais em `main.py`**

## 🧪 Testes

Os agentes podem ser testados individualmente ou em conjunto. O arquivo `main.py` contém cenários de demonstração que mostram o funcionamento de cada tipo de pedido.

## 📚 Tecnologias Utilizadas

- **SPADE 3.2+**: Framework para desenvolvimento de sistemas multiagente
- **Python 3.8+**: Linguagem de programação
- **XMPP**: Protocolo de comunicação entre agentes
- **asyncio**: Para programação assíncrona
- **colorama**: Para output colorido no terminal

## 🎓 Conceitos de Sistemas Multiagente

Este projeto demonstra:
- **Autonomia**: Cada agente tem sua própria lógica e responsabilidades
- **Comunicação**: Agentes comunicam via mensagens XMPP
- **Coordenação**: O Agente Assistente coordena a interação entre agentes
- **Especialização**: Cada agente é especializado em um domínio
- **Distribuição**: Processamento distribuído entre múltiplos agentes

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para:
- Reportar bugs
- Sugerir novas funcionalidades
- Melhorar a documentação
- Adicionar novos tipos de agentes

## 📝 Licença

Este projeto é de código aberto e está disponível para fins educacionais.

## 👨‍💻 Autor

Rafael Silva

## 📧 Contato

Para dúvidas ou sugestões, abra uma issue no GitHub.

---

**Nota**: Este é um projeto educacional para demonstrar conceitos de sistemas multiagente usando SPADE. Para uso em produção, seria necessário adicionar autenticação, persistência de dados, interface web, e tratamento robusto de erros.