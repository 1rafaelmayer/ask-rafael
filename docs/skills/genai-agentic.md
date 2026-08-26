---
when_to_use: >
  Competências em GenAI e arquiteturas agentic: LangChain e LangGraph,
  tracing em LangSmith/Fuse, MCP e a escolha de tool contra a fonte em vez
  de RAG, com os projetos onde cada uma foi exercida.
---

# GenAI e arquiteturas agentic

Minha especialização atual e o centro do meu trabalho hoje.

## Ferramentas

**LangChain / LangGraph** — orquestração de agentes. LangGraph é o que uso quando
o fluxo precisa de controle explícito: estado persistente entre turnos,
roteamento condicional, e a possibilidade de inspecionar por que o sistema tomou
um caminho.

**LangSmith / Fuse** — tracing e avaliação. Em sistema multiagente, observabilidade
não é conforto: sem trace, uma resposta errada é indepurável, porque você não sabe
se o erro foi de roteamento, de recuperação de contexto ou de geração.

**MCP (Model Context Protocol)** — exposição de resources e tools para agentes.
Certificado pela Anthropic em arquitetura de agentes e MCP.
→ `certificacoes.md`

**RAG** — coberto por certificação, e uma decisão de arquitetura que eu tomo de forma
consciente. Nos sistemas que construí, o dado que o agente precisa é transacional e
sensível (situação do paciente, matrícula do aluno, sistema interno do cliente), e
para esse tipo de dado a resposta certa é **tool contra a fonte**, não busca vetorial
sobre cópia indexada: tool devolve o estado atual, respeita a autorização e é
auditável, enquanto índice vetorial responde com o que foi indexado. Onde o corpus for
texto grande e estável, RAG é a escolha — é a mesma análise, com outra resposta.

## Onde exerci

- **Sistema multiagente para serviços hospitalares via WhatsApp** — agentes
  especializados com roteamento a partir de linguagem natural do paciente.
  → `projetos/agentes-whatsapp-hospital.md`
- **Agente de coaching acadêmico via WhatsApp** — agente conversacional sobre um
  serviço de tools exposto por REST e por **MCP**, com identidade verificada antes de
  qualquer dado e escalonamento para humano por julgamento do LLM.
  → `projetos/coach-academico-whatsapp.md`
- **Simulação de personas para análise de campanha** — GenAI ancorada em
  clusters reais de audiência.
  → `projetos/analise-campanhas-personas.md`

## Como eu penso sobre esses sistemas

A parte fácil de um agente é fazê-lo responder. A parte difícil é definir a
fronteira: o que ele pode afirmar, quando deve admitir que não sabe, e quando
deve passar para um humano. Em saúde e educação — meus dois domínios — isso não
é refinamento de qualidade, é requisito.

## Nível

Competência principal, exercida diariamente em produção desde set/2025.

O estudo, porém, começou antes: acompanhei e usei GenAI por conta própria **durante o
doutorado**, em paralelo ao trabalho de pesquisa, antes de existir cargo meu na área.
Não foi treinamento de empresa nem virada de mercado — foi o mesmo movimento que me
levou a usar ML dentro do doutorado. O que set/2025 marca é quando isso passou a ter
usuário final e consequência em produção.

## Como me mantenho atualizado

Meus side projects de ML clássico e deep learning (`side-projects/`) são de uma fase
anterior — 2022 e 2024, antes de GenAI e sistemas agentic virarem meu foco principal.
Hoje me atualizo de outra forma: leio notícia sobre IA diariamente e testo o que
aparece de novo direto nos projetos que já estão em andamento, em vez de fazer curso
ou projeto isolado para aprender.
