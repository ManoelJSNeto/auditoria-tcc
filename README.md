# 🎓 Auditoria-TCC: Esteira Modular de Auditoria Acadêmica

> **Pipeline determinístico de auditoria para TCCs e monografias.** Garante integridade matemática (zero perda de dados via SHA-256), modularidade de capítulos contra o problema de *Lost-in-the-Middle* de LLMs e conformidade com normas ABNT, sem nunca alterar a voz autoral do pesquisador.

---

### 📋 Metadados do Repositório (GitHub About)
* **Descrição Curta:** Pipeline modular de auditoria acadêmica para TCCs e monografias usando agentes de IA e garantia matemática de integridade (SHA-256). Validação estrita de normas ABNT, cruzamento bibliográfico e gestão cumulativa de contexto.
* **Tags / Topics:** `tcc`, `abnt`, `academic-audit`, `llm-pipeline`, `python`, `antigravity`, `sha256-integrity`, `linter-academico`, `markdown`

---

## 📌 O Que É e Por Que Este Projeto Existe?

Submeter um TCC inteiro (30 a 80+ páginas) diretamente em um único prompt de IA quase sempre gera falhas metodológicas críticas:

1. **Janela de Contexto Diluída (*Lost-in-the-Middle*):** Modelos ignoram inconsistências no miolo do trabalho e focam apenas no início e no fim.
2. **Alucinação Bibliográfica:** IAs instruídas a "revisar e arrumar" costumam inventar dados, anos e autores fictícios.
3. **Perda da Voz Autoral:** Ao pedir para a IA reescrever trechos, ela simplifica conceitos técnicos avançados e introduz riscos de plágio sutil.
4. **Falsos Alarmes de Siglas:** Como a IA não mantém memória leve entre prompts, acusa termos já explicados nos primeiros capítulos como "conceitos não definidos".

O **Auditoria-TCC** resolve isso tratando a monografia como um pipeline de software: os dados são higienizados, passam por checagem criptográfica de integridade, são divididos em capítulos atômicos e auditados de forma estritamente diagnóstica — **a IA aponta as falhas em relatórios acionáveis, e você mantém 100% do controle sobre a escrita.**

---

## 🏗️ Como a Esteira Funciona

```text
[ Google Docs / Word ] 
          │
          │ (Exportar em Markdown .md)
          ▼
   input/raw_tcc.md
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 00. Document Sanitizer                                      │
│ - Remove lixo invisível (BOM, zero-width space, nbsp)       │
│ - Gera a "impressão digital" canônica SHA-256              │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 01. Document Splitter                                       │
│ - Segmenta em docs/capitulos/ (01, 02, ..., referencias.md)  │
│ - Recalcula o SHA-256 canônico e valida: ZERO perda de dados│
│ - Inicializa o docs/glossario_acumulado.json                │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│ 02. Academic Auditor (Capítulo a Capítulo)                  │
│ - Rigor máximo em fundamentação teórica                     │
│ - Tolerância contextual em metodologia/código próprio       │
│ - Checagem ABNT NBR 10520 / 6023 (caixa alta, apud, anos)   │
│ - Alimenta e reutiliza o glossário cumulativo               │
└─────────────────────────────────────────────────────────────┘
          │
          ▼
   reports/audit_cap_XX.md
   (Tabelas: "O que está faltando" e "O que está errado")
```

---

## 📂 Estrutura de Pastas

```text
auditoria-tcc/
├── .antigravity/
│   └── skills/
│       ├── 00_document-sanitizer.md      # Protocolo de higienização
│       ├── 01_document-splitter.md       # Protocolo de fatiamento atômico
│       ├── 02_academic-auditor.md        # Protocolo de auditoria ABNT e fontes
│       └── pipeline-runner.md            # Orquestrador mestre interativo
├── scripts/
│   └── canonical.py                      # Motor matemático de integridade SHA-256
├── input/
│   └── raw_tcc.md                        # Onde você coloca seu TCC bruto
├── docs/
│   ├── tcc_sanitizado.md                 # Texto higienizado
│   ├── manifest_integridade.json         # Registro do hash original
│   ├── glossario_acumulado.json          # Memória leve de siglas e conceitos
│   └── capitulos/                        # Capítulos fatiados (01, 02, ..., referencias)
└── reports/                              # Relatórios executivos gerados
    ├── audit_01_introducao.md
    ├── audit_02_referencial_teorico.md
    └── ...
```

---

