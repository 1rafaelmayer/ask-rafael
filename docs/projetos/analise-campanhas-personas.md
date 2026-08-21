---
when_to_use: >
  Projeto de plataforma de júri sintético para pesquisa de campanhas
  publicitárias: clusterização com k-modes, geração de personas ancoradas
  em dado real, entrevistas simuladas, relatório e os limites honestos da
  técnica.
---

# Plataforma de Júri Sintético para pesquisa e análise de campanhas

**Onde:** Distrito · AI Factory · 2025 – presente
**Papel:** engenheiro de IA/ML — responsável pelo fluxo de IA inteiro da plataforma

## Contexto

Testar campanha publicitária com público real é caro e lento: recruta-se painel,
aplica-se estímulo, coleta-se resposta, e o ciclo leva semanas. A pergunta do
projeto foi se dava para antecipar parte desse aprendizado antes de gastar o
orçamento de veiculação.

## O que construí

O **fluxo de IA** de uma plataforma de júri sintético: da definição de audiência
até o relatório. Cada etapa é uma peça:

1. **Clusterização** da base de audiência para identificar perfis representativos —
   os segmentos que de fato existem nos dados, em vez das personas que o time de
   marketing imagina que existem.
2. **Geração de personas** sintéticas a partir desses segmentos.
3. **Roteiro de entrevista** gerado para o objetivo da pesquisa.
4. **Entrevistas simuladas**, individuais e em lote, das personas contra os
   estímulos (peças em vídeo ou imagem).
5. **Relatório** que analisa o conjunto de respostas.

A ordem das duas primeiras importa: o cluster é o que ancora a persona em dado
real. Sem ele, a persona é só o LLM inventando um consumidor plausível.

A clusterização usa **k-modes**, não k-means: a base de audiência é descrita por
atributos categóricos, e média de categoria não significa nada — moda por atributo
significa. O número de clusters é fixo, definido pelo negócio: o time precisa de um
conjunto estável de personas com que trabalhar, não do k que otimiza uma métrica
interna.

De cluster a persona são três etapas:

1. **Seed demográfica**, extraída do representante do cluster — o ancoradouro em
   dado real.
2. **Geração de biografia**, que transforma a seed em um sujeito coerente, com
   história, em vez de uma lista de atributos.
3. **Enriquecimento**, que personaliza a persona com os dados da audiência
   definida para aquela campanha.

A ordem é o ponto: a biografia só é escrita depois que a seed fixou quem é essa
pessoa nos dados. Invertido, o LLM escreveria um consumidor plausível e a seed
viraria decoração.

## A objeção honesta

Persona simulada por LLM é uma técnica com limite real, e vale ter a resposta
pronta: o modelo pode produzir resposta plausível e sistematicamente enviesada,
porque reflete o que estava no treino e não o público do cliente. A defesa do
projeto não é fingir que isso não acontece — é o que foi construído em volta para
conter: ancoragem em cluster real e validação da metodologia junto ao cliente,
aplicando estímulos diferentes às personas e comparando com o resultado final
observado das sugestões.

## Decisões técnicas e trade-offs

**K-modes em vez de k-means.** A base é categórica. K-means exigiria one-hot e
distância euclidiana sobre atributo nominal, o que produz centroide sem
interpretação possível — e persona precisa ser legível para o time de marketing. O
custo é ficar sem as ferramentas mais maduras do ecossistema de k-means, incluindo
as métricas usuais de seleção de k.

**Número fixo de clusters, definido pelo negócio.** Deixar o algoritmo decidir k
daria segmentação mais fiel à estrutura dos dados, mas instável entre execuções e
sem correspondência com o modo de trabalhar do cliente. O custo é conhecido: com k
imposto, um cluster pode agrupar perfis que os dados separariam, e a persona
resultante fica mais grossa que a realidade.

**Seed real antes da geração de texto.** A alternativa mais rápida era descrever a
audiência em prosa e pedir personas ao LLM. Descartada porque é exatamente a falha
que o projeto existe para evitar. O custo é uma pipeline mais longa, com três
etapas para manter e depurar.

**Tudo que é lento vai para fila.** Clusterização, geração de personas, execução de
entrevistas simuladas e geração de relatório rodam como tarefas Celery numa fila
dedicada, não no request. Nenhuma dessas operações fecha em tempo de HTTP, e uma
rodada de entrevistas em lote pode levar minutos. O progresso volta ao frontend por
WebSocket, em vez de o cliente ficar fazendo polling. O custo é a complexidade
usual de sistema assíncrono: estado de tarefa a persistir, falha parcial a tratar e
worker a operar como serviço separado.

**Modelo por feature, não um modelo para tudo.** Cada etapa aponta para um modelo
Gemini configurável: `pro` onde a qualidade do texto define o resultado (geração de
persona, roteiro, relatório) e `flash` onde o volume domina (enriquecimento,
entrevistas). Isso é o que torna viável rodar entrevistas em lote — o custo por
rodada cairia num modelo só de topo. O custo é ter mais um eixo de configuração que
precisa ser avaliado por etapa.

## Stack

Backend da plataforma de Júri Sintético: **FastAPI** (Python 3.12) com API REST +
WebSocket, **PostgreSQL 15** com SQLAlchemy 2.0 e Alembic, **Celery + Redis** para
as tarefas de IA assíncronas, **Google Gemini** (2.5 pro/flash, escolhido por
feature) na geração e simulação, **k-modes** na clusterização, storage em MinIO
(dev) e Google Cloud Storage (prod), tracing de LLM em **Langfuse**, deploy em
**Cloud Run** com Cloud SQL e Memorystore. Frontend em Next.js consome a API.

## Resultado

Em uso diário para desenvolver campanhas reais. Não há números disponíveis para
citar — nem volume de campanhas nem efeito medido sobre o processo de pesquisa.
