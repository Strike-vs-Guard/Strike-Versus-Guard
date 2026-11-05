---
# "How a command travels" on the Programme page, under the two tracks. Owned by ST Engineering with CMU.
# Each item is one box, left to right; `passes:` is the label on the arrow after that box.
eyebrow: How a command travels
title: From a team decision to the motors
order: 11
note: Both strategy approaches plug into the same interface, so they run, and can be compared, on the same drones.
items:
  - label: Decision layer
    title: Team strategy
    text: The NUS or UPenn strategy decides what each drone should do next.
    partners: [nus, upenn]
    passes: Nominal velocity commands
  - label: Ground controller
    title: AirStack
    text: CMU's ground controller runs each drone's task and keeps it inside the geofence.
    partners: [cmu]
  - label: Safety filter
    title: Safety filter
    text: Changes a command only when it would bring two drones too close.
    partners: [cmu, upenn]
    passes: Safe commands
  - label: On each drone
    title: PX4 flight controller
    text: Flies each command and keeps the final say on the motors.
---
