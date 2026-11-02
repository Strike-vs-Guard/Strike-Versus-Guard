---
# ─────────────────────────────────────────────────────────────────────────────
# National University of Singapore's partner file. Edit the fields below and the
# text under the second "---". See CONTRIBUTING.md for how to preview before publishing.
# ─────────────────────────────────────────────────────────────────────────────
short: NUS
institution: National University of Singapore
lab: MARMot Lab
labFull: Multi-Agent Robotic Motion Lab
lead: Prof Guillaume Sartoretti
role: Partner
contribution: Learning-based strategy track
summary: >-
  The NUS MARMot Lab leads the learning-based approach: agents discover their
  own skills and team behaviours through experience, and a planner picks the
  play that best fits the situation.
# What you do on each layer (one line each, max 90 characters). Shown in the
# "who does what" grid on the home page. Layers: strategy, safety, flight, localisation, drones, integration.
work:
  strategy: "Leads the learning-based track: drones discover their own skills and team plays."
  drones: "First flew the team strategy on palm-sized Crazyflie drones."
logo: ./NUS/nus.png
labLogo: ./NUS/marmot-lab.png
logoAlt: National University of Singapore
website: https://www.marmotlab.org
order: 3
updated: 2026-11-03
---

## Our role in Strike vs Guard

The Multi-Agent Robotic Motion (MARMot) Lab at NUS leads the **learning-based
track** of the programme. Rather than hand-writing a playbook for each scenario,
the drones discover their own skills and team behaviours through experience.

## Approach

The team builds up a library of learned plays. For a given situation, a planner
predicts how well each play is likely to work and picks the best one, so the
team can adapt when the other side changes its approach.

![Four plays the Guard team discovered for the same situation, each with its predicted chance of success](./NUS/learned-plays.png)

**Strength:** finds moves nobody programmed.
**Trade-off:** its choices are harder to explain.

## Results so far

The NUS team strategy first flew on palm-sized Crazyflie drones, then on
full-size Starling 2 Max drones running CMU's AirStack.

![The NUS team strategy flying on Crazyflie drones](./NUS/crazyflie-flight.jpg)

## In simulation

NUS trains its team plays in a simple simulated version of the game: three Strike drones, 1.5 times
faster, against five Guard drones that hold the zone. Each new generation of players trains against
the earlier ones, so both sides keep improving. A separate planner flies one drone fast through a
field of obstacles on routes that are hard to predict, and reaches its goal in over 99 % of runs;
flying it with a team comes next.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-nus-selfplay.jpg" aria-label="Simulation clip: the Guard team holds the zone"><source src="../../media/sim-nus-selfplay.mp4" type="video/mp4"></video><figcaption>Five Guard drones (blue) keep three faster Strike drones (red) out of the zone (green).</figcaption></figure>

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-nus-obstacles.jpg" aria-label="Simulation clip: one drone plans a route through obstacles"><source src="../../media/sim-nus-obstacles.mp4" type="video/mp4"></video><figcaption>One drone (yellow path) plans a fast route through 70 pillars, seen from four angles.</figcaption></figure>

## People

- Prof Guillaume Sartoretti, MARMot Lab, National University of Singapore
