---
when_to_use: >
  Competências em machine learning, deep learning e NLP: scikit-learn,
  PyTorch, clusterização e processo gaussiano, onde cada uma foi exercida,
  e os hábitos de validação que diferenciam a atuação nesse eixo.
---

# Machine Learning, Deep Learning e NLP

## Escopo

Machine learning clássico e deep learning, incluindo NLP. Ferramenta principal é
**scikit-learn** (classificação, clusterização, regressão — incluindo processo
gaussiano na reconstrução de imagem no doutorado), com PyTorch nos projetos de rede
neural. Análise e preparação de dados com Pandas, NumPy e Matplotlib.

## Onde exerci

**Redes neurais multitarefa em sinal de sensor** — Samsung. Feature engineering
sobre sinal de wearable e análise segmentada de desempenho para achar falha que a
média esconde. → `projetos/wearables-samsung-modelos.md`

**Deep learning aplicado a OCR** — Amil. Reconhecimento em documento médico de
qualidade ruim, com OpenCV no pré-processamento e a decisão central sendo
quando *não* confiar na predição. → `projetos/ocr-documentos-medicos.md`

**Classificação de risco acadêmico** — Distrito. Protótipo determinístico, baseado em
regra sobre dado institucional (nota, frequência, atividade em atraso), que classifica
o risco do aluno e alimenta o que o agente pode dizer. Ainda em definição; a
modelagem estatística é o passo seguinte esperado, não o que está no ar.
→ `projetos/coach-academico-whatsapp.md`

**Clusterização** — Distrito. Segmentação de audiência para ancorar personas
geradas em perfis que existem no dado.
→ `projetos/analise-campanhas-personas.md`

**ML em instrumentação científica** — doutorado. Técnica acelerada de microscopia
s-SNOM. → `projetos/microscopia-acelerada-ml.md`

## O que me diferencia nessa competência

Não é a lista de algoritmos — é a parte de validação. Vindo de física
experimental, meu instinto diante de um resultado bom é procurar o artefato que
o explicaria. Na prática isso aparece em três hábitos:

- **Segmentar antes de acreditar na média.** Modelo com boa métrica agregada e
  falha sistemática numa subpopulação é o caso comum, não a exceção.
- **Atacar o dado na origem.** Na Samsung, usei física do sensor e teoria de detecção
  para melhorar o sinal antes do modelo, em vez de compensar ruído com capacidade.
- **Escolher a métrica pelo custo do erro.** Em risco de evasão, falso negativo e
  falso positivo têm custos completamente diferentes; onde colocar o corte é decisão
  de produto, não de código. Em OCR de documento médico é a mesma pergunta com outra
  roupa: onde parar de aceitar automático e mandar para revisão humana.

## Nível

Competência central, em produção: ML clássico (clusterização, regressão,
classificação), feature engineering sobre sinal, avaliação e diagnóstico de modelo por
segmento, e todo o trabalho de dado em volta.

Onde eu sou mais forte é em decidir se um modelo está certo pelo motivo certo, e em
construir o dado que entra nele — a parte que separa métrica bonita de sistema que
funciona com usuário real.
