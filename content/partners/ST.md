---
# ─────────────────────────────────────────────────────────────────────────────
# ST Engineering's partner file. Edit the fields below and the text under the
# second "---". See CONTRIBUTING.md for how to preview before publishing.
# ─────────────────────────────────────────────────────────────────────────────
short: ST Engineering
institution: ST Engineering
lab: AI.R.STC · NEAR Lab
labFull: AI and Robotics Strategic Technology Centre, NEAR Lab
role: Lead partner
contribution: Coordination, system integration and the Singapore flight lab
summary: >-
  ST Engineering's AI and Robotics Strategic Technology Centre coordinates the
  programme, integrates every layer of the system and runs the Singapore flight lab.
# What you do on each layer (one line each, max 90 characters). Shown in the
# "who does what" grid on the home page. Layers: strategy, safety, flight, localisation, drones, integration.
work:
  localisation: "Leads camera-based localisation: proven in simulation first, then on Starlings."
  drones: "Runs the Singapore flight lab."
  integration: "Coordinates the programme and brings every layer together on Starling 2 Max."
logo: ./ST/st-engineering.png
labLogo: ./ST/near-lab.png
logoAlt: ST Engineering
website: https://www.stengg.com
order: 2
updated: 2026-11-03
---

## Our role in Strike vs Guard

The NEAR Lab in ST Engineering's AI and Robotics Strategic Technology Centre
(AI.R.STC) is the lead partner. We coordinate the programme and bring the
partners' work together into one system, from team strategy and safety down to flight software and hardware, and
we run the Singapore flight lab where the drone teams are tested.

## What we are working on

- **Integration.** Making sure the strategy policies from NUS and UPenn, the
  safety filter, and CMU's AirStack run together as one stack on Starling 2 Max
  drones.
- **The Singapore flight lab.** An indoor flight space at ST Engineering for
  testing multi-drone teams locally, alongside CMU's flight cage.
- **Simulation and localisation.** Flying the Starling 2 Max in the AirStack simulator and starting camera-only localisation there.
- **The benchmark.** Running Strike vs Guard games so that the learning-based
  and formal approaches can be compared on the same hardware.

## Results so far

The first Starling 2 Max flights have taken place in the Singapore lab, with
more drones on the way.

![Starling drones in the ST Engineering flight lab in Singapore](./ST/singapore-flight-lab.jpg)

## In simulation

We brought the Starling 2 Max into the AirStack simulator (Isaac Sim with Pegasus) and built a
construction-site world for it, where up to three drones fly at once. Camera-only localisation runs
there first: over a 162 m flight, its position had an average error of 0.081 m against the drone's
own flight-controller estimate (not yet against the simulator's true position). With three Starlings
flying, each kept track of itself without a loss.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-st-three-starlings.jpg" aria-label="Simulation clip: three Starlings in AirStack"><source src="../../media/sim-st-three-starlings.mp4" type="video/mp4"></video><figcaption>Three simulated Starlings: one drone's camera view (left) and all three in the ground station (right).</figcaption></figure>

![Simulated Starling 2 Max drones over the construction-site world in the AirStack simulator](./ST/sim-construction-site.jpg)

## People

<!-- Add names and roles here, one per line, e.g. "- Jane Tan, Research Engineer" -->

- NEAR Lab, AI.R.STC, ST Engineering
