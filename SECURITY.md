# Security Policy

## Supported versions

| Trainer | Marathon build | Status |
|---------|----------------|--------|
| 0.9.x   | 2026.1 - 2026.3 | Supported |
| 0.8.x   | 2026.0         | Best effort |
| < 0.8   | any            | Unsupported |

## Scope

Marathon Trainer performs **read/write memory access** to the local Marathon process via `pymem` and `win32api`. This is inherently privileged. We take the following seriously:

- Arbitrary code execution introduced via config files (YAML anchors, `!!python/object`).
- Supply-chain issues in `requirements.txt`.
- Silent writes to offsets not declared in `src/processors/`.
- Any feature that reaches out to a network endpoint.

## Reporting

Email `security@marathon-trainer.invalid` (PGP key in `docs/pgp.txt`) or open a private advisory. Do **not** open a public issue for memory-corruption or RCE bugs.

We aim to respond within 72 hours. Please include a minimal repro config and the crash log.

## Out of scope

- Anti-cheat detections on online servers (we don't support online play).
- Game crashes caused by incompatible Marathon builds.
- Anything requiring kernel-mode drivers.