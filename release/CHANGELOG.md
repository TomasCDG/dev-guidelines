# CHANGELOG del paquete

Versión instalada en un proyecto: `dev/.package-version`.

## 0.7.0 — 2026-10-27

Feedback del método desde cada proyecto. Motivo: la retro vivía en el paquete, pero quienes la escriben son los proyectos instalados, que no tienen acceso a él; ahora cada `dev/` guarda sus retros y una skill las convierte en propuestas de cambio al paquete.

### Añadido

- Skill `dev-feedback` (sin scripts propios): convierte las filas `pendiente` de `dev/RETRO.md` en propuestas (evidencia, archivo del paquete afectado, parche y riesgo), las valida contigo y las guarda en `dev/.feedback/AAAA-MM-DD-feedback.md`. No modifica `dev/method/` ni el repositorio del paquete.
- `dev/RETRO.md` por proyecto (plantilla en `dev-template/RETRO.md`): archivo del proyecto, lo crea el instalador si falta y nunca lo pisa.
- `release/ROADMAP.md`: backlog de funcionalidades futuras del paquete (R1–R8).
- `historia/`: `diseno.md` (por qué el paquete es como es) y `retro-aplicadas.md` (mejoras que llegaron por retro, con su versión).

### Cambiado

- La retro de cierre de task se escribe como fila `pendiente` en `dev/RETRO.md` (antes, en el README de la task); `diagnose` cuenta esas filas y recomienda «feedback del método» si hay 3 o más; la nota de «Retro pendiente» de `INDEX.md` apunta a `RETRO.md`.
- `check.py`: nueva comprobación suave `check_retro` (columnas y estados de `RETRO.md`; solo avisos, el archivo no es obligatorio).
- `dev/.feedback/` se excluye de git como `dev/.backup/` (modo A: `.git/info/exclude`; modo B: `dev/.gitignore`).
- `build-skill.py` empaqueta y versiona las tres skills. `dev-setup` menciona el feedback en su mensaje de cierre. README y `docs/` actualizados; `docs/03-uso.md` gana «Feedback del método» y se quitan repeticiones entre documentos.

### Eliminado

- `00-informe-analisis.md`, `01-plan-migracion.md` y `RETRO.md` de la raíz del paquete: su contenido útil pasa a `historia/`.

### Migración

Sin pasos obligatorios; opcional, trasladar retros ya escritas (sección 0.7.0 de `MIGRATIONS.md`).

## 0.6.1 — 2026-10-27

Raíz del paquete ordenada por función. Motivo: en la raíz convivían instaladores, verificador, notas de versión, guías y carpetas de datos; ahora cada grupo tiene su carpeta y el README es la única puerta de entrada.

### Cambiado

- Raíz reordenada: `scripts/` (`install.py`, `check.py`, `migrate.py`, `build-skill.py` y `adapters/`), `release/` (`VERSION`, `CHANGELOG.md`, `MIGRATIONS.md`) y `docs/` (incluye `00-quickstart.md`, antes `QUICKSTART.md`). `dev-template/`, `skills/` y `examples/` no cambian.
- Uso: `python -I scripts/install.py …` desde la raíz del paquete. `install.py` localiza sus recursos con una sola función (`find_source`) que funciona en la raíz del paquete y en el bundle de la skill, y los errores dicen qué falta.
- El bundle `skills/dev-setup/` mantiene su disposición (`scripts/` y `assets/`): lo instalado y los `SKILL.md` no cambian.
- `README.md` se reduce a una puerta de entrada corta; se quita la duplicación con el quickstart y con `docs/01-instalacion.md`.

### Eliminado

- `INSTALL.md` (solo apuntaba a `docs/01-instalacion.md`) y la carpeta `tools/` (su contenido va a `scripts/`).

### Migración

Ninguna: sin cambios en archivos del proyecto (sección 0.6.1 de `MIGRATIONS.md`).

## 0.6.0 — 2026-10-27

Estructura de `dev/` más clara. Motivo: en la raíz de `dev/` convivían lo que el paquete reemplaza (`guidelines/`, `templates/`), el trabajo del equipo (`tasks/`, `bugs/`, `reports/`, `changelogs/`) y la verdad técnica (`docs/`, `decisions/`); ahora cada grupo tiene una carpeta y está claro qué se actualiza y qué es tuyo.

### Cambiado

