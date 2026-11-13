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
  We are NEAR Lab, the Next-gen Edge AI and Robotics Lab, part of ST Engineering's
  AI and Robotics Strategic Technology Centre in Singapore. We work towards teams
  of different robots, from each robot's skills to the team's strategy, tested on
  real hardware. In Strike vs Guard we coordinate the partners, integrate every
  layer and run the Singapore flight lab.
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
updated: 2026-11-13
people:
  - name: William Teo
    role: Director and Founder of NEAR Lab
    photo: ./ST/people/william-teo.jpg
    lead: true
    bio: >-
      William Teo founded and directs NEAR Lab at ST Engineering and leads
      Strike vs Guard for the lab. His research focuses on skills and strategy for
      multi-robot systems, including how teams of robots learn to coordinate and to
      respond to opponents and the unexpected.
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
- **Flying by hand, safely.** A gamepad can fly one drone while the fence and the safety
  filter still check every command.
- **The game.** Running Strike vs Guard so the learning-based and formal
  approaches can be compared on the same hardware.

## The Singapore lab

Two Starling 2 Max drones now fly together in the Singapore lab, with more drones on the way. On 12 November 2026 we sent one at the other and the safety filter held them 1.5 m apart; on 13 November it held a hand-flown drone 1.76 m from a hovering one.

![Two Starling drones over the coloured floor tiles of the ST Engineering flight lab in Singapore, labelled drone_1 and drone_2](./ST/singapore-flight-lab.jpg)

The lab is a netted flight volume in our hangar, tracked by OptiTrack cameras at up to 240 Hz, with
a wired network for tracking and a separate Wi-Fi network for commands.

Bringing up the Starling takes six steps (status as of November 2026):

| Step | What it checks | Status |
|---|---|---|
| M1 | Rehearsal on three simulated drones, including a geofence breach and recovery | Done |
| M2 | Ground station: network, motion capture, clock sync | Done |
| M3 | Drone link to the ground station, propellers off | Done |
| M4 | Tracking fused into the drone's estimate, propellers off | Done |
| M5 | Hand-carry check through the flight volume | Done |
| M6 | First flight: take-off, hover, landing | Done |

Since that first flight:

| What we flew | When |
|---|---|
| Flights to points sent from the ground station, with nobody on the sticks | 11 November 2026 |
| The geofence: sent beyond the edge, the drone brakes at the edge | 11 November 2026 |
| Two drones together, with the safety filter on | 12 November 2026 |
| One drone flown by hand with a gamepad: turning, the fence wall, letting go of the stick | 13 November 2026 |
| A hand-flown drone sent at a hovering one, safety filter on: 1.76 m at the closest | 13 November 2026 |

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/st-two-starlings.jpg" aria-label="Flight clip: the ground station's view of two Starlings in the Singapore lab"><source src="../../media/st-two-starlings.mp4" type="video/mp4"></video><figcaption>Two Starlings in the Singapore lab on 12 November 2026, as the ground station draws them. One holds its position and we send the other straight at it. Watch both rings turn from green to blue as the safety filter eases the drones apart. Video: NEAR Lab, ST Engineering.</figcaption></figure>

## Strike vs Guard on Crazyflies

Palm-sized Crazyflie 2.1 drones fly in the same lab, up to seven at a time, so a team strategy can
be tried in an afternoon before it goes on a Starling.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/st-cf-formation.jpg" aria-label="Flight clip: five Crazyflies fly formations in the Singapore lab"><source src="../../media/st-cf-formation.mp4" type="video/mp4"></video><figcaption>Five Crazyflies on 5 August 2026: a waypoint tour as one group, then a pentagon, a spin, a triangle with a tail and an orbit of the room centre. Watch the shape hold while the group moves. Video: NEAR Lab, ST Engineering.</figcaption></figure>

On 6 November 2026 Nathan Ly, our SUTD intern, ran the first Strike vs Guard match in Singapore
with a moving zone. The zone is a DJI flown by hand. Four Guard Crazyflies (blue lights) fly a ring
around it; three Strike Crazyflies (red lights) try to reach it. The Guard side runs a role-based
strategy developed at NEAR Lab (paper under review): each Guard drone takes a role, predicts where
each Strike drone is heading over the next moment, and moves to put itself between that drone and
the zone, while a local controller written in signal temporal logic keeps the Guard drones apart and
clear of collisions. Nothing is planned in advance. OptiTrack tracks every drone and the DJI, every
position is computed live, and so the ring goes wherever the DJI goes.

A Guard drone tags a Strike drone by closing within the tag radius; a Strike drone scores by
reaching the zone. In this run the Guard team tagged all three. In another run the same afternoon a
Strike drone got through. Also in place: minimum separations between drones, a geofence that keeps
the DJI inside the flyable volume, automatic landing if tracking is lost, and a one-click stop.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/st-cf-game.jpg" aria-label="Flight clip: four Guard Crazyflies hold a ring around a hand-flown DJI while three Strike Crazyflies try to reach it"><source src="../../media/st-cf-game.mp4" type="video/mp4"></video><figcaption>The match on 6 November 2026 from the lab's camera, with the ground station's view inset. Watch the ring turn so that a blue light stays between each red light and the DJI. Video: NEAR Lab, ST Engineering.</figcaption></figure>

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