## 🚀 Instalação e Pré-requisitos

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/auditoria-tcc.git](https://github.com/seu-usuario/auditoria-tcc.git)
   cd auditoria-tcc
   ```

2. **Requisitos:**
   * Python 3.10+ instalado no sistema.
   * Não requer bibliotecas externas (`pip install` desnecessário — utiliza apenas a biblioteca padrão: `hashlib`, `re`, `sys`, `pathlib`).

3. **Verifique se o motor de hash está operacional:**
   ```bash
   python scripts/canonical.py scripts/canonical.py
   ```
   *(Deve retornar um hash hexadecimal de 64 caracteres).*

---

## 📖 Passo a Passo: Como Usar

### 1. Preparar a Entrada
1. No seu **Google Docs**, clique em: **Arquivo > Fazer o download > Formato Markdown (.md)**.
2. Salve o arquivo baixado como:
   ```text
   input/raw_tcc.md
   ```

### 2. Disparar a Esteira Automatizada
No assistente de IA configurado no seu workspace (Antigravity, Claude Desktop, Kiro ou Codex), basta enviar o gatilho:

```text
menu de auditoria
```
*(ou simplesmente: `rodar esteira`)*

A IA exibirá o menu:
* **[1] Completo:** Sanitiza, fatia e roda a auditoria em todos os capítulos em sequência, acumulando o glossário.
* **[2] Rápido:** Apenas limpa o arquivo, divide os capítulos e valida o hash.
* **[3] Focado:** Permite escolher um capítulo específico para reauditar após uma alteração.
* **[4] Status:** Exibe uma tabela consolidada com o panorama geral de pendências.

### 3. Aplicar as Correções
1. Abra a pasta `reports/` e visualize os arquivos gerados (ex: `audit_02_referencial_teorico.md`).
2. Mantenha o relatório aberto em um lado da tela e o Google Docs no outro.
3. Utilize os trechos exatos apontados na tabela para dar `Ctrl + F`, corrigir os desvios normativos e preencher as fontes faltantes.

---

## 💡 Dicas de Prompts para Diferentes Ferramentas

Se você não estiver usando o Antigravity e quiser rodar este pipeline em outros assistentes (como Claude Web, ChatGPT ou Kiro), utilize os templates abaixo:

### Prompt 1: Auditoria em Lote (Claude Projects ou Web)
> Anexe `referencias.md`, `glossario_acumulado.json` e o capítulo desejado (ex: `02_referencial_teorico.md`).  
> **Comando:**  
> *"Atue como um auditor acadêmico rigoroso com base nas normas ABNT NBR 10520 e NBR 6023. Analise o capítulo anexo cruzando cada citação com o arquivo `referencias.md` (aplicando a regra de apud). Verifique no `glossario_acumulado.json` se as siglas utilizadas já foram explicadas anteriormente. Não reescreva o texto sob hipótese alguma. Gere uma tabela dividida estritamente em: (1) O que está faltando (afirmações sem fontes, siglas soltas, referências ausentes) e (2) O que está errado (erros de caixa alta em parênteses, divergências de datas, inconsistências estruturais)."*

### Prompt 2: Reauditoria Focada após Correção
> *"Acabei de aplicar correções pontuais no arquivo `docs/capitulos/03_metodologia_estudo_de_caso.md`. Reexecute a auditoria apenas neste capítulo, aplicando tolerância contextual para decisões de arquitetura e métricas empíricas próprias, e me diga se todas as pendências da tabela anterior foram saneadas."*

---

## 🛡️ O Que a Auditoria Verifica?

| Categoria | Regra Analisada | Exemplo de Falha Detectada |
| :--- | :--- | :--- |
| **Sintaxe ABNT** | NBR 10520 (Autor-Data) | `(Engemon, 2026)` → Deve ser caixa alta: `(ENGEMON, 2026)`. |
| **Regra de *Apud*** | NBR 10520 | `Silva (2015, apud Souza, 2020)` → Valida apenas `SOUZA` em referências. |
| **Ambiguidade de Ano** | NBR 6023 | Múltiplas obras do mesmo autor no mesmo ano → Exige `AWS (2026a)` e `AWS (2026b)`. |
| **Embasamento Crítico** | Rigor Epistemológico | Dados quantitativos ou princípios de engenharia soltos sem whitepaper/artigo atrelado. |
| **Tolerância Contextual** | Escopo de Engenharia | Não cobra fontes externas para código próprio, schemas de banco ou rotas de API. |
| **Artefatos de Modelo** | Limpeza Editorial | Detecta textos residuais esquecidos de templates de instituições (ex: Etec, Fatec). |

---

## ⚖️ Licença
Distribuído sob a licença MIT. Consulte `LICENSE` para mais informações.