# Migraciones entre versiones

**Fecha:** 27 de octubre de 2026 · **Versión del paquete:** 0.7.0

Guía para actualizar un `dev/` ya instalado. La usa la skill `dev-update` (copiada como `assets/MIGRATIONS.md` en `dev-setup`) para adaptar los archivos del **proyecto** que el instalador no toca. El instalador sí reemplaza solos los archivos del paquete (`AGENTS.md`, `method/`, `.tools/check.py`; hasta 0.5.0 `guidelines/` y `templates/`); aquí solo se resume qué cambia en ellos.

## Contenido

1. [Cómo leer este archivo](#cómo-leer-este-archivo)
2. [0.7.0](#070)
3. [0.6.1](#061)
4. [0.6.0](#060)
5. [0.5.0](#050)
6. [0.4.0](#040)
7. [0.3.0](#030)
8. [0.2.0](#020)

## Cómo leer este archivo

- Una sección `## X.Y.Z` por versión, de la más nueva a la más antigua. Para pasar de la versión A a la B se leen las secciones mayores que A y hasta B inclusive.
- Cada sección tiene tres partes: archivos del paquete que se reemplazan, cambios en archivos del proyecto (tabla con acción propuesta y riesgo) y compatibilidad.
- Riesgo **bajo**: edición mecánica y acotada; **medio**: toca estado vivo o contenido escrito por el equipo; **alto**: puede perder información si se hace mal.
- Las acciones son propuestas: el agente las muestra y espera aprobación antes de aplicarlas. Los reports, changelogs y decisiones históricos no se reescriben salvo que la fila lo diga.

## 0.7.0

Cada proyecto guarda sus retros en `dev/RETRO.md` y la skill `dev-feedback` las convierte en propuestas de mejora del paquete. **Ningún cambio es obligatorio**: la actualización funciona sin adaptar nada.

### Archivos del paquete que se reemplazan

- `method/playbooks/close-session.md`: la retro de cierre de task es una fila `pendiente` en `RETRO.md`.
- `method/playbooks/diagnose.md`: cuenta las filas `pendiente` de `RETRO.md` y recomienda «feedback del método» si hay 3 o más.
- `INDEX.md` no es del paquete (no se reemplaza) y `AGENTS.md` no cambia de contenido; el catálogo de `INDEX.md` conserva el texto anterior de `close-session` hasta que lo cambies a mano.
- `.tools/check.py`: nueva comprobación suave de `RETRO.md` (solo avisos).
- Exclusiones de git: `dev/.feedback/` (modo A, `.git/info/exclude`; modo B, `dev/.gitignore`), igual que `dev/.backup/`. El instalador las añade en la actualización.

### Cambios en archivos del proyecto (que el instalador NO toca) y cómo adaptarlos

| Orden | Archivo | Cambio | Acción propuesta | Riesgo |
|---|---|---|---|---|
| 1 | `dev/RETRO.md` | Archivo nuevo del proyecto. | Ninguna: lo crea el instalador si falta y nunca lo pisa. | bajo |
| 2 | READMEs de tasks (`work/tasks/**/README.md`, también archivadas) | Si tienen una retro de 3 líneas escrita, ahora esa retro vive en `RETRO.md`. | Con aprobación, trasladar cada retro como fila `pendiente` a `dev/RETRO.md` (fecha, task, qué funcionó, qué falló, qué cambiarías) y dejar la retro original donde está. Si no hay ninguna, descartar la fila. | bajo |
| 3 | `dev/INDEX.md` | La nota de la columna «Retro pendiente» y la descripción de `close-session` en el catálogo citan la retro antigua. | Opcional: sustituir por «fila `pendiente` en `RETRO.md`» y «anota la retro de una task en `RETRO.md`». | bajo |

### Compatibilidad

- Total con 0.6.x: misma estructura de `dev/` y mismos comandos. `check.py` no exige `RETRO.md`, así que un `dev/` 0.6.x sigue en 0 errores hasta actualizar.

## 0.6.1

Reorganización de la raíz del **paquete** (scripts en `scripts/`, versión y notas en `release/`, quickstart en `docs/00-quickstart.md`; se eliminan `INSTALL.md` y `tools/`). **No hay cambios en archivos del proyecto**: `dev/` queda igual y no hay nada que adaptar.

### Archivos del paquete que se reemplazan

- `.tools/check.py` y los adaptadores se reinstalan sin cambios de contenido; el instalador solo actualiza `.package-version`.

### Cambios en archivos del proyecto (que el instalador NO toca) y cómo adaptarlos

Ninguno.

### Compatibilidad

- Total con 0.6.0: misma estructura de `dev/`, mismos comandos del instalador, misma disposición del bundle de las skills (`scripts/install.py`, `scripts/migrate.py` y `assets/…`). Solo cambian las rutas dentro del repositorio del paquete: `python -I scripts/install.py …` en lugar de `python -I install.py …`.

## 0.6.0

Reorganización **obligatoria** de la estructura de `dev/`: `work/` (tasks, bugs, reports, changelogs), `docs/decisions/` (los ADR globales) y `method/` (lo que el paquete reemplaza: playbooks, stacks, plantillas y README). El orden es: `--status` → `--dry-run` → **`migrate.py`** (con aprobación) → `install.py --yes` → adaptaciones → `check.py`. Con la estructura antigua `install.py` avisa «estructura anterior: ejecuta la migración» y no reemplaza nada.

Mapa de rutas (relativo a `dev/`): `tasks/`→`work/tasks/`, `bugs/`→`work/bugs/`, `reports/`→`work/reports/`, `changelogs/`→`work/changelogs/`, `decisions/`→`docs/decisions/`, `guidelines/README.md`→`method/README.md`, `guidelines/playbooks/`→`method/playbooks/`, `guidelines/stacks/`→`method/stacks/`, `templates/`→`method/templates/`. El archivo `decisions.md` de cada task no se mueve.

### Archivos del paquete que se reemplazan

- `AGENTS.md`: rutas nuevas y fila `method/` en «Estructura».
- `method/` (antes `guidelines/` y `templates/`): playbooks, stacks y plantillas con las rutas nuevas. La migración los traslada tal cual para conservar tus ediciones; después `install.py` respalda en `dev/.backup/` lo que editaste y los actualiza.
- `.tools/check.py`: árbol nuevo; error «estructura anterior a 0.6.0» si encuentra el antiguo.
- Adaptadores: `PLAYBOOKS_REL` pasa a `dev/method/playbooks` y las reglas `paths:` a `dev/work/**`, `dev/docs/**` y `dev/docs/decisions/**`; se regeneran solos al actualizar.
- `install.py`: gestiona `AGENTS.md` y `method/`; `work/` y `docs/` son del proyecto.

### Cambios en archivos del proyecto (que el instalador NO toca) y cómo adaptarlos

| Orden | Archivo | Cambio | Acción propuesta | Riesgo |
|---|---|---|---|---|
| 1 | Carpetas de `dev/` y enlaces entre `.md` | Las carpetas cambian de sitio y los enlaces relativos dejan de resolver. | Mover carpetas y reescribir enlaces: ejecutar `migrate.py --target dev --dry-run`, mostrar el resultado y pedir aprobación; después `migrate.py --target dev`. Usa `git mv` si `dev/` es un repo git (modo B) y deja copia en `dev/.backup/<fecha>-migracion-0.6.0/`. | medio |
| 2 | `dev/INDEX.md`, `dev/PROJECT.md`, `dev/COMANDOS.md`, `dev/docs/**` | Citan rutas antiguas en prosa o entre acentos graves (`tasks/…`, `guidelines/playbooks/…`) que `migrate.py` no reescribe (solo enlaces Markdown). | Actualizar el catálogo y rutas de `INDEX.md` si cita rutas antiguas en prosa (`guidelines/playbooks/` → `method/playbooks/`, `tasks/archive/` → `work/tasks/archive/`, etc.); revisar con `grep` las demás. | bajo |
| 3 | `.claude/rules/dev-*.md`, `.claude/skills/dev-*`, `.cursor/rules/dev-*.mdc` | Apuntan a `dev/guidelines/playbooks/` y a las rutas antiguas en `paths:`. | Ninguna: reglas de adaptadores, se regeneran solas con `install.py` (no pases `--adapters`; se conservan los instalados). | bajo |
| 4 | Reports, changelogs, tasks y ADR históricos | Citan rutas antiguas en prosa. | Ninguna: son históricos y no se reescriben (sus enlaces ya los corrige `migrate.py`). | bajo |
| 5 | Hook `SessionStart` en `settings.json` | Ninguno: apunta a `dev/.adapters/session-start.py`, que se regenera. | Ninguna. | bajo |

### Compatibilidad

- La migración es obligatoria. Hasta migrar, `check.py` da el error «estructura anterior a 0.6.0: migra con dev-update» y `install.py` avisa «estructura anterior: ejecuta la migración» sin tocar nada; `install.py --dry-run` también lo informa.
- `migrate.py` se detiene sin mover nada si `work/`, `docs/decisions/` o `method/` ya tienen contenido, y no hace nada si el `dev/` ya tiene la estructura nueva. Si `guidelines/` conserva archivos propios tras migrar, los deja donde están y los lista.
- Los enlaces cuyo destino no existía antes se dejan igual y se listan. Los respaldos de `.backup/` anteriores no se reescriben.
- Desde 0.5.0 (y desde versiones anteriores pasando por las secciones intermedias: primero la migración de formato de 0.5.0).

## 0.5.0

Cambio de formato **obligatorio**: `PROJECT.md` y `DEV-PROFILE.md` se reducen y nace `COMANDOS.md`. Hazlo en el orden de la tabla; antes de tocar cada archivo guarda una copia del original en `dev/.backup/` (la carpeta que crea el instalador o una `<fecha>-migracion/`), muestra el antes/después y espera aprobación.

### Archivos del paquete que se reemplazan

- `AGENTS.md`: al empezar lee `PROJECT.md` (núcleo), `DEV-PROFILE.md` e `INDEX.md` «Activo ahora»; `COMANDOS.md` solo bajo demanda. Ya no avisa por campos vacíos.
- `guidelines/` (playbooks `start-session`, `develop-code`, `fix-bug`, `commit-pr`, `write-task`, `write-report`, `update-docs`, `diagnose` y packs de `stacks/`) y `templates/`: referencias renumeradas (alias → `PROJECT.md` §1, idiomas → §2, restricciones → §3, zonas → §4; stacks, comandos y commits → `COMANDOS.md`); desaparece «Modelos sugeridos» (el campo «Modelo sugerido» del brief queda como texto libre opcional).
- `.tools/check.py`: error si falta `COMANDOS.md`; alias en `PROJECT.md` §1; los `TODO` literales siguen avisando (las plantillas ya no los traen, usan `—`).
- Adaptador del hook `session-start.py`: avisa solo si falta `PROJECT.md` o `COMANDOS.md`, o hay `TODO` literales; no por `—`.
- El instalador crea `COMANDOS.md` con la plantilla vacía si falta (no sustituye a la migración de la tabla siguiente).

### Cambios en archivos del proyecto (que el instalador NO toca) y cómo adaptarlos

| Orden | Archivo | Cambio | Acción propuesta | Riesgo |
|---|---|---|---|---|
| 1 | `dev/COMANDOS.md` | Archivo nuevo con Stacks activos, Comandos y Commits/PR. El instalador lo crea vacío (`—`). | Trasladar a él los valores de las antiguas secciones de `PROJECT.md`: §4 Stacks activos → `COMANDOS.md` §1, §5 Comandos del proyecto → §2, §8 Commits y pull requests → §3. Cambiar los `TODO` que queden por `—`. Si el proyecto tiene contenido, mostrarlo y pedir aprobación. | medio |
| 2 | `dev/PROJECT.md` | Pasa a núcleo: §1 Repos y alias, §2 Idiomas, §3 Restricciones, §4 Zonas intocables. | Reescribir con la plantilla de `dev-template/PROJECT.md` conservando alias (antes §2), idiomas (antes §3), restricciones `C1…` (antes §6) y zonas intocables (antes §7). Se descartan §1 Identidad y §9 Modelos sugeridos: avisar de ello. Cambiar los `TODO` por `—`. | medio |
| 3 | `dev/DEV-PROFILE.md` | Pasa a una tabla de 5 filas. | Reescribir con la plantilla conservando lo equivalente: «Tecnologías que NO conozco», «Idioma de las explicaciones en el chat» y «Atribución de IA» (antes §5). Se descartan nombre/rol, glosario sí/no (se deduce de «Tecnologías que NO conozco»), nivel de detalle, sistema operativo/shell, herramientas del agente, preferencia de modelo y «Estado del perfil». «Particularidades del entorno» puede recoger WSL o contenedor si lo había. Si «Cómo levantar el proyecto aquí» tenía contenido, proponer moverlo a una página de `docs/runbook/`. | medio |
| 4 | `tasks/`, `bugs/`, `reports/`, `docs/`, `decisions/` | Citan «`PROJECT.md` §N» con la numeración antigua. | Ninguna: son históricos y no se reescriben. | bajo |
| 5 | Subtasks y briefs existentes | Tienen el campo «Modelo sugerido». | Ninguna: sigue siendo un campo libre opcional. | bajo |

### Compatibilidad

- La migración es obligatoria. Al actualizar, el instalador crea `COMANDOS.md` vacío (`—`); hasta migrar, `check.py` da el error «formato anterior a 0.5.0» mientras `PROJECT.md` conserve las secciones antiguas (Stacks activos, Comandos del proyecto, Modelos sugeridos), y el error «falta COMANDOS.md» si el paquete se copió a mano. Los playbooks nuevos leen `COMANDOS.md`: con la plantilla vacía el agente preguntará los datos que falten, pero no verá los comandos que siguen en el `PROJECT.md` antiguo.
- Desde 0.4.0 (y desde versiones anteriores pasando por las secciones intermedias).

## 0.4.0

### Archivos del paquete que se reemplazan

- `dev/.tools/check.py`: ignora `dev/.backup/` al comprobar enlaces y numeración.
- El resto de `AGENTS.md`, `guidelines/` y `templates/` no cambia de contenido respecto a 0.3.0.
- Nuevos archivos de control que escribe el instalador: `dev/.package-manifest` (hash de cada archivo del paquete) y, solo si editaste archivos del paquete, `dev/.backup/<fecha>-v<versión previa>/`.

### Cambios en archivos del proyecto (que el instalador NO toca) y cómo adaptarlos

| Archivo | Cambio | Acción propuesta | Riesgo |
|---|---|---|---|
| (ninguno) | La carpeta `template/` pasó a `dev-template/` **solo en el paquete**; en el proyecto sigue siendo `dev/`. | Ninguna. | bajo |
| `dev/.package-version` | Gana `previous=<versión anterior>` en las actualizaciones. | Ninguna: lo escribe el instalador. | bajo |
| Exclusiones de git | `dev/.backup/` se excluye (modo A: `.git/info/exclude`; modo B: `dev/.gitignore`). | Ninguna si se actualiza con el instalador; en modo B con `.gitignore` propio, comprobar que lista `.backup/`. | bajo |

### Compatibilidad

- Se actualiza desde 0.3.0 (y desde 0.2.0 o 0.1.0 pasando por las secciones intermedias) sin cambios obligatorios en el proyecto.
- Una instalación 0.3.0 no tiene `.package-manifest`: la primera actualización trata todo archivo del paquete que difiera del nuevo como editado y lo respalda en `dev/.backup/`.

## 0.3.0

### Archivos del paquete que se reemplazan

- `AGENTS.md` (enrutador): lista el playbook `diagnose`.
- `guidelines/playbooks/diagnose.md`: playbook nuevo (ahora son 10).
- `.tools/check.py`: nuevo en el proyecto (antes solo existía en el paquete); admite `--json`, exige el playbook `diagnose` y revisa `.claude/agents/dev-*.md`.
- Los scripts `install.sh` e `install.ps1` desaparecen del paquete; se instala con `install.py` o con la skill `dev-setup`.

### Cambios en archivos del proyecto (que el instalador NO toca) y cómo adaptarlos

| Archivo | Cambio | Acción propuesta | Riesgo |
|---|---|---|---|
| `dev/INDEX.md` | «Catálogo de guías» (§2) no tiene la fila de `diagnose`. | Añadir la fila: `diagnose` · «Ejecuta `check.py`, interpreta los hallazgos y propone arreglos.» · «Diagnostica dev/; al cerrar una task; tras actualizar el paquete.» · skill `dev-diagnose`. Copiar el formato de las filas vecinas. | bajo |
| `.claude/agents/dev-doctor.md` | Agente nuevo (solo lectura) generado a partir del playbook. | Si el proyecto tiene el adaptador `claude` (campo `adapters=` de `.package-version`), el instalador lo genera solo. Si no usa adaptadores, no hay nada que hacer. | bajo |
| `dev/.tools/check.py` | Aparece en el proyecto. | Si algún script, CI o documento del proyecto invoca un `check.py` del paquete, apuntarlo a `python -I dev/.tools/check.py dev`. | bajo |
| Scripts del proyecto o documentos | Citan `install.sh` o `install.ps1`. | Sustituir por `python -I install.py --mode A\|B --target DIR` (o la skill `dev-setup`). | bajo |
| `dev/PROJECT.md`, `dev/DEV-PROFILE.md`, `tasks/`, `reports/`, `docs/` | Sin cambios de formato. | Ninguna. | bajo |

### Compatibilidad

- Desde 0.2.0: actualización directa; la única adaptación manual es la fila de `diagnose` en `INDEX.md`.
- `check.py` de 0.2.0 no conoce `diagnose`; tras actualizar, el de 0.3.0 en adelante lo exige y marca error si falta el playbook (el instalador lo copia).

## 0.2.0

### Archivos del paquete que se reemplazan

- `guidelines/` pasa a `guidelines/playbooks/` (9 playbooks de una situación, con `name` y `description`); `guidelines/stacks/` se conserva. Desaparecen `WORKFLOW.md`, `TASKS.md`, `REPORTING.md`, `DOCS.md`, `DEVELOPMENT.md`, `BUGS.md` e `INSTALL.md` de `guidelines/`.
- `AGENTS.md` queda como enrutador corto (≤ 60 líneas) que apunta a los playbooks.
- `templates/`: plantillas del paquete, reemplazadas.
- Adaptadores opcionales (`--adapters claude,cursor`): skills `dev-<playbook>`, reglas por ruta y hook `SessionStart` opcional; `CLAUDE.md` de la raíz pasa a `@AGENTS.md`.

### Cambios en archivos del proyecto (que el instalador NO toca) y cómo adaptarlos

| Archivo | Cambio | Acción propuesta | Riesgo |
|---|---|---|---|
| `dev/INDEX.md` | Gana las secciones «Activo ahora» (§1) y «Catálogo de guías» (§2); tasks, bugs y backlog pasan a §3, §4 y §5. | Añadir ambas secciones con el formato de `dev-template/INDEX.md`, rellenando «Activo ahora» con la task o bug en curso real (leer el README de la task) y conservando intactas las tablas de tasks, bugs y backlog. Actualizar el índice «Contenido». | medio |
| `tasks/*/README.md`, briefs, `reports/`, `docs/`, `decisions/` | Enlaces a `guidelines/WORKFLOW.md`, `TASKS.md`, `REPORTING.md`, `DOCS.md`, `DEVELOPMENT.md` o `BUGS.md` quedan rotos. Equivalencias: `WORKFLOW` → `start-session` / `close-session`; `TASKS` → `write-task`; `REPORTING` → `write-report`; `DOCS` → `update-docs`; `DEVELOPMENT` → `develop-code`; `BUGS` → `fix-bug`. | Ejecutar `check.py` y corregir solo los enlaces que reporte en tasks y bugs vivos. En reports y changelogs históricos, no reescribir: dejar el aviso o, si el equipo lo aprueba, cambiar solo la ruta del enlace. | medio |
| `dev/tasks/archive/` y `dev/bugs/archive/` | Carpetas para lo cerrado; el inicio de sesión no las lee. | `tasks/archive/` la crea el instalador. Crear `bugs/archive/` con un `.gitkeep` solo si se va a archivar un bug. Las tasks ya cerradas pueden moverse a `tasks/archive/` y figurar en `INDEX.md` §3 como `hecha (archivada)` con su ruta; es opcional y se hace con aprobación. | medio |
| `AGENTS.md` y `CLAUDE.md` de la raíz del proyecto | `CLAUDE.md` pasa a contener `@AGENTS.md`; el instalador nunca los sobrescribe. | Comprobar que apuntan a `dev/AGENTS.md`. Si el `CLAUDE.md` es el antiguo, proponer añadir la referencia al final (el instalador ya pregunta). | bajo |
| `dev/AGENTS.md` con texto propio del proyecto | El enrutador se reemplaza entero; lo añadido a mano se pierde (queda en `dev/.backup/` desde 0.4.0). | Llevar las reglas propias a `PROJECT.md` §3 (restricciones) o §4 (zonas intocables; en versiones anteriores a 0.5.0, §6 y §7), no a `AGENTS.md`. | alto |
| `dev/PROJECT.md`, `dev/DEV-PROFILE.md` | El hook opcional `SessionStart` los lee; el formato no cambia. | Ninguna. | bajo |
| `dev/.package-version` | Recuerda los adaptadores (`adapters=`). | Ninguna: lo reescribe el instalador. | bajo |
| Adaptadores generados | Se regeneran y se podan los obsoletos; se excluyen de git en modo A. | Ninguna si se actualiza con el instalador. Los archivos `dev-*` sin la marca `dev-guidelines:generated` se omiten salvo `--yes`. | bajo |

### Compatibilidad

- Desde 0.1.0: cambio de estructura de `guidelines/`; revisar los enlaces con `check.py` después de actualizar.
- `check.py` de 0.2.0 añade avisos de presupuesto (`AGENTS.md` ≤ 60 líneas, playbooks ≤ 120) que con `--strict` pasan a error.
