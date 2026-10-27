"""Genera los adaptadores de herramientas a partir de los playbooks de dev/.

Uso:
    python -I scripts/adapters/generate.py --target RAIZ --adapters claude,cursor [--yes]

RAIZ es la raíz del repo (modo A) o del workspace (modo B): la carpeta que contiene dev/.
Fuente única de verdad: dev/method/playbooks/*.md. Los adaptadores NO duplican su
contenido; solo llevan name/description y mandan leer el playbook.

- claude: .claude/skills/dev-<name>/SKILL.md, .claude/rules/dev-*.md (con paths:) y
          dev/.adapters/{session-start.py,settings-snippet.json} (hook opcional).
- cursor: .cursor/rules/dev-*.mdc (AGENTS.md siempre; cada playbook "Apply Intelligently").

Idempotente: regenera lo que lleva la marca de generado, elimina lo generado que ya no
corresponde a un playbook y no pisa archivos sin marca salvo --yes (sin terminal interactiva
y sin --yes, los omite). Solo usa la biblioteca estándar.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

MARKER = "<!-- dev-guidelines:generated -->"
PLAYBOOKS_REL = "dev/method/playbooks"
HERE = Path(__file__).resolve().parent

RULE_PATHS: dict[str, list[str]] = {
    "update-docs": ["dev/docs/**"],
    "fix-bug": ["dev/work/bugs/**"],
    "write-task": ["dev/work/tasks/**"],
    "write-report": ["dev/work/reports/**", "dev/work/changelogs/**"],
    "record-decision": ["dev/docs/decisions/**"],
}

FRONT_RE = re.compile(r"\A---\r?\n(.*?)\r?\n---\r?\n", re.S)


def parse_frontmatter(text: str) -> dict[str, str]:
    """Lee name/description de un frontmatter YAML simple (claves de una línea o `>` plegado)."""
    m = FRONT_RE.match(text)
    if not m:
        return {}
    data: dict[str, str] = {}
    key: str | None = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            if val in (">", "|", ">-", "|-"):
                val = ""
            data[key] = val.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def load_playbooks(target: Path) -> dict[str, str]:
    """Devuelve {name: description} de los playbooks válidos."""
    base = target / PLAYBOOKS_REL
    out: dict[str, str] = {}
    if not base.is_dir():
        return out
    for path in sorted(base.glob("*.md")):
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
        name, desc = fm.get("name", ""), fm.get("description", "")
        if name != path.stem or not desc:
            print(f"· omitido {path.name}: frontmatter name/description inválido", file=sys.stderr)
            continue
        out[name] = desc
    return out


class Writer:
    """Escribe archivos generados respetando la política de no pisar."""

    def __init__(self, yes: bool) -> None:
        self.yes = yes
        self.written = 0
        self.unchanged = 0
        self.skipped: list[Path] = []

    def _may_overwrite(self, path: Path) -> bool:
        if not path.exists():
            return True
        if MARKER in path.read_text(encoding="utf-8", errors="replace"):
            return True
        if self.yes:
            return True
        if sys.stdin.isatty():
            try:
                reply = input(f"{path} existe y no fue generado por el paquete. ¿Sobrescribir? [s/N] ")
            except EOFError:
                return False
            return reply.strip().lower() in ("s", "y")
        return False

    def write(self, path: Path, content: str) -> None:
        if not self._may_overwrite(path):
            self.skipped.append(path)
            return
        if path.exists() and path.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n") == content:
            self.unchanged += 1
            return
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        self.written += 1


def prune(base: Path, pattern: str, keep: set[str]) -> int:
    """Elimina lo generado (con marca) que ya no corresponde a ningún playbook."""
    removed = 0
    if not base.is_dir():
        return removed
    for item in sorted(base.glob(pattern)):
        marker_file = item / "SKILL.md" if item.is_dir() else item
        if not marker_file.is_file() or MARKER not in marker_file.read_text(encoding="utf-8", errors="replace"):
            continue
        if item.name in keep:
            continue
        shutil.rmtree(item) if item.is_dir() else item.unlink()
        removed += 1
    return removed


def one_line(text: str) -> str:
    return text.replace('"', "'").replace("\n", " ").strip()


def gen_claude(target: Path, books: dict[str, str], w: Writer) -> int:
    skills = target / ".claude" / "skills"
    rules = target / ".claude" / "rules"
    for name, desc in books.items():
        body = (
            f"---\nname: dev-{name}\ndescription: {one_line(desc)}\n---\n{MARKER}\n\n"
            f"Lee `{PLAYBOOKS_REL}/{name}.md` y sigue sus pasos. Es la única fuente de las reglas;\n"
            f"esta skill no las duplica. Si no puedes leerlo, avisa al desarrollador.\n"
        )
        w.write(skills / f"dev-{name}" / "SKILL.md", body)
    removed = prune(skills, "dev-*", {f"dev-{n}" for n in books})
    keep_rules = set()
    for name, paths in RULE_PATHS.items():
        if name not in books:
            continue
        keep_rules.add(f"dev-{name}.md")
        listed = "\n".join(f'  - "{p}"' for p in paths)
        body = (
            f"---\npaths:\n{listed}\n---\n{MARKER}\n\n"
            f"Al trabajar en estos archivos, sigue `{PLAYBOOKS_REL}/{name}.md` "
            f"(skill `dev-{name}`).\n"
        )
        w.write(rules / f"dev-{name}.md", body)
    removed += prune(rules, "dev-*.md", keep_rules)
    agents = target / ".claude" / "agents"
    keep_agents = set()
    if "diagnose" in books:
        keep_agents.add("dev-doctor.md")
        w.write(
            agents / "dev-doctor.md",
            f"---\nname: dev-doctor\ndescription: {one_line(books['diagnose'])}\n"
            f"tools: Read, Grep, Glob, Bash\n---\n{MARKER}\n\n"
            f"Eres el doctor de dev/. Lee `{PLAYBOOKS_REL}/diagnose.md` y sigue sus pasos.\n"
            "Solo lees y propones: no edites archivos. Devuelve el informe del §4 y nada más.\n",
        )
    removed += prune(agents, "dev-*.md", keep_agents)
    adapters_dir = target / "dev" / ".adapters"
    for fname in ("session-start.py", "settings-snippet.json"):
        shutil.copyfile(HERE / "claude" / "hooks" / fname, _ensure(adapters_dir / fname))
    return removed


def _ensure(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def gen_cursor(target: Path, books: dict[str, str], w: Writer) -> int:
    base = target / ".cursor" / "rules"
    w.write(
        base / "dev-agents.mdc",
        f"---\ndescription: Protocolo de desarrollo agéntico del proyecto\nalwaysApply: true\n---\n{MARKER}\n\n"
        "Lee `dev/AGENTS.md` al empezar y sigue sus reglas.\n",
    )
    for name, desc in books.items():
        w.write(
            base / f"dev-{name}.mdc",
            f"---\ndescription: {one_line(desc)}\nalwaysApply: false\n---\n{MARKER}\n\n"
            f"Lee `{PLAYBOOKS_REL}/{name}.md` y sigue sus pasos (única fuente de las reglas).\n",
        )
    return prune(base, "dev-*.mdc", {"dev-agents.mdc"} | {f"dev-{n}.mdc" for n in books})


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=True, help="raíz del repo o workspace (contiene dev/)")
    ap.add_argument("--adapters", default="", help="lista separada por comas: claude,cursor")
    ap.add_argument("--yes", action="store_true", help="sobrescribe archivos sin marca de generado")
    args = ap.parse_args(argv)

    target = Path(args.target).resolve()
    chosen = [a.strip() for a in args.adapters.split(",") if a.strip()]
    unknown = [a for a in chosen if a not in ("claude", "cursor")]
    if unknown or not chosen:
        print(f"Adaptadores inválidos o vacíos: {unknown or chosen} (usa claude,cursor)", file=sys.stderr)
        return 2
    books = load_playbooks(target)
    if not books:
        print(f"No hay playbooks en {target / PLAYBOOKS_REL}", file=sys.stderr)
        return 2

    w = Writer(args.yes)
    removed = 0
    if "claude" in chosen:
        removed += gen_claude(target, books, w)
    if "cursor" in chosen:
        removed += gen_cursor(target, books, w)
    print(f"Adaptadores {','.join(chosen)}: {w.written} escritos, {w.unchanged} sin cambios, {removed} obsoletos eliminados, {len(books)} playbooks.")
    for p in w.skipped:
        print(f"· omitido (existe sin marca; usa --yes para sobrescribir): {p}")
    if "claude" in chosen:
        print(
            "\nHook SessionStart (opcional, NO activado): copia el fragmento de "
            f"{target / 'dev' / '.adapters' / 'settings-snippet.json'} a tu .claude/settings.json "
            "(ajusta python/python3)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
