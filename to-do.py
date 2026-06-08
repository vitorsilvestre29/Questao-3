#!/usr/bin/env python3
"""
To-Do CLI — Gerenciador de tarefas via linha de comando.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

DATA_FILE = Path("tasks.json")

def load() -> dict:
    """Carrega o arquivo de dados. Cria estrutura inicial se não existir."""
    if not DATA_FILE.exists():
        return {"next_id": 1, "tasks": []}
    try:
        with DATA_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
        # Garante campos obrigatórios caso o arquivo esteja incompleto
        data.setdefault("next_id", 1)
        data.setdefault("tasks", [])
        return data
    except (json.JSONDecodeError, ValueError):
        print("Erro: arquivo tasks.json corrompido. Iniciando com dados vazios.")
        return {"next_id": 1, "tasks": []}


def save(data: dict) -> None:
    """Persiste os dados no arquivo JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def cmd_add(args: argparse.Namespace) -> None:
    """Adiciona uma nova tarefa."""
    title = args.title.strip()

    # RN-05: título não pode ser vazio
    if not title:
        print("Erro: o título da tarefa não pode ser vazio.")
        sys.exit(1)

    if len(title) > 200:
        print("Erro: o título não pode ter mais de 200 caracteres.")
        sys.exit(1)

    data = load()
    task = {
        "id": data["next_id"],
        "title": title,
        "done": False,
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }
    data["tasks"].append(task)
    data["next_id"] += 1
    save(data)

    print(f"✅ Tarefa #{task['id']} adicionada: \"{task['title']}\"")


def cmd_list(args: argparse.Namespace) -> None:
    """Lista as tarefas com filtro opcional."""
    data = load()
    tasks = data["tasks"]

    # Filtros
    if getattr(args, "pending", False):
        tasks = [t for t in tasks if not t["done"]]
    elif getattr(args, "done", False):
        tasks = [t for t in tasks if t["done"]]

    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return

    # Cabeçalho
    print(f"\n{'ID':<5} {'Status':<8} {'Criada em':<22} Título")
    print("─" * 70)

    for t in tasks:
        status = "✓ feita" if t["done"] else "✗ pendente"
        created = _format_date(t["created_at"])
        print(f"#{t['id']:<4} {status:<8} {created:<22} {t['title']}")

    total = len(data["tasks"])
    done = sum(1 for t in data["tasks"] if t["done"])
    print(f"\n{done}/{total} concluída(s)\n")


def cmd_toggle(args: argparse.Namespace) -> None:
    """Inverte o status de conclusão de uma tarefa (RN-04)."""
    data = load()
    task = next((t for t in data["tasks"] if t["id"] == args.id), None)

    # RN-06: ID inexistente
    if task is None:
        print(f"Erro: tarefa #{args.id} não encontrada.")
        sys.exit(1)

    task["done"] = not task["done"]
    save(data)

    novo_status = "concluída ✓" if task["done"] else "pendente ✗"
    print(f"Tarefa #{task['id']} marcada como {novo_status}: \"{task['title']}\"")


def _format_date(iso: str) -> str:
    """Formata ISO 8601 para DD/MM/YYYY HH:MM."""
    try:
        dt = datetime.fromisoformat(iso)
        return dt.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return iso


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="todo",
        description="📋 To-Do CLI — gerencie suas tarefas no terminal.",
    )
    sub = parser.add_subparsers(dest="command", metavar="<comando>")
    sub.required = True

    # add
    p_add = sub.add_parser("add", help="Adiciona uma nova tarefa")
    p_add.add_argument("title", help="Título da tarefa (entre aspas)")
    p_add.set_defaults(func=cmd_add)

    # list
    p_list = sub.add_parser("list", help="Lista as tarefas")
    group = p_list.add_mutually_exclusive_group()
    group.add_argument("--pending", action="store_true", help="Apenas pendentes")
    group.add_argument("--done", action="store_true", help="Apenas concluídas")
    p_list.set_defaults(func=cmd_list)

    # toggle
    p_toggle = sub.add_parser("toggle", help="Marca/desmarca tarefa como concluída")
    p_toggle.add_argument("id", type=int, help="ID da tarefa")
    p_toggle.set_defaults(func=cmd_toggle)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()