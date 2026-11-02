---
# ─────────────────────────────────────────────────────────────────────────────
# Carnegie Mellon University's partner file. Edit the fields below and the text
# under the second "---". See CONTRIBUTING.md for how to preview before publishing.
# ─────────────────────────────────────────────────────────────────────────────
short: CMU
institution: Carnegie Mellon University
lab: AirLab
lead: Prof Sebastian Scherer
role: Partner
contribution: AirStack flight software, safety filter and flight testing
summary: >-
  CMU's AirLab provides AirStack, the shared flight software that both strategy
  tracks run on, co-develops the safety filter, and flies the drone teams in its
  indoor flight cage.
# What you do on each layer (one line each, max 90 characters). Shown in the
# "who does what" grid on the home page. Layers: strategy, safety, flight, localisation, drones, integration.
work:
  safety: "Co-develops the safety filter with UPenn."
  flight: "Provides AirStack, the shared flight software for both tracks."
  localisation: "Provides the AirStack simulator and technical advice from its flight experience."
  drones: "Flies the drone team in its indoor flight cage in Pittsburgh."
logo: ./CMU/cmu.png
labLogo: ./CMU/airlab.png
logoAlt: Carnegie Mellon University
website: https://theairlab.org
order: 5
updated: 2026-11-03
---

## Our role in Strike vs Guard

The AirLab at Carnegie Mellon University provides the common ground that makes
a head-to-head comparison possible: **AirStack**, the flight software that turns
team plans into flight on real Starling 2 Max drones. Both the learning-based
and the formal strategy tracks run on it.

## What we are working on

- **AirStack.** A shared autonomy stack for the whole programme, from simulation
  to real drones.
- **Safety filter.** With UPenn, a layer that checks every command so that the
  drones never collide, whatever the strategy above it decides.
- **Flight testing.** Multi-drone flights in CMU's indoor flight cage.

## Results so far

Three Starling 2 Max drones have flown in CMU's flight cage with no pilot: changing
formation while keeping their spacing, flying to separate goals with crossing
paths resolved on their own, and continuing their task while a hand-flown drone
cut across them. A virtual boundary kept every drone inside the flight area. This was CMU's flight day in October 2026. More of CMU's flight recordings, with the settings behind them, are on CMU's own project site.

In one working visit, the NUS team strategy went from palm-sized drones to
full-size Starlings on AirStack: the programme's first successful run on
full-size drones.

![Starling 2 Max drones flying in the CMU flight cage](./CMU/starling-flight-cage.jpg)

![The Strike vs Guard team outside the Robotics Innovation Center at CMU](./CMU/team-robotics-innovation-center.jpg)

## In simulation

AirStack already runs real and simulated drones side by side under the same safety filter, so new
ideas can be tried on simulated Starlings first.

From the July 2026 report: the safety filter works on velocity commands. It was first tested in a
point-mass simulation across drone sizes, safety distances, numbers of drones and speeds, then in the
AirStack simulator with a two-drone close-proximity test and a five-drone mission. AirStack can use two
simulators: AirSim starts in 6.75 s against 70.5 s for Isaac Sim, so AirSim serves fast iteration and
Isaac Sim the high-fidelity checks before real flights. To make the simulated Starling match the real
one, CMU measured its motor thrust and motor response time (74 ms) on a test stand; the real drone flies
for 43 minutes on two 4 Ah batteries.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-cmu-safety-filter.jpg" aria-label="Simulation clip: the safety filter in a point-mass simulation"><source src="../../media/sim-cmu-safety-filter.mp4" type="video/mp4"></video><figcaption>Point-mass simulation: green arrows are the commands each drone (blue) was given; red arrows show where the filter changed one to keep the drones' safety rings apart.</figcaption></figure>

![A Starling 2 Max motor and propeller mounted on a test stand that measures thrust](./CMU/starling-thrust-stand.jpg)

The next
steps are proposals, not yet demonstrated: solving the game mathematically for each side, a fast
controller learned from human pilots, games that mix real drones with simulated opponents, and a
safety filter that works from each drone's own map of its surroundings.

## People

- Prof Sebastian Scherer, AirLab, Carnegie Mellon University

## Code and documentation

- Strike vs Guard ground control, project page and developer docs:
  <https://strike-vs-guard.github.io/svg-website/>
- AirStack: <https://github.com/castacks/AirStack>
