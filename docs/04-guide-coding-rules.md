<div align="center">

# Bug_Storm Coding Rules

**Constraints for deterministic gameplay on STM32L151**

</div>

## 1. Fixed memory only

- Use compile-time sized arrays for Bullets, Eggs, Gifts and Bugs.
- Reuse an inactive pool slot; never allocate in a game tick.
- A full pool means the spawn request is skipped safely.
- Keep constant drawing/lookup data read-only.

Current capacities are 20 player Bullets, 5 Eggs, 3 Gifts and 18 Bugs.

## 2. One owner of game state

Gameplay state belongs to `scr_game.cpp`. Hardware callbacks post AK messages;
only the display-task/screen-handler path may update Ship position, score, wave,
lives, HP or pools.

```text
Button hardware -> callback -> AK queue -> display task -> scr_game_handle()
```

## 3. Tick-based timing

Use integer counters advanced by `AC_DISPLAY_GAME_TICK`. Do not block the display
task with a delay or busy-wait.

| Counter | Current value |
|---|---:|
| Game tick | 100 ms |
| Fire cooldown | 2 ticks |
| Invulnerability | 12 ticks |
| Wave-clear delay | 12 ticks |

## 4. Update before render

For each tick:

1. Update animation and cooldown counters.
2. Fire automatically if due.
3. Update the active phase (Formation or Boss).
4. Move Bullets, Eggs and Gifts.
5. Resolve collisions and deactivate consumed objects.
6. Spawn an enemy Egg if due.
7. Evaluate phase transitions.
8. Render the resulting state.

Drawing functions must not mutate game rules or object pools.

## 5. Coordinate and collision convention

- `(0, 0)` is upper-left; X grows right and Y grows down.
- Logical screen area is 124 × 60 px.
- HUD uses Y `0..8`; play begins at Y `9`; Ship Y is `52`.
- Use the same AABB convention for all hit boxes.
- Immediately set a consumed projectile to inactive.

```cpp
return ax < bx + bw && ax + aw > bx &&
       ay < by + bh && ay + ah > by;
```

## 6. Explicit state transitions

Do not infer every phase from sprite coordinates. Preserve explicit state such
as `game_over`, `boss_active`, `next_wave_ticks`, `invulnerable_ticks`,
`bugs_left` and `boss_hp`.

Clear obsolete pools when entering Boss, after Boss defeat and when the player
is hit so objects cannot leak between phases.

## 7. Bounded difficulty

Difficulty formulas must retain valid periods, speeds and indexes at high wave
numbers:

```text
Formation move period = max(1, 4 - wave / 2)
Formation move step   = 1 + (wave - 1) / 3
Egg fall speed        = 2 + wave / 4
Egg minimum delay     = max(3, 7 - wave / 2)
Boss HP               = 10 + wave × 5
Boss move period      = max(1, 2 - wave / 4)
Boss move step        = 1 + wave / 4
```

## 8. Naming

- Constants: `UPPER_SNAKE_CASE`.
- Types: `lower_snake_case_t`.
- Functions and variables: `lower_snake_case`.
- Boolean names describe a true condition, such as `active` or `boss_active`.
- Existing AK signal spelling is preserved for framework compatibility.

## 9. Documentation and bitmap rule

Ship, Bug and Boss visuals are drawing code in `scr_game.cpp`, not arbitrary
illustrations. When documentation needs an exact gameplay image, dump the OLED
framebuffer and convert it with `tools/framebuffer_to_png.py`.

## 10. Verification before flashing

- Build cleanly and inspect new compiler warnings.
- Verify every loop stays inside its fixed pool.
- Verify the RIGHT button moves right and the LEFT button moves left.
- Verify automatic fire and manual MODE request cannot exceed 20 Bullets.
- Verify `P:4` is the maximum power level.
- Verify the Boss appears only after all 18 Bugs are destroyed.
- Verify the next wave starts only after Boss defeat and 12 ticks.
- Verify any short button restarts after Game Over.
- Verify holding MODE removes the game timer and returns to startup.