- Nueva estructura: `work/` (`tasks/`, `bugs/`, `reports/`, `changelogs/`), `docs/` (incluye `docs/decisions/`, los ADR globales) y `method/` (`README.md`, `playbooks/`, `stacks/`, `templates/`; lo que el paquete reemplaza al actualizar). `AGENTS.md`, `INDEX.md`, `PROJECT.md`, `COMANDOS.md` y `DEV-PROFILE.md` siguen en la raíz de `dev/`. El `decisions.md` de cada task no se mueve.
- `install.py`: gestiona `AGENTS.md` y `method/`; `work/` y `docs/` son del proyecto. Con la estructura antigua avisa «estructura anterior: ejecuta la migración» y no toca nada (también en `--dry-run`).
- `check.py`: árbol nuevo en estructura, numeración, archivo, enlaces, alias, fechas y adaptadores; error claro «estructura anterior a 0.6.0: migra con dev-update».
- Adaptadores: playbooks en `dev/method/playbooks`; reglas `paths:` en `dev/work/**`, `dev/docs/**` y `dev/docs/decisions/**`; hook y textos actualizados.
- Playbooks, plantillas, `AGENTS.md`, ejemplo, skills (`dev-update` ejecuta primero `migrate.py --dry-run`, pide aprobación y solo después `install.py --yes`) y documentación, con las rutas nuevas.

### Añadido

- `tools/migrate.py` (copiado a `skills/dev-setup/scripts/migrate.py`): migración determinista de un `dev/` 0.5.0; mueve las carpetas (`git mv` si `dev/` es un repo git), reescribe los enlaces Markdown relativos conservando anclas, respalda en `dev/.backup/<fecha>-migracion-0.6.0/` y admite `--dry-run`.

### Migración

Obligatoria, vía `dev-update` (sección 0.6.0 de `MIGRATIONS.md`): `migrate.py` y después `install.py --yes`. Hasta entonces `check.py` da el error «estructura anterior a 0.6.0».

## 0.5.0 — 2026-10-26

Menos lectura obligatoria en cada sesión. Motivo: `PROJECT.md` y `DEV-PROFILE.md` sumaban ~5,7 KB de campos `TODO` que el agente leía siempre y que provocaban avisos de arranque; ahora el núcleo cabe en menos de 2 KB y el resto se lee bajo demanda.

### Cambiado

- `PROJECT.md` queda como núcleo (repos y alias, idiomas, restricciones, zonas intocables); sin índice, sin Identidad ni Modelos sugeridos.
- `DEV-PROFILE.md` se reduce a una tabla de 5 filas opcionales (tecnologías que no conoces, idioma del chat, formato de la respuesta final, atribución de IA, particularidades del entorno). Desaparecen nombre/rol, glosario sí/no, nivel de detalle (campo que nadie leía), sistema/shell, cómo levantar el proyecto, herramientas del agente, preferencia de modelo y «Estado del perfil».
- Nuevo `COMANDOS.md` (lectura bajo demanda) con stacks activos, comandos y política de commits/PR, antes en `PROJECT.md` §4, §5 y §8. Lo crea `install.py` y `check.py` lo exige.
- Sin avisos por campos vacíos: las plantillas usan `—`, no `TODO`. El agente pregunta el dato que le falta en el momento, propone un valor y lo anota en el archivo correspondiente.
- Se elimina «Modelos sugeridos»; el campo «Modelo sugerido» de los briefs es libre y opcional.
- `check.py` busca los alias en `PROJECT.md` §1, exige `COMANDOS.md` y sigue avisando de `TODO` literales; el hook `session-start.py` no avisa por `—`.
- Playbooks, plantillas, `AGENTS.md`, skills `dev-setup` (una pregunta opcional para el perfil) y `dev-update` (migraciones con traslado de contenido: antes/después, aprobación y copia en `dev/.backup/`), ejemplo y documentación actualizados.

### Migración

Obligatoria, vía `dev-update` (sección 0.5.0 de `MIGRATIONS.md`): crear `COMANDOS.md` trasladando las antiguas §4, §5 y §8 de `PROJECT.md`, reducir `PROJECT.md` y `DEV-PROFILE.md`. Hasta entonces `check.py` da el error «falta COMANDOS.md».

## 0.4.0 — 2026-10-26

Actualizar un `dev/` pasa a ser trazable y seguro. Motivo: una actualización reemplazaba en silencio los archivos del paquete (se perdían ediciones a mano) y no había forma de saber qué versión se tenía ni qué había que adaptar en los archivos del proyecto.

### Añadido

