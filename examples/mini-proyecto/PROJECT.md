# PROJECT — núcleo del proyecto

Versionado, lo lee el agente en cada sesión. Stacks, comandos y commits: [COMANDOS.md](./COMANDOS.md). Lo personal: [DEV-PROFILE.md](./DEV-PROFILE.md). `—` = sin definir.

## 1. Repos y alias

Briefs y docs enlazan al código con `@alias/ruta/archivo.ext:línea`.

| Alias | Ruta relativa a `dev/` | Descripción |
|---|---|---|
| `@back` | `../back` | API HTTP en Python (FastAPI) |
| `@front` | `../front` | Interfaz web en React + TypeScript |

Modo B: `dev/` junto a `back/` y `front/`.

## 2. Idiomas

| Qué | Idioma |
|---|---|
| Documentación (`docs/`, reports, briefs) | Español |
| Interfaz del producto | Español |
| Código y commits | Inglés |

## 3. Restricciones

Valen para toda task; se citan por ID (`C1`…).

| ID | Restricción |
|---|---|
| C1 | La API solo escucha en `127.0.0.1` (ver [ADR-001](./docs/decisions/ADR-001-solo-localhost.md)) |
| C2 | Sin dependencias nuevas sin aprobación del desarrollador |
| C3 | Los cambios de la API son aditivos: no se quitan ni renombran campos publicados |

## 4. Zonas intocables

Sin autorización expresa del desarrollador no se modifican.

| Ruta (con alias) | Motivo |
|---|---|
| `@back/migrations/` | Migraciones ya aplicadas; se añaden nuevas, no se editan |
