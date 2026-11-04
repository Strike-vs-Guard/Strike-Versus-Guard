---
title: "October: Starlings in the simulator, three flights at CMU"
date: 2026-11-03
partner: st
author: Jeremy Chia Hwe Huang
summary: >-
  The Starling 2 Max now flies in the AirStack simulator, camera-only
  localisation has a first number, and three Starlings flew themselves at CMU.
---

October was the month the Starling 2 Max started flying in the AirStack simulator. We built a
construction-site world for it, and up to three Starlings now fly there at once on the same software
as the real drones.

We started camera-only localisation in that world too. Over a 162 m flight the camera's position was
off by 0.081 m on average. That's a first number, not a result: we're comparing against the drone's
own estimate, not the simulator's true position.

In Pittsburgh, three Starlings flew in CMU's flight cage with nobody on the sticks and the safety
filter on the whole time. In the same visit the NUS team strategy moved from Crazyflies to the
Starlings. CMU's clips are on the Flights page.

Rebuilding AirStack ourselves on the Starling turned up two bugs in the shared stack. Neither was
dramatic, but both cost us time.

**Known problems, and where they stand**

- A camera start-up race in Isaac Sim left simulated drones without depth, so they flew erratically.
  Fixed, but only after we'd spent time blaming the drone's position estimate.
- A logging fault in the ground controller stopped the commander on the first failed command. Fixed.
- Localisation is still scored against the drone's own estimate, not the simulator's true position.
  Not fixed yet.
