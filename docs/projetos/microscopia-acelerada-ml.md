---
when_to_use: >
  Projeto de doutorado que acelerou microscopia s-SNOM com amostragem
  esparsa e regressão por processo gaussiano: escolha do método, ajuste de
  hiperparâmetros e como se valida imagem reconstruída sem inventar
  estrutura.
---

# Técnica de microscopia acelerada por machine learning

**Onde:** Doutorado · UNICAMP / LNLS-CNPEM · 2021 – 2025
**Código público:** [spiral-scans-reconstruction](https://github.com/1rafaelmayer/spiral-scans-reconstruction)
— tutorial em notebook: varredura espiral sobre dado real de s-SNOM, reconstrução
por processo gaussiano e escolha de kernel.

## Contexto

Microscopia óptica de campo próximo (s-SNOM) produz imagem em nanoescala varrendo
ponto por ponto. Isso torna cada imagem lenta: o tempo de aquisição escala com o
número de pontos, e experimento de nanofotônica precisa de muitas imagens em
condições variadas (frequência, temperatura, campo). O tempo de máquina é o
recurso escasso, e num laboratório nacional ele é disputado.

## O que fizemos

Uma **técnica acelerada de microscopia** baseada em **reconstrução a partir de
amostragem esparsa**: em vez de varrer a grade completa, mede-se um subconjunto de
pontos e **regressão por processo gaussiano** reconstrói a imagem. O ganho vem do que
não precisa ser medido.

Processo gaussiano é a escolha natural aqui por dois motivos além da precisão: ele
funciona com poucos pontos e devolve **incerteza junto com a predição** — em imagem
reconstruída, saber onde o modelo está inseguro é parte do resultado, não extra.

A escolha por regressão clássica em vez de rede neural foi deliberada: o volume de
imagem disponível num laboratório de s-SNOM não sustenta treino de rede, e método
mais simples é mais fácil de auditar quando o resultado é medição científica.

**Como o modelo foi ajustado e demonstrado.** A otimização de hiperparâmetros usou
imagens completas já medidas, subamostradas artificialmente — ali existe verdade de
referência para comparar. A demonstração final foi experimental: imagem adquirida
já com poucos pontos, no microscópio, com o método reconstruindo a partir do que foi
efetivamente medido. As duas etapas respondem perguntas diferentes: a primeira
calibra, a segunda mostra que funciona em aquisição real.

## Como se valida uma imagem reconstruída

Esse é o ponto metodológico do trabalho. Modelo que preenche o que não foi medido
pode produzir estrutura plausível e inexistente — e em microscopia isso não é erro
de métrica, é resultado científico falso. A validação foi em duas frentes:

- **Amostra de referência conhecida:** medir material cuja estrutura já está
  caracterizada e verificar se a reconstrução a recupera.
- **Comportamento físico esperado:** checar se o padrão reconstruído tem a
  assinatura correta de resposta polaritônica/ressonante da amostra. Ruído de modelo
  não obedece física; estrutura real obedece.

## Decisões técnicas e trade-offs

**Fidelidade contra tempo de aquisição.** Menos pontos acelera linearmente, mas há
um piso: abaixo de certa densidade de amostragem o detalhe fino deixa de ser
recuperável e a reconstrução passa a suavizar estrutura que existe. O trabalho vive
nesse limite — o objetivo não é o máximo de compressão possível, é a maior aceleração
que ainda preserva o que o experimento precisa medir.

**Processo gaussiano em vez de rede neural.** Menos capacidade de representação, em
troca de funcionar com poucos dados, entregar incerteza calibrada e produzir resultado
que se explica. Em medição científica, modelo auditável vale mais que modelo poderoso.
O custo é escala: processo gaussiano cresce mal com o número de pontos, o que impõe
limite ao tamanho da imagem tratada de uma vez.

## Resultado

A abordagem ampliou as capacidades experimentais do grupo e rendeu publicação
revisada por pares: *Accelerated Nano-Optical Imaging through Sparse Sampling*,
**Nano Letters** 24(7), 2149 (2024).

Não há fator de speedup que eu possa citar como número consolidado — o ganho depende
da amostra e da densidade de amostragem escolhida.

## Por que esse projeto abre a conversa sobre minha transição

Quando perguntam "por que um físico está fazendo IA", esse é o projeto que
responde sem discurso: eu não migrei de área depois de terminar o doutorado —
usei machine learning dentro dele, para resolver um gargalo real de instrumento,
e foi essa experiência que me levou para IA aplicada.

Ele também carrega o problema metodológico que eu levo para GenAI: um modelo que
preenche o que não foi medido é útil e perigoso pela mesma razão. Aprender a
validar isso em microscopia é o que me deixa desconfortável com sistema de
linguagem que não tem grounding verificável.
