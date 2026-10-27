# dev-guidelines

Método de desarrollo agéntico portable (versión 0.7.0): tasks con briefs autocontenidos, informes, documentación técnica como fuente de verdad y un protocolo de sesión para retomar el trabajo con una frase («continúa task-N»).

Se instala como una carpeta `dev/` en tu repo (modo **A**) o junto a varios repos (modo **B**). Pocos tokens: el agente lee un enrutador corto y, de ahí, solo el playbook de la situación.

## Instalar

Necesitas Python 3.10+ y git. Elige **una** de las dos vías.

### Vía 1: con el agente (recomendada)

1. Desde la carpeta de tu proyecto, instala las skills (`dev-setup`, `dev-update` y `dev-feedback`):

```bash
npx skills add TomasCDG/dev-guidelines
```

2. Abre una sesión nueva del agente en esa carpeta y escribe: «instala dev-guidelines en este proyecto». El agente detecta el modo, te hace una pregunta y ejecuta el instalador.

### Vía 2: a mano, sin agente

1. Descarga el paquete en cualquier carpeta fuera de tu proyecto:

```bash
git clone https://github.com/TomasCDG/dev-guidelines.git
```

2. Entra en **tu proyecto** y ejecuta el instalador desde ahí. Ajusta la ruta a donde clonaste:

```bash
cd ruta/a/mi-repo
python ../dev-guidelines/scripts/install.py --mode A --adapters claude
```

- **Modo A** (un solo repo): lo de arriba. `dev/` queda dentro de `mi-repo/`.
- **Modo B** (varios repos, p. ej. `front/` y `back/`): entra en la carpeta que los contiene y usa `--mode B --git-init`.
- Si `python` no existe, prueba `python3` o `py`. En Windows, `..\dev-guidelines\scripts\install.py`.
- Sin `--mode` el instalador te lo pregunta. Para ver qué haría sin escribir nada, añade `--dry-run`.

Al terminar corre un chequeo y debe decir `0 errores`. Siguientes pasos y detalle: [docs/00-quickstart.md](./docs/00-quickstart.md) (5 minutos) y [docs/README.md](./docs/README.md) (índice).

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
