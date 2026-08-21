---
when_to_use: >
  Cargo atual de AI/ML Engineer na AI Factory do Distrito
  (set/2025–presente): escopo, os três projetos de saúde, educação e
  marketing, stack de agentes e a responsabilidade de arquitetura e
  contato direto com o cliente.
---

# AI/ML Engineer — Distrito

**Período:** setembro de 2025 – presente · tempo integral · remoto
**Área:** AI Factory

## Escopo

Engenheiro de IA/ML na AI Factory do Distrito, construindo sistemas de IA que
vão para produção e atendem usuários finais. O trabalho cobre a cadeia inteira:
entender o problema de negócio com o cliente, desenhar a arquitetura do sistema
de agentes, implementar, instrumentar observabilidade e acompanhar o
comportamento em produção.

Atuo em projetos de setores distintos — saúde, educação e marketing — o que
significa trocar de domínio de dados com frequência e não poder depender de
familiaridade prévia com a regra de negócio.

## Projetos

- **Agentes de IA integrados para serviços via WhatsApp** na rotina de milhares
  de pacientes de um grande hospital de São Paulo.
  → `projetos/agentes-whatsapp-hospital.md`
- **Plataforma de júri sintético** para pesquisa e análise de campanhas: clusterização
  da base de audiência para identificar perfis reais, geração de personas ancoradas
  nesses clusters e entrevistas simuladas contra estímulos publicitários. Respondo
  pelo fluxo de IA inteiro.
  → `projetos/analise-campanhas-personas.md`
- **Agente de coaching acadêmico via WhatsApp** para uma rede de ensino
  internacional: agente conversacional sobre um serviço de tools que expõe dado
  institucional por REST e MCP, mais uma pipeline de agentes que extrai conteúdo de
  cursos de documentos não estruturados.
  → `projetos/coach-academico-whatsapp.md`

## Stack

LangChain e LangGraph para orquestração de agentes. LangSmith (Fuse) e Langfuse para
tracing e avaliação. FastAPI nas APIs, Celery e Redis para trabalho assíncrono,
PostgreSQL como banco principal. MCP para expor dado institucional a agentes. Deploy
em Cloud Run (GCP) e Azure Container Apps.

## Responsabilidade além do código

Engenheiro de IA único no projeto: decido arquitetura do sistema de agentes. Time composto
normalmente por um engenheiro e um PO. Constantemente, faço a comunicação com o cliente para 
extrair valor e converter em histórias técnicas. Eu executo desde o planejamento até a execução
da operação.

Falo direto com o cliente. Isso muda a natureza do trabalho: parte do resultado é
traduzir regra de negócio em comportamento de agente e, na direção inversa, explicar
ao cliente o que um sistema de LLM pode e não pode garantir — inclusive dizer não
quando o pedido esconde um risco que a demo não mostra.

## Resultados

O que existe de sólido: sistema de agentes em produção em hospital de grande porte,
com o agente de check-in atendendo milhares de pacientes por mês (ordem de grandeza),
e plataforma de júri sintético em uso diário para desenvolver campanhas reais.
Além disso, um agente coach acadêmico para ajudar alunos de uma rede de universidades global.

