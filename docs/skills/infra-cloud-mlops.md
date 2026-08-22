---
when_to_use: >
  Competências de infraestrutura, nuvem e MLOps: Docker, GCP, Azure,
  Databricks, certificações AWS e Oracle, deploy em serviço gerenciado e
  observabilidade de sistema de LLM.
---

# Infraestrutura, nuvem e MLOps

## Containers e orquestração

**Docker** — empacotamento de modelos e serviços. Usado na Amil e no Distrito.
**Serviço gerenciado de container** — Cloud Run e Azure Container Apps são onde meus
sistemas rodam: entregam escala e disponibilidade sem cluster para operar, e é a
escolha certa para o porte dos serviços de IA que construo.
**Git** — controle de versão.

## Nuvem

**Google Cloud (GCP)** — deploy em Cloud Run, no Distrito.
**Microsoft Azure** — Azure Container Apps no Distrito; Azure e Document
Intelligence na Amil.
**Databricks** — plataforma de dados na Amil.
**Oracle Cloud Infrastructure** — duas certificações profissionais (Generative AI
e Data Science). → `certificacoes.md`
**AWS** — certificação ML Engineer Associate, cobrindo SageMaker e Bedrock.

Cobertura de três dos quatro grandes provedores, com prática real em GCP e Azure
e certificação em AWS e Oracle.

## MLOps

Ciclo de vida de modelo em produção: empacotamento, deploy, observabilidade e
avaliação contínua. Em sistemas de agentes, a camada de observabilidade é
LangSmith/Fuse. → `skills/genai-agentic.md`

O que eu faço de fato nesse eixo:

- **Observabilidade e avaliação de sistema de LLM** — é a minha parte forte aqui.
  Tracing de execução de agente e avaliação de comportamento em LangSmith/Fuse e
  Langfuse, usados para depurar decisão de agente e detectar regressão entre versões.
- **Custo de inferência** — acompanho e trato como variável de projeto: a escolha de
  modelo por etapa (modelo de topo onde a qualidade define o resultado, modelo rápido
  onde o volume domina) é decisão de custo tanto quanto de qualidade.
  → `projetos/analise-campanhas-personas.md`

Nos sistemas de agentes que construí, o eixo de MLOps que importa é observabilidade de
execução: o que precisa ser depurado é a decisão do agente, e é ali que invisto.

## Nível

Levo sistema de IA a produção fim a fim em serviço gerenciado — empacotar, expor,
fazer deploy e instrumentar, sem depender de um time de plataforma para publicar. A
prática está concentrada em GCP e Azure, e a largura vem de certificação em AWS e
Oracle.
