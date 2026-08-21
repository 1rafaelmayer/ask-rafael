---
when_to_use: >
  Projeto de agente de coaching acadêmico via WhatsApp para uma rede de
  ensino internacional: agente conversacional com onboarding, serviço de
  tools exposto por REST e MCP, e pipeline LangGraph que estrutura
  syllabus em JSON.
---

# Agente de IA para coaching acadêmico via WhatsApp

**Onde:** Distrito · AI Factory · 2025 – presente
**Papel:** engenheiro de IA/ML — camada de agentes, serviço de tools e pipeline de
conteúdo de cursos
**Cliente:** rede de ensino internacional. Os alunos são atendidos em espanhol; o
trabalho com o time do cliente é conduzido em inglês, no dia a dia
**Estágio:** em desenvolvimento, com escopo já em operação assistida

## Contexto

Instituições de ensino costumam descobrir que um aluno está em risco de evasão
depois que ele já parou de aparecer. Os dados que anunciam o risco existem —
notas, frequência, atividade na plataforma —, mas ninguém tem tempo de olhar aluno
por aluno, e quando alguém olha, já é tarde.

O produto é um **coach acadêmico** por WhatsApp: acompanha o aluno ao longo do
semestre, comenta como ele está indo, ajuda a se organizar e passa o caso para um
orientador humano quando a situação sai do que um coach pode resolver. O recorte é
tão importante quanto a função: ele não ensina conteúdo, não resolve tarefa, não
faz trâmite acadêmico e não trata assunto financeiro.

## O que construí

**O agente conversacional.** Fluxo de onboarding no primeiro contato — identifica
o aluno, confirma os dados que o sistema tem sobre ele, explica o que faz e o que
não faz, e captura preferências (nome pelo qual quer ser chamado, horário
preferido de contato, motivação no curso). Depois disso, o aluno cai direto em
coaching, e as preferências são recuperadas nas conversas seguintes.

**O serviço de execução de tools.** Um serviço em FastAPI que é a única porta do
agente para os dados acadêmicos: perfil do aluno, indicadores de risco,
coordenador responsável, preferências e conteúdo de curso. Ele é exposto de duas
formas sobre a mesma lógica — REST atrás do API Gateway do GCP, para consumo por
outros sistemas, e **servidor MCP**, para o agente consumir como tools.

**A pipeline de conteúdo de cursos.** Grafo em LangGraph que converte documentos de
syllabus em Word (`.doc`/`.docx`) em JSON estruturado consumível pelo agente: extrai
texto e tabelas na ordem do documento — convertendo `.doc` legado via LibreOffice
headless —, estrutura o conteúdo com LLM contra um schema explícito, e embrulha no
formato que a base de conhecimento de cursos aceita. Cada arquivo gera um JSON, e um
CSV de relatório registra o que passou e o motivo de cada falha. Sem isso, o agente
fala da situação do aluno mas não sabe falar do curso dele — o material que descreve
o curso chega como documento pensado para pessoa, não para máquina.

**Um protótipo de classificação de risco** sobre os dados do cliente, agregando três
sinais — nota abaixo do mínimo aprobatório, percentual de faltas e matérias sem
entrega — em risco baixo, médio ou alto. Os limiares e a forma final ainda estão em
definição com a instituição.

## A parte difícil: identidade, escopo e o que o agente não sabe

**Identidade antes de qualquer dado.** O agente não revela nota, matéria, risco —
nem confirma o nome do aluno — antes de a matrícula ser reconhecida. Se não bate, ele
pede uma reconferência e encaminha para humano em vez de insistir. É a guarda mais
simples do sistema e a que tem o custo mais alto se falhar.

**Nada é afirmado sem tool.** Tudo que o agente diz sobre nota, falta, data ou risco
vem do serviço de tools. Isso não é só antialucinação: define o que o agente pode
prometer. Ele tem parciais e final, não a nota de uma tarefa específica; conhece as
matérias e o calendário do período, não a grade de horários. Deixar isso explícito no
comportamento evita a falha mais chata desse tipo de produto, que é o agente
inventar a resposta que o aluno queria ouvir.

