"""Verificador de estructura y consistencia de una carpeta dev/.

Uso:
    python -I scripts/check.py [RUTA_A_DEV] [--strict] [--json]

--json: imprime el resultado como JSON ({root, errors, warnings, counts}) en lugar de texto.
Sin argumento busca ./dev y, si no existe, usa el directorio actual si contiene AGENTS.md.
--strict: los TODO literales de PROJECT.md/COMANDOS.md y los excesos de presupuesto de tokens pasan de aviso a error.
Código de salida: 0 sin errores (puede haber advertencias), 1 con errores, 2 uso incorrecto.
Solo usa la biblioteca estándar.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_FILES = [
    "AGENTS.md",
    "PROJECT.md",
    "INDEX.md",
    "docs/README.md",
]
# Archivos que el instalador crea pero que una instalación anterior a 0.5.0 no tiene: mensaje propio.
MIGRATED_FILES = {
    "COMANDOS.md": "falta COMANDOS.md (stacks, comandos y commits, desde 0.5.0): actualiza con dev-update",
}
REQUIRED_PLAYBOOKS = (
    "start-session",
    "close-session",
    "write-task",
    "write-report",
    "update-docs",
    "fix-bug",
    "commit-pr",
    "develop-code",
    "record-decision",
    "diagnose",
)
AGENTS_MAX_LINES = 60
PLAYBOOK_MAX_LINES = 120
PLAYBOOK_TOC_LINES = 100
DESCRIPTION_MAX = 300
RETRO_COLUMNS = ("fecha", "task o bug", "qué funcionó", "qué falló o sobró", "qué cambiarías", "estado")
RETRO_STATES = ("pendiente", "propuesta", "enviada", "descartada")
GENERATED_MARKER = "dev-guidelines:generated"
REQUIRED_DIRS = ["work", "work/tasks", "work/bugs", "work/reports", "work/changelogs", "docs", "docs/decisions", "method", "method/playbooks", "method/templates"]
SUBTASK_STATES = ("pendiente", "en curso", "hecha")
SKIP_LINK_DIRS = {"method/templates"}
SKIP_LINK_FILES = {"docs/_page-template.md"}
ALIAS_SCAN_DIRS = ("work", "docs")
DATED_DIRS = ("work/reports", "work/changelogs", "docs")
OLD_STRUCTURE_MSG = "estructura anterior a 0.6.0 (guidelines/, templates/, tasks/… en la raíz de dev/): migra con dev-update"
FENCE_RE = re.compile(r"^(```|~~~)")
LINK_RE = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
ALIAS_RE = re.compile(r"(?<![\w@.\-/])@([a-z][\w\-]*)/")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
IGNORED_ALIASES = {"repo", "alias", "main-ejemplo"}


class Report:
    """Acumula errores y advertencias."""

    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, where: str, msg: str) -> None:
        self.errors.append(f"ERROR  {where}: {msg}")

    def warn(self, where: str, msg: str) -> None:
        self.warnings.append(f"AVISO  {where}: {msg}")


def slugify(heading: str) -> str:
    """Convierte un encabezado en el ancla estilo GitHub."""
    text = re.sub(r"`", "", heading.strip().lower())
    text = re.sub(r"[^\w\s\-]", "", text, flags=re.UNICODE)
    return re.sub(r"\s", "-", text)


def strip_fences(text: str) -> list[tuple[int, str]]:
    """Devuelve (nº de línea, línea) fuera de bloques de código."""
    out: list[tuple[int, str]] = []
    in_fence = False
    for n, line in enumerate(text.splitlines(), 1):
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            continue
        if not in_fence:
            out.append((n, line))
    return out


def headings(path: Path, cache: dict[Path, set[str]]) -> set[str]:
    if path not in cache:
        slugs: set[str] = set()
        for _, line in strip_fences(path.read_text(encoding="utf-8")):
            m = HEADING_RE.match(line)
            if m:
                slugs.add(slugify(m.group(2)))
        cache[path] = slugs
    return cache[path]


def md_files(root: Path) -> list[Path]:
    return sorted(p for p in root.rglob("*.md") if ".git" not in p.parts and ".backup" not in p.parts)


def old_structure(root: Path) -> bool:
    """Árbol anterior a 0.6.0: guidelines/ o tasks/ en la raíz de dev/ y sin method/."""
    return ((root / "guidelines").exists() or (root / "tasks").exists()) and not (root / "method").exists()


def check_structure(root: Path, rep: Report) -> None:
    if old_structure(root):
        rep.error("dev/", OLD_STRUCTURE_MSG)
        return
    for rel in REQUIRED_FILES:
        if not (root / rel).is_file():
            rep.error(rel, "falta el archivo")
    for rel, msg in MIGRATED_FILES.items():
        if not (root / rel).is_file():
            rep.error(rel, msg)
    project = root / "PROJECT.md"
    if project.is_file():
        old = [m.group(2) for _, line in strip_fences(project.read_text(encoding="utf-8")) if (m := HEADING_RE.match(line))
               and re.search(r"stacks activos|comandos del proyecto|modelos sugeridos", m.group(2), re.I)]
        if old:
            rep.error("PROJECT.md", f"formato anterior a 0.5.0 (secciones «{old[0]}»…): migra con dev-update; stacks, comandos y commits pasan a COMANDOS.md")
    for rel in REQUIRED_DIRS:
        if not (root / rel).is_dir():
            rep.error(rel + "/", "falta la carpeta")
    if (root / "work" / "tasks").is_dir() and not (root / "work" / "tasks" / "archive").is_dir():
        rep.warn("work/tasks/archive/", "falta la carpeta de tasks cerradas")
    if not (root / "DEV-PROFILE.md").is_file():
        rep.warn("DEV-PROFILE.md", "no existe (es opcional): el agente usará valores por defecto")
    if not (root / ".package-version").is_file():
        rep.warn(".package-version", "no existe (instalación manual)")


def check_numbering(root: Path, rep: Report) -> None:
    for folder, prefix in (("work/tasks", "task"), ("work/bugs", "bug")):
        base = root / folder
        if not base.is_dir():
            continue
        seen: dict[int, str] = {}
        children = [p for p in base.iterdir() if p.is_dir() and p.name != "archive"]
        archive = base / "archive"
        if archive.is_dir():
            children += [p for p in archive.iterdir() if p.is_dir()]
        for d in sorted(children):
            where = d.relative_to(root).as_posix()
            m = re.match(rf"^{prefix}-(\d+)-[\w\-]+$", d.name)
            if not m:
                rep.error(where, f"nombre inválido, se espera {prefix}-N-nombre")
                continue
            n = int(m.group(1))
            if n in seen:
                rep.error(where, f"número {n} repetido con {seen[n]}")
            seen[n] = d.name
            if not (d / "README.md").is_file():
                rep.error(where, "falta README.md")
            subs: dict[int, str] = {}
            for f in sorted(d.glob("*.md")):
                if f.name in ("README.md", "decisions.md"):
                    continue
                sm = re.match(r"^subtask-(\d+)-[\w\-]+\.md$", f.name)
                if not sm:
                    rep.warn(f"{where}/{f.name}", "no sigue el nombre subtask-N-descripcion.md")
                    continue
                sn = int(sm.group(1))
                if sn in subs:
                    rep.error(f"{where}/{f.name}", f"subtask {sn} repetida con {subs[sn]}")
                subs[sn] = f.name
            if prefix == "task" and not (d / "decisions.md").is_file():
                rep.warn(where, "falta decisions.md")


def check_index(root: Path, rep: Report) -> None:
    index = root / "INDEX.md"
    if not index.is_file():
        return
    text = index.read_text(encoding="utf-8")
    warned: set[str] = set()
    for folder, prefix in (("work/tasks", "task"), ("work/bugs", "bug")):
        base = root / folder
        if not base.is_dir():
            continue
        for d in sorted(p for p in base.iterdir() if p.is_dir()):
            m = re.match(rf"^({prefix}-\d+)-", d.name)
            if m and m.group(1) not in warned and not re.search(rf"(?<![\w-]){m.group(1)}(?![\w]|-\d)", text):
                warned.add(m.group(1))
                rep.warn("INDEX.md", f"{m.group(1)} existe en {folder}/ pero no aparece en el índice")


def parse_aliases(root: Path, rep: Report) -> dict[str, str]:
    project = root / "PROJECT.md"
    aliases: dict[str, str] = {}
    if not project.is_file():
        return aliases
    in_section = False
    for _, line in strip_fences(project.read_text(encoding="utf-8")):
        m = HEADING_RE.match(line)
        if m:
            in_section = "repos y alias" in m.group(2).lower()
            continue
        if in_section and line.startswith("|"):
            cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
            if len(cells) >= 2 and cells[0].startswith("@") and len(cells[0]) > 1:
                aliases[cells[0][1:]] = cells[1]
    if not aliases:
        rep.error("PROJECT.md", "§1 no declara ningún alias @repo")
    for name, rel in aliases.items():
        if rel.upper() == "TODO" or rel in ("", "—", "-"):
            continue
        if not (root / rel).resolve().exists():
            rep.warn("PROJECT.md", f"el alias @{name} apunta a '{rel}', que no existe desde dev/")
    return aliases


def check_links(root: Path, rep: Report) -> None:
    cache: dict[Path, set[str]] = {}
    for path in md_files(root):
        rel = path.relative_to(root).as_posix()
        if any(rel.startswith(d + "/") for d in SKIP_LINK_DIRS) or rel in SKIP_LINK_FILES:
            continue
        text = path.read_text(encoding="utf-8")
        for n, line in strip_fences(text):
            line = re.sub(r"`[^`]*`", "", line)
            for m in LINK_RE.finditer(line):
                target = m.group(1)
                if re.match(r"^(https?:|mailto:|@)", target) or target.startswith("<"):
                    continue
                file_part, _, anchor = target.partition("#")
                dest = path if not file_part else (path.parent / file_part).resolve()
                if not dest.exists():
                    rep.error(f"{rel}:{n}", f"enlace roto → {target}")
                    continue
                if anchor and dest.suffix == ".md" and dest.is_file():
                    if anchor.lower() not in headings(dest, cache):
                        rep.warn(f"{rel}:{n}", f"ancla no encontrada → {target}")


def check_aliases(root: Path, aliases: dict[str, str], rep: Report) -> None:
    for folder in ALIAS_SCAN_DIRS:
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(root).as_posix()
            if rel in SKIP_LINK_FILES:
                continue
            for n, line in strip_fences(path.read_text(encoding="utf-8")):
                for m in ALIAS_RE.finditer(line):
                    name = m.group(1)
                    if name not in aliases and name not in IGNORED_ALIASES:
                        rep.error(f"{rel}:{n}", f"alias @{name}/ no declarado en PROJECT.md §1")


def check_subtask_states(root: Path, rep: Report) -> None:
    for folder in ("work/tasks", "work/bugs"):
        base = root / folder
        if not base.is_dir():
            continue
        for readme in sorted(list(base.glob("*/README.md")) + list(base.glob("archive/*/README.md"))):
            rel = readme.relative_to(root).as_posix()
            for n, line in strip_fences(readme.read_text(encoding="utf-8")):
                if not line.startswith("|") or "subtask-" not in line:
                    continue
                cells = [c.strip() for c in line.strip().strip("|").split("|")]
                state = cells[-1].strip("`*_ ").lower()
                if state.startswith("<!--"):
                    continue
                if not any(state == s or state.startswith(s + " (") for s in SUBTASK_STATES):
                    rep.error(f"{rel}:{n}", f"estado de subtask inválido: '{cells[-1]}'")


def check_retro(root: Path, rep: Report) -> None:
    """Comprobación suave de RETRO.md (aviso, nunca error): columnas esperadas y estados válidos."""
    path = root / "RETRO.md"
    if not path.is_file():
        return
    header: list[str] | None = None
    for n, line in strip_fences(path.read_text(encoding="utf-8")):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if header is None:
            header = [c.lower() for c in cells]
            if tuple(header) != RETRO_COLUMNS:
                rep.warn(f"RETRO.md:{n}", "columnas distintas de: " + " | ".join(RETRO_COLUMNS))
                return
            continue
        if all(set(c) <= set("-: ") for c in cells):
            continue
        state = cells[-1].strip("`*_ ").lower()
        if state in ("", "—", "-") or any(state == s or state.startswith(s + " (") for s in RETRO_STATES):
            continue
        rep.warn(f"RETRO.md:{n}", f"estado de retro inválido: '{cells[-1]}' (usa {', '.join(RETRO_STATES)})")
    if header is None:
        rep.warn("RETRO.md", "sin tabla de entradas")


def check_todos(root: Path, rep: Report, strict: bool = False) -> None:
    """Avisa de `TODO` literales (las plantillas usan `—` para «sin definir», no TODO)."""
    for name, severity in (("PROJECT.md", "error" if strict else "warn"), ("COMANDOS.md", "error" if strict else "warn"), ("DEV-PROFILE.md", "warn")):
        path = root / name
        if not path.is_file():
            continue
        lines = [n for n, line in strip_fences(path.read_text(encoding="utf-8")) if re.search(r"\bTODO\b", re.sub(r"`[^`]*`", "", line))]
        if lines:
            msg = f"{len(lines)} TODO literales en líneas {', '.join(map(str, lines[:8]))}{'…' if len(lines) > 8 else ''}: cámbialos por «—» si el dato no está definido"
            (rep.error if severity == "error" else rep.warn)(name, msg)


def frontmatter(text: str) -> dict[str, str]:
    """Lee name/description de un frontmatter YAML simple (una línea o `>` plegado)."""
    m = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    data: dict[str, str] = {}
    if not m:
        return data
    key: str | None = None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if km:
            key, val = km.group(1), km.group(2).strip()
            data[key] = "" if val in (">", "|", ">-", "|-") else val.strip("\"'")
        elif key and line.startswith((" ", "\t")):
            data[key] = (data[key] + " " + line.strip()).strip()
    return data


def budget(rep: Report, strict: bool, where: str, msg: str) -> None:
    """Exceso de presupuesto de tokens: aviso, o error con --strict."""
    (rep.error if strict else rep.warn)(where, msg)


def md_links(text: str) -> list[str]:
    """Destinos .md relativos de los enlaces fuera de bloques de código."""
    out: list[str] = []
    for _, line in strip_fences(text):
        for m in LINK_RE.finditer(re.sub(r"`[^`]*`", "", line)):
            target = m.group(1).partition("#")[0]
            if target.endswith(".md") and not re.match(r"^(https?:|@)", target):
                out.append(target)
    return out


def check_depth(root: Path, playbook: Path, rep: Report) -> None:
    """Avisa si un playbook enlaza a una referencia de apoyo que a su vez encadena a otra.

    Solo cuentan las referencias de method/ que no son playbooks ni plantillas (stacks, etc.): enlazar
    de un playbook a otro («siguiente paso») o de una plantilla a otra no es una cadena de lectura.
    """
    method = (root / "method").resolve()
    playbooks = playbook.parent.resolve()
    templates = (root / "method" / "templates").resolve()

    def is_reference(p: Path) -> bool:
        return p.is_file() and method in p.parents and playbooks not in p.parents and templates not in p.parents

    me = playbook.resolve()
    for target in md_links(playbook.read_text(encoding="utf-8")):
        dest = (playbook.parent / target).resolve()
        if not is_reference(dest) or dest == me:
            continue
        for inner in md_links(dest.read_text(encoding="utf-8")):
            d2 = (dest.parent / inner).resolve()
            if is_reference(d2) and d2 != dest:
                rep.warn(playbook.relative_to(root).as_posix(), f"enlaza a {dest.name}, que enlaza a {d2.name}: más de un nivel de profundidad")
                return


def check_budget(root: Path, rep: Report, strict: bool) -> None:
    agents = root / "AGENTS.md"
    if agents.is_file():
        n = len(agents.read_text(encoding="utf-8").splitlines())
        if n > AGENTS_MAX_LINES:
            budget(rep, strict, "AGENTS.md", f"{n} líneas (máximo {AGENTS_MAX_LINES}): debe ser un enrutador corto")
    pb = root / "method" / "playbooks"
    if not pb.is_dir():
        return
    for name in REQUIRED_PLAYBOOKS:
        if not (pb / f"{name}.md").is_file():
            rep.error(f"method/playbooks/{name}.md", "falta el playbook")
    for path in sorted(pb.glob("*.md")):
        rel = path.relative_to(root).as_posix()
        text = path.read_text(encoding="utf-8")
        n = len(text.splitlines())
        fm = frontmatter(text)
        if fm.get("name") != path.stem:
            rep.error(rel, f"frontmatter 'name' debe ser '{path.stem}' (es '{fm.get('name', '')}')")
        desc = fm.get("description", "")
        if not desc:
            rep.error(rel, "falta 'description' en el frontmatter")
        elif len(desc) > DESCRIPTION_MAX:
            rep.error(rel, f"'description' de {len(desc)} caracteres (máximo {DESCRIPTION_MAX})")
        if n > PLAYBOOK_MAX_LINES:
            budget(rep, strict, rel, f"{n} líneas (máximo {PLAYBOOK_MAX_LINES})")
        if n > PLAYBOOK_TOC_LINES and not re.search(r"^#{2,3}\s+(contenido|índice|indice)\b", text, re.M | re.I):
            rep.warn(rel, f"más de {PLAYBOOK_TOC_LINES} líneas sin índice (## Contenido)")
        check_depth(root, path, rep)


def check_adapters(root: Path, rep: Report) -> None:
    """Los adaptadores generados deben apuntar a playbooks que existen."""
    top = root.parent
    pb = root / "method" / "playbooks"
    for pat in (".claude/skills/dev-*/SKILL.md", ".claude/rules/dev-*.md", ".claude/agents/dev-*.md", ".cursor/rules/dev-*.mdc"):
        for path in sorted(top.glob(pat)):
            text = path.read_text(encoding="utf-8", errors="replace")
            if GENERATED_MARKER not in text:
                continue
            for name in re.findall(r"playbooks/([\w\-]+)\.md", text):
                if not (pb / f"{name}.md").is_file():
                    rep.error(path.relative_to(top).as_posix(), f"apunta al playbook inexistente '{name}' (regenera con el instalador)")


def check_archive(root: Path, rep: Report) -> None:
    """El inicio de sesión no referencia archive/; las tasks archivadas están cerradas."""
    texts: list[tuple[str, str]] = []
    for rel in ("AGENTS.md", "method/playbooks/start-session.md"):
        f = root / rel
        if f.is_file():
            texts.append((rel, f.read_text(encoding="utf-8")))
    index = root / "INDEX.md"
    if index.is_file():
        active: list[str] = []
        grab = False
        for line in index.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                grab = "activo ahora" in line.lower()
            elif grab:
                active.append(line)
        texts.append(("INDEX.md (Activo ahora)", "\n".join(active)))
    for where, text in texts:
        if re.search(r"\]\([^)]*(tasks|bugs)/archive/", text):
            rep.warn(where, "enlaza a archive/: el inicio de sesión no debe leer tasks cerradas")
    for folder in ("work/tasks", "work/bugs"):
        arch = root / folder / "archive"
        if not arch.is_dir():
            continue
        for d in sorted(p for p in arch.iterdir() if p.is_dir()):
            readme = d / "README.md"
            if not readme.is_file():
                rep.error(d.relative_to(root).as_posix(), "task archivada sin README.md")
                continue
            states = []
            for _, line in strip_fences(readme.read_text(encoding="utf-8")):
                if line.startswith("|") and "subtask-" in line:
                    states.append([c.strip() for c in line.strip().strip("|").split("|")][-1].strip("`*_ ").lower())
            pending = [x for x in states if not x.startswith("hecha")]
            if pending:
                rep.warn(readme.relative_to(root).as_posix(), f"task archivada con {len(pending)} subtasks no hechas")


def check_dates_and_index(root: Path, rep: Report) -> None:
    for folder in DATED_DIRS:
        base = root / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.md")):
            rel = path.relative_to(root).as_posix()
            if path.name in ("README.md", "_page-template.md", "glossary.md"):
                continue
            text = path.read_text(encoding="utf-8")
            head = "\n".join(text.splitlines()[:15]).lower()
            if "fecha" not in head and "date" not in head:
                rep.warn(rel, "sin fecha al inicio")
            if len(text.splitlines()) > 40 and not re.search(r"^#{2,3}\s+(contenido|índice|indice)\b", text, re.M | re.I):
                rep.warn(rel, "documento largo sin índice (## Contenido)")


def resolve_root(argv: list[str]) -> Path | None:
    args = [a for a in argv if not a.startswith("--")]
    if args:
        return Path(args[0]).resolve()
    for cand in (Path("dev"), Path(".")):
        if (cand / "AGENTS.md").is_file():
            return cand.resolve()
    return None


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if "-h" in argv or "--help" in argv:
        print(__doc__)
        return 0
    root = resolve_root(argv)
    if root is None or not root.is_dir():
        print("Uso: python -I scripts/check.py [RUTA_A_DEV]", file=sys.stderr)
        return 2
    rep = Report()
    check_structure(root, rep)
    if old_structure(root):
        return finish(root, rep, argv)
    check_numbering(root, rep)
    check_index(root, rep)
    aliases = parse_aliases(root, rep)
    check_links(root, rep)
    check_aliases(root, aliases, rep)
    check_subtask_states(root, rep)
    strict = "--strict" in argv
    check_todos(root, rep, strict=strict)
    check_budget(root, rep, strict)
    check_adapters(root, rep)
    check_archive(root, rep)
    check_dates_and_index(root, rep)
    check_retro(root, rep)
    return finish(root, rep, argv)


def finish(root: Path, rep: Report, argv: list[str]) -> int:
    if "--json" in argv:
        print(json.dumps({
            "root": str(root),
            "errors": [split_finding(x) for x in rep.errors],
            "warnings": [split_finding(x) for x in rep.warnings],
            "counts": {"errors": len(rep.errors), "warnings": len(rep.warnings)},
        }, ensure_ascii=False, indent=2))
        return 1 if rep.errors else 0
    print(f"Verificando {root}")
    for line in rep.errors + rep.warnings:
        print(line)
    print(f"\n{len(rep.errors)} errores, {len(rep.warnings)} avisos")
    return 1 if rep.errors else 0


def split_finding(line: str) -> dict[str, str]:
    """Convierte «ERROR  donde: mensaje» en {where, msg}."""
    _, _, rest = line.partition("  ")
    where, _, msg = rest.partition(": ")
    return {"where": where, "msg": msg}


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
