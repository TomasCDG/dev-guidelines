# Referencia

**Fecha:** 27 de octubre de 2026 · **Versión del paquete:** 0.7.0

## Contenido

1. [Mapa del paquete](#1-mapa-del-paquete)
2. [Mapa de la carpeta dev/ instalada](#2-mapa-de-la-carpeta-dev-instalada)
3. [Playbooks](#3-playbooks)
4. [Plantillas](#4-plantillas)
5. [Estados](#5-estados)
6. [Frases de entrada](#6-frases-de-entrada)
7. [Convenciones de nombres y numeración](#7-convenciones-de-nombres-y-numeración)
8. [Qué comprueba check.py](#8-qué-comprueba-checkpy)
9. [Cuánto contexto se lee y cuándo](#9-cuánto-contexto-se-lee-y-cuándo)
10. [Versionado y publicación](#10-versionado-y-publicación)
11. [Glosario](#11-glosario)

## 1. Mapa del paquete

| Ruta (en `dev-guidelines/`) | Función |
|---|---|
| `dev-template/` | Lo que se copia como `dev/` en un proyecto |
| `README.md` | Puerta de entrada: qué es, cómo instalar y dónde está qué |
| `release/VERSION` | Versión del paquete (`X.Y.Z`); fuente única que lee `install.py` |
| `release/CHANGELOG.md` | Versiones del paquete |
| `release/MIGRATIONS.md` | Por versión: qué se reemplaza y cómo adaptar los archivos del proyecto; lo usa `dev-update` |
| `scripts/install.py` | Instalación y actualización (Python, solo biblioteca estándar); `--status`, `--dry-run`, respaldo en `dev/.backup/`; copia `check.py` a `dev/.tools/` y lo ejecuta al final |
| `scripts/migrate.py` | Migración determinista de un `dev/` 0.5.0 a la estructura 0.6.0 (`work/`, `docs/decisions/`, `method/`): mueve carpetas, reescribe enlaces relativos, `--dry-run`; se copia a `skills/dev-setup/scripts/` |
| `scripts/check.py` | Verificador de estructura, enlaces, alias y presupuesto; `--json` para máquinas |
| `scripts/build-skill.py` | Regenera `skills/dev-setup/` desde `release/VERSION`, `release/MIGRATIONS.md`, `dev-template/`, `scripts/adapters/`, `scripts/check.py`, `scripts/install.py` y `scripts/migrate.py`, y escribe `metadata.version` en las tres skills (`--check` verifica que está al día) |
| `scripts/adapters/generate.py` | Genera skills, reglas y el agente `dev-doctor` desde los playbooks |
| `scripts/adapters/claude/hooks/` | Hook `SessionStart` y su fragmento de configuración |
| `scripts/adapters/AGENTS.md`, `scripts/adapters/CLAUDE.md` | Apuntes que se copian a la raíz del proyecto |
| `scripts/adapters/gitignore-modo-A.txt`, `gitignore-modo-B.txt` | Reglas de exclusión de git por modo |
| `skills/dev-setup/` | Skill de instalación (`SKILL.md`, `scripts/install.py`, `assets/`); `scripts/` y `assets/` son copia generada |
| `skills/dev-update/` | Skill de actualización (solo `SKILL.md`); usa el instalador y `MIGRATIONS.md` de `dev-setup` |
| `skills/dev-feedback/` | Skill de feedback del método (solo `SKILL.md`): convierte `dev/RETRO.md` en propuestas de cambio al paquete |
| `docs/` | Esta documentación para humanos (empieza por `00-quickstart.md`) |
| `examples/mini-proyecto/` | Proyecto ficticio con una task en curso |
| `historia/` | Memoria del porqué: `diseno.md` (problemas y decisiones de origen) y `retro-aplicadas.md` (mejoras que llegaron por retro) |
| `release/ROADMAP.md` | Backlog de funcionalidades futuras del paquete (no son compromisos) |

## 2. Mapa de la carpeta dev/ instalada

| Ruta | Qué contiene | Quién la modifica | Se reemplaza al actualizar |
|---|---|---|---|
| `AGENTS.md` | Enrutador de ≤ 60 líneas: qué playbook leer en cada situación | Paquete | Sí |
| `PROJECT.md` | Núcleo del proyecto: alias, idiomas, restricciones, zonas intocables (se lee siempre) | Tú | No |
| `COMANDOS.md` | Stacks activos, comandos, commits y PR (se lee bajo demanda) | Tú | No |
| `DEV-PROFILE.md` | Preferencias personales, 5 filas opcionales (no se versiona) | Tú | No |
| `INDEX.md` | Estado vivo y catálogo de guías | El agente | No |
| `RETRO.md` | Retros del proyecto sobre el método: una fila por task cerrada | El agente y tú | No (se crea si falta) |
| `method/playbooks/` | 10 guías, una por situación | Paquete | Sí |
| `method/stacks/` | Packs por tecnología | Paquete | Sí |
| `method/templates/` | Plantillas de documentos | Paquete | Sí |
| `work/tasks/task-N-nombre/` | README, `decisions.md`, `subtask-N-*.md`, `assets/` | El agente y tú | No |
| `work/tasks/archive/` | Tasks cerradas | El agente | No |
| `work/bugs/bug-N-nombre/` | Igual que una task, para un bug | El agente y tú | No |
| `docs/` | Verdad técnica del estado actual, por categoría | El agente | No |
| `docs/decisions/` | ADR globales | El agente y tú | No |
| `work/reports/task-N-nombre/` | Informes por subtask, `00-plan-vs-actual.md`, `assets/` | El agente | No |
| `work/changelogs/task-N-nombre/` | Cambios de código por subtask | El agente | No |
| `.adapters/` | Hook y fragmento de ajustes (solo con `--adapters claude`) | Generado | Se regenera |
| `.tools/check.py` | Copia del verificador para usarlo sin el paquete | Instalador | Sí |
| `.package-version` | `version`, `installed`, `mode`, `adapters` y, tras actualizar, `previous` | Instalador | Sí |
| `.package-manifest` | `sha256  ruta` de cada archivo del paquete instalado | Instalador | Sí |
| `.feedback/AAAA-MM-DD-feedback.md` | Propuestas de cambio al paquete que redactó `dev-feedback` y validaste (excluido de git) | La skill `dev-feedback` | No |
| `.backup/<fecha>-v<versión>/` | Copia de los archivos del paquete que habías editado, hecha antes de actualizar | Instalador | No (se crea si hace falta; excluido de git) |

Fuera de `dev/`, en la raíz del proyecto: `AGENTS.md` y `CLAUDE.md` (punteros) y, con adaptadores, `.claude/skills/dev-*/`, `.claude/rules/dev-*.md`, `.claude/agents/dev-doctor.md` y `.cursor/rules/dev-*.mdc`.

## 3. Playbooks

Archivo: `dev/method/playbooks/<nombre>.md`. Skill (si hay adaptador): `dev-<nombre>`. Son 10. Cada uno tiene `name` y `description` en el frontmatter y ≤ 120 líneas.

| Playbook | Para qué | Cuándo se usa | Plantillas que usa |
|---|---|---|---|
| [`start-session`](../dev-template/method/playbooks/start-session.md) | Retomar el trabajo: resuelve la frase, lee lo mínimo, verifica el repo | «continúa task-N», «siguiente», «bug-N», brief adjunto | — |
| [`close-session`](../dev-template/method/playbooks/close-session.md) | Lista única de cierre; cierre y archivo de una task; retro en `RETRO.md` | Al terminar o interrumpir una subtask; al cerrar la última | — |
| [`write-task`](../dev-template/method/playbooks/write-task.md) | Planificar una task y redactar README y briefs | Planear un desarrollo; crear o editar subtasks; cambiar estados | `task-README`, `subtask` |
| [`write-report`](../dev-template/method/playbooks/write-report.md) | Report, changelog derivado y plan-vs-actual | Cerrar una subtask; terminar una investigación | `report`, `changelog`, `plan-vs-actual` |
| [`update-docs`](../dev-template/method/playbooks/update-docs.md) | Decidir dónde va cada conocimiento; mantener `docs/` fresco | Tocar un área documentada; cambiar comportamiento; cerrar un cambio | `docs/_page-template.md` |
| [`fix-bug`](../dev-template/method/playbooks/fix-bug.md) | Planificar y corregir un bug con prueba que falla antes | Corregir un error en código existente | `bug-README`, `bug-subtask` |
| [`develop-code`](../dev-template/method/playbooks/develop-code.md) | Código limpio, arquitectura, testing y stacks activos | Escribir, modificar o probar código | — |
| [`record-decision`](../dev-template/method/playbooks/record-decision.md) | Registrar decisiones y promover a ADR | Aprobar o tomar por defecto una decisión; cerrar una task | `decisions`, `adr` |
| [`commit-pr`](../dev-template/method/playbooks/commit-pr.md) | Mensaje de commit por subtask e informe de PR por task | Cerrar subtask o task; pedir commit | `commit`, `pr` |
| [`diagnose`](../dev-template/method/playbooks/diagnose.md) | Diagnosticar la salud de `dev/` con `check.py --json` y una revisión manual; solo propone | «diagnostica dev/»; tras actualizar; al cerrar una task; si algo parece inconsistente | — |

El agente `dev-doctor` (`.claude/agents/dev-doctor.md`, generado con `--adapters claude`) ejecuta `diagnose`: solo lectura (Read, Grep, Glob, Bash).

## 4. Plantillas

En `dev/method/templates/`. Cada una lleva comentarios `<!-- -->` que indican qué rellenar.

| Plantilla | Se copia a |
|---|---|
| `task-README.md` | `work/tasks/task-N-nombre/README.md` |
| `subtask.md` | `work/tasks/task-N-nombre/subtask-N-descripcion.md` |
| `decisions.md` | `work/tasks/task-N-nombre/decisions.md` |
| `adr.md` | `docs/decisions/ADR-NNN-nombre.md` |
| `bug-README.md`, `bug-subtask.md` | `work/bugs/bug-N-nombre/README.md` y `subtask-N-*.md` |
| `report.md` | `work/reports/task-N-nombre/subtask-N-descripcion.md` |
| `changelog.md` | `work/changelogs/task-N-nombre/subtask-N-descripcion.md` |
| `plan-vs-actual.md` | `work/reports/task-N-nombre/00-plan-vs-actual.md` |
| `commit.md`, `pr.md` | Guías para el mensaje de commit y el informe de PR |

## 5. Estados

| Objeto | Estados | Dónde se anota |
|---|---|---|
| **Subtask** | `pendiente` · `en curso` · `hecha` (sin commit) · `hecha (commit <hash>)` | Tabla del README de la task |
| **Task** | `borrador` · `en curso` · `pausada` · `hecha (archivada)` | `INDEX.md` §3 |
| **Bug** | Igual que una task | `INDEX.md` §4 |
| **Decisión** | `vigente` · `reemplazada por <ID>` · `promovida a ADR-NNN` | `decisions.md` |
| **Página de docs** | `vigente` · `obsoleta` | Cabecera de la página y `docs/README.md` |
| **Retro** | «Retro pendiente»: `sí` / `no` | `INDEX.md` §3 |
| **Fila de `RETRO.md`** | `pendiente` · `propuesta` · `enviada` · `descartada` | `RETRO.md` |
| **Funcionalidad del roadmap** | `idea` · `planeada` · `en curso` · `hecha` · `descartada` | `release/ROADMAP.md` |

`pendiente` no significa «no hay trabajo hecho»: el agente verifica el repo, y si el trabajo ya está lo trata como `hecha` y corrige el índice.

## 6. Frases de entrada

| Frase | Resuelve a |
|---|---|
| `continúa task-N` | La primera subtask `en curso` de esa task o, si no hay, la primera `pendiente` con dependencias `hecha` |
| `siguiente` | La de «Activo ahora» en `INDEX.md` (pregunta si está vacío) |
| `subtask N de task-M` | Esa subtask, avisando si sus dependencias no están hechas |
| `bug-N` | La subtask correspondiente en `work/bugs/bug-N-*/`, con el playbook `fix-bug` |
| Brief adjunto | Ese brief manda; se contrasta con `INDEX.md` |

## 7. Convenciones de nombres y numeración

| Elemento | Convención |
|---|---|
| Task | `task-N-nombre-en-minusculas-con-guiones` |
| Bug | `bug-N-nombre` |
| Subtask | `subtask-N-descripcion.md`, consecutivas dentro de la task |
| Numeración | Una sola secuencia por proyecto para tasks y otra para bugs; **no se reinicia ni se reutiliza**, ni siquiera tras archivar |
| Decisiones de task | `T<N>-D1`, `T<N>-D2`… (el prefijo evita choques entre tasks) |
| Restricciones | Proyecto: `C1`, `C2`… (`PROJECT.md` §3); de task: `T<N>-C1`… |
| ADR | `ADR-NNN-titulo.md`, numeración consecutiva única |
| Alias de repo | `@nombre/ruta/archivo.ext:línea`, declarado en `PROJECT.md` §1 |
| Reports | `work/reports/task-N-nombre/subtask-N-descripcion.md`; plan-vs-actual como `00-plan-vs-actual.md` |
| Capturas de un report | `work/reports/task-N-nombre/assets/` |
| Material de origen de un brief | `work/tasks/task-N-nombre/assets/` |
| Skills generadas | `dev-<playbook>` |
| Idiomas | Los de `PROJECT.md` §2 |
| Fechas | `AAAA-MM-DD` |

## 8. Qué comprueba check.py

`python -I dev/.tools/check.py [RUTA_A_DEV] [--strict] [--json]`. Salida `0` sin errores, `1` con errores, `2` uso incorrecto. Con `--json` imprime `{root, errors: [{where, msg}], warnings, counts}` en vez de texto.

| Comprobación | Resultado si falla |
|---|---|
| Archivos y carpetas obligatorios, y los 10 playbooks (incluido `diagnose`) | Error |
| Frontmatter de cada playbook: `name` igual al archivo, `description` ≤ 300 caracteres | Error |
| `AGENTS.md` ≤ 60 líneas y cada playbook ≤ 120 | Aviso (Error con `--strict`) |
| Playbook de más de 100 líneas sin índice | Aviso |
| Referencia de apoyo que encadena a otra (más de un nivel) | Aviso |
| Adaptador generado (`.claude/skills`, `.claude/rules`, `.claude/agents/dev-*.md`, `.cursor/rules`) que apunta a un playbook inexistente | Error |
| El inicio (`AGENTS.md`, `start-session`, «Activo ahora») enlaza a `archive/` | Aviso |
| Task archivada sin `README.md` | Error |
| Task archivada con subtasks no hechas | Aviso |
| Falta `work/tasks/archive/` | Aviso |
| Numeración única de `task-N` y `bug-N` (incluidas las archivadas) y de `subtask-N` | Error |
| Enlaces relativos entre archivos (se ignoran `method/templates/` y la plantilla de docs) | Error |
| Anclas de enlaces (`#seccion`) | Aviso |
| Alias `@repo/` usados en tasks, bugs, reports, docs, decisiones y changelogs, contra `PROJECT.md` §1 | Error |
| Alias cuya ruta no existe desde `dev/` | Aviso |
| Estado de subtask en el README: `pendiente`, `en curso`, `hecha`, `hecha (commit <hash>)` | Error |
| `TODO` literal en `PROJECT.md` o `COMANDOS.md` (las plantillas usan `—`) | Aviso (Error con `--strict`) |
| `TODO` literal en `DEV-PROFILE.md` | Aviso |
| Falta `COMANDOS.md`; `PROJECT.md` con secciones anteriores a 0.5.0 (Stacks activos, Comandos del proyecto, Modelos sugeridos) | Error |
| `dev/` con la estructura anterior a 0.6.0 (`guidelines/` o `tasks/` en la raíz y sin `method/`): el verificador se detiene tras este error | Error |
| Tasks y bugs que no aparecen en `INDEX.md` | Aviso |
| Reports, changelogs y docs sin fecha al inicio o largos sin índice | Aviso |
| `RETRO.md` (si existe) con columnas distintas o un estado inválido | Aviso |
| Task sin `decisions.md`, falta de `.package-version` | Aviso |

## 9. Cuánto contexto se lee y cuándo

El diseño busca que el agente lea poco y solo lo necesario (divulgación progresiva):

| Capa | Qué | Cuándo |
|---|---|---|
| 1. Siempre | `AGENTS.md` (enrutador), `PROJECT.md`, `DEV-PROFILE.md`, `INDEX.md` («Activo ahora») | Al empezar |
| 2. Bajo demanda | `COMANDOS.md` | Al escribir o probar código o al commitear |
| 2. Bajo demanda | Un playbook de ~15 a 80 líneas (y solo las plantillas que ese playbook enlaza) | Cuando la situación lo pide |
| 3. Opcional | Skills, reglas y hook generados | Si instalaste adaptadores; son envoltorios que apuntan a la capa 2 |

Tamaños de referencia por archivo y total al empezar: [02-configuracion.md §6](./02-configuracion.md#6-qué-se-lee-siempre-y-qué-bajo-demanda). Los playbooks miden entre 13 y 80 líneas. No se leen `work/tasks/archive/` ni reports antiguos salvo que un brief los cite.

## 10. Versionado y publicación

| Elemento | Dónde | Notas |
|---|---|---|
| Versión del paquete | `release/VERSION` | Un solo número `X.Y.Z`. Fuente única: `install.py` la lee de ahí; no hay constante en el código |
| Versión en la skill | `assets/VERSION` y `metadata.version` de las tres skills | Los escribe `scripts/build-skill.py`; `--check` los compara |
| Versión instalada | `dev/.package-version` (`version`, y `previous` tras actualizar) | `install.py --status` la compara con la del paquete |
| Historial de cambios | `release/CHANGELOG.md` | Una entrada por versión |
| Adaptación de proyectos | `release/MIGRATIONS.md` | Una sección `## X.Y.Z` por versión, de la más nueva a la más antigua; la lee `dev-update` |

Para publicar: sube `release/VERSION`, añade la entrada a `release/CHANGELOG.md` y la sección a `release/MIGRATIONS.md`, ejecuta `python -I scripts/build-skill.py` y verifica con `--check`. Paso a paso en [01-instalacion.md §13](./01-instalacion.md#13-mantener-el-paquete-publicar-una-versión).

## 11. Glosario

| Término | Significado |
|---|---|
| Task | Carpeta con el plan completo de un desarrollo |
| Subtask | Cada markdown dentro de una task; una unidad de trabajo de una sesión |
| Brief | El markdown de una subtask: traspaso autocontenido para un agente sin memoria |
| Playbook | Guía de una sola situación, con frontmatter `name` y `description` |
| Skill | Envoltorio de Claude Code que apunta a un playbook y se activa por su descripción |
| `dev-setup` | Skill de instalación del paquete: instala, configura y verifica |
| `dev-update` | Skill de actualización: actualiza `dev/`, adapta los archivos del proyecto según `MIGRATIONS.md` y verifica |
| `dev-feedback` | Skill que convierte las filas `pendiente` de `RETRO.md` en propuestas de cambio al paquete |
| Manifiesto | `dev/.package-manifest`: hashes de los archivos del paquete instalados, para detectar ediciones |
| `--dry-run` / `--status` | Opciones de `install.py`: imprimir el plan sin escribir / comparar versión instalada y nueva |
| `dev-doctor` | Agente de solo lectura que diagnostica la salud de `dev/` |
| Regla (rule) | Archivo de Claude Code o Cursor que carga un playbook al tocar ciertas rutas o por su descripción |
| Hook | Script que Claude Code ejecuta en un evento (aquí, `SessionStart`) |
| Adaptador | Skill, regla o hook generado desde los playbooks; nunca se edita a mano |
| Enrutador | `AGENTS.md`: solo dice qué playbook leer, no contiene las reglas |
| Divulgación progresiva | Leer solo lo necesario en cada momento, de lo más corto a lo más detallado |
| Frontmatter | Bloque de metadatos `---` … `---` al inicio de un markdown |
| Alias de repo | Atajo `@nombre` a la ruta de un repo, declarado en `PROJECT.md` §2 |
| ADR | *Architecture Decision Record*: decisión global, un archivo por decisión |
| Docs (dev) | Hechos verificables del sistema, fuente de verdad para agentes; distinto de la documentación oficial |
| Report | Informe para el desarrollador con el resultado de una subtask |
| Changelog | Lista de cambios de código funcional, derivada del report |
| Plan vs realidad | Informe que compara lo planeado con lo construido |
| Frescura | «Verificado contra» y estado `vigente`/`obsoleta` de una página de docs |
| Retro | Fila de `dev/RETRO.md` al cerrar una task: qué funcionó, qué falló y qué cambiarías del método |
| Feedback | Propuestas de cambio al paquete redactadas por `dev-feedback` a partir de las retros; se guardan en `dev/.feedback/` |
| Roadmap | `release/ROADMAP.md`: backlog de funcionalidades futuras del paquete, sin compromiso |
| Historia | Carpeta `historia/`: el porqué del diseño y las retros ya aplicadas |
| Modo A / modo B | `dev/` dentro del repo / `dev/` junto a varios repos |
| `—` | Marca de «sin definir» en las plantillas; no es un aviso. Si el agente necesita el dato, lo pregunta en ese momento |
| `TODO` | Texto literal que `check.py` avisa si alguien lo deja en `PROJECT.md`, `COMANDOS.md` o `DEV-PROFILE.md` |
| `--strict` | Opción de `check.py` que convierte ciertos avisos en errores |
| `--json` | Opción de `check.py` que imprime el resultado como JSON |
