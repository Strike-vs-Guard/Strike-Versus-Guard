---
# Two strategy tracks. Owned by ST Engineering with NUS and UPenn.
eyebrow: Two tracks, one stack
title: Learning and formal methods, compared on the same drones
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
    plus: Finds moves nobody programmed
    minus: Harder to explain its choices
  - label: Track B · Formal
    title: Behaviour specified in signal temporal logic
    partners: [upenn]
    text: >-
      Engineers write the task as exact rules over time: reach the flag, avoid
      opponents, beat the clock. The software learns moves that satisfy the
      rules and assigns roles within the team.
    image: ./images/upenn-mission-rules.png
    alt: Three rules (reach the flag, avoid opponents, beat the clock) and the resulting plan, where one drone holds a button to open a gate while two others reach the flag.
    plus: Behaviour can be checked against the rules
    minus: Someone has to write the right rules
---

We're developing the team strategy policies along two parallel tracks. NUS is
leading a learning-based approach, where agents discover their own skills and
team behaviours through experience. UPenn is leading a formal approach,
specifying behaviour directly through signal temporal logic. Both run on the
same stack, CMU's AirStack on Starling 2 Max drones, so the two approaches can
be compared head-to-head on real hardware.
