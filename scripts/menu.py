import os
import subprocess
import sys
from pathlib import Path

def print_header():
    print("\n" + "="*50)
    print("      ESTEIRA DE AUDITORIA TCC - PECUARIA-GEST")
    print("="*50)

def menu():
    while True:
        print_header()
        print("1. Sanitizar e Fatiar (Skill 00 + Skill 01)")
        print("2. Ver Status de Integridade (Hash SHA-256)")
        print("3. Limpar Relatórios Antigos")
        print("4. Sair")
        print("-" * 50)
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            print("\nExecutando sanitizacao e fatiamento...")
            # Roda o script de integridade diretamente
            res = subprocess.run([sys.executable, "scripts/canonical.py", "input/raw_tcc.md"], capture_output=True, text=True)
            print(f"Hash do arquivo de entrada: {res.stdout.strip()}")
            print(">> Agora peca no Antigravity: 'Execute a opcao 1 do pipeline-runner'")
        elif opcao == "2":
            manifest = Path("docs/manifest_integridade.json")
            if manifest.exists():
                print(f"\nManifesto atual:\n{manifest.read_text(encoding='utf-8')}")
            else:
                print("\nManifesto ainda nao gerado.")
        elif opcao == "3":
            reports = list(Path("reports").glob("*.md"))
            for r in reports:
                r.unlink()
            print(f"\n{len(reports)} relatorios removidos.")
        elif opcao == "4":
            print("\nSaindo...")
            break
        else:
            print("\nOpcao invalida!")

if __name__ == "__main__":
    menu()