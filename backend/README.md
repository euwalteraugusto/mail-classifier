# Mail Classifier Service

Serviço backend para classificação automática de emails como **Produtivos** ou **Improdutivos**,
utilizando uma abordagem híbrida baseada em heurísticas semânticas e classificação zero-shot
com modelos NLP.

## Objetivo

Demonstrar uma arquitetura simples e extensível para classificação de emails corporativos,
com foco em:
- alta assertividade
- baixo acoplamento
- decisões explicáveis

## Arquitetura

- Flask para API HTTP
- Heurísticas semânticas para casos óbvios
- Zero-shot classification (BART MNLI) para casos ambíguos
- Fallback seguro para evitar falsos negativos críticos

## Execução local

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python backend/app.py