**Escalada para humano é julgamento do LLM.** O agente escala quando o aluno mostra
sofrimento real, quando a causa é não acadêmica (financeira, de saúde, crise
pessoal), quando pede para falar com alguém, ou quando recusa ajuda estando
claramente em risco. Nenhum desses sinais se reduz a gatilho de palavra-chave — mas é
o ponto que mais precisa de avaliação, porque falso negativo significa aluno pedindo
ajuda e não sendo ouvido.

**Proatividade é o próximo passo, não o estado atual.** O agente hoje responde dentro
da conversa; ele não aborda o aluno por iniciativa própria. O desenho da abordagem
proativa — batch periódico sobre a lista de risco, com controle de cadência de
contato — está definido e é a fase seguinte. Vale ser exato sobre isso: o problema
difícil de agente proativo (decidir quem abordar, quando, com qual mensagem e quando
desistir, com custo assimétrico dos dois lados) é o que vem, não o que já está em pé.

## Decisões técnicas e trade-offs

**MCP e REST sobre a mesma lógica de acesso a dados.** O serviço poderia expor
apenas tools para o agente. Expor também REST atrás do API Gateway custa um pouco
mais de superfície para manter, e paga em duas coisas: outros sistemas do cliente
consomem os mesmos dados sem passar pelo agente, e a lógica de acesso fica testável
por fora do LLM — os testes cobrem a regra, não o comportamento conversacional.

**Classificação de risco por regra, não por modelo.** Nota abaixo do mínimo, faltas
acima do limite e matérias sem entrega são critérios que a instituição já usa e sabe
defender. Um modelo preditivo poderia antecipar risco mais cedo, mas a decisão de
declarar um aluno em risco é sensível e precisa ser explicável para quem vai agir
sobre ela. O custo é ficar limitado ao sinal que já é visível — o modelo é o passo
que faz sentido depois, com histórico suficiente.

**Agentes na extração de syllabus, não parser determinístico.** O layout varia demais
entre documentos, e a extração exige interpretar e sintetizar conteúdo, não localizar
campo. O contrapeso é um schema explícito na saída — campo obrigatório ausente ou
fora de formato não entra — mais revisão amostral humana contra o documento original.
O custo é uma pipeline com dependência de LLM em etapa de ingestão, com o tracing das
execuções como forma de auditar o que saiu de cada arquivo.

**Personalização por tool, não por prompt carregado.** O agente consulta o dado do
aluno quando precisa, em vez de receber o histórico inteiro antecipadamente. Limita o
que ele pode afirmar ao que o sistema devolveu e reduz a chance de o modelo preencher
lacuna com invenção plausível. O custo é mais chamadas e mais latência por conversa.

## Stack

Python 3.13, FastAPI, Pydantic, httpx, servidor MCP (SDK oficial), agente em
LangChain/LangGraph com `langchain-mcp-adapters`, LLM da OpenAI. API Gateway e Secret
Manager no GCP. Pipeline de syllabus em LangGraph com python-docx e LibreOffice
headless, tracing em LangSmith. Testes em pytest, `ruff` e pre-commit, CI em Azure
DevOps com análise SonarQube.

## Resultado

Projeto em desenvolvimento. Não há número a citar: alunos alcançados, taxa de
resposta, casos encaminhados e efeito sobre evasão são exatamente as métricas
previstas para medir quando entrar em operação plena.

## Por que esse projeto é bom em entrevista

É o meu exemplo mais completo de agente com **fronteira bem desenhada**: um sistema
que fala com um aluno sobre a própria vida acadêmica, onde quase todo o trabalho de
engenharia está em delimitar o que ele pode afirmar, o que ele não sabe, quando ele
tem que calar e chamar uma pessoa. Também é o caso em que fiz as três camadas —
ingestão de conteúdo não estruturado, serviço de dados como tools, e o agente — o que
permite responder por qualquer ponta que o entrevistador puxar.