- Skill `skills/dev-update/`: comprueba la versión (`--status`), enseña el plan (`--dry-run`), adapta los archivos del proyecto según `MIGRATIONS.md` con tu aprobación, actualiza, revisa los respaldos y verifica con `check.py`. No lleva scripts propios: usa los de `dev-setup`.
- `VERSION` (raíz): fuente única de la versión del paquete. `install.py` la lee (ya no hay constante en el código); `tools/build-skill.py` la copia a `skills/dev-setup/assets/VERSION` y la escribe en `metadata.version` del frontmatter de `dev-setup` y `dev-update` (`--check` también lo compara).
- `MIGRATIONS.md` (raíz, copiado a `assets/` de `dev-setup`): una sección por versión con los archivos del paquete que se reemplazan, la tabla de cambios en archivos del proyecto (acción propuesta y riesgo) y la compatibilidad. Incluye 0.4.0, 0.3.0 y 0.2.0.
- `install.py --status`: `instalada=X nueva=Y estado=al-día|desactualizada|sin-instalar`.
- `install.py --dry-run`: imprime el plan sin escribir (versión, archivos del paquete nuevos, cambiados, sin cambios y editados por ti, archivos de usuario que faltan, adaptadores).
- `dev/.package-manifest`: hash sha256 de cada archivo del paquete instalado. Antes de reemplazar, los archivos que editaste (o, sin manifiesto previo, los que difieren del nuevo) se copian a `dev/.backup/<fecha>-v<versión previa>/` y se listan en la salida. `.backup/` se excluye de git en ambos modos.
- `dev/.package-version` gana `previous=<versión anterior>` cuando es una actualización.
- Documentación: procedimiento para publicar una versión (`docs/01-instalacion.md` §13) y sección de versionado en `docs/04-referencia.md`.

### Cambiado

- La carpeta `template/` del paquete se llama ahora `dev-template/` (lo que se copia como `dev/`). Solo afecta al paquete: en los proyectos ya instalados no cambia nada.
- `check.py` ignora `dev/.backup/` (los respaldos no cuentan para enlaces, numeración ni estructura).
- La skill `dev-setup` remite a `dev-update` cuando el proyecto ya está instalado.
- `docs/01-instalacion.md` §10 (actualizar) reescrita alrededor de `dev-update`.

## 0.3.0 — 2026-10-26

Instalación en un solo lenguaje y guiada por el agente. Motivo: mantener dos instaladores (Bash y PowerShell) duplicaba lógica y fallaba en silencio sin terminal; un instalador en Python es el mismo en todos los sistemas, y una skill puede inferir la configuración que un script no conoce.

### Añadido

- Skill de instalación `skills/dev-setup/` (formato Agent Skills): detecta modo A/B, hace una sola pregunta, ejecuta `scripts/install.py`, propone `PROJECT.md` inspeccionando los repos, entrevista para `DEV-PROFILE.md` y verifica. Se distribuye con `npx skills add <repo>` o copiando la carpeta.
- `install.py`: `python -I install.py --mode A|B --target DIR [--yes] [--git-init] [--adapters claude,cursor]`. Solo biblioteca estándar.
- Playbook n.º 10 `diagnose` (skill `dev-diagnose`) y agente generado `.claude/agents/dev-doctor.md` (solo lectura: Read, Grep, Glob, Bash): ejecuta `check.py --json`, revisa lo que el script no ve y devuelve veredicto, hallazgos y «¿Aplico estos arreglos?». Se invoca con «diagnostica dev/».
- `check.py --json` (`{root, errors, warnings, counts}`); exige el playbook `diagnose` y revisa también `.claude/agents/dev-*.md`.
- `tools/build-skill.py` (`--check` verifica que está al día): regenera `skills/dev-setup/scripts` y `assets` desde `template/`, `adapters/`, `check.py` e `install.py`.
- `dev/.tools/check.py`: el instalador copia el verificador al proyecto y lo actualiza con el paquete.

### Cambiado

- `install.sh` e `install.ps1` se sustituyen por `install.py` (Python 3.9+ y git; mismo comando en Linux, macOS, Windows y WSL). Al terminar ejecuta `check.py`.
- Ahora son 10 playbooks (antes 9); `AGENTS.md` e `INDEX.md` listan `diagnose`.
- Documentación (README, QUICKSTART, INSTALL, `docs/`) reescrita para las dos vías de instalación.

### Corregido

- El instalador sin `--mode` y sin terminal ya no sale en silencio: falla con un mensaje claro (código 2). Actualizar una instalación existente sin terminal exige `--yes`.
- `--help` completa.
- Los punteros `AGENTS.md`/`CLAUDE.md` creados y los adaptadores se excluyen de git en modo A y, si la raíz del workspace es un repo git, también en modo B.
- `record-decision` y `decisions.md` dicen lo mismo sobre el estado de una decisión promovida a ADR.

## 0.2.0 — 2026-10-26

