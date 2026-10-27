"""Empaqueta las skills dev-setup, dev-update y dev-feedback: copia los recursos del paquete dentro de skills/.

Uso:
    python -I scripts/build-skill.py         # regenera skills/dev-setup/{scripts,assets} y la versión en las skills
    python -I scripts/build-skill.py --check   # solo comprueba que está al día (código 1 si no)

Fuente única de verdad: release/VERSION, release/MIGRATIONS.md, dev-template/, scripts/adapters/, scripts/check.py,
scripts/install.py y scripts/migrate.py de la raíz del paquete. Lo de skills/dev-setup/scripts y assets es una copia generada: no se edita a mano.
La versión de VERSION también se escribe en el frontmatter de skills/dev-setup/SKILL.md y
skills/dev-update/SKILL.md y skills/dev-feedback/SKILL.md como `metadata:` + `version: "X.Y.Z"`; el resto del texto
de las skills es a mano. dev-update y dev-feedback no llevan scripts propios.
Solo usa la biblioteca estándar.
"""

from __future__ import annotations

import filecmp
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "dev-setup"
SKILL_FILES = [SKILL / "SKILL.md", ROOT / "skills" / "dev-update" / "SKILL.md", ROOT / "skills" / "dev-feedback" / "SKILL.md"]
FILES = {
    "scripts/install.py": "scripts/install.py",
    "scripts/migrate.py": "scripts/migrate.py",
    "scripts/check.py": "assets/check.py",
    "release/VERSION": "assets/VERSION",
    "release/MIGRATIONS.md": "assets/MIGRATIONS.md",
}
DIRS = {"dev-template": "assets/dev-template", "scripts/adapters": "assets/adapters"}
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


def package_version() -> str:
    path = ROOT / "release" / "VERSION"
    if not path.is_file():
        sys.exit("Falta release/VERSION en la raíz del paquete.")
    version = path.read_text(encoding="utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        sys.exit(f"release/VERSION inválido: '{version}' (se espera X.Y.Z).")
    return version


def with_version(text: str, version: str) -> str:
    """Devuelve `text` con `metadata:\\n  version: "X.Y.Z"` en el frontmatter, sin tocar el resto."""
    nl = "\r\n" if "\r\n" in text else "\n"
    lines = text.split(nl)
    if not lines or lines[0] != "---" or "---" not in lines[1:]:
        sys.exit("La skill no empieza con un frontmatter '---' válido.")
    end = lines.index("---", 1)
    fm = lines[1:end]
    entry = f'  version: "{version}"'
    if "metadata:" in fm:
        i = fm.index("metadata:")
        j = i + 1
        while j < len(fm) and fm[j].startswith((" ", "\t")):
            if fm[j].strip().startswith("version:"):
                fm[j] = entry
                break
            j += 1
        else:
            fm.insert(i + 1, entry)
    else:
        fm += ["metadata:", entry]
    return nl.join([lines[0]] + fm + lines[end:])


def same_tree(a: Path, b: Path) -> bool:
    if not b.is_dir():
        return False
    cmp = filecmp.dircmp(a, b, ignore=["__pycache__"])
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False
    return all(same_tree(a / d, b / d) for d in cmp.common_dirs)


def stale() -> list[str]:
    out = []
    for src, dst in FILES.items():
        if not (SKILL / dst).is_file() or not filecmp.cmp(ROOT / src, SKILL / dst, shallow=False):
            out.append(dst)
    for src, dst in DIRS.items():
        if not same_tree(ROOT / src, SKILL / dst):
            out.append(dst)
    expected = {Path(d).parts[1] for d in list(FILES.values()) + list(DIRS.values()) if d.startswith("assets/")}
    assets = SKILL / "assets"
    if assets.is_dir():
        out += [f"assets/{p.name} (sobra)" for p in sorted(assets.iterdir()) if p.name not in expected]
    version = package_version()
    for path in SKILL_FILES:
        rel = path.relative_to(ROOT / "skills").as_posix()
        if not path.is_file():
            out.append(f"{rel} (falta)")
        elif path.read_text(encoding="utf-8") != with_version(path.read_text(encoding="utf-8"), version):
            out.append(f"{rel} (metadata.version != {version})")
    return out


def main(argv: list[str]) -> int:
    if "--check" in argv:
        old = stale()
        print("skills/ al día." if not old else "Desactualizado: " + ", ".join(old))
        return 1 if old else 0
    version = package_version()
    for sub in ("scripts", "assets"):
        if (SKILL / sub).exists():
            shutil.rmtree(SKILL / sub)
    for src, dst in FILES.items():
        (SKILL / dst).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / src, SKILL / dst)
    for src, dst in DIRS.items():
        shutil.copytree(ROOT / src, SKILL / dst, ignore=IGNORE)
    for path in SKILL_FILES:
        if not path.is_file():
            sys.exit(f"Falta {path.relative_to(ROOT)}.")
        text = path.read_text(encoding="utf-8")
        new = with_version(text, version)
        if new != text:
            path.write_text(new, encoding="utf-8", newline="")
    print(f"skills/ regenerada (versión {version}).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
