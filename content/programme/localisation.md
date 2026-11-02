---
eyebrow: Localisation
title: Knowing where every drone is
order: 9
status: In the AirStack simulator, camera-only localisation followed a 162 m flight with an average error of 0.081 m against the drone's own estimate; a real Starling comes next.
---

**Why.** Today the drone teams fly indoors with an external camera system that tells each drone where it is. The programme's third year is flight without that system and without GPS, so each drone must know where it is on its own.

**How.** Each drone carries a camera and a motion sensor and estimates its own position. Teammates share only their position and heading, so the team keeps one picture. Only a drone's own estimate steers it, so a bad message from a teammate cannot crash a drone.

**Status.** Camera-only localisation works in the AirStack simulator, where the Starling 2 Max now flies. Over a 162 m simulated flight it had an average error of 0.081 m and never lost track. That error is measured against the drone's own flight-controller estimate, not yet against the simulator's true position. Three Starlings have run it at once, and it moves to a real Starling next.
