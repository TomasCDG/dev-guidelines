# Stack: Python

Activar en `COMANDOS.md` §1. Complementa [develop-code](../playbooks/develop-code.md).

- **Docstrings en formato Google:** propósito, parámetros, tipo de retorno y excepciones.
- **Tipado estricto:** anota parámetros y retornos de todas las funciones; compatible con `mypy`.
- **Excepciones explícitas:** nunca `try/except` genérico ni `pass` que silencie errores. Captura excepciones específicas o define excepciones de dominio.
- **Asincronía no bloqueante:** en flujos de E/S (red, almacenamiento, consultas externas) usa `async/await` de forma consistente y no ejecutes llamadas bloqueantes dentro del bucle de eventos.
- **Validación en los bordes:** esquemas declarativos (por ejemplo Pydantic) para entradas externas.
