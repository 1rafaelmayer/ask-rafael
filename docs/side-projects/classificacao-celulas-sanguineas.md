---
when_to_use: >
  Side project de classificação de 8 tipos de células sanguíneas no
  BloodMNIST comparando MLP e CNN: dados, resultados por configuração,
  achados contraintuitivos sobre kernel e número de filtros, decisões
  explícitas e análise de erro.
---

# Classificação de células sanguíneas (MLP vs CNN)

**Repo:** github.com/1rafaelmayer/deep-learning-of-blood-cells · publicado ago/2024
**Stack:** Python, TensorFlow/Keras, scikit-learn, medmnist, Colab

## Problema
Classificar 8 tipos de células sanguíneas em imagens de microscopia. Objetivo:
percorrer o caminho completo (EDA → arquitetura → tuning → análise de erro)
decidindo por medição, não por convenção.

## Dados
BloodMNIST (Acevedo 2020; Yang 2021): 17.092 imagens 28×28×3, split 7:1:2
(11.959 treino). Classes: basófilos, eosinófilos, eritroblastos, granulócitos
imaturos, linfócitos, monócitos, neutrófilos, plaquetas.
Desbalanceado (>2.000 vs <1.000 imagens de treino), mas com a mesma distribuição
nos três splits. Normalização RGB p/ [0,1] + one-hot.

## Modelos e resultados (acurácia em teste)
| Modelo | Config | Acc |
|---|---|---|
| MLP 1 camada | N=32, BatchNorm, ReLU, dropout 0.1, Adam, early stopping | 85% |
| MLP 2 camadas | N=64 | 86% |
| CNN 1 conv | 16 filtros, kernel 1×1, maxpool 4×4 | **88%** |

## Achados que valem mais que o número
- **Mais filtros não ajudam:** ótimo em 16 (testado até 2048). Com 28×28 e ~12k
  imagens, capacidade extra não tem onde ser aprendida.
- **Kernel 1×1 ≈ 3×3 ≈ 5×5:** em crop centrado numa célula, o sinal
  discriminante está em cor/intensidade por pixel (combinação de canais RGB),
  não em textura espacial. Contraria a intuição de "CNN aprende bordas".
- **Adam > SGD** em convergência e desempenho final.
- **Modelo menor por padrão:** critério de escolha foi "menor modelo com
  desempenho equivalente" (N=32 vs N=512 → ~0,5pp de diferença).

## Decisões explícitas
- **Sem cross-validation:** medido e descartado por custo computacional em Colab,
  mesmo no modelo mais simples. Mantido o split oficial do dataset, o que também
  preserva comparabilidade com a literatura.
- **Tuning manual por eixo** (um hiperparâmetro por vez): ignora interações, mas
  cada curva gerada é informação legível sobre o modelo. Random search /
  otimização bayesiana ficaram registrados como próximo passo.

## Análise de erro
Erro concentrado na classe 3 (granulócitos imaturos), confundida com 0, 4, 5 e 6.
Inspeção visual confirma: é um estágio de maturação, não uma categoria
morfologicamente disjunta. Acurácia agregada de 88% esconde que o erro está
justamente na classe cuja distinção tem significado clínico.

Não percorrido: data augmentation, CNNs mais profundas, busca automatizada.
