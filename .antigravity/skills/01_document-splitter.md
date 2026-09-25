# Skill: document-splitter
Description: Fatie o documento sanitizado em capítulos atômicos garantindo integridade matemática via SHA-256.

## Entradas:
- `docs/tcc_sanitizado.md`
- `docs/manifest_integridade.json`

## Regras de Execução:
1. Divisão por Cabeçalhos:
   - Localizar os títulos de primeiro nível (`# 1`, `# 2`, etc.) e separar o arquivo nas seguintes divisões dentro de `docs/capitulos/`:
     - `00_pre_textuais.md`
     - `01_introducao.md`
     - `02_referencial_teorico.md`
     - `03_metodologia_estudo_de_caso.md`
     - `04_resultados_discussao.md`
     - `05_conclusao.md`
     - `referencias.md` (obrigatório: isolar toda a seção de bibliografia final aqui)
2. Preservação de Conteúdo (Zero Data Loss):
   - Proibido reescrever, formatar, resumir ou deletar qualquer trecho.
3. Validação de Integridade:
   - Concatenar virtualmente todos os arquivos gerados em `docs/capitulos/` em ordem.
   - Rodar o algoritmo de canonicalização via `scripts/canonical.py` e gerar o novo hash.
   - Comparar com `hash_canonico_original`. Se houver divergência, abortar e avisar onde houve divergência.
4. Inicialização de Estado:
   - Criar `docs/glossario_acumulado.json` com a estrutura inicial: `{"siglas": {}, "conceitos": {}}`.

## Arquivos de Saída:
- Diretório `docs/capitulos/` populado com os arquivos modulares.
- `docs/glossario_acumulado.json` inicializado.