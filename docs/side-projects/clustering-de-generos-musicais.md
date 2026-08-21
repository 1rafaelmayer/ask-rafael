---
when_to_use: >
  Side project de clustering não supervisionado de gêneros musicais sobre
  atributos acústicos do Spotify: PCA e UMAP, KMeans/Mean-
  Shift/hierárquico, escolha de k e por que a métrica ótima produzia
  partição degenerada.
---

# Clustering de gêneros musicais (não supervisionado)

**Repo:** github.com/1rafaelmayer/music-clustering · notebook dez/2022, publicado ago/2024
**Stack:** Python, scikit-learn, UMAP, pandas, matplotlib, Colab · inclui artigo em PDF

## Problema
Gênero musical é rótulo cultural, não medida. A pergunta: atributos acústicos
agrupam músicas de forma que reproduza gêneros? E quais atributos importam?

## Dados
Spotify Tracks Dataset (Kaggle): 114 gêneros × 1.000 músicas. 15 atributos
numéricos usados (popularidade, duração, explicitness, danceability, energy, key,
loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence,
tempo, time signature), reescalados 0–1. Gênero removido do treino e reintroduzido
só para comparação — validação externa de clusters não supervisionados.
Amostra de 30% para custo computacional.

## Método
- **Redução de dimensionalidade:** PCA e UMAP para visualização.
- **PCA** (exploratório): 10 componentes = 96,5% da variância; 2 componentes só
  45,2%. PC1 correlaciona forte e negativamente com *mode*; PC2 positivamente com
  *acousticness* e negativamente com *energy*. No plano PC1×PC2, romance separa de
  opera (modo menor vs maior) e sleep separa de punk (energia/acústica).
- **Decisão:** PCA **não** foi usado para o clustering. Componentes principais
  destroem a interpretabilidade dos clusters, que era o produto do trabalho.
  Modelos treinados nos 15 atributos originais.
- **Clustering:** KMeans (k-means++), Mean-Shift e hierárquico. Escolha de k por
  silhouette.

## Escolha de k — o ponto metodológico
Silhouette é máximo em k=2, mas a inspeção dos atributos mostrou que com k=2 o
modelo separava **apenas por *mode*** (maior/menor): partição trivial e sem
informação. k=6 foi escolhido por equilibrar separação e não-trivialidade
(S ≈ 0,24 — baixo, e reportado como tal).

Métrica ótima ≠ resultado útil: a métrica não sabe que a partição vencedora é
degenerada.

## Resultado — k=6
| Cluster | Atributo dominante | Gêneros top |
|---|---|---|
| 1 | explicitness | comedy, sad, emo, j-dance |
| 2 | mode 0 (menor) | turkish, romance, dub, progressive-house |
| 3 | mode 1 (maior) | r-n-b, country, party, j-idol |
| 4 | key baixo | punk-rock, ska, power-pop, salsa |
| 5 | instrumentalness | study, minimal-techno, detroit-techno, idm |
| 6 | acousticness | opera, classical, honky-tonk, disney |

Atributos relevantes: **mode, explicitness, energy, acousticness**. Apesar da
variância alta *dentro* de cada gênero, os três modelos de clustering
convergiram para agrupamentos semelhantes — consistência entre métodos como
evidência, na ausência de ground truth.

## Limites reconhecidos
S ≈ 0,24 indica clusters mal separados: gêneros se sobrepõem no espaço acústico e
atribuição rígida é a modelagem errada. Próximo passo registrado: **fuzzy
k-means** (pertencimento parcial), que é o que a estrutura do dado pede.
