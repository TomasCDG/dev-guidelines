# ROADMAP — backlog del paquete

**Fecha:** 27 de octubre de 2026 · **Versión del paquete:** 0.7.0

Backlog de funcionalidades futuras de dev-guidelines. **No son compromisos**: sirve para no perder ideas y ver qué viene. Lo que sale en una versión se mueve a `hecha` y se detalla en [CHANGELOG.md](./CHANGELOG.md). El porqué del diseño está en [historia/](../historia/README.md).

## Contenido

1. [Backlog](#backlog)
2. [Reglas](#reglas)

## Backlog

Estados: `idea`, `planeada`, `en curso`, `hecha`, `descartada`.

| ID | Funcionalidad | Por qué | Estado | Notas |
|---|---|---|---|---|
| R1 | `dev-feedback` arma ramas y empuja al repo del paquete las sugerencias que el desarrollador valide | Hoy solo redacta el feedback y llevarlo al paquete es manual | planeada | Requiere indicar la ruta o URL del repo del paquete (se guardaría como `source=` en `.package-version`); crea rama local, commit sin atribución de IA y push **solo con confirmación expresa en cada ejecución**; nunca a la rama principal |
| R2 | Probar las skills, el agente `dev-doctor` y el hook SessionStart en sesiones reales de Claude Code | Hasta ahora solo se verificaron con scripts y lectura | planeada | — |
| R3 | Verificar que `npx skills add` descubre `dev-setup`, `dev-update` y `dev-feedback` | La instalación recomendada depende de ese descubrimiento | planeada | — |
| R4 | CI del paquete: `check.py` sobre el ejemplo, `build-skill.py --check` y pruebas de instalación y migración | Evitar que el bundle de las skills quede desactualizado o se rompa la instalación | idea | — |
| R5 | Inicializar git del paquete y publicarlo en un repositorio | Sin repo no hay `npx skills add <repo>` ni issues | hecha | 0.7.0: repositorio git local creado (rama `main`, tag `v0.7.0`); falta publicar el remoto. Bloquea R1, R3 y R4 |
| R6 | Distribución como plugin o marketplace de Claude Code, además de `npx skills` | Instalación y actualización en un paso para quien usa Claude Code | idea | — |
| R7 | Activación asistida del hook SessionStart desde `dev-setup`, con confirmación | Hoy hay que copiar el fragmento a mano | idea | Modificar la configuración de la herramienta exige aprobación expresa |
| R8 | Packs de stack definidos por el usuario, más allá de `python`, `typescript-react` y `swift` | Otros lenguajes y frameworks sin tocar el paquete | idea | Tendría que sobrevivir a las actualizaciones (hoy `method/stacks/` lo reemplaza el paquete) |

## Reglas

- Cada funcionalidad nueva recibe un ID `R<n>` correlativo, en una sola línea de la tabla; los IDs no se reutilizan.
- Al salir en una versión: estado `hecha`, y en Notas la versión y la referencia a su entrada de [CHANGELOG.md](./CHANGELOG.md) (por ejemplo «0.8.0, ver CHANGELOG»).
- Una idea descartada se queda en la tabla con el motivo en Notas.
- Pasar de `idea` a `planeada` requiere que alguien la haya pedido con un caso de uso; las retros enviadas son la fuente principal.
