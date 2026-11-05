---
# ─────────────────────────────────────────────────────────────────────────────
# University of Pennsylvania's partner file. Edit the fields below and the text
# under the second "---". See CONTRIBUTING.md for how to preview before publishing.
# ─────────────────────────────────────────────────────────────────────────────
short: UPenn
institution: University of Pennsylvania
lab: xLab
labFull: Safe Autonomous Systems Lab
labBlurb: >-
  We are xLab, the Safe Autonomous Systems Lab at the University of Pennsylvania
  and part of the PRECISE Center. We develop safety-critical autonomous systems by
  combining formal methods with learning and control, from autonomous vehicles to
  medical devices. In Strike vs Guard we lead the formal track and co-develop the
  safety filter with CMU.
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
logoMark: ./UPenn/mark.png
labLogo: ./UPenn/xlab.png
logoAlt: University of Pennsylvania
website: https://xlab.upenn.edu
order: 4
updated: 2026-11-04
people:
  - name: Prof Rahul Mangharam
    role: Professor, Electrical and Systems Engineering
    photo: ./UPenn/people/rahul-mangharam.jpg
    lead: true
    bio: >-
      Rahul Mangharam is a Professor of Electrical and Systems Engineering at the
      University of Pennsylvania and directs xLab, the Safe Autonomous Systems
      Lab. His work sits where formal methods, machine learning and control meet;
      PhD in Electrical and Computer Engineering from Carnegie Mellon.
    link: https://xlab.upenn.edu/team/rahul/
  - name: Hongrui (Billy) Zheng
    photo: ./UPenn/people/hongrui-zheng.jpg
  - name: Wei Wang
    photo: ./UPenn/people/wei-wang.jpg
publications:
  - title: "STL-SVPIO: Signal Temporal Logic guided Stein Variational Path Integral Optimization"
    authors: Hongrui Zheng, Zirui Zang, Ahmad Amine, Cristian Ioan Vasile, Rahul Mangharam
    venue: IROS 2026
    year: 2026
    status: published
    link: https://arxiv.org/abs/2603.13333
    pdf: https://arxiv.org/pdf/2603.13333
---

## What we write down

We lead the **formal track**. Instead of letting the team discover its behaviour,
we write it down first in **signal temporal logic (STL)**: exact rules about what
has to happen, and by when.

A task becomes a handful of rules over time, like *reach the flag*, *avoid
opponents* and *beat the clock*. The software then learns moves that satisfy them
and gives each drone a role. In the example below, one drone holds a button so a
gate opens, and two others go through and reach the flag.

![Mission rules written in signal temporal logic, and the team plan that satisfies them](./UPenn/mission-rules.png)

We can check the behaviour against the rules we wrote. The rules have to be right first.

We also work with CMU on the safety filter that sits under both tracks and keeps
the drones apart.

## What the simulator tells us

We train in our own simulator. Single-drone versions came first, as a baseline. The first runs where
teams train against each other have now produced candidate strategies; we haven't scored them
against the rules yet.

From the July 2026 report: with the rules as the training signal, the planner scaled from
one-against-one up to four-against-four and eight-against-four reach-avoid games (one team has to
reach a goal while avoiding the other), and it learned faster than a standard reinforcement-learning
baseline. A second approach, a hierarchical policy, gives each drone a skill in a capture-the-flag
game: one presses a button while the others take the flag.

We used the same policy to look at team size. Against one Strike drone, going from 1 to 10 Guard
drones raised the time the zone stayed clear from 31 % to 94 %. Against 5 or 10 Strike drones,
adding Guard drones didn't fix it. The team has to coordinate better, not just get bigger.

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-upenn-reach-avoid.jpg" aria-label="Simulation clip: a four-against-four reach-avoid game"><source src="../../media/sim-upenn-reach-avoid.mp4" type="video/mp4"></video><figcaption>A four-against-four reach-avoid game with simulated quadcopters in a high-fidelity physics simulator.</figcaption></figure>

<figure class="clip"><video controls muted playsinline preload="none" poster="../../media/sim-upenn-capture-flag.jpg" aria-label="Simulation clip: capture the flag with a hierarchical policy"><source src="../../media/sim-upenn-capture-flag.mp4" type="video/mp4"></video><figcaption>Capture the flag: each team (red, blue) has a zone and a flag. The upper policy gives each drone a skill, such as pressing a button (yellow) or taking the flag.</figcaption></figure>
