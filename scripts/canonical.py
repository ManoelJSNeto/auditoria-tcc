import hashlib
import re
import sys
from pathlib import Path

def canonicalize(text: str) -> str:
    # 1. Remove marcações de formatação Markdown para isolar o texto puro
    clean = re.sub(r'[#*_`~>\[\]()|\-+]', '', text)
    # 2. Converte tudo para minúsculas
    clean = clean.lower()
    # 3. Colapsa múltiplos espaços, quebras de linha e tabs em um único espaço
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

def compute_hash(text: str) -> str:
    canon = canonicalize(text)
    return hashlib.sha256(canon.encode('utf-8')).hexdigest()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python scripts/canonical.py <caminho_do_arquivo.md>")
        sys.exit(1)
        
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"Erro: Arquivo '{file_path}' nao encontrado.")
        sys.exit(1)
        
    content = file_path.read_text(encoding='utf-8')
    print(compute_hash(content))