Divulgación progresiva: el agente lee un enrutador corto y solo el playbook de la situación. Motivo: el inicio obligatorio de 0.1.0 pesaba ~20 KB y las guías largas se leían enteras. La investigación de métodos externos (AGENTS.md, Agent Skills, reglas por ruta, OpenSpec, Kiro, Cline Memory Bank, MADR) aconsejó un núcleo portable en markdown con adaptadores finos generados desde una sola fuente.

| Área | Cambio |
|---|---|
| Guías | `guidelines/` pasa a `guidelines/playbooks/` (9 playbooks de una situación cada uno, con `name` y `description`); `AGENTS.md` queda como enrutador; `INDEX.md` gana el «Catálogo de guías». |
| Ciclo de vida | `tasks/archive/` y `bugs/archive/` para lo cerrado; el inicio de sesión no los lee. |
| Adaptadores (opcionales) | `adapters/generate.py` crea skills `dev-<name>`, reglas `.claude/rules` con `paths:` y reglas `.cursor/rules/*.mdc` desde los playbooks, sin duplicar contenido; `CLAUDE.md` raíz pasa a `@AGENTS.md`. |
| Hook | `adapters/claude/hooks/session-start.py` (opcional, no se activa solo): inyecta «Activo ahora» y el estado de `PROJECT.md`/`DEV-PROFILE.md`. |
| Instaladores | `--adapters claude,cursor` / `-Adapters`; idempotentes, regeneran y podan adaptadores obsoletos, recuerdan la elección en `.package-version` (`adapters=`), excluyen los generados en el modo A y eligen un Python que funcione (ignoran shims rotos). |
| `check.py` | Lint de presupuesto (`AGENTS.md` ≤ 60 líneas, playbooks ≤ 120, frontmatter válido, índice si > 100 líneas, referencias a más de un nivel), adaptadores que apuntan a playbooks inexistentes, `archive/` fuera del inicio y tasks archivadas cerradas. `--strict` convierte los excesos de presupuesto en error. |
| Documentación | `INSTALL.md` pasa a la raíz y cubre adaptadores, hook y lint; README raíz con las capas de lectura. |

## 0.1.0 — 2026-10-26

Primera versión, extraída del método de desarrollo agéntico de un proyecto de origen (sin historial ni contenido de ese proyecto).

| Área | Contenido |
|---|---|
| Núcleo | `AGENTS.md`, `PROJECT.md`, `DEV-PROFILE.md` (no versionado, con aviso si queda en `TODO`), `INDEX.md`. |
| Guías | `WORKFLOW.md`, `TASKS.md`, `REPORTING.md`, `DOCS.md`, `DEVELOPMENT.md`, `BUGS.md`, `INSTALL.md`; stacks Python, TypeScript+React, Swift. |
| Plantillas | Task, subtask, decisiones por task, ADR, bug, report, changelog, plan-vs-actual, commit, PR. |
| Herramientas | `install.sh`, `install.ps1` (sustituidos por `install.py` en 0.3.0), `check.py`, `adapters/`. |
| Ejemplo | `examples/mini-proyecto`. |

### Correcciones tras la prueba de humo (misma versión 0.1.0)

| Cambio | Archivos |
|---|---|
| Estados de subtask: `pendiente`, `en curso`, `hecha` (sin commit) y `hecha (commit <hash>)`; `check.py` los valida. | `TASKS.md`, `WORKFLOW.md`, plantillas, `check.py` |
| `TODO` de `PROJECT.md` pasan a aviso; error solo con `check.py --strict`. El agente avisa y propone rellenar `PROJECT.md` antes de escribir código. | `check.py`, `AGENTS.md`, `WORKFLOW.md` §2, `INSTALL.md`, `README.md` |
| Inicio de sesión: lista única de `WORKFLOW.md` §2, report parcial de la subtask en curso, `git` en cada repo afectado, «y lo que cite el brief»; cambios sin commitear coherentes con la subtask en curso se asumen propios. | `AGENTS.md`, `WORKFLOW.md` |
| Cierre: fecha y «Verificado contra» en `docs/README.md`; marcar resueltas las filas de «Qué necesita del desarrollador». | `WORKFLOW.md` §6 |
| Capturas: `reports/task-N/assets/` para evidencia, `tasks/task-N/assets/` para material del brief. | `TASKS.md`, `REPORTING.md` |
| Ejemplo: `bugs/.gitkeep`, plantilla de página y glosario de docs, report parcial de la subtask 2, restricciones críticas repetidas en un brief, perfil listo para renombrar, receta de montaje y aclaración de verificación teórica. | `examples/` |
