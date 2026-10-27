---
name: dev-update
description: Actualiza dev/ a una versión nueva de dev-guidelines, adapta las discrepancias en los archivos del proyecto y verifica. Úsala cuando el desarrollador pida actualizar dev-guidelines o diga que dev/ está desactualizado.
metadata:
  version: "0.7.0"
---

# Actualizar dev-guidelines en un proyecto

Actualiza un `dev/` ya instalado a la versión del paquete que trae la skill hermana `dev-setup`, y adapta los archivos del proyecto que el instalador no toca (`INDEX.md`, `PROJECT.md`, `COMANDOS.md`…). **Nunca copies archivos a mano**: ejecuta el instalador.

Esta skill no lleva scripts propios. Usa los de la carpeta hermana `../dev-setup/` (`<dev-setup>` en adelante):

- `<dev-setup>/scripts/install.py`
- `<dev-setup>/scripts/migrate.py` (solo al pasar de 0.5.0 a 0.6.0: mueve carpetas y reescribe enlaces)
- `<dev-setup>/assets/MIGRATIONS.md` (qué cambia entre versiones)
- `<dev-setup>/assets/VERSION`

Si esa carpeta no existe, párate: la skill `dev-setup` no está instalada o está incompleta. Dile al desarrollador que la instale o la actualice (`npx skills add <repo>` o `npx skills update`, o que copie `skills/dev-setup` junto a esta skill) y que te vuelva a llamar. Si `python` no funciona, prueba `python3` o `py`.

## 1. Ver si hace falta

```bash
python -I <dev-setup>/scripts/install.py --status --target <raíz>
```

`<raíz>` es la carpeta que contiene `dev/` (raíz del repo en modo A, del workspace en modo B). La salida es `instalada=X nueva=Y estado=…`:

- `al-día`: díselo y **para**.
- `sin-instalar`: no hay nada que actualizar; remite a `dev-setup` para instalar y para.
- `desactualizada`: sigue.

## 2. Ver el plan sin tocar nada

```bash
python -I <dev-setup>/scripts/install.py --dry-run --target <raíz>
```

Resume al desarrollador, en pocas líneas: versión instalada → nueva, cuántos archivos del paquete cambian, y **qué archivos suyos editados se respaldarán** en `dev/.backup/` (los lista el plan en «Editados por ti»). No escribe nada.

Si `dev/` tiene la estructura anterior a 0.6.0 (`guidelines/`, `templates/` o `tasks/` en su raíz y sin `method/`), el instalador no muestra plan: avisa «estructura anterior: ejecuta la migración» y no reemplaza nada hasta que la migración esté hecha (paso 4).

## 3. Preparar la adaptación

1. Lee `<dev-setup>/assets/MIGRATIONS.md` y **solo** las secciones `## X.Y.Z` entre la versión instalada (exclusiva) y la nueva (inclusive). Si falta alguna versión intermedia, dilo y limítate a lo que sí documenta; no inventes cambios.
2. Para cada fila de «Cambios en archivos del proyecto» comprueba si **aplica a este proyecto** inspeccionando `dev/INDEX.md`, `dev/PROJECT.md`, `dev/work/tasks/` (o `dev/tasks/` si aún no se migró), `.claude/`, etc. Descarta las que no aplican.
3. Prepara el parche mínimo de cada una (sin escribirlo todavía).
4. Muestra el plan de adaptación y **espera aprobación**: las de riesgo bajo pueden ir en una sola pregunta; las de riesgo medio y alto, una a una, enseñando el cambio exacto.
5. Si `MIGRATIONS.md` marca filas de riesgo medio con **traslado de contenido** (como las de 0.5.0: partir `PROJECT.md`, crear `COMANDOS.md`, reducir `DEV-PROFILE.md`), hazlas en el orden indicado. Para cada archivo del proyecto muestra el **antes/después** y espera aprobación, y guarda antes una copia del original en `dev/.backup/` (la carpeta que crea el instalador o una `<fecha>-migracion/` junto a ella).

## 4. Migrar la estructura (solo si MIGRATIONS.md lo pide)

Si la sección `## 0.6.0` de `MIGRATIONS.md` aplica (el `dev/` está en 0.5.0 o anterior), el orden es: `--status` → `--dry-run` → **migración** → `install.py` → adaptaciones → `check.py`. Primero muestra qué haría, **sin escribir**:

```bash
python -I <dev-setup>/scripts/migrate.py --target <raíz>/dev --dry-run
```

Enséñale al desarrollador los movimientos, cuántos enlaces se reescriben y los que quedan sin resolver, y **espera su aprobación** (riesgo medio). Solo entonces:

```bash
python -I <dev-setup>/scripts/migrate.py --target <raíz>/dev
```

Usa `git mv` si `dev/` es un repo git (modo B) y deja una copia de los archivos reescritos en `dev/.backup/<fecha>-migracion-0.6.0/`. Si termina con error, no sigas con el instalador: léelo y reporta. Las rutas citadas en prosa (entre acentos graves) no se reescriben: revisa `INDEX.md` y `PROJECT.md` con la fila correspondiente de `MIGRATIONS.md`.

## 5. Actualizar

Lee el modo de `dev/.package-version` (`mode=`).

```bash
python -I <dev-setup>/scripts/install.py --mode <A|B> --target <raíz> --yes
```

No pases `--adapters`: se conservan y regeneran los ya instalados. Si la salida termina con errores, no sigas: léelos y aplica el playbook `diagnose`.

## 6. Aplicar las adaptaciones aprobadas

Aplica solo lo que el desarrollador aprobó en el paso 3 (la migración de carpetas ya se hizo en el paso 4), con ediciones mínimas.

## 7. Revisar lo respaldado

Si el instalador respaldó archivos en `dev/.backup/<fecha>-v<versión>/`: compara cada uno con el archivo nuevo. Si la edición era sustancial, **propón** dónde conservarla (por ejemplo `PROJECT.md` §3 restricciones o §4 zonas intocables) en vez de reeditar los archivos gestionados; si era trivial, di que se puede descartar. No borres el respaldo.

## 8. Verificar

```bash
python -I dev/.tools/check.py dev
```

Resume el resultado. Si hay errores, aplica el playbook `diagnose` (`dev/method/playbooks/diagnose.md`).

## 9. Cerrar

Termina con un mensaje corto:

1. Versión anterior → nueva y resultado de la verificación.
2. Qué se adaptó (y qué respaldos se crearon).
3. Qué quedó pendiente o sin aprobar.

## Reglas

- No edites a mano `dev/AGENTS.md` ni `dev/method/`: el paquete los reemplaza.
- No hagas commits ni toques el historial git.
- No toques `work/` ni `docs/` salvo la migración de estructura o una adaptación de formato que el desarrollador aprobó.
- Si `MIGRATIONS.md` no cubre una versión intermedia, dilo.
- Ante un `AGENTS.md` o `CLAUDE.md` preexistente en la raíz, el script pregunta antes de añadir la referencia; no lo resuelvas por tu cuenta.
