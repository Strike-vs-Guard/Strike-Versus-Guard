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
people:
  - name: Tanishq Duhan
  - name: Prof Guillaume Sartoretti
    lead: true
  - name: Jeric Lew
---

## What we're trying

We lead the **learning-based track**. Rather than hand-writing a playbook for each
scenario, we let the drones find their own skills and team plays by practising.

What they learn goes into a library of plays. In a given situation, a planner
predicts how likely each play is to work and picks the best one, so the team can
switch when the other side changes how it plays.

![Four plays the Guard team discovered for the same situation, each with its predicted chance of success](./NUS/learned-plays.png)

It found plays we hadn't thought of. We can't always say why it chose one.

## What we've flown

Our team strategy first flew on palm-sized Crazyflie drones. In October 2026, at
CMU, it moved to full-size Starling 2 Max drones running AirStack.

![The NUS team strategy flying on Crazyflie drones](./NUS/crazyflie-flight.jpg)

## Where it breaks

We train in a simple simulated version of the game: three Strike drones, 1.5 times faster, against
five Guard drones holding the zone. Each new generation of players trains against the earlier ones,
so both sides keep getting better. A separate planner flies one drone fast through a field of
obstacles on routes that are hard to predict. It reaches its goal in over 99 % of runs, and flying it
with a team comes next.

The July 2026 report has the number that worries us. On SMAC, a standard three-against-three
benchmark in multi-agent research, our learned plays win close to 100 % of games when the players
start from fixed positions. In a first, preliminary Strike vs Guard test, two Guard drones against
one Strike drone, they held the zone in about 20 % of games. The skills fall apart in situations
unlike the ones they trained on, and that's the gap we have to close.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-nus-selfplay.jpg" aria-label="Simulation clip: the Guard team holds the zone"><source src="../../media/sim-nus-selfplay.mp4" type="video/mp4"></video><figcaption>Five Guard drones (blue) keep three faster Strike drones (red) out of the zone (green).</figcaption></figure>

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-nus-obstacles.jpg" aria-label="Simulation clip: one drone plans a route through obstacles"><source src="../../media/sim-nus-obstacles.mp4" type="video/mp4"></video><figcaption>One drone (yellow path) plans a fast route through 70 pillars, seen from four angles.</figcaption></figure>

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-nus-two-guards.jpg" aria-label="Simulation clip: two Guard drones keep one Strike drone away from the zone"><source src="../../media/sim-nus-two-guards.mp4" type="video/mp4"></video><figcaption>Preliminary test: two Guard drones (blue) keep one Strike drone (red) away from the zone (green). One of the games they won.</figcaption></figure>
