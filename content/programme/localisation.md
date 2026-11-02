---
# Localisation on the Programme page (full) and the Flights page (`status:` only). Owned by ST Engineering; CMU advises.
# The three items are the three questions, shown as cards. Dates and pass marks are targets, not results.
eyebrow: Localisation
title: Knowing where every drone is
order: 9
status: In the AirStack simulator, camera-only localisation followed a 162 m flight with an average error of 0.081 m against the drone's own estimate; a real Starling comes next.
items:
  - label: "1 · Each drone, on its own"
    title: Where am I?
    text: Each drone works out its own position from its camera and motion sensor. This is the only layer that steers the drone.
  - label: "2 · One shared picture"
    title: Where are my teammates?
    text: Teammates share only their position and heading, and the drones measure the distance to each other by radio ranging. This picture never steers a drone.
  - label: "3 · Moving obstacles"
    title: Where is the other team?
    text: The other side does not share where it is, so its drones are treated as moving obstacles, detected by our drones' cameras and two ground sensor stations.
note: Only layer 1 steers a drone. Layers 2 and 3 feed the team strategy and the safety filter, never the autopilot, so a bad message from a teammate can never crash a drone.
image: ./images/loc-sim-scenes.png
imageAlt: "Two plots of a simulated flight path. Left: in a bare flat world the camera's path (red) jumps away from the drone's own estimate (grey). Right: over a construction site the two paths stay together."
caption: "Simulation only, camera only. Left: a bare flat world gives the camera few features, and its path (red) jumped 5–10 m from the drone's estimate (grey). Right: the construction site, with no jumps over 162 m."
---

**Why.** Today the drone teams fly indoors with an external camera system that tells each drone where it is. The programme's third year is flight without that system and without GPS, so each drone must know where it is on its own.

**How.** Each drone carries a camera and a motion sensor, and an add-on computer turns them into a position (visual-inertial odometry). If that computer goes quiet or its position looks wrong, the drone switches to its built-in estimate within a second.

**Status.** Camera-only localisation works in the AirStack simulator, where the Starling 2 Max now flies. Over a 162 m simulated flight it had an average error of 0.081 m and never lost track. That error is measured against the drone's own flight-controller estimate, not yet against the simulator's true position. Three Starlings have run it at once, and it moves to a real Starling next.

**Plan.** These are targets, not results.

| Target date | Step |
|---|---|
| Dec 2026 | First accuracy number, from a camera carried by hand |
| Apr–Jun 2027 | Flying on the camera |
| Mid-2027 | Radio ranging tags on the drones |
| Late 2027 | Tests in the Singapore hangar |
| 2028 | Tests in an outdoor flight cage |
| Jun 2029 | Localisation due |

**Target pass marks:** drift of at most 1 % of the distance flown; teammates lined up within 0.3 m and 2° of heading; drones of the other team spotted at 15 m, with their position within 2 m.
