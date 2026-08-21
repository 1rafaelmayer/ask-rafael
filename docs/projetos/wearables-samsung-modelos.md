---
when_to_use: >
  Projeto de modelos de IA para wearables da Samsung: pipelines de dados,
  feature engineering sobre sinal de sensor, diagnóstico de falha em redes
  multitarefa por segmento e o trade-off entre feature física e capacidade
  de rede.
---

# Modelos de IA para dispositivos wearables — Samsung

**Onde:** Samsung R&D Institute Brazil (SRBR) · abr/2025 – ago/2025
**Papel:** Senior AI Researcher / cientista de dados

## Contexto

Desenvolvimento dos novos modelos de IA para os dispositivos wearables da
Samsung. O dado de origem é sinal de sensor em contato com o corpo — ruidoso por
natureza, dependente de como o dispositivo está posicionado, e afetado por
variação entre pessoas.

## O que fiz

**Pipelines de dados escaláveis** para alimentar os modelos de rede neural,
dimensionados para o volume e a cadência do time de modelagem.

**Análise de sinais e feature engineering.** A contribuição principal: melhorar a
qualidade das representações que entram no modelo. Em problema de sinal, uma
feature bem construída a partir de entendimento físico do fenômeno frequentemente
vale mais que capacidade extra de rede.

**Análise de redes multitarefa.** Modelo multitarefa esconde falha na média: ele
pode ter desempenho agregado bom e errar sistematicamente numa subpopulação ou
numa condição de uso específica. Meu trabalho foi segmentar os dados e procurar
esses padrões de desempenho por segmento, produzindo o diagnóstico que orientava a
próxima iteração dos modelos.

**Física do sensor e teoria de detecção aplicadas à qualidade do dado.** Aqui a
formação em física entrou direto: entender como o sinal é gerado e detectado permite
atacar o ruído na origem, em vez de compensá-lo depois com modelo maior.

Os padrões de falha que a segmentação expôs são de três tipos, e a distinção importa
porque cada um pede correção diferente: erro sistemático em **subpopulação** (o
modelo vai bem na média e mal num grupo de pessoas), erro em **condição de uso**
específica, e **uma tarefa dominando o treino** — melhorando a métrica agregada às
custas das demais cabeças do modelo multitarefa.

## Decisões técnicas e trade-offs

**Feature construída sobre entendimento do fenômeno, em vez de mais capacidade de
rede.** A alternativa padrão é entregar o sinal cru e deixar a rede aprender a
representação. Em sinal de sensor corporal, isso funciona quando há dado abundante e
homogêneo — não é o caso quando o ruído depende de posicionamento do dispositivo e de
variação fisiológica entre pessoas. O custo assumido é que feature derivada de
modelo físico carrega uma hipótese: se a hipótese não vale para um segmento, a
feature degrada ali, e é preciso descobrir isso por análise segmentada em vez de
esperar que a rede compense.

**Avaliar por segmento, não pela média.** Métrica agregada é o que reporta bem e o
que esconde falha. Segmentar custa mais análise, mais fatias para acompanhar e
decisão sobre quais segmentos importam — em troca, é o único jeito de ver o erro
sistemático antes de o produto vê-lo.

## Confidencialidade

Produto não lançado, sob contrato. O que **pode** ser dito é o que está neste
arquivo: a classe de problema (modelagem sobre sinal de sensor corporal), o tipo de
trabalho (pipeline de dados, feature engineering a partir de física do sensor,
avaliação segmentada de rede multitarefa) e os tipos de padrão de falha encontrados.

O que **não** pode: qual sensor e qual sinal, quais e quantas tarefas o modelo
cobria, arquitetura, dado, métrica e qualquer número. Em entrevista, a resposta a
"que sensor era?" é que o contrato não permite entrar nisso — e seguir descrevendo o
raciocínio, que é o que interessa de fato.

## Resultado

Não há resultado que eu possa reivindicar: saí da Samsung antes de acompanhar o
desfecho dos modelos, então não sei quanto das features e das análises sobreviveu à
iteração seguinte. O que entreguei foi diagnóstico — onde o modelo multitarefa errava
de forma sistemática — e a representação de entrada melhorada. Se isso virou ganho de
métrica no produto, eu não estava lá para medir.

## Por que esse projeto é bom em entrevista

É a melhor evidência de que meu diferencial não é retórico. "Formação em física
ajuda" é frase de currículo; aplicar óptica e teoria de detecção para melhorar
dado de sensor em um produto de consumo é a coisa acontecendo.
