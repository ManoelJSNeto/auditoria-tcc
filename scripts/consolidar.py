#!/usr/bin/env python3
"""
scripts/consolidar.py
Compila todos os relatórios em reports/audit_*.md em um único CHECKLIST_MESTRE.md.
Não requer dependências externas (Python standard library pura).
"""

import re
from pathlib import Path

def parse_audit_report(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    lines = content.splitlines()
    
    cap_match = re.search(r"Capítulo\s+([0-9]{2})|audit_([0-9]{2})", file_path.name, re.IGNORECASE)
    cap_num = cap_match.group(1) or cap_match.group(2) if cap_match else file_path.stem
    
    items = []
    in_table = False
    headers = []
    
    for line in lines:
        line_str = line.strip()
        if line_str.startswith("|") and line_str.endswith("|"):
            cols = [c.strip() for c in line_str.split("|")[1:-1]]
            
            # Linha divisória de tabela
            if cols and all(re.match(r"^:?-+:?$", c) for c in cols):
                in_table = True
                continue
            
            if not in_table:
                headers = [h.lower() for h in cols]
            else:
                # Linha de dados da tabela
                if len(cols) >= 3:
                    localizador = cols[0]
                    # Identifica a coluna de ação / correção
                    acao = cols[-1] if len(cols) >= 3 else cols[1]
                    
                    # Ignora se for indicação de item já correto
                    if "correto" in acao.lower() or "nenhuma ação" in acao.lower():
                        continue
                    
                    tipo = cols[1] if len(cols) >= 4 else "Pendente"
                    items.append({
                        "capitulo": cap_num,
                        "localizador": localizador,
                        "tipo": tipo,
                        "acao": acao
                    })
        else:
            in_table = False

    return items

def categorizar_item(item):
    acao_lower = item["acao"].lower()
    tipo_lower = item["tipo"].lower()
    
    if any(k in acao_lower or k in tipo_lower for k in ["caixa", "grafia", "padronizar", "remover", "link", "hífen", "sigla", "acrônimo"]):
        return "rapidas"
    elif any(k in acao_lower or k in tipo_lower for k in ["referencia", "referência", "bibliografia", "abnt", "autor"]):
        return "bibliografia"
    else:
        return "conteudo"

def main():
    root = Path(__file__).resolve().parent.parent
    reports_dir = root / "reports"
    output_file = root / "CHECKLIST_MESTRE.md"

    if not reports_dir.exists():
        print("[ERRO] Pasta 'reports/' não encontrada.")
        return

    reports = sorted(list(reports_dir.glob("audit_*.md")))
    if not reports:
        print("[AVISO] Nenhum relatório audit_*.md encontrado em reports/.")
        return

    todos_itens = []
    for rep in reports:
        todos_itens.extend(parse_audit_report(rep))

    rapidas = []
    bibliografia = []
    conteudo = []

    for item in todos_itens:
        cat = categorizar_item(item)
        texto_item = f"- [ ] **Cap. {item['capitulo']} ({item['localizador']}):** {item['acao']}"
        if cat == "rapidas":
            rapidas.append(texto_item)
        elif cat == "bibliografia":
            bibliografia.append(texto_item)
        else:
            conteudo.append(texto_item)

    saida = [
        "# 📋 CHECKLIST MESTRE DE CORREÇÃO DO TCC",
        "",
        "> Este arquivo reúne todas as pendências detectadas nos relatórios individuais da pasta `reports/`.",
        "> Abra o seu documento no Google Docs e marque com `[x]` conforme for corrigindo.",
        "",
        f"**Total de apontamentos mapeados:** {len(todos_itens)}",
        "",
        "---",
        "",
        "## 🟢 1. Correções Rápidas de Ctrl+F (Formatação, Siglas e Erros Formais)",
        "> Ajustes sintáticos e remoções pontuais.",
        ""
    ]
    saida.extend(rapidas if rapidas else ["- [x] Nenhuma pendência rápida encontrada."])

    saida.extend([
        "",
        "---",
        "",
        "## 🟡 2. Ajustes Bibliográficos e Referências",
        "> Inclusão ou ajuste de autores, anos e normas de citação.",
        ""
    ])
    saida.extend(bibliografia if bibliografia else ["- [x] Nenhuma pendência bibliográfica encontrada."])

    saida.extend([
        "",
        "---",
        "",
        "## 🔴 3. Lacunas de Conteúdo e Sustentação Teórica",
        "> Afirmações sem fonte, descrição de artefato ou escrita de seções pendentes.",
        ""
    ])
    saida.extend(conteudo if conteudo else ["- [x] Nenhuma lacuna de conteúdo encontrada."])

    output_file.write_text("\n".join(saida), encoding="utf-8")
    print(f"[SUCESSO] Checklist mestre gerado em: {output_file.name} com {len(todos_itens)} itens.")

if __name__ == "__main__":
    main()