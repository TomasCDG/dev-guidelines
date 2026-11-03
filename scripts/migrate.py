"""Migra una carpeta dev/ a la estructura actual: 0.5.0 -> 0.6.0 (work/, docs/decisions/, method/) y
0.7.x -> 0.8.0 (config/, e INDEX.md y RETRO.md dentro de work/).

Uso:
    python -I scripts/migrate.py --target DIR_DEV [--dry-run]

  --target   la carpeta dev/ del proyecto (la que contiene AGENTS.md), no la raíz del repo.
  --dry-run  imprime los movimientos y cuántos enlaces se reescribirían; no escribe nada.

Mapa de rutas (antiguo -> nuevo, relativo a dev/):
  0.6.0
    tasks/ bugs/ reports/ changelogs/  ->  work/tasks/ work/bugs/ work/reports/ work/changelogs/
    decisions/                         ->  docs/decisions/
    guidelines/README.md               ->  method/README.md
    guidelines/playbooks/ stacks/      ->  method/playbooks/ method/stacks/
    templates/                         ->  method/templates/
  0.8.0
    PROJECT.md COMANDOS.md DEV-PROFILE.md  ->  config/PROJECT.md config/COMANDOS.md config/DEV-PROFILE.md
    INDEX.md RETRO.md                      ->  work/INDEX.md work/RETRO.md

Qué hace, en este orden:
  1. Detecta qué migraciones faltan: las que tienen algún origen del mapa en dev/. Si no falta ninguna,
     lo dice y sale con 0. Las pendientes se aplican juntas, en una sola pasada (sus rutas no se solapan).
     Si el destino de un movimiento ya existe con contenido, se detiene sin mover nada.
  2. Calcula, antes de tocar nada, los enlaces Markdown relativos `[texto](ruta#ancla)` que cambian:
     resuelve cada uno contra la ubicación ANTIGUA del archivo, mapea el destino antiguo -> nuevo y
     recalcula la ruta relativa desde la ubicación NUEVA del archivo. Las anclas se conservan; los
     enlaces externos, las anclas puras y los alias `@repo/` no se tocan; los enlaces cuyo destino no
     existía se dejan como están y se listan. Los bloques de código y el código en línea se ignoran.
  3. Respalda en dev/.backup/<fecha>-migracion-<versión>/ el contenido original de los archivos que se
     reescriben.
  4. Mueve carpetas y archivos (git mv si dev/ es un repo git; shutil.move si no, o si git no lo sigue).
  5. Escribe los archivos reescritos en su ubicación nueva y traslada las rutas del manifiesto.

No reescribe AGENTS.md ni lo que pasa a method/: son del paquete, no se editan, y así el instalador
(`scripts/install.py --yes`) los reconoce como intactos y los actualiza sin respaldos innecesarios; lo que
hayas editado a mano de ahí lo respalda él. Las rutas citadas en prosa o entre acentos graves
(`tasks/...`, `PROJECT.md` §3) no se tocan: revísalas en work/INDEX.md y config/PROJECT.md.

Código de salida: 0 correcto (o ya migrada), 1 algo no se pudo hacer, 2 uso incorrecto.
Solo usa la biblioteca estándar.
"""

from __future__ import annotations

import argparse
import datetime
import posixpath
import re
import shutil
import subprocess
import sys
from pathlib import Path

