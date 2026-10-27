"""Hook SessionStart opcional de Claude Code para dev-guidelines.

Imprime como contexto adicional (en forma de hechos, < 2000 caracteres) la sección
«Activo ahora» de dev/INDEX.md y avisa solo si falta PROJECT.md o COMANDOS.md, o si
quedan `TODO` literales (un `—` significa «sin definir» y no se avisa).
No bloquea ni falla: ante cualquier problema no imprime nada.

Matcher recomendado: startup|resume|compact. Solo usa la biblioteca estándar.
Uso: python session-start.py [RUTA_A_DEV]
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

LIMIT = 1800


def find_dev(argv: list[str]) -> Path | None:
    if argv:
        return Path(argv[0])
    for base in (os.environ.get("CLAUDE_PROJECT_DIR"), os.getcwd()):
        if base and (Path(base) / "dev" / "INDEX.md").is_file():
            return Path(base) / "dev"
    return None


def section(text: str, title_part: str) -> str:
    """Devuelve el cuerpo de la sección `## ...` cuyo título contiene title_part."""
    lines = text.splitlines()
    out: list[str] = []
    inside = False
    for line in lines:
        if line.startswith("## "):
            if inside:
                break
            inside = title_part in line.lower()
            continue
        if inside:
            out.append(line)
    return "\n".join(out).strip()


def count_todos(path: Path) -> int | None:
    if not path.is_file():
        return None
    in_fence = False
    total = 0
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
        elif not in_fence and re.search(r"\bTODO\b", re.sub(r"`[^`]*`", "", line)):
            total += 1
    return total


def build(dev: Path) -> str:
    facts: list[str] = []
    index = dev / "INDEX.md"
    if index.is_file():
        active = section(index.read_text(encoding="utf-8", errors="replace"), "activo ahora")
        rows = [r for r in active.splitlines() if r.startswith("|") and not re.match(r"^\|[\s\-|]+\|$", r)]
        facts.append("Estado activo (dev/INDEX.md):")
        facts.extend(rows[1:] if len(rows) > 1 else rows)
    for name in ("PROJECT.md", "COMANDOS.md"):
        if not (dev / name).is_file():
            facts.append(f"{name}: no existe" + (" (actualiza con dev-update)." if name == "COMANDOS.md" else "."))
    for name in ("PROJECT.md", "COMANDOS.md", "DEV-PROFILE.md"):
        todos = count_todos(dev / name)
        if todos:
            facts.append(f"{name}: {todos} líneas con TODO literal (cámbialas por «—» si no hay dato).")
    facts.append("Protocolo: dev/AGENTS.md y dev/method/playbooks/start-session.md.")
    return "\n".join(facts)[:LIMIT]


def main(argv: list[str]) -> int:
    try:
        dev = find_dev(argv)
        if dev is None:
            return 0
        text = build(dev)
        payload = {"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": text}}
        sys.stdout.reconfigure(encoding="utf-8") if hasattr(sys.stdout, "reconfigure") else None
        print(json.dumps(payload, ensure_ascii=False))
    except Exception:  # el hook nunca debe romper el arranque de la sesión
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
