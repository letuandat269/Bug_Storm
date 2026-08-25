# Bug_Storm Documentation

The documents in this directory describe the firmware as it is implemented in
the current source tree. Diagrams use the real object pools, signals, timing
values and state transitions from `application/sources/app/screens/scr_game.cpp`.

## Reading order

| No. | Document | Purpose |
|---:|---|---|
| 01 | [Getting Started](01-guide-getting-started.md) | Hardware, repository layout, Linux build, firmware output and flashing. |
| 02 | [Game Object Design and Sequences](02-design-sequence-object.md) | Ownership, state and lifecycle of Ship, Bullet, Bug, Egg, Gift and Boss. |
| 03 | [Runtime Signal and Game Sequences](03-design-sequence-runtime.md) | Complete flow from buttons and timer messages to update, render and Game Over. |
| 04 | [Coding Rules](04-guide-coding-rules.md) | Constraints for deterministic embedded gameplay and safe future changes. |

## Source of truth

When documentation and firmware disagree, the source code is authoritative:

```text
application/sources/app/screens/scr_startup.cpp
application/sources/app/screens/scr_game.cpp
application/sources/app/task/task_display.cpp
application/sources/app/screens/scr_mng.cpp
```

The Mermaid diagrams render directly on GitHub.
