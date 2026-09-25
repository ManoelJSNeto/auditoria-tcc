"""
Pipeline: document-sanitizer  +  document-splitter
Executa as Skills 00 e 01 em um único passo.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

# ─────────────────────────────────────────
# Paths
# ─────────────────────────────────────────
BASE         = Path(__file__).resolve().parent.parent
INPUT_FILE   = BASE / "input" / "TCC_Infraestrutura_Em_Nuvem.md"
OUT_SANITIZED = BASE / "docs" / "tcc_sanitizado.md"
OUT_MANIFEST  = BASE / "docs" / "manifest_integridade.json"
CAPITULOS_DIR = BASE / "docs" / "capitulos"
OUT_GLOSSARIO = BASE / "docs" / "glossario_acumulado.json"

# ─────────────────────────────────────────
# Shared canonical hash (same logic as canonical.py)
# ─────────────────────────────────────────
def canonicalize(text: str) -> str:
    clean = re.sub(r'[#*_`~>\[\]()|\-+]', '', text)
    clean = clean.lower()
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

def compute_hash(text: str) -> str:
    return hashlib.sha256(canonicalize(text).encode('utf-8')).hexdigest()

# ─────────────────────────────────────────
# SKILL 00 – document-sanitizer
# ─────────────────────────────────────────
def sanitize(raw: str) -> str:
    # 1. Normaliza quebras de linha
    text = raw.replace('\r\n', '\n').replace('\r', '\n')
    # 2. Artefatos Unicode
    text = text.replace('\ufeff', '')   # BOM
    text = text.replace('\u200b', '')   # zero-width space
    text = text.replace('\u00ad', '')   # soft hyphen
    text = text.replace('\u00a0', ' ')  # non-breaking space → espaço ASCII
    # 3. Limita saltos consecutivos a dois
    text = re.sub(r'\n{3,}', '\n\n', text)
    # 4. Cabeçalhos: garante exatamente um espaço após #
    text = re.sub(r'^(#{1,6})\s+', r'\1 ', text, flags=re.MULTILINE)
    # 5. Elimina espaços/tabs no final de cada linha
    text = re.sub(r'[ \t]+$', '', text, flags=re.MULTILINE)
    return text

# ─────────────────────────────────────────
# SKILL 01 – document-splitter  (divisão)
# ─────────────────────────────────────────
# Mapeamento: padrão de título (regex, case-insensitive) → nome do arquivo de saída
# O padrão bate na linha inteira (que pode ser "1. # **TITULO** {#ancora}")
CHAPTER_MAP = [
    (r'INTRODU',     '01_introducao.md'),
    (r'JUSTIFICATIVA','01_introducao.md'),
    (r'PERGUNTA',    '01_introducao.md'),
    (r'REVIS',       '02_referencial_teorico.md'),
    (r'BIBLIOGR',    '02_referencial_teorico.md'),
    (r'MATERIAIS',   '03_metodologia_estudo_de_caso.md'),
    (r'M.TODOS',     '03_metodologia_estudo_de_caso.md'),
    (r'RESULTADOS',  '04_resultados_discussao.md'),
    (r'DISCUSS',     '04_resultados_discussao.md'),
    (r'CONSIDERA',   '05_conclusao.md'),
    (r'CONCLUS',     '05_conclusao.md'),
    (r'REFER',       'referencias.md'),
]

def split_document(sanitized: str):
    """
    Divide o documento sanitizado em fatias por cabeçalho H1.
    Suporta tanto `# TITULO` quanto `1. # TITULO` (listas numeradas com H1 inline).
    Retorna dict {nome_arquivo: conteúdo}.
    """
    lines = sanitized.splitlines(keepends=True)

    # Padrão: linha que é H1 puro OU lista numerada com H1 inline
    # Ex: "# INTRODUÇÃO", "1. # **INTRODUÇÃO** {#introdução}"
    H1_PATTERN = re.compile(r'^(?:\d+\.\s+)?# ')

    # Identifica os índices de cada cabeçalho H1
    h1_indices = []
    for i, line in enumerate(lines):
        if H1_PATTERN.match(line):
            h1_indices.append(i)

    if not h1_indices:
        print("AVISO: Nenhum cabeçalho H1 encontrado. Verifique o arquivo sanitizado.")
        sys.exit(1)

    # Pré-textuais: tudo antes do primeiro H1
    pre_textuais = ''.join(lines[:h1_indices[0]])

    # Fatias por H1
    slices = {}
    for idx, start in enumerate(h1_indices):
        end = h1_indices[idx + 1] if idx + 1 < len(h1_indices) else len(lines)
        chunk = ''.join(lines[start:end])
        title_line = lines[start].strip()

        # Determina nome de arquivo baseado no título
        target = None
        for pattern, fname in CHAPTER_MAP:
            if re.search(pattern, title_line, re.IGNORECASE):
                target = fname
                break
        if target is None:
            # fallback genérico
            slug = re.sub(r'[^a-z0-9]+', '_', title_line.lower())[:40]
            target = f'misc_{slug}.md'

        if target in slices:
            slices[target] += chunk
        else:
            slices[target] = chunk

    result = {'00_pre_textuais.md': pre_textuais}
    result.update(slices)
    return result

# ─────────────────────────────────────────
# SKILL 01 – validação de integridade
# ─────────────────────────────────────────
ORDERED_FILES = [
    '00_pre_textuais.md',
    '01_introducao.md',
    '02_referencial_teorico.md',
    '03_metodologia_estudo_de_caso.md',
    '04_resultados_discussao.md',
    '05_conclusao.md',
    'referencias.md',
]

def validate_integrity(slices: dict, original_hash: str) -> bool:
    # Concatena na ordem canônica
    concatenated = ''
    for fname in ORDERED_FILES:
        if fname in slices:
            concatenated += slices[fname]
    # Arquivos extras não previstos na ordem
    for fname, content in slices.items():
        if fname not in ORDERED_FILES:
            concatenated += content

    new_hash = compute_hash(concatenated)
    print(f"\n  Hash original   : {original_hash}")
    print(f"  Hash recalculado: {new_hash}")
    return new_hash == original_hash

# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────
def main():
    print("=" * 60)
    print("SKILL 00 — document-sanitizer")
    print("=" * 60)

    raw = INPUT_FILE.read_text(encoding='utf-8')
    sanitized = sanitize(raw)

    OUT_SANITIZED.parent.mkdir(parents=True, exist_ok=True)
    OUT_SANITIZED.write_text(sanitized, encoding='utf-8')
    print(f"✔ Sanitizado gravado em: {OUT_SANITIZED}")

    original_hash = compute_hash(sanitized)
    manifest = {
        "hash_canonico_original": original_hash,
        "status": "sanitizado"
    }
    OUT_MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding='utf-8')
    print(f"✔ Manifesto gravado em : {OUT_MANIFEST}")
    print(f"  Hash canônico        : {original_hash}")

    print()
    print("=" * 60)
    print("SKILL 01 — document-splitter")
    print("=" * 60)

    slices = split_document(sanitized)

    CAPITULOS_DIR.mkdir(parents=True, exist_ok=True)
    for fname, content in slices.items():
        dest = CAPITULOS_DIR / fname
        dest.write_text(content, encoding='utf-8')
        lines = content.count('\n')
        print(f"  ✔ {fname}  ({lines} linhas)")

    print("\nValidando integridade via hash canônico...")
    ok = validate_integrity(slices, original_hash)
    if ok:
        print("  ✅ INTEGRIDADE CONFIRMADA — hashes idênticos.")
    else:
        print("  ❌ DIVERGÊNCIA DE HASH DETECTADA — abortando.")
        # Identifica onde houve divergência
        for fname, content in slices.items():
            h = compute_hash(content)
            print(f"     {fname}: {h}")
        sys.exit(2)

    # Inicializa glossário
    OUT_GLOSSARIO.write_text(
        json.dumps({"siglas": {}, "conceitos": {}}, indent=2, ensure_ascii=False),
        encoding='utf-8'
    )
    print(f"\n✔ Glossário inicializado em: {OUT_GLOSSARIO}")
    print("\nPipeline concluído com sucesso.")

if __name__ == "__main__":
    main()
