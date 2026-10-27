# Stack: Swift / iOS

Activar en `COMANDOS.md` §1. Complementa [develop-code](../playbooks/develop-code.md).

- **Arquitectura:** MVVM o Clean Architecture; vistas (SwiftUI o ViewControllers) desacopladas de la lógica de negocio y de las llamadas de red.
- **Concurrencia moderna:** `async/await` y `Task` estructurados en lugar de closures o *completion handlers* anidados.
- **Documentación:** mantén el código bien organizado y documentado, sobre todo si sirve de referencia para una migración a otra plataforma.
- **Equivalencias en migraciones:** al portar a otra tecnología, conserva la equivalencia funcional y usa los patrones idiomáticos del destino (por ejemplo `@State`/`@StateObject` → estado local o *hooks* en React).
