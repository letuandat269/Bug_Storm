<div align="center">

![MCU](https://img.shields.io/badge/MCU-STM32L151CBT6-03234B?style=flat-square&logo=stmicroelectronics)
![Display](https://img.shields.io/badge/OLED-128x64_1--bit-white?style=flat-square&labelColor=black)
![Firmware](https://img.shields.io/badge/Firmware-v1.1.0.0-blue?style=flat-square)

</div>

# Bug_Storm

**Bug_Storm** is a monochrome 1-bit arcade shooter developed for the **AK Embedded Base Kit** using the STM32L151CBT6 microcontroller and a 128 x 64 OLED display.

The player controls a spacecraft that fires automatically, destroys formations of flying Bugs and collects square Gifts to increase firepower from one to four shots. After every formation is cleared, a Boss appears with its own health bar, movement pattern and attacks.

The game includes progressive wave difficulty, three Player lives, scoring, a high-score record, sound effects and a compact interface designed for three physical buttons.

## Game Objects

| Bitmap | Object | Description |
|:---:|---|---|
| <img src="resources/images/bitmap/ship.svg" width="64" alt="Player Ship"/> | **Player Ship** | Moves horizontally, fires automatically and starts with three lives. |
| <img src="resources/images/bitmap/bullet.svg" height="48" alt="Bullet"/> | **Bullet** | Travels upward and damages Bugs or the Boss. |
| <img src="resources/images/bitmap/bug.svg" width="64" alt="Bug"/> | **Bug** | Flies in formation, moves toward the Player and awards points when destroyed. |
| <img src="resources/images/bitmap/egg.svg" height="48" alt="Egg"/> | **Egg** | Falls from Bugs or the Boss and removes one Player life on impact. |
| <img src="resources/images/bitmap/gift.svg" width="48" alt="Gift"/> | **Gift** | Increases firepower from one to a maximum of four simultaneous shots. |
| <img src="resources/images/bitmap/boss.svg" width="96" alt="Boss"/> | **Boss** | Appears after each formation is cleared and must be defeated to advance. |

## Gameplay Bitmap Interface

The following image represents the 128 x 64 monochrome OLED frame generated from the game's 1-bit bitmap objects. The status bar shows Score (`S`), Wave (`W`), Power (`P`) and remaining Lives (`V`).

<p align="center">
  <img src="resources/images/screens/scr_gameplay.svg" width="744" alt="Bug_Storm 1-bit gameplay interface"/>
</p>

## Button-to-End-Game Logic

```mermaid
flowchart TD
    A[Physical button input] --> B[10 ms button_timer_polling]
    B --> C[Debounce and classify press]
    C --> D[BSP callback posts display signal]
    D --> E[AK message queue]
    E --> F[Display task and screen manager]
    F --> G[scr_game_handle]

    G -->|UP pressed| H[Move Player right and clamp X]
    G -->|DOWN pressed| I[Move Player left and clamp X]
    G -->|MODE pressed| J[Fire immediately]
    G -->|MODE held| K[Stop game timer and return to menu]
    G -->|100 ms GAME_TICK| L[game_update]

    H --> R[Render OLED frame]
    I --> R
    J --> R
    L --> M[Automatic fire and move formation or Boss]
    M --> N[Move bullets, eggs and gifts]
    N --> O[Check collisions]
    O -->|Gift collected| P[Increase Power up to 4]
    O -->|Bug hit| Q[Reduce bugs_left and add score]
    Q -->|bugs_left equals 0| S[Start Boss fight]
    O -->|Boss hit| T[Reduce boss_hp]
    T -->|boss_hp equals 0| U[Wave Clear delay]
    U --> V[Increase wave and spawn new formation]
    O -->|Egg hit or formation reaches Player| W[game_player_hit]
    W --> X[Decrease lives]
    X -->|lives greater than 0| Y[Reset Player position and continue]
    X -->|lives equals 0| Z[Set game_over and stop GAME_TICK]
    Z --> AA[Display GAME OVER and final score]

    P --> R
    Q --> R
    S --> R
    V --> R
    Y --> R
    R --> L
```

## Video Demo

<p align="center">
  <video
    src="https://github.com/user-attachments/assets/cace2061-e597-41b6-9cb5-8d4b5ea76f48"
    controls
    width="800"
    style="max-width: 100%; transform: rotate(180deg);">
  </video>
</p>
