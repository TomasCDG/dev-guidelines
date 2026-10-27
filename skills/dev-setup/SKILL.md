---
name: dev-setup
description: Instala el método de desarrollo agéntico (carpeta dev/ con work/, docs/ y method/) en un proyecto, configura PROJECT.md, COMANDOS.md y DEV-PROFILE.md y verifica con check.py. Úsala para instalar dev-guidelines; para actualizar un dev/ existente está dev-update.
metadata:
  version: "0.7.0"
---

# Instalar dev-guidelines en un proyecto

El copiado lo hace `scripts/install.py` (determinista). **Nunca copies los archivos a mano**: ejecuta el script. Tu trabajo es decidir los parámetros, configurar lo que el script no puede saber y verificar.

Los recursos viajan junto a esta skill: `scripts/install.py`, `scripts/migrate.py` (solo lo usa `dev-update`) y `assets/` (`dev-template/`, adaptadores, `check.py`, `VERSION`, `MIGRATIONS.md`). Usa la ruta de esta skill, no la del proyecto.

**Para actualizar un proyecto ya instalado usa la skill `dev-update`** (hermana de esta): comprueba la versión, adapta los archivos del proyecto con `MIGRATIONS.md` y respalda lo que editaste. Esta skill es para instalar.

## 1. Detectar el contexto

Mira el directorio de trabajo, sin preguntar todavía:

| Observas | Modo propuesto |
|---|---|
| La carpeta es un repo git y no contiene otros repos | **A** (`dev/` dentro del repo) |
| La carpeta contiene dos o más repos git (por ejemplo `front/` y `back/`) | **B** (`dev/` junto a ellos) |
| Existe `dev/` con `.package-version` | **Ya instalado**: no reinstales; remite a `dev-update` |

Si ya está instalado, lee `dev/.package-version`, di qué versión hay y, si el desarrollador quiere actualizar, **usa la skill `dev-update`** (o, si no está disponible, pídele que la instale junto a esta). No ejecutes tú la actualización desde aquí. Si dice que quiere reinstalar o repetir la instalación (por ejemplo para añadir adaptadores), puedes seguir con el paso 3 con `--status` y `--dry-run` antes de ejecutar.

## 2. Confirmar con el desarrollador

Haz **una sola pregunta** con los valores propuestos:

- Modo (A o B) y carpeta destino.
- Adaptadores: `claude` si usa Claude Code (propuesta por defecto), `cursor` si existe `.cursor/`; ambos si usa los dos.
- Solo modo B: ¿ejecutar `git init` en `dev/` para que sea su propio repo? (propuesta: sí).

## 3. Ejecutar el instalador

```bash
python -I <ruta de esta skill>/scripts/install.py --mode <A|B> --target <carpeta> --adapters <claude,cursor> --yes
```

Añade `--git-init` en modo B si se aceptó. Si `python` no funciona, prueba `python3` o `py`. El script copia, genera adaptadores, añade las exclusiones de git y ejecuta `check.py` al final.

- Una repetición del instalador sobre un `dev/` existente es una actualización: reemplaza solo los archivos del paquete (respaldando en `dev/.backup/` los que el desarrollador editó) y no toca `PROJECT.md`, `COMANDOS.md`, `DEV-PROFILE.md`, `INDEX.md`, `docs/`, `work/` ni lo demás. Para eso usa `dev-update`, que además adapta los archivos del proyecto.
- Si la salida termina con `errores` distintos de 0, no sigas: lee el mensaje, corrige la causa y vuelve a ejecutar. Si no la entiendes, aplica el playbook `diagnose`.

## 4. Configurar `PROJECT.md` (núcleo) y `COMANDOS.md` (solo en una instalación nueva)

Inspecciona los repos y propón solo valores reales. No inventes nada; lo que no encuentres queda en `—`.

**`PROJECT.md`** (se lee siempre; pocas líneas):

| Sección | De dónde sale |
|---|---|
| §1 Repos y alias | Modo A: `@main` → `..` (ya viene). Modo B: un alias por repo (`@front`, `@back`) con su ruta relativa |
| §2 Idiomas | Inferirlos del `README` y de los commits; pregunta solo si no se pueden inferir |
| §3 Restricciones y §4 Zonas intocables | Una sola pregunta: «¿Hay algo que el agente no deba hacer ni tocar?». Si no hay nada, deja `—` |

**`COMANDOS.md`** (bajo demanda):

| Sección | De dónde sale |
|---|---|
| §1 Stacks | `pyproject.toml`/`requirements.txt` → `python`; `package.json` con React → `typescript-react`; `Package.swift`/`*.xcodeproj` → `swift` |
| §2 Comandos | `package.json` scripts, `Makefile`, `pyproject.toml`, `README`; `—` en lo que no encuentres |
| §3 Commits y PR | `git log -20 --oneline` para inferir el formato; `—` en lo demás |

Muestra ambos al desarrollador y espera su aprobación antes de escribir.

## 5. Configurar `DEV-PROFILE.md` (opcional)

Es personal y no se versiona. Haz como máximo **una pregunta corta y opcional**: tecnologías que no conoce, idioma de las explicaciones, formato de la respuesta final y atribución de IA en commits («puedes saltar esto: lo preguntaré cuando haga falta»). Acepta «saltar» y deja el archivo como está. Nada de entrevista larga.

## 6. Verificar y cerrar

```bash
python -I dev/.tools/check.py dev
```

Debe dar `0 errores` y `0 avisos`. Si hay avisos, menciónalos.

Termina con un mensaje corto:

1. Qué se instaló (versión, modo, adaptadores) y el resultado de la verificación.
2. Cómo seguir: «Crea la task `<nombre>`…» o «continúa task-1»; para revisar la salud de `dev/` más adelante, pedir «diagnostica dev/» (agente `dev-doctor`). Los `—` que queden no son tarea pendiente: el agente los pregunta cuando los necesite.
3. El hook `SessionStart` es opcional y **no está activado**; si lo quiere, la instrucción está en `dev/.adapters/settings-snippet.json`.
4. El método tiene feedback propio: cuando termines tasks, pide «feedback del método» (dev-feedback).

## Reglas

- No edites `dev/AGENTS.md` ni `dev/method/`: el paquete los reemplaza en cada actualización.
- No hagas commits ni toques el historial git de los repos.
- Ante un `AGENTS.md` o `CLAUDE.md` preexistente en la raíz, el script pregunta antes de añadir la referencia; no lo resuelvas por tu cuenta.
