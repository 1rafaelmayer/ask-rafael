---
when_to_use: >
  Competências de infraestrutura, nuvem e MLOps: Docker, GCP, Azure,
  Databricks, certificações AWS e Oracle e observabilidade de LLM — com as
  lacunas declaradas (Kubernetes, CI/CD, versionamento de modelo,
  monitoramento de drift).
---

# Infraestrutura, nuvem e MLOps

## Containers e orquestração

**Docker** — empacotamento de modelos e serviços. Usado na Amil e no Distrito.
**Kubernetes** — conhecimento conceitual, **sem uso prático**. Registro assim de
propósito: nos meus projetos o deploy é em serviço gerenciado de container (Cloud Run,
Azure Container Apps), que resolve o problema sem cluster para operar. Se a vaga exige
operar Kubernetes, essa é uma lacuna real minha, não um detalhe de currículo.
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

O que eu faço de fato nesse eixo, delimitado:

- **Observabilidade e avaliação de sistema de LLM** — é a minha parte forte aqui.
  Tracing de execução de agente e avaliação de comportamento em LangSmith/Fuse e
  Langfuse, usados para depurar decisão de agente e detectar regressão entre versões.
- **Custo de inferência** — acompanho e trato como variável de projeto: a escolha de
  modelo por etapa (modelo de topo onde a qualidade define o resultado, modelo rápido
  onde o volume domina) é decisão de custo tanto quanto de qualidade.
  → `projetos/analise-campanhas-personas.md`

O que **não** é meu terreno, e vale dizer antes que a pergunta chegue: não configuro
pipeline de CI/CD hoje, não uso ferramenta dedicada de versionamento de modelo e dado
(MLflow, DVC), e não montei monitoramento de drift com alerta e retreino automático.
Nos sistemas de agentes que construí, o eixo de MLOps que importou foi observabilidade
de execução, não ciclo de retreino de modelo próprio.

## Nível

Suficiente para levar sistema de IA a produção fim a fim em serviço gerenciado —
empacotar, expor, fazer deploy e instrumentar. Não é onde está minha profundidade:
não sou engenheiro de plataforma, e o eixo de infraestrutura pesada (cluster,
malha de serviço, IaC) é conhecimento de superfície. A largura vem de certificação
(AWS, Oracle) e a prática real está concentrada em GCP e Azure gerenciados.
