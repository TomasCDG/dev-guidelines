# Desarrollo agéntico — enrutador

`dev/` guarda planes, informes, decisiones y docs técnicos. Este archivo solo enruta: lee el playbook de lo que vas a hacer, no todos. El `CLAUDE.md` de la raíz del repo contiene solo `@AGENTS.md`.

## Al empezar (léelo todo, es corto)

- [PROJECT.md](./PROJECT.md): repos y alias `@repo/`, idiomas, restricciones, zonas intocables.
- [DEV-PROFILE.md](./DEV-PROFILE.md): preferencias personales. Opcional; un campo vacío (`—`) no es un aviso: usa el valor por defecto.
- [INDEX.md](./INDEX.md): solo «Activo ahora» (estado vivo); el catálogo de guías, si lo necesitas.

**Bajo demanda:** [COMANDOS.md](./COMANDOS.md) (stacks, comandos, commits y PR) solo cuando escribas o pruebes código o commitees. Si necesitas un dato vacío, pregúntalo una vez, propón un valor y anótalo en el archivo que corresponda.

## Playbooks

Cada uno está en `method/playbooks/<nombre>.md`. Si tu herramienta tiene skills, invoca la skill `dev-<nombre>`; si no, lee el archivo.

| Si vas a… | Playbook |
|---|---|
| Empezar o retomar («continúa task-N», «siguiente», «bug-N») | [start-session](./method/playbooks/start-session.md) |
| Terminar una subtask o cerrar una task | [close-session](./method/playbooks/close-session.md) |
| Planificar una task o redactar subtasks | [write-task](./method/playbooks/write-task.md) |
| Redactar un report o changelog | [write-report](./method/playbooks/write-report.md) |
| Leer, crear o actualizar docs técnicos | [update-docs](./method/playbooks/update-docs.md) |
| Corregir un bug | [fix-bug](./method/playbooks/fix-bug.md) |
| Escribir o probar código | [develop-code](./method/playbooks/develop-code.md) |
| Registrar una decisión | [record-decision](./method/playbooks/record-decision.md) |
| Redactar un commit o un informe de PR | [commit-pr](./method/playbooks/commit-pr.md) |
| Revisar la salud de `dev/` («diagnostica», «audita dev») | [diagnose](./method/playbooks/diagnose.md) |

Las plantillas están en `method/templates/` y las enlaza el playbook que las usa.

## Estructura

| Ruta | Contenido |
|---|---|
| `work/tasks/` · `work/bugs/` | Un plan por carpeta (`task-N-…`, `bug-N-…`); las cerradas van a `archive/`. |
| `work/reports/` · `work/changelogs/` | Historial por task o bug. |
| `docs/` | Verdad técnica del estado actual; sin planes ni notas de sesión. |
| `docs/decisions/` | Decisiones globales (ADR). |
| `method/` | El método (playbooks, stacks, plantillas): lo reemplaza el paquete al actualizar; no lo edites. |

## Reglas innegociables

- **Verifica el repo real**; no des por hecho algo porque `INDEX.md` o un brief lo digan.
- **Docs ≠ trabajo:** planes, pendientes y reflexiones van a `work/tasks/`, `work/reports/` o `INDEX.md`, nunca a `docs/`.
- **Un solo escritor por archivo compartido.**
- **Pregunta solo lo necesario**, una vez, con un valor por defecto propuesto.
- **Cierra siempre** con la lista de [close-session](./method/playbooks/close-session.md).
- No explores `work/tasks/archive/` ni `work/reports/` antiguos salvo que el brief lo cite.
- Idioma de docs y UI: el de `PROJECT.md` §2. Explicaciones, glosarios y formato de la respuesta final: según `DEV-PROFILE.md`.
