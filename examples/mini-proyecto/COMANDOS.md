# COMANDOS — stacks, comandos y commits

Lo leen develop-code, fix-bug y commit-pr cuando lo necesitan (no al empezar la sesión). Se rellena con lo que se encuentra en el proyecto; `—` = sin definir (el agente lo pregunta cuando lo necesita).

## 1. Stacks activos

Packs de `method/stacks/` que aplican.

| Stack | Activo |
|---|---|
| `python.md` | sí |
| `typescript-react.md` | sí |
| `swift.md` | no |

## 2. Comandos

Valen en cualquier máquina. Los de una máquina concreta (WSL, rutas, puertos) van en `docs/`.

| Acción | Comando | Repo (alias) |
|---|---|---|
| Instalar dependencias | `pip install -e .[dev]` | `@back` |
| Instalar dependencias | `npm install` | `@front` |
| Pruebas | `pytest` | `@back` |
| Pruebas | `npm test` | `@front` |
| Lint | `ruff check .` | `@back` |
| Type-check | `mypy src` · `npm run typecheck` | `@back` · `@front` |
| Ejecutar en desarrollo | `uvicorn pendientes.main:app --reload` | `@back` |
| Ejecutar en desarrollo | `npm run dev` | `@front` |
| Build | — | |

## 3. Commits y pull requests

| Campo | Valor |
|---|---|
| Formato de commit | Conventional Commits `tipo(ámbito): resumen` |
| Cuándo se commitea | Solo cuando el desarrollador lo pide |
| Un commit por | subtask |
| Informe de PR al cerrar la task | sí |
| Multirepo | Un commit por repo afectado, con el mismo ID de task en el mensaje. |

La atribución de IA es personal: fila «Atribución de IA» de [DEV-PROFILE.md](./DEV-PROFILE.md).
