---
when_to_use: >
  Projeto de sistema multiagente de IA para serviços hospitalares via
  WhatsApp: arquitetura de roteamento entre agentes especializados,
  máquina de estados do check-in, persistência de estado em PostgreSQL e
  trade-offs assumidos.
---

# Sistema de agentes de IA para serviços via WhatsApp em hospital

**Onde:** Distrito · AI Factory · 2025 – presente
**Papel:** engenheiro de IA/ML no time do projeto
**Cliente:** grande hospital de São Paulo

## Contexto

Um hospital de grande porte em São Paulo precisava oferecer serviços de rotina
aos pacientes por WhatsApp — o canal onde essas pessoas já estão, e que não exige
instalar aplicativo nem lembrar senha. A escala é de milhares de pacientes.

O desafio dominante não é conversar: é que cada serviço toca um sistema
diferente do hospital, com regra própria, e o paciente não sabe (nem deveria
saber) qual serviço ele está pedindo. Ele escreve uma frase.

## O que construí

Um sistema de **agentes de IA integrados**, onde agentes especializados cobrem
serviços distintos e a orquestração decide o roteamento a partir da mensagem do
paciente.

A divisão é por serviço: check-in, orçamento, exame, consulta, informações gerais
e um agente identificador, que autentica o paciente antes de qualquer serviço
avançar. Cada mensagem passa por um guardrail de entrada, vai ao agente
coordenador — que classifica a intenção por tema e despacha — e é executada pelo
agente do serviço com suas próprias tools contra os sistemas do hospital.

Trabalhei principalmente no **agente de check-in**. Como o fluxo é bem definido,
ele não é um agente livre: implementei uma **máquina de estados** que determina, a
cada passo, quais ferramentas ficam disponíveis e qual prompt é montado. O estado
concentra o escopo em vez de deixar o modelo escolher entre tudo.

Enquanto o paciente está no fluxo, uma flag faz a mensagem **pular o
coordenador**. Sem isso, pergunta ambígua no meio do fluxo era capturada pelo
roteador e resolvida fora do agente, quebrando o contexto. Com a flag, a
ambiguidade se resolve dentro do check-in, e o paciente só sai quando sinaliza que
quer sair.

O estado persiste em **checkpointer no PostgreSQL**, por thread do paciente — a
resposta pode vir horas depois, e o check-in tem etapas que não podem recomeçar do
zero.

## Decisões técnicas e trade-offs

**Máquina de estados no check-in, em vez de agente livre com tools.** A
alternativa era um agente ReAct único com todas as ferramentas e um prompt grande
descrevendo o processo. Descartei por imprevisibilidade: em fluxo com etapas
obrigatórias e efeito em sistema do hospital, o agente livre pulava etapa, chamava
a tool errada ou repetia uma já concluída. O custo é rigidez — caso não previsto
não é resolvido por criatividade do modelo, e cobrir caminho novo exige mexer na
máquina, não só no prompt. Em fluxo hospitalar, é o lado certo do trade-off.

**Flag de permanência no fluxo, em vez de rotear toda mensagem.** Rotear sempre é
mais simples e uniforme, mas arrancava o paciente do fluxo por uma frase ambígua.
A flag inverte o padrão: dentro de um fluxo, a mensagem é do agente dono do fluxo.
O custo é que trocar de assunto de propósito exige sinal mais explícito, e a saída
do fluxo passa a ser um caminho a tratar e testar.

**Tools como única fonte de afirmação.** O agente não responde a partir do que o
modelo "sabe": o que ele afirma vem de tool contra sistema do hospital, com prompt
restritivo de escopo e comportamento validado por avaliação no LangSmith/Fuse. Em
saúde, alucinação não é bug de qualidade, é risco — onde havia modo de falha
conhecido, entrou guarda dedicada.

## Stack

LangChain/LangGraph, LangSmith (Fuse) para tracing e avaliação, FastAPI,
PostgreSQL (também como checkpointer do grafo), deploy em
Azure Container Apps.

A entrada não é webhook: o sistema expõe uma **API síncrona própria** em FastAPI,
chamada pelo lado do hospital. Sem fila absorvendo latência, cada requisição
precisa fechar dentro do tempo de resposta do chamador.

## Resultado

Em produção. O agente de check-in, minha parte principal, atende **milhares de
pacientes por mês** (ordem de grandeza aproximada).

Não há métrica de negócio que eu possa citar — resolução sem humano e tempo de
espera antes/depois não foram instrumentados. O que existe é observabilidade de
execução via tracing, usada para inspecionar decisão de agente e regressão.

## Como contar em entrevista (STAR curto)

**Situação:** hospital de grande porte, milhares de pacientes, serviços de rotina
presos a canais que geram fila e ligação.
**Tarefa:** levar esses serviços para o WhatsApp sem que o paciente precise saber
qual sistema interno atende seu pedido.
**Ação:** desenhei e implementei um sistema multiagente em LangGraph, com agentes
especializados por serviço e roteamento a partir da linguagem natural do paciente,
integrado aos sistemas do hospital e instrumentado com tracing para inspecionar
cada decisão.
**Resultado:** sistema em produção; o agente de check-in atende milhares de
pacientes por mês, com o escopo do que ele pode afirmar preso a tools contra os
sistemas do hospital.