# Por versión, (antiguo, nuevo): se aplican por prefijo de ruta. Orígenes y destinos no se solapan entre
# versiones, así que las migraciones pendientes se aplican juntas.
MIGRATIONS = (
    ("0.6.0", (
        ("tasks", "work/tasks"),
        ("bugs", "work/bugs"),
        ("reports", "work/reports"),
        ("changelogs", "work/changelogs"),
        ("decisions", "docs/decisions"),
        ("guidelines/README.md", "method/README.md"),
        ("guidelines/playbooks", "method/playbooks"),
        ("guidelines/stacks", "method/stacks"),
        ("templates", "method/templates"),
    )),
    ("0.8.0", (
        ("PROJECT.md", "config/PROJECT.md"),
        ("COMANDOS.md", "config/COMANDOS.md"),
        ("DEV-PROFILE.md", "config/DEV-PROFILE.md"),
        ("INDEX.md", "work/INDEX.md"),
        ("RETRO.md", "work/RETRO.md"),
    )),
)
Moves = tuple[tuple[str, str], ...]
MANAGED_NEW = ("AGENTS.md", "method")
SKIP_DIRS = {".backup", ".git", ".tools", "node_modules", "__pycache__"}
FENCE_RE = re.compile(r"^(```|~~~)")
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
CODE_SPAN_RE = re.compile(r"(`[^`]*`)")
EXTERNAL_RE = re.compile(r"^(https?:|mailto:|@|#|<)|://")
FAKE_ROOT = "/R/R/R/R/R/R/R/dev"  # profundidad suficiente para resolver «..» sin salir del árbol


def old_to_new(rel: str, moves: Moves) -> str:
    """Ruta antigua (relativa a dev/, con `/`) -> ruta nueva. Lo que no se mueve queda igual."""
    for old, new in moves:
        if rel == old or rel.startswith(old + "/"):
            return new + rel[len(old):]
    return rel


def has_files(path: Path) -> bool:
    return path.is_dir() and any(p.is_file() for p in path.rglob("*"))


def pending(dev: Path) -> tuple[list[str], Moves]:
    """Versiones con migración pendiente y sus movimientos (solo los orígenes que existen en dev/)."""
    versions: list[str] = []
    moves: list[tuple[str, str]] = []
    for version, table in MIGRATIONS:
        found = [(old, new) for old, new in table if (dev / old).exists()]
        if found:
            versions.append(version)
            moves += found
    return versions, tuple(moves)


def conflicts(dev: Path, moves: Moves) -> list[str]:
    """Destinos que ya existen con contenido (una carpeta vacía de una ejecución anterior no cuenta)."""
    return [f"{new} ya existe (origen: {old})" for old, new in moves if (dev / new).is_file() or has_files(dev / new)]


def is_managed_new(rel: str) -> bool:
    return rel == "AGENTS.md" or rel == "method" or rel.startswith("method/")


def rewrite_text(text: str, old_rel: str, new_rel: str, dev: Path, moves: Moves, missing: list[str]) -> tuple[str, int, int]:
    """Reescribe los enlaces de un archivo. Devuelve (texto nuevo, enlaces cambiados, enlaces sin cambio)."""
    old_parent = posixpath.dirname(old_rel)
    new_parent = posixpath.dirname(new_rel)
    changed = 0
    kept = 0
    in_fence = False
    out_lines: list[str] = []
    for n, line in enumerate(text.split("\n"), 1):
        if FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            out_lines.append(line)
            continue
        if in_fence:
            out_lines.append(line)
            continue
        parts = CODE_SPAN_RE.split(line)
        for i in range(0, len(parts), 2):  # los impares son código en línea
            def repl(m: re.Match[str]) -> str:
                nonlocal changed, kept
                target = m.group(1)
                if EXTERNAL_RE.search(target):
                    return m.group(0)
                file_part, hash_, anchor = target.partition("#")
                if not file_part or "%" in file_part:
                    return m.group(0)
                dest_old = posixpath.normpath(posixpath.join(old_parent, file_part))
                inside = not (dest_old == ".." or dest_old.startswith("../"))
                if inside and not (dev / dest_old).exists():
                    missing.append(f"{old_rel}:{n}: {target}")
                    return m.group(0)
                dest_new = old_to_new(dest_old, moves) if inside else dest_old
                abs_dest = posixpath.normpath(posixpath.join(FAKE_ROOT, dest_new))
                abs_start = posixpath.normpath(posixpath.join(FAKE_ROOT, new_parent))
                rel_new = posixpath.relpath(abs_dest, abs_start)
                if posixpath.normpath(file_part) == rel_new:
                    kept += 1
                    return m.group(0)
                if file_part.endswith("/"):
                    rel_new += "/"
                if file_part.startswith("./") and not rel_new.startswith("../"):
                    rel_new = "./" + rel_new
                changed += 1
                new_target = rel_new + hash_ + anchor
                return m.group(0).replace(target, new_target, 1)

            parts[i] = LINK_RE.sub(repl, parts[i])
        out_lines.append("".join(parts))
    return "\n".join(out_lines), changed, kept


