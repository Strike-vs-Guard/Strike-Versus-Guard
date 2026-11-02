---
# Two strategy tracks. Owned by ST Engineering with NUS and UPenn.
eyebrow: Two tracks, one stack
title: Two ways to decide, tested on the same drones
order: 2
note: Both tracks run on the same stack, CMU's AirStack on Starling 2 Max drones.
items:
  - label: Track A · Learning-based
    title: Agents discover their own team behaviours
    partners: [nus]
    text: >-
      The drones learn skills and team plays through experience. For each
      situation, a planner predicts which learned play is most likely to work
      and picks it.
    image: ./images/nus-learned-plays.png
    alt: Four team plays the Guard drones discovered for the same situation, with a bar showing each play's predicted chance of success. The first play is selected.
    plus: It found plays we hadn't thought of
    minus: We can't always say why it chose one
  - label: Track B · Formal
    title: Behaviour specified in signal temporal logic
    partners: [upenn]
    text: >-
      Engineers write the task as exact rules over time: reach the flag, avoid
      opponents, beat the clock. The software learns moves that satisfy the
      rules and assigns roles within the team.
    image: ./images/upenn-mission-rules.png
    alt: Three rules (reach the flag, avoid opponents, beat the clock) and the resulting plan, where one drone holds a button to open a gate while two others reach the flag.
    plus: We can check the behaviour against the rules we wrote
    minus: The rules have to be right first
---

We're building the team strategy two ways at once. At NUS the drones learn their
skills and team plays by practising. At UPenn the behaviour is written down first,
as rules in signal temporal logic, and the drones learn to follow them. Because
both end up on the same drones, we can put them side by side on real hardware
rather than argue about which is better.
