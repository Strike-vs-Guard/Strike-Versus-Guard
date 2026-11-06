---
# ─────────────────────────────────────────────────────────────────────────────
# ST Engineering's partner file. Edit the fields below and the text under the
# second "---". See CONTRIBUTING.md for how to preview before publishing.
# ─────────────────────────────────────────────────────────────────────────────
short: ST Engineering
institution: ST Engineering
lab: AI.R.STC · NEAR Lab
labFull: AI and Robotics Strategic Technology Centre, NEAR Lab
labBlurb: >-
  We are the Next-gen Edge AI and Robotics Lab, part of ST Engineering's AI and
  Robotics Strategic Technology Centre in Singapore. We study how teams of robots
  learn to coordinate, and build systems that carry from simulation to the field.
  In Strike vs Guard we coordinate the partners, integrate every layer and run the
  Singapore flight lab.
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
logoMark: ./ST/mark.png
labLogo: ./ST/near-lab.png
logoAlt: ST Engineering
lead: William Teo
website: https://nearlab.ai
order: 2
updated: 2026-11-06
people:
  - name: William Teo
    role: Director and Founder of NEAR Lab
    photo: ./ST/people/william-teo.jpg
    lead: true
    bio: >-
      William Teo founded and directs NEAR Lab at ST Engineering and leads
      Strike vs Guard for the lab. His research focuses on skills and strategy for
      multi-robot systems, including how teams of robots learn to coordinate.
    link: https://nearlab.ai/#/people
  - name: Derek Tan Ming Siang
    role: Principal AI Engineer
    photo: ./ST/people/derek.jpg
  - name: Chen Jiaying
    role: Principal AI Engineer
    photo: ./ST/people/chen-jiaying.jpg
  - name: Jeremy Chia Hwe Huang
    role: AI Robotics Engineer
    photo: ./ST/people/jeremy-chia.jpg
  - name: Nathan Ly
    role: SUTD intern, September to December 2026
    photo: ./ST/people/nathan-ly.jpg
    group: Interns
publications:
  - title: Pairwise Approximation Can Select the Wrong Multi-Robot Plan
    authors: William Teo (MARMoT Lab, NUS; NEAR Lab, ST Engineering)
    venue: IROS 2026 Workshop on Intelligent Information Gathering
    year: 2026
    status: workshop
    image: ./ST/pubs/pairwise-approximation-poster.jpg
  - title: "When Is It Worth Looking Again? Cost-Aware Active Information Gathering for ObjectNav"
    authors: Jiaying Chen, Chia Hwe Huang
    venue: IROS 2026 (workshop poster)
    year: 2026
    status: workshop
    image: ./ST/pubs/worth-looking-again-poster.jpg
---

## What we build

We're the NEAR Lab in ST Engineering's AI and Robotics Strategic Technology Centre
(AI.R.STC), and we're the lead partner. In practice that means joining the
partners' work up into one system, from team strategy and safety down to flight
software and hardware, and running the Singapore flight lab where the drone teams
are tested.

- **Integration.** Getting the NUS and UPenn strategies, the safety filter and
  CMU's AirStack to run together as one stack on Starling 2 Max drones.
- **The Singapore flight lab.** An indoor flight space at ST Engineering, so we
  can test drone teams here as well as in CMU's cage.
- **Simulation and localisation.** Flying the Starling 2 Max in the AirStack
  simulator, and starting camera-only localisation there.
- **The game.** Running Strike vs Guard so the learning-based and formal
  approaches can be compared on the same hardware.

## The Singapore lab

The first Starling 2 Max flights have taken place in the Singapore lab, with more
drones on the way.

![Starling drones in the ST Engineering flight lab in Singapore](./ST/singapore-flight-lab.jpg)

The lab is a netted flight volume in our hangar, tracked by OptiTrack cameras at up to 240 Hz, with
a wired network for tracking and a separate Wi-Fi network for commands. We commissioned it on
palm-sized Crazyflie 2.1 drones first, with a go/no-go preflight dashboard that we check before every
flight.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/st-crazyflie-preflight.jpg" aria-label="Flight clip: a Crazyflie in the Singapore lab with the preflight dashboard"><source src="../../media/st-crazyflie-preflight.mp4" type="video/mp4"></video><figcaption>Commissioning on a Crazyflie: the preflight dashboard (left), the tracked position (top right) and the flight (bottom right).</figcaption></figure>

![The netted flight volume in the Singapore hangar, with OptiTrack cameras on stands and the floor axes marked](./ST/hangar-flight-volume.jpg)

Bringing up the Starling takes six steps (status as of November 2026):

| Step | What it checks | Status |
|---|---|---|
| M1 | Rehearsal on three simulated drones, including a geofence breach and recovery | Done |
| M2 | Ground station: network, motion capture, clock sync | Done |
| M3 | Drone link to the ground station, propellers off | Done |
| M4 | Tracking fused into the drone's estimate, propellers off | Done |
| M5 | Hand-carry check through the flight volume | Done |
| M6 | First flight: take-off, hover, landing | Done |

## In the simulator

We brought the Starling 2 Max into the AirStack simulator (Isaac Sim with Pegasus) and built a
construction-site world for it, where up to three drones fly at once. Camera-only localisation runs
there first; with three Starlings flying, each kept track of itself without a loss. We still score it
against the drone's own estimate, not the simulator's true position.

We also rebuilt CMU's AirStack ourselves on the Starling 2 Max, to check that a second partner can
run it. Doing that turned up two bugs in the shared stack, which we fixed: a camera start-up race in
the simulator that made simulated drones fly erratically, and a fault that stopped the ground
controller after a single failed command.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-st-three-starlings.jpg" aria-label="Simulation clip: three Starlings in AirStack"><source src="../../media/sim-st-three-starlings.mp4" type="video/mp4"></video><figcaption>Three simulated Starlings: one drone's camera view (left) and all three in the ground station (right).</figcaption></figure>

![Simulated Starling 2 Max drones over the construction-site world in the AirStack simulator](./ST/sim-construction-site.jpg)
