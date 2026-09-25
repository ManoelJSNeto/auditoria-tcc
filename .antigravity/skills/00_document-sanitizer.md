# Skill: document-sanitizer
Description: Higieniza o arquivo bruto de Markdown exportado do Google Docs e gera a base canônica para auditoria de integridade.

## Entradas:
- `input/raw_tcc.md` (export original do Google Docs)

## Regras de Sanitização:
1. Normalização de Quebras de Linha:
   - Converter `\r\n` universalmente para `\n`.
   - Limitar saltos de linha consecutivos a no máximo dois (`\n\n`).
2. Limpeza de Artefatos Unicode:
   - Remover Byte Order Mark (`\ufeff`), espaços de largura zero (`\u200b`) e soft hyphens (`\u00ad`).
   - Converter non-breaking spaces (`\u00a0`) para espaços padrão ASCII (`0x20`).
3. Normalização de Cabeçalhos e Parágrafos:
   - Garantir rigorosamente um espaço antes do título em marcações `#` a `######` (`^#{1,6}\s+`).
   - Eliminar espaços em branco e tabulações no final de linhas (`[ \t]+$`).
4. Geração de Hash Canônico:
   - Executar via terminal: `python scripts/canonical.py docs/tcc_sanitizado.md`.
   - Gravar o hash resultante no manifesto.

## Arquivos de Saída:
- `docs/tcc_sanitizado.md`: Documento normalizado pronto para fatiamento.
- `docs/manifest_integridade.json`: Contendo `{"hash_canonico_original": "<HASH_GERADO>", "status": "sanitizado"}`.