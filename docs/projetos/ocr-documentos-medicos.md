---
when_to_use: >
  Projeto de OCR na Amil para extrair dados de documentos médicos e
  administrativos: pré-processamento em OpenCV, comparação entre EasyOCR e
  Azure Document Intelligence, roteamento por tipo de documento e trade-
  offs de custo.
---

# OCR para extração de dados de documentos médicos e administrativos

**Onde:** Grupo Amil (via Cuboconnect) · jan/2025 – abr/2025
**Papel:** cientista de dados
**Estágio:** protótipo

## Contexto

O Grupo Amil processa volume alto de documentos médicos e administrativos cuja
informação precisa entrar em sistema estruturado. Feito à mão, é trabalho
repetitivo e caro; feito por OCR ingênuo, gera dado errado que contamina
processo a jusante — o que é pior que não ter dado.

## O problema real

Documento de saúde reúne quase todas as dificuldades de OCR ao mesmo tempo:
letra manuscrita, carimbo sobre texto, digitalização torta ou de baixo
contraste, e layout que varia por unidade emissora. O reconhecimento de
caractere é a parte resolvida do problema. A parte difícil é decidir **quando o
reconhecimento não é confiável** e o documento precisa de olho humano.

## O que fiz

- Protótipo de pipeline de extração, do pré-processamento de imagem à entrega do
  dado estruturado.
- Pré-processamento com OpenCV (correção de inclinação, contraste,
  binarização) — em documento ruim, é onde se ganha mais acurácia por hora de
  trabalho investida.
- Comparação entre **EasyOCR** e **Azure Document Intelligence** sobre os mesmos
  documentos, incluindo a confiança devolvida por cada um.
- Classificação de tipo de documento e extração de campo com scikit-learn, para
  rotear cada documento ao tratamento adequado.
- Empacotamento em Docker e exposição via FastAPI, sobre Databricks e Azure.

## Decisões técnicas e trade-offs

**Solução comercial em vez de OCR open source.** A comparação entre EasyOCR e Azure
Document Intelligence decidiu por dois motivos que se somaram. O primeiro é
operacional: com a volumetria de documentos e a exigência de processar em tempo
real, o EasyOCR precisaria de GPU dedicada — custo de infraestrutura e de operação
que a solução gerenciada absorve. O segundo é simples: os resultados do Document
Intelligence foram muito melhores nesses documentos. O custo assumido é custo por
página e dependência de fornecedor, com o dado saindo do ambiente para um serviço
externo — em contrapartida, sem GPU para dimensionar nem modelo próprio para manter.

**Peso no pré-processamento, não no modelo.** Com digitalização torta e de baixo
contraste, correção geométrica e binarização em OpenCV melhoram o resultado mais
rápido do que trocar de motor de OCR. Em protótipo com tempo curto, é onde o
esforço se paga.

Vale registrar o limite: **não houve nota de corte calibrada** entre "aceita
automático" e "manda para revisão humana". Essa é a decisão que transformaria o
protótipo em sistema utilizável em operação, e ela não foi tomada dentro do escopo
do trabalho.

## Resultado

Protótipo entregue e funcional, sem métrica que eu possa citar: não houve medição
formal de acurácia por tipo de campo nem volume processado em operação. O que ele
produziu foi a decisão de motor de OCR sustentada por comparação, e o mapa das
dificuldades reais do documento de saúde.

## Por que esse projeto importa na minha narrativa

Foi a primeira entrega minha em ambiente de indústria, ainda durante o
doutorado. É o ponto onde a transição de pesquisa para engenharia aplicada
deixou de ser intenção e passou a ter evidência.
