# ADR-001 — La API solo escucha en 127.0.0.1

**Fecha:** 2026-03-01
**Estado:** vigente
**Origen:** T1-D1 ([decisions.md de la task 1](../../work/tasks/task-1-listado-tareas/decisions.md))
**Decide:** desarrollador

## Contexto

La API no tiene autenticación y guarda datos personales (las tareas). Se usa en una sola máquina, junto a la UI.

## Decisión

El servicio se enlaza únicamente a `127.0.0.1`. Ninguna task puede abrirlo a otras interfaces sin una decisión nueva que reemplace a esta.

## Alternativas consideradas

| Alternativa | Ventajas | Desventajas |
|---|---|---|
| Escuchar en `0.0.0.0` con token | Acceso desde otros equipos | Exige diseñar autenticación; superficie de ataque mayor. |
| Solo `127.0.0.1` | Sin autenticación necesaria | Solo uso local. |

## Consecuencias

- Las pruebas y la UI usan `http://127.0.0.1:8000`.
- Cualquier cambio de interfaz o de despliegue remoto requiere un ADR nuevo.
- Riesgo: otro proceso local podría acceder; se acepta para un uso personal.

## Referencias

- Restricción `C1` en [PROJECT.md](../../PROJECT.md).
- Página [docs/contracts/api-tareas.md](../contracts/api-tareas.md).
- Código: `@back/src/pendientes/main.py`.
