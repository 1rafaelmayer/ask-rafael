---
when_to_use: >
  Competências de engenharia de software, backend e dados: Python,
  FastAPI, Celery, PostgreSQL, Redis e pipelines de dados, com nível
  declarado e onde cada uma foi exercida. Não cobre nuvem nem MLOps — ver
  skills/infra-cloud-mlops.md.
---

# Engenharia de software, dados e backend

## Linguagens

**Python** — linguagem principal, desde a graduação. Uso contínuo há mais de dez
anos, atravessando três contextos diferentes: análise de dados científicos,
simulação numérica e hoje backend e sistemas de agentes em produção.

Também passei por linguagem compilada na formação em engenharia física e em trabalho
de simulação numérica — hoje trabalho em Python, e é nele que a profundidade está.

## Backend e APIs

**FastAPI** — framework que uso para expor modelos e agentes como serviço. Usado
na Amil (servir o pipeline de OCR) e no Distrito (APIs dos sistemas de agentes).

**Celery** — processamento assíncrono e tarefas em background. Necessário quando
o trabalho do agente não cabe no tempo de resposta de um webhook.

**PostgreSQL** — banco relacional principal.
**Redis** — cache e broker de mensagens.

## Dados

Pandas, NumPy e Matplotlib no tratamento e na visualização. Construção de
**pipelines de dados escaláveis** — feito na Samsung para alimentar modelos de
rede neural. → `projetos/wearables-samsung-modelos.md`

## Como isso aparece na prática

O que distingue um sistema de IA que funciona na demo de um que funciona em
produção normalmente não é o modelo: é o que está em volta. Fila para o trabalho
que não cabe no request, estado persistido para a conversa que retoma horas
depois, cache para não repetir chamada caindo em custo, e trace para descobrir o
que aconteceu quando alguém reclama.

## Nível

Assumo o backend de um serviço de IA sozinho, fim a fim: API, modelo de dados, fila,
persistência de estado, deploy e observabilidade. Não é aspiração — é o que já fiz em
projeto de cliente em produção, em time pequeno, onde não havia engenheiro de backend
separado para dividir a tarefa.
