# Ejemplos

## `mini-proyecto/`

Una carpeta `dev/` ya usada, de un proyecto ficticio («Pendientes»: API en Python + UI web), en modo **B** (junto a dos repos, `@back` y `@front`). No contiene nada de ningún proyecto real.

| Qué mirar | Dónde | Qué ilustra |
|---|---|---|
| Configuración rellenada | [PROJECT.md](./mini-proyecto/config/PROJECT.md), [ENTORNO.md](./mini-proyecto/config/ENTORNO.md), [COMANDOS.md](./mini-proyecto/config/COMANDOS.md), [DEV-PROFILE.md.example](./mini-proyecto/config/DEV-PROFILE.md.example) | Núcleo (alias, idiomas, restricciones `C1…`, zonas intocables), herramientas por etapa (API y front locales, regla `E1`), comandos bajo demanda y perfil personal de 5 filas (en un proyecto real el perfil no se versiona). |
| Estado vivo | [INDEX.md](./mini-proyecto/work/INDEX.md) | Una task en curso: es lo que lee el agente con «continúa task-1». |
| Task completa | [work/tasks/task-1-listado-tareas/](./mini-proyecto/work/tasks/task-1-listado-tareas/README.md) | README con estado por subtask, decisiones con IDs `T1-…`, dos subtasks (la API hecha y la UI en curso, separadas por el corte D2) con la columna «Corte». |
| Cierre de una subtask | [report](./mini-proyecto/work/reports/task-1-listado-tareas/subtask-1-api.md) y [changelog](./mini-proyecto/work/changelogs/task-1-listado-tareas/subtask-1-api.md) | El changelog reproduce la tabla «Qué cambió» del report. |
| Retro del proyecto | [RETRO.md](./mini-proyecto/work/RETRO.md) | Una fila `pendiente` de muestra (ficticia): lo que `dev-feedback` procesaría. |
| Decisión global | [docs/decisions/ADR-001](./mini-proyecto/docs/decisions/ADR-001-solo-localhost.md) | Promoción de T1-D1 a ADR. |
| Docs técnicos | [docs/README.md](./mini-proyecto/docs/README.md) | Índice con «léela cuando…», cabecera de frescura en cada página. |

El método (`method/`: playbooks, stacks y plantillas) no se copia aquí: está en `dev-template/`. El agente entra por `AGENTS.md` (enrutador), lee `INDEX.md` («Activo ahora» y catálogo) y abre solo el playbook que necesita.

## Montar el ejemplo para probarlo

1. Copia `mini-proyecto/` a una carpeta temporal y llámala `dev/`.
2. Copia dentro de `dev/` desde `dev-template/`: `AGENTS.md` y `method/` (incluye `playbooks/`, `stacks/` y `templates/`).
3. Renombra `DEV-PROFILE.md.example` a `DEV-PROFILE.md`.
4. Desde la raíz del paquete, ejecuta `python -I scripts/check.py <ruta>/dev`. Se espera 0 errores; avisan que `.package-version` no existe y que los alias `@back` y `@front` no existen desde esa ruta (los repos son ficticios).
5. En una sesión nueva, di «continúa task-1»: el agente sigue el playbook `start-session` y debe abrir la subtask 2 leyendo `INDEX.md`, el README de la task, el brief y los reports (el de la subtask 1 y el parcial de la 2). Al cerrar la task usaría `close-session`, que la mueve a `work/tasks/archive/` (ya existe vacía en el ejemplo).

**La verificación contra el repo real es teórica en el ejemplo:** los repos `back/` y `front/` y el commit `a1b2c3d` no existen. Sirve para ensayar la lectura documental y el cierre, no los comandos `git`.