def plan_rewrites(dev: Path, moves: Moves) -> tuple[list[tuple[str, str, str, int]], int, list[str]]:
    """Calcula los archivos a reescribir: [(ruta antigua, ruta nueva, texto nuevo, enlaces cambiados)]."""
    plan: list[tuple[str, str, str, int]] = []
    missing: list[str] = []
    kept_total = 0
    for f in sorted(dev.rglob("*.md")):
        rel_parts = f.relative_to(dev).parts
        if any(p in SKIP_DIRS for p in rel_parts):
            continue
        old_rel = "/".join(rel_parts)
        new_rel = old_to_new(old_rel, moves)
        if is_managed_new(new_rel):
            continue
        text = f.read_bytes().decode("utf-8")
        new_text, changed, kept = rewrite_text(text, old_rel, new_rel, dev, moves, missing)
        kept_total += kept
        if changed:
            plan.append((old_rel, new_rel, new_text, changed))
    return plan, kept_total, missing


def unique_backup(dev: Path, today: str, version: str) -> Path:
    base = dev / ".backup" / f"{today}-migracion-{version}"
    cand, n = base, 2
    while cand.exists():
        cand = base.with_name(f"{base.name}-{n}")
        n += 1
    return cand


def do_move(dev: Path, old: str, new: str, use_git: bool) -> str:
    src, dst = dev / old, dev / new
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_dir() and not has_files(dst):
        shutil.rmtree(dst)  # carpeta vacía de una ejecución anterior: se reemplaza
    if use_git:
        r = subprocess.run(["git", "-C", str(dev), "mv", old, new], capture_output=True, text=True)
        if r.returncode == 0:
            return "git mv"
    shutil.move(str(src), str(dst))
    return "mover"


