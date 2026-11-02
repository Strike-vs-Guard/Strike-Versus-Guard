---
eyebrow: Localisation
title: Knowing where every drone is
order: 9
status: Camera-only localisation is being proven in the AirStack simulator before it flies on a real Starling.
---

**Why.** Today the drone teams fly indoors with an external camera system that tells each drone where it is. The programme's third year is flight without that system and without GPS, so each drone must know where it is on its own.

**How.** Each drone carries a camera and a motion sensor and estimates its own position. Teammates share only their position and heading, so the team keeps one picture. Only a drone's own estimate steers it, so a bad message from a teammate cannot crash a drone.

**Status.** Camera-only localisation has started in the AirStack simulator, where the Starling 2 Max now flies. It moves to a real Starling after it works in simulation.
