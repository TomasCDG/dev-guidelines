# Plantilla de mensaje de commit

<!-- Guía: method/playbooks/commit-pr.md. Va en la sección «Mensaje de commit sugerido» del report. El formato exacto y cuándo commitear están en COMANDOS.md §3; la atribución de IA, en la fila «Atribución de IA» de DEV-PROFILE.md. -->

```
<tipo>(<ámbito>): <resumen breve en imperativo> [task-N]

- <cambio funcional 1>
- <cambio funcional 2>
- <cambio funcional 3>
```

| Campo | Regla |
|---|---|
| `tipo` | `feat`, `fix`, `refactor`, `docs`, `test`, `chore`… (ajusta al formato de `COMANDOS.md` §3). |
| `ámbito` | Módulo, área o repo afectado. |
| `[task-N]` | ID de la task o bug; el **mismo** en cada repo afectado. |
| Lista | Breve: funcionalidades cambiadas, no archivos. |
| Atribución de IA | **Ninguna por defecto.** Añade la línea de atribución solo si la fila «Atribución de IA» de `DEV-PROFILE.md` dice `la de la herramienta`, y copia el texto que la herramienta indique. |

<!-- Multirepo: un mensaje por repo, mismo [task-N]. No hagas commit salvo que COMANDOS.md §3 o el desarrollador lo indiquen. -->
