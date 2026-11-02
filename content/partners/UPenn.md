---
# ─────────────────────────────────────────────────────────────────────────────
# University of Pennsylvania's partner file. Edit the fields below and the text
# under the second "---". See CONTRIBUTING.md for how to preview before publishing.
# ─────────────────────────────────────────────────────────────────────────────
short: UPenn
institution: University of Pennsylvania
lab: xLab
lead: Prof Rahul Mangharam
role: Partner
contribution: Formal strategy track using signal temporal logic
summary: >-
  UPenn's xLab leads the formal approach: team behaviour is specified directly
  in signal temporal logic, so it can be checked against the rules it was
  written to follow.
# What you do on each layer (one line each, max 90 characters). Shown in the
# "who does what" grid on the home page. Layers: strategy, safety, flight, localisation, drones, integration.
work:
  strategy: "Leads the formal track: team behaviour specified in signal temporal logic."
  safety: "Co-develops the safety filter with CMU."
  drones: "Runs the formal-track strategy on the shared Starling 2 Max drones."
logo: ./UPenn/penn.png
labLogo: ./UPenn/xlab.png
logoAlt: University of Pennsylvania
website: https://xlab.upenn.edu
order: 4
updated: 2026-11-03
---

## Our role in Strike vs Guard

UPenn's xLab leads the **formal track** of the programme. Instead of letting the
team discover its behaviour, we specify it directly in **signal temporal logic
(STL)**: precise rules about what must happen, and by when.

## Approach

Engineers write the task as rules over time, such as *reach the flag*, *avoid
opponents* and *beat the clock*. The software then learns moves that satisfy
those rules and assigns roles within the team. In the example below, one drone
holds a button so that a gate opens, while two others go through and reach the
flag.

![Mission rules written in signal temporal logic, and the team plan that satisfies them](./UPenn/mission-rules.png)

**Strength:** behaviour can be checked against the rules.
**Trade-off:** someone has to write the right rules.

With CMU, we also work on the safety filter that sits under both strategy
tracks and keeps the drones apart.

## In simulation

UPenn trains its formal-track strategies in its own simulator. Single-drone versions came first, as
a baseline to compare against. The first runs where teams of drones train against each other have
now produced candidate strategies, and they have not yet been scored against the rules.

From the July 2026 report: using the rules as the training signal, the planner scaled from
one-against-one to four-against-four and eight-against-four reach-avoid games (one team must reach a
goal while avoiding the other), and it learned faster than a standard reinforcement-learning baseline.
A second approach, a hierarchical policy, gives each drone a skill in a capture-the-flag game: one
presses a button while the others take the flag.

The same policy was used to study team sizes. Against one Strike drone, going from 1 to 10 Guard drones
raised the time with the zone clear from 31 % to 94 %. Against 5 or 10 Strike drones, more Guard drones
alone were not enough: the team needs better coordination, not just more drones.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-upenn-reach-avoid.jpg" aria-label="Simulation clip: a four-against-four reach-avoid game"><source src="../../media/sim-upenn-reach-avoid.mp4" type="video/mp4"></video><figcaption>A four-against-four reach-avoid game with simulated quadcopters in a high-fidelity physics simulator.</figcaption></figure>

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-upenn-capture-flag.jpg" aria-label="Simulation clip: capture the flag with a hierarchical policy"><source src="../../media/sim-upenn-capture-flag.mp4" type="video/mp4"></video><figcaption>Capture the flag: each team (red, blue) has a zone and a flag. The upper policy gives each drone a skill, such as pressing a button (yellow) or taking the flag.</figcaption></figure>

## People

- Prof Rahul Mangharam, xLab, University of Pennsylvania