def migrate_manifest(dev: Path, moves: Moves) -> int:
    """Traslada las rutas del manifiesto previo al mapa nuevo (los hashes no cambian)."""
    path = dev / ".package-manifest"
    if not path.is_file():
        return 0
    lines = path.read_text(encoding="utf-8").splitlines()
    out: list[str] = []
    n = 0
    for line in lines:
        digest, sep, rel = line.partition("  ")
        if sep and rel.strip():
            new = old_to_new(rel.strip(), moves)
            n += new != rel.strip()
            out.append(f"{digest}  {new}")
        else:
            out.append(line)
    out.sort(key=lambda x: x.partition("  ")[2])
    path.write_text("\n".join(out) + "\n", encoding="utf-8", newline="\n")
    return n


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--target", required=False)
    ap.add_argument("--dry-run", action="store_true")
    try:
        args = ap.parse_args(argv)
    except SystemExit as e:
        return 0 if e.code == 0 else 2
    if not args.target:
        print("Uso: python -I scripts/migrate.py --target DIR_DEV [--dry-run]", file=sys.stderr)
        return 2
    dev = Path(args.target).resolve()
    if not dev.is_dir() or not (dev / "AGENTS.md").is_file():
        print(f"{dev} no es una carpeta dev/ (falta AGENTS.md): indica la carpeta dev/, no la raíz del repo.", file=sys.stderr)
        return 2

    versions, moves = pending(dev)
    if not versions:
        if (dev / "method").exists():
            print(f"{dev} ya tiene la estructura actual: no hay nada que migrar.")
            return 0
        print(f"No se reconoce la estructura de {dev}: no hay guidelines/, tasks/ ni method/. No se hace nada.", file=sys.stderr)
        return 2
    clash = conflicts(dev, moves)
    if clash:
        print("No se mueve nada porque el destino ya tiene contenido (estado mixto: revisa a mano cuál es el vigente):", file=sys.stderr)
        for c in clash:
            print(f"  {c}", file=sys.stderr)
        return 1

    plan, kept, missing = plan_rewrites(dev, moves)
    links = sum(p[3] for p in plan)
    use_git = (dev / ".git").exists()
    today = datetime.date.today().isoformat()
    tag = "plan (--dry-run, no se escribe nada)" if args.dry_run else "migración"
    print(f"dev-guidelines migrate: {tag}")
    print(f"Destino: {dev}  ({'repo git: git mv' if use_git else 'sin repo git: mover'})")
    print(f"Migraciones: {', '.join(versions)}")
    print(f"Movimientos: {len(moves)}")
    for old, new in moves:
        print(f"  {old} -> {new}")
    print(f"Archivos con enlaces a reescribir: {len(plan)} ({links} enlaces; {kept} enlaces ya correctos)")
    for old_rel, new_rel, _, n in plan:
        print(f"  {old_rel}" + (f" (-> {new_rel})" if new_rel != old_rel else "") + f": {n}")
    print(f"Enlaces con destino inexistente (se dejan igual): {len(missing)}")
    for m in missing:
        print(f"  {m}")
    if args.dry_run:
        print(f"\nCopia previa que se haría: .backup/{today}-migracion-{versions[-1]}/ ({len(plan)} archivos).")
        return 0

    failures = 0
    backup = unique_backup(dev, today, versions[-1])
    for old_rel, _, _, _ in plan:
        out = backup / old_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dev / old_rel, out)
    manifest = dev / ".package-manifest"
    if manifest.is_file():
        backup.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(manifest, backup / ".package-manifest")
    if plan or manifest.is_file():
        print(f"\nCopia previa en {backup}")

    for old, new in moves:
        try:
            how = do_move(dev, old, new, use_git)
            print(f"  [{how}] {old} -> {new}")
        except OSError as e:
            failures += 1
            print(f"  ERROR moviendo {old} -> {new}: {e}", file=sys.stderr)
    if failures:
        print(f"\n{failures} movimientos fallaron: no se reescribió ningún enlace. Hay copia previa en {backup}.", file=sys.stderr)
        return 1

    for _, new_rel, text, _ in plan:
        try:
            (dev / new_rel).write_text(text, encoding="utf-8", newline="")
        except OSError as e:
            failures += 1
            print(f"  ERROR escribiendo {new_rel}: {e}", file=sys.stderr)
    moved_keys = migrate_manifest(dev, moves)

    leftovers = [p.relative_to(dev).as_posix() for p in sorted((dev / "guidelines").rglob("*")) if p.is_file()] if (dev / "guidelines").is_dir() else []
    if (dev / "guidelines").is_dir() and not leftovers:
        shutil.rmtree(dev / "guidelines")
    print(f"\nMigrado: {len(moves)} movimientos, {links} enlaces reescritos en {len(plan)} archivos, "
          f"{moved_keys} rutas del manifiesto trasladadas.")
    if leftovers:
        print("Quedan en guidelines/ archivos que no son del paquete (no se tocan):")
        for rel in leftovers:
            print(f"  {rel}")
    if missing:
        print(f"{len(missing)} enlaces apuntaban a destinos inexistentes y se dejaron igual (listados arriba).")
    print("\nSiguiente: python -I scripts/install.py --yes (actualiza method/ y AGENTS.md; respalda lo que editaste), "
          "revisa las rutas citadas en prosa en work/INDEX.md y config/PROJECT.md, y ejecuta: python -I dev/.tools/check.py dev")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
