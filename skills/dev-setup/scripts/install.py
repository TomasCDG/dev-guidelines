"""Instala (o actualiza) dev-template/ como dev/ en un proyecto y verifica el resultado.

Uso:
    python -I scripts/install.py --mode A|B --target DIR [--yes] [--git-init] [--adapters claude,cursor]
    python -I scripts/install.py --status --target DIR
    python -I scripts/install.py --dry-run --target DIR [--mode A|B] [--adapters claude,cursor]

  --mode A    dev/ dentro del repo (se excluye con .git/info/exclude)
  --mode B    dev/ junto a varios repos, dentro de un workspace (su propio repo git)
  --target    raíz del repo (modo A) o del workspace (modo B). Por defecto, el directorio actual.
  --yes       confirma sin preguntar (también actualiza una instalación existente)
  --git-init  modo B: ejecuta `git init` en dev/ si aún no es un repo
  --adapters  claude (skills, reglas, agente dev-doctor, hook opcional) y/o cursor (.cursor/rules).
              Por defecto ninguno; en una actualización se regeneran los ya instalados.
  --dry-run   no escribe nada: imprime el plan (versión instalada -> nueva; archivos del paquete
              nuevos, cambiados, sin cambios y editados por ti que se respaldarían; archivos de
              usuario que faltan y se crearían; adaptadores que se regenerarían).
  --status    imprime una línea `instalada=X nueva=Y estado=al-día|desactualizada|sin-instalar`
              (código 0) y no hace nada más.

La versión del paquete sale de release/VERSION (raíz del paquete) o de assets/VERSION (bundle de la skill).

Si dev/ ya existe no se sobrescribe nada sin confirmar. En una actualización solo se reemplazan
los archivos del paquete (AGENTS.md, method/, .tools/); PROJECT.md, COMANDOS.md, DEV-PROFILE.md,
INDEX.md, RETRO.md, docs/ (incluye docs/decisions/) y work/ (tasks, bugs, reports, changelogs) solo se crean
si faltan. Si dev/ tiene la estructura anterior a 0.6.0 (guidelines/, templates/ o tasks/ en su raíz y
sin method/), no se toca nada: avisa «estructura anterior: ejecuta la migración (dev-update)»
(`migrate.py`) y termina; `--dry-run` también lo informa. Antes de reemplazar, los archivos del paquete que editaste a mano (su hash no coincide
con dev/.package-manifest) se copian a dev/.backup/<fecha>-v<versión previa>/. Al terminar escribe
dev/.package-manifest (sha256 de cada archivo del paquete) y ejecuta check.py sobre el resultado.

Sin terminal interactiva hay que indicar --mode y, para actualizar, --yes.
Código de salida: 0 correcto, 1 la verificación final da errores, 2 uso incorrecto.
Solo usa la biblioteca estándar.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import NamedTuple

HERE = Path(__file__).resolve().parent
MANAGED = ("AGENTS.md", "method")
MANIFEST = ".package-manifest"
BACKUP_DIR = ".backup"
FEEDBACK_DIR = ".feedback"
USER_OWNED = ("PROJECT.md", "DEV-PROFILE.md", "COMANDOS.md", "INDEX.md", "RETRO.md", "docs", "work")
OLD_STRUCTURE_MSG = "estructura anterior: ejecuta la migración (dev-update, migrate.py)"


def old_structure(dest: Path) -> bool:
    """dev/ de 0.5.0: guidelines/, templates/ o tasks/ en la raíz y sin method/."""
    return dest.is_dir() and not (dest / "method").exists() and any((dest / d).exists() for d in ("guidelines", "templates", "tasks"))


def stray_old_dirs(dest: Path) -> list[str]:
    """Carpetas antiguas que conviven con method/ (migración incompleta o carpetas propias): no se tocan."""
    if not (dest / "method").exists():
        return []
    return [d for d in ("guidelines", "templates") if (dest / d).exists()]


class Sources(NamedTuple):
    """Recursos del paquete, según la disposición en la que se ejecuta el script."""
    layout: str
    template: Path   # dev-template/
    adapters: Path   # adapters/ (con generate.py)
    check: Path      # check.py
    version: Path    # VERSION


def find_source() -> Sources:
    """Localiza los recursos en las dos disposiciones posibles.

    paquete: <raíz>/scripts/install.py con <raíz>/dev-template, <raíz>/scripts/adapters, <raíz>/scripts/check.py
             y <raíz>/release/VERSION.
    skill:   <skill>/scripts/install.py con <skill>/assets/{dev-template,adapters,check.py,VERSION}.
    """
    root = HERE.parent
    layouts = (
        Sources("paquete", root / "dev-template", HERE / "adapters", HERE / "check.py", root / "release" / "VERSION"),
        Sources("skill", root / "assets" / "dev-template", root / "assets" / "adapters",
                root / "assets" / "check.py", root / "assets" / "VERSION"),
    )
    for cand in layouts:
        if cand.template.is_dir() and cand.adapters.is_dir() and cand.check.is_file():
            return cand
    missing = []
    for cand in layouts:
        miss = [str(p) for p in cand[1:4] if not p.exists()]
        missing.append(f"  {cand.layout}: faltan " + ", ".join(miss))
    sys.exit("Paquete incompleto: no se encuentran dev-template/, adapters/ y check.py en ninguna disposición.\n" + "\n".join(missing))


def read_version(src: Sources) -> str:
    """Versión del paquete: release/VERSION (o assets/VERSION en la skill), única fuente de verdad."""
    path = src.version
    if not path.is_file():
        sys.exit(f"Falta el archivo de versión {path}: el paquete está incompleto; vuelve a descargarlo o actualiza la skill.")
    version = path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"VERSION inválido en {path}: '{version}' (se espera X.Y.Z).")
    return version


def interactive() -> bool:
    return sys.stdin is not None and sys.stdin.isatty()


def ask(question: str, yes: bool) -> bool:
    if yes:
        return True
    if not interactive():
        return False
    try:
        return input(f"{question} [s/N] ").strip().lower() in ("s", "y")
    except EOFError:
        return False


def copy_managed(src: Sources, dest: Path, rel: str) -> None:
    """Reemplaza siempre."""
    target = dest / rel
    if target.is_dir():
        shutil.rmtree(target)
    elif target.exists():
        target.unlink()
    target.parent.mkdir(parents=True, exist_ok=True)
    s = src.template / rel
    shutil.copytree(s, target) if s.is_dir() else shutil.copyfile(s, target)


def copy_if_missing(src: Sources, dest: Path, rel: str) -> None:
    """Crea solo lo que falta, recursivamente."""
    s = src.template / rel
    if s.is_dir():
        (dest / rel).mkdir(parents=True, exist_ok=True)
        for child in sorted(s.iterdir()):
            copy_if_missing(src, dest, f"{rel}/{child.name}")
    elif not (dest / rel).exists():
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(s, dest / rel)


def read_kv(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            k, sep, v = line.partition("=")
            if sep:
                out[k.strip()] = v.strip()
    return out


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def package_files(src: Sources) -> dict[str, Path]:
    """Archivos gestionados por el paquete: ruta relativa a dev/ (con `/`) -> archivo fuente."""
    out: dict[str, Path] = {}
    base = src.template
    for rel in MANAGED:
        s = base / rel
        if s.is_dir():
            for f in sorted(s.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    out[f.relative_to(base).as_posix()] = f
        else:
            out[rel] = s
    out[".tools/check.py"] = src.check
    return out


def user_files(src: Sources) -> list[str]:
    """Archivos de usuario del paquete (se crean solo si faltan)."""
    base = src.template
    out: list[str] = []
    for rel in USER_OWNED:
        s = base / rel
        if s.is_dir():
            out += [f.relative_to(base).as_posix() for f in sorted(s.rglob("*")) if f.is_file()]
        else:
            out.append(rel)
    return out


def read_manifest(dest: Path) -> dict[str, str] | None:
    path = dest / MANIFEST
    if not path.is_file():
        return None
    out: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        digest, sep, rel = line.partition("  ")
        if sep and rel.strip():
            out[rel.strip()] = digest.strip()
    return out


def write_manifest(dest: Path, files: dict[str, Path]) -> None:
    lines = [f"{sha256(dest / rel)}  {rel}" for rel in sorted(files)]
    (dest / MANIFEST).write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def installed_stale(dest: Path, files: dict[str, Path]) -> list[str]:
    """Archivos de las carpetas gestionadas de dev/ que el paquete nuevo ya no trae."""
    out: list[str] = []
    for rel in MANAGED:
        d = dest / rel
        if d.is_dir():
            for f in sorted(d.rglob("*")):
                r = f.relative_to(dest).as_posix()
                if f.is_file() and r not in files and "__pycache__" not in f.parts:
                    out.append(r)
    return out


def classify(dest: Path, files: dict[str, Path]) -> dict[str, list[str]]:
    """Compara dev/ con el paquete nuevo.

    nuevos: no existen en dev/. iguales: idénticos al nuevo. cambiados: el paquete los cambió y
    tú no los tocaste (coinciden con el manifiesto previo). editados: los editaste tú (o no hay
    manifiesto previo y difieren del nuevo); se respaldan. retirados: ya no vienen en el paquete.
    """
    manifest = read_manifest(dest)
    res: dict[str, list[str]] = {"nuevos": [], "cambiados": [], "iguales": [], "editados": [], "retirados": []}
    for rel, s in files.items():
        cur = dest / rel
        if not cur.is_file():
            res["nuevos"].append(rel)
            continue
        h = sha256(cur)
        if h == sha256(s):
            res["iguales"].append(rel)
        elif manifest is not None and manifest.get(rel) == h:
            res["cambiados"].append(rel)
        else:
            res["editados"].append(rel)
    for rel in installed_stale(dest, files):
        if manifest is not None and manifest.get(rel) == sha256(dest / rel):
            res["retirados"].append(rel)  # intacto: se elimina sin más
        else:
            res["editados"].append(rel)  # propio o editado: se respalda antes de borrar
    for k in res:
        res[k].sort()
    return res


def missing_user_files(src: Sources, dest: Path) -> list[str]:
    return [rel for rel in user_files(src) if not (dest / rel).exists()]


def backup_path(dest: Path, today: str, prev: str | None) -> Path:
    base = dest / BACKUP_DIR / f"{today}-v{prev or 'desconocida'}"
    cand, n = base, 2
    while cand.exists():
        cand = base.with_name(f"{base.name}-{n}")
        n += 1
    return cand


def do_backup(dest: Path, rels: list[str], target: Path) -> None:
    for rel in rels:
        out = target / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dest / rel, out)


def print_plan(dest: Path, files: dict[str, Path], cls: dict[str, list[str]], missing: list[str],
               prev: str | None, new: str, mode: str, adapters: str, today: str) -> None:
    def section(title: str, items: list[str]) -> None:
        print(f"{title}: {len(items)}")
        for rel in items:
            print(f"  {rel}")

    print("dev-guidelines: plan (--dry-run, no se escribe nada)")
    print(f"Destino: {dest}")
    print(f"Versión: {prev + ' -> ' + new if prev else 'instalación nueva -> ' + new}")
    print(f"Modo: {mode or 'sin definir'}")
    print(f"Archivos del paquete: {len(files)}")
    section("Nuevos", cls["nuevos"])
    section("Cambiados", cls["cambiados"])
    print(f"Sin cambios: {len(cls['iguales'])}")
    section(f"Editados por ti (se respaldarían en dev/{BACKUP_DIR}/{today}-v{prev or 'desconocida'}/)", cls["editados"])
    section("Retirados del paquete (se eliminarían)", cls["retirados"])
    section("Archivos de usuario que faltan (se crearían)", missing)
    print(f"Adaptadores que se regenerarían: {adapters or 'ninguno'}")


def install_stubs(src: Sources, target: Path, yes: bool) -> list[str]:
    """Punteros AGENTS.md/CLAUDE.md en la raíz: nunca se sobrescriben. Devuelve los que se crearon."""
    created: list[str] = []
    for stub in ("AGENTS.md", "CLAUDE.md"):
        path = target / stub
        content = (src.adapters / stub).read_text(encoding="utf-8")
        if not path.exists():
            path.write_text(content, encoding="utf-8", newline="\n")
            created.append(stub)
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if "dev/AGENTS.md" in text or "@AGENTS.md" in text:
            print(f"· {stub} ya apunta a dev/AGENTS.md")
        elif ask(f"{stub} ya existe. ¿Añadir al final la referencia a dev/AGENTS.md?", yes):
            path.write_text(text.rstrip("\n") + "\n\n---\n\n" + content, encoding="utf-8", newline="\n")
        else:
            print(f"· {stub} sin cambios: añade a mano la referencia a dev/AGENTS.md")
    return created


def run_generate(src: Sources, target: Path, adapters: str, yes: bool) -> None:
    cmd = [sys.executable, "-I", str(src.adapters / "generate.py"), "--target", str(target), "--adapters", adapters]
    if yes:
        cmd.append("--yes")
    if subprocess.run(cmd).returncode != 0:
        print("Aviso: falló la generación de adaptadores.", file=sys.stderr)


def add_excludes(git_dir: Path, lines: list[str]) -> None:
    exclude = git_dir / "info" / "exclude"
    exclude.parent.mkdir(parents=True, exist_ok=True)
    current = exclude.read_text(encoding="utf-8").splitlines() if exclude.is_file() else []
    new = [x for x in lines if x not in current]
    if new:
        with exclude.open("a", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(new) + "\n")


def adapter_excludes(adapters: str) -> list[str]:
    names = adapters.split(",")
    out: list[str] = []
    if "claude" in names:
        out += [".claude/skills/dev-*/", ".claude/rules/dev-*.md", ".claude/agents/dev-*.md"]
    if "cursor" in names:
        out.append(".cursor/rules/dev-*.mdc")
    return out


def main(argv: list[str]) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--mode", choices=["A", "B", "a", "b"])
    ap.add_argument("--target", default=".")
    ap.add_argument("--yes", action="store_true")
    ap.add_argument("--git-init", action="store_true")
    ap.add_argument("--adapters", default="")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args(argv)

    src = find_source()
    new_version = read_version(src)
    target = Path(args.target).resolve()
    if not target.is_dir():
        print(f"No existe el directorio destino: {target}", file=sys.stderr)
        return 2
    dest = target / "dev"
    installed_kv = read_kv(dest / ".package-version") if dest.is_dir() else {}
    prev = installed_kv.get("version") or None

    if args.status:
        state = "sin-instalar" if not prev else ("al-día" if prev == new_version else "desactualizada")
        print(f"instalada={prev or '-'} nueva={new_version} estado={state}")
        return 0

    adapters = ",".join(a.strip() for a in args.adapters.split(",") if a.strip())
    bad = [a for a in adapters.split(",") if a and a not in ("claude", "cursor")]
    if bad:
        print(f"Adaptadores inválidos: {bad} (usa claude,cursor)", file=sys.stderr)
        return 2
    exists = dest.is_dir() and any(dest.iterdir())
    if exists and not adapters:
        adapters = installed_kv.get("adapters", "")
    today = datetime.date.today().isoformat()
    files = package_files(src)

    if old_structure(dest):
        print(f"{dest}: {OLD_STRUCTURE_MSG}. No se modifica nada.", file=sys.stderr if not args.dry_run else sys.stdout)
        return 0 if args.dry_run else 1
    stray = stray_old_dirs(dest)
    if stray:
        print(f"Aviso: {dest} conserva {', '.join(d + '/' for d in stray)} de la estructura anterior junto a method/; no se tocan (migración incompleta: revisa con dev-update).")

    if args.dry_run:
        mode = (args.mode or installed_kv.get("mode", "")).upper()
        print_plan(dest, files, classify(dest, files), missing_user_files(src, dest), prev, new_version, mode, adapters, today)
        return 0

    mode = (args.mode or "").upper()
    if not mode:
        if not interactive():
            print("Falta --mode A|B y no hay terminal para preguntarlo.", file=sys.stderr)
            return 2
        try:
            mode = input("Modo de instalación (A: dentro del repo, B: junto a varios repos): ").strip().upper()
        except EOFError:
            print("\nFalta --mode A|B y no hay entrada para preguntarlo.", file=sys.stderr)
            return 2
    if mode not in ("A", "B"):
        print(f"Modo inválido: '{mode}' (usa A o B)", file=sys.stderr)
        return 2
    if mode == "A" and not (target / ".git").is_dir():
        print(f"Aviso: {target} no es la raíz de un repo git; no se podrá añadir la exclusión local.", file=sys.stderr)

    backed_up: list[str] = []
    backup_dir: Path | None = None
    if exists:
        print(f"Ya existe una instalación en {dest}.")
        if not ask("¿Actualizar los archivos del paquete (AGENTS.md, method/, .tools/)? Tus datos no se tocan; "
                   f"lo que hayas editado de esos archivos se respalda en dev/{BACKUP_DIR}/.", args.yes):
            print("Cancelado. No se modificó nada (para actualizar sin preguntar usa --yes).")
            return 0
        edited = classify(dest, files)["editados"]
        if edited:
            backup_dir = backup_path(dest, today, prev)
            do_backup(dest, edited, backup_dir)
            backed_up = edited

    dest.mkdir(parents=True, exist_ok=True)
    for rel in MANAGED:
        copy_managed(src, dest, rel)
    (dest / ".tools").mkdir(exist_ok=True)
    shutil.copyfile(src.check, dest / ".tools" / "check.py")
    for rel in USER_OWNED:
        copy_if_missing(src, dest, rel)
    write_manifest(dest, files)
    info = f"version={new_version}\ninstalled={today}\nmode={mode}\nadapters={adapters}\n"
    if exists and prev:
        info += f"previous={prev}\n"
    (dest / ".package-version").write_text(info, encoding="utf-8", newline="\n")

    created_stubs = install_stubs(src, target, args.yes)
    if adapters:
        run_generate(src, target, adapters, args.yes)

    if mode == "A":
        if (target / ".git").is_dir():
            add_excludes(target / ".git", ["dev/", "dev/DEV-PROFILE.md", f"dev/{BACKUP_DIR}/", f"dev/{FEEDBACK_DIR}/"]
                         + [f"/{s}" for s in created_stubs] + adapter_excludes(adapters))
    else:
        gi = dest / ".gitignore"
        wanted = [x for x in (src.adapters / "gitignore-modo-B.txt").read_text(encoding="utf-8").splitlines() if x and not x.startswith("#")]
        if not gi.exists():
            gi.write_text("\n".join(wanted) + "\n", encoding="utf-8", newline="\n")
        else:
            have = gi.read_text(encoding="utf-8").splitlines()
            missing = [x for x in wanted if x not in have]
            if missing:
                with gi.open("a", encoding="utf-8", newline="\n") as fh:
                    fh.write("\n".join(missing) + "\n")
        if args.git_init and not (dest / ".git").is_dir():
            if subprocess.run(["git", "-C", str(dest), "init", "-q"]).returncode == 0:
                print(f"· git init en {dest}")
            else:
                print("Aviso: no se pudo ejecutar git init.", file=sys.stderr)
        if (target / ".git").is_dir():
            add_excludes(target / ".git", [f"/{s}" for s in created_stubs] + adapter_excludes(adapters))

    print(f"\nInstalado dev-guidelines {new_version} en {dest} (modo {mode}).")
    if backed_up and backup_dir is not None:
        print(f"\nRespaldados {len(backed_up)} archivos del paquete que habías editado, en {backup_dir}:")
        for rel in backed_up:
            print(f"  {rel}")
        print("El paquete los ha reemplazado. Si querías conservar esos cambios, llévalos a PROJECT.md o al paquete.")
    print()
    check = subprocess.run([sys.executable, "-I", str(dest / ".tools" / "check.py"), str(dest)])
    print("\nSiguiente: revisa dev/PROJECT.md (alias, idiomas, restricciones) y rellena dev/COMANDOS.md con lo que encuentres. DEV-PROFILE.md es opcional; «—» significa «sin definir» y no es un aviso.")
    return 1 if check.returncode == 1 else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
