---
when_to_use: >
  Passagem como cientista de dados no Grupo Amil (jan–abr/2025, via
  Cuboconnect): escopo, stack Databricks/Azure/FastAPI e resultados do
  trabalho de OCR em documentos médicos. Não detalha a implementação do
  pipeline — isso está em projetos/ocr-documentos-medicos.md.
---

# Cientista de Dados — Grupo Amil

**Período:** janeiro de 2025 – abril de 2025 (4 meses) · terceirizado, via Cuboconnect · remoto

## Escopo

Cientista de dados no Grupo Amil, alocado pela Cuboconnect, desenvolvendo
soluções de OCR para extração e processamento de informações de documentos
médicos e administrativos.

Foi minha primeira posição em indústria, sobreposta à reta final do doutorado —
a transição deliberada de pesquisa acadêmica para engenharia aplicada.

## O problema

Documento médico é um dos piores cenários possíveis para OCR: formulário
manuscrito, carimbo sobre texto, digitalização torta, layout que muda por
unidade emissora. Extrair campo estruturado disso não é resolver reconhecimento
de caractere — é decidir quando o reconhecimento não é confiável.

→ `projetos/ocr-documentos-medicos.md`

## Stack

Databricks e Azure como plataforma. Docker e FastAPI para empacotar e servir.
EasyOCR e Azure Document Intelligence no reconhecimento. PyTorch,
scikit-learn e OpenCV no pré-processamento e na modelagem.

## Resultados

- Ajudei a decidir o modelo de OCR que seria usado.
- Projeto ajudou a estruturar e detectar fraudes em milhares de documentos médicos usados para reembolços de procedimentos médicos.
