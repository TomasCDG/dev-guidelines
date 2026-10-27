# dev-guidelines

Método de desarrollo agéntico portable (versión 0.7.0): tasks con briefs autocontenidos, informes, documentación técnica como fuente de verdad y un protocolo de sesión para retomar el trabajo con una frase («continúa task-N»).

Se instala como una carpeta `dev/` en tu repo (modo **A**) o junto a varios repos (modo **B**). Pocos tokens: el agente lee un enrutador corto y, de ahí, solo el playbook de la situación.

## Instalar (Python 3.10+ y git)

- **Con la skill `dev-setup` (recomendada):** `npx skills add <repo>` instala tres skills (`dev-setup`, `dev-update` y `dev-feedback`). Dile al agente «instala dev-guidelines en este proyecto».
- **Directo:**

```bash
python -I scripts/install.py --mode A|B --target /ruta/a/mi-repo --adapters claude
```

Siguientes pasos y detalle: [docs/00-quickstart.md](./docs/00-quickstart.md) (5 minutos) y [docs/README.md](./docs/README.md) (índice).

## Skills

| Skill | Para qué |
|---|---|
| `dev-setup` | Instalar el método en un proyecto |
| `dev-update` | Actualizar un `dev/` ya instalado |
| `dev-feedback` | Convertir las retros de `dev/RETRO.md` en propuestas de mejora del paquete |

## Dónde está qué

| Carpeta | Qué contiene |
|---|---|
| `dev-template/` | Lo que se copia como `dev/` en un proyecto |
| `skills/` | Las tres skills; el bundle de `dev-setup` se genera |
| `scripts/` | `install.py`, `check.py`, `migrate.py`, `build-skill.py` y `adapters/` |
| `docs/` | Guías para personas: quickstart, instalación, configuración, uso y referencia |
| `examples/` | `mini-proyecto/`, una `dev/` ya usada |
| `historia/` | El porqué del diseño y las retros ya aplicadas |
| `release/` | `VERSION`, `CHANGELOG.md`, `MIGRATIONS.md` y [`ROADMAP.md`](./release/ROADMAP.md) (backlog de funcionalidades futuras) |
