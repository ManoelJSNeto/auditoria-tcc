# Skill: pipeline-runner
Description: Orquestrador mestre do pipeline de auditoria. Controla a higienização, fatiamento e execução em lote ou pontual das auditorias.

## Gatilho de Ativação:
Sempre que o usuário solicitar "rodar esteira", "menu de auditoria" ou iniciar o processo.

## Protocolo Interativo:
Apresente imediatamente ao usuário as opções abaixo e aguarde a escolha:

1. **[Completo] Fatiar e Auditar Tudo:** Executa Skill 00, Skill 01 e audita todos os capítulos em sequência (01 -> 02 -> 03 -> 04 -> 05), acumulando o glossário automaticamente e gerando todos os relatórios em `reports/`.
2. **[Rápido] Apenas Sanitizar e Fatiar:** Atualiza os arquivos em `docs/capitulos/` a partir de `input/raw_tcc.md` e valida a integridade do SHA-256.
3. **[Focado] Auditar Capítulo Específico:** Permite escolher um único capítulo (ex: 03_metodologia) para reauditá-lo após uma alteração no Google Docs, usando o `glossario_acumulado.json` existente.
4. **[Status] Resumo Geral da Monografia:** Exibe uma tabela consolidada com o total de erros e alertas encontrados em cada relatório gerado até o momento.

## Regras de Execução em Lote (Opção 1):
- A execução dos capítulos DEVE ser estritamente sequencial (01 -> 02 -> 03...) para garantir que o glossário acumulado receba os termos na ordem cronológica correta.
- Ao final, exiba um sumário executivo com os bloqueadores de cada capítulo.