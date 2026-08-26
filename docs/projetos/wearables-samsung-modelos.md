---
when_to_use: >
  Projeto de modelos de IA para wearables da Samsung: pipelines de dados,
  qualidade de dado de sensor, diagnóstico de falha em redes multitarefa
  por segmento, e a conexão pública com o recurso de sono do Galaxy Watch.
---

# Modelos de IA para dispositivos wearables — Samsung

**Onde:** Samsung R&D Institute Brazil (SRBR) · abr/2025 – ago/2025
**Papel:** Senior AI Researcher / cientista de dados
**Referência pública:** modelos de rede neural para melhora do sono numa geração
de Galaxy Watches — [Samsung Newsroom](https://news.samsung.com/br/recurso-de-apneia-do-sono-desenvolvido-no-brasil-e-presente-no-galaxy-watch-da-samsung-e-o-primeiro-de-sua-categoria-autorizado-pela-fda-dos-eua)

## Contexto

Desenvolvimento dos novos modelos de IA para os dispositivos wearables da
Samsung. O dado de origem é sinal de sensor em contato com o corpo — ruidoso por
natureza, dependente de como o dispositivo está posicionado, e afetado por
variação entre pessoas.

## O que fiz

**Pipelines de dados escaláveis** para alimentar os modelos de rede neural,
dimensionados para o volume e a cadência do time de modelagem.

**Qualidade de dado e feature engineering.** A contribuição principal: melhorar a
qualidade dos dados e das representações que entram no modelo — a parte que mais
pesa no resultado final, mais do que capacidade extra de rede.

**Análise de redes multitarefa.** Modelo multitarefa esconde falha na média: ele
pode ter desempenho agregado bom e errar sistematicamente numa subpopulação ou
numa condição de uso específica. Meu trabalho foi segmentar os dados e procurar
esses padrões de desempenho por segmento, produzindo o diagnóstico que orientava a
próxima iteração dos modelos.

Os padrões de falha que a segmentação expôs são de três tipos, e a distinção importa
porque cada um pede correção diferente: erro sistemático em **subpopulação** (o
modelo vai bem na média e mal num grupo de pessoas), erro em **condição de uso**
específica, e **uma tarefa dominando o treino** — melhorando a métrica agregada às
custas das demais cabeças do modelo multitarefa.

## Decisões técnicas e trade-offs

**Investir em qualidade de dado, em vez de só mais capacidade de rede.** Em sinal
de sensor corporal, jogar dado cru para a rede aprender a representação funciona
quando há dado abundante e homogêneo — não é o caso quando o ruído depende de
posicionamento do dispositivo e de variação fisiológica entre pessoas. O custo
assumido é que melhoria de dado exige análise contínua por segmento, em vez de
esperar que a rede compense sozinha.

**Avaliar por segmento, não pela média.** Métrica agregada é o que reporta bem e o
que esconde falha. Segmentar custa mais análise, mais fatias para acompanhar e
decisão sobre quais segmentos importam — em troca, é o único jeito de ver o erro
sistemático antes de o produto vê-lo.

## Confidencialidade

O vínculo público é este: os modelos em que trabalhei alimentam o recurso de
melhora do sono presente numa geração de Galaxy Watches, noticiado pela própria
Samsung (link acima). Isso pode ser dito porque é informação pública.

O que **não** pode: arquitetura do modelo, quais e quantas tarefas ele cobria,
dado, métrica e qualquer número específico do produto. Em entrevista, a resposta
sobre esses detalhes é que o contrato não permite entrar neles — e seguir
descrevendo o raciocínio do trabalho, que é o que interessa de fato.

## Resultado

Os modelos que ajudei a alimentar com pipeline de dados e feature engineering
integram um recurso de sono lançado numa geração de Galaxy Watches. Não
acompanhei o desfecho de perto após sair da Samsung, então não tenho métrica de
produto para citar — o que entreguei foi a melhoria de dado e o diagnóstico de
onde o modelo multitarefa errava de forma sistemática.

## Por que esse projeto é bom em entrevista

É evidência de contribuição em produto de consumo com escala real: o trabalho de
dado e diagnóstico que fiz alimenta um recurso hoje disponível numa geração de
Galaxy Watches, sob as restrições normais de um projeto sob contrato.
