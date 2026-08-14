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

## Video Demo

<p align="center">
  <video
    src="https://github.com/user-attachments/assets/cace2061-e597-41b6-9cb5-8d4b5ea76f48"
    controls
    width="800"
    style="max-width: 100%; transform: rotate(180deg);">
  </video>
</p>
