---
# Test ladder on the Flights page: ST Engineering's six steps to the first Starling flight in Singapore.
# Owned by ST Engineering. `state:` is the status as of the July 2026 report; update the note when it changes.
eyebrow: Test ladder
title: Six steps before a Starling flies in Singapore
order: 12
note: Status as of July 2026, except M6, flown since. Each step must pass before the next one starts.
# The annotated photo under the ladder. `points:` are in percent of the photo from the top left
# (placed by eye on the 1100 x 623 original); `lx`/`ly` place each label.
image: ../partners/ST/singapore-flight-lab.jpg
imageAlt: "ST Engineering's flight lab in Singapore: motion-capture cameras on tall stands around a grey floor, a row of white start pads, and one Starling 2 Max on the floor."
caption: ST Engineering's flight lab in Singapore, where the ladder ends.
points:
  - { x: 21.8, y: 17, label: Motion-capture cameras, lx: 37, ly: 9.5 }
  - { x: 52.1, y: 48.6, label: Start pads, lx: 44, ly: 60 }
  - { x: 62.4, y: 70.9, label: Starling 2 Max, lx: 52, ly: 82 }
items:
  - label: M1
    title: Simulation rehearsal
    text: The full flight-day routine on three simulated drones running the real PX4 software, including a geofence breach and recovery.
    state: Done
  - label: M2
    title: Ground station
    text: Network, motion-capture set-up and clock sync on the ground workstation.
    state: In progress
  - label: M3
    title: Drone link, propellers off
    text: PX4 on the drone streams its full telemetry to the ground station over the lab Wi-Fi.
    state: Done
  - label: M4
    title: Tracking into the drone, propellers off
    text: The OptiTrack position is fused into the drone's own estimate, and the frames are checked.
    state: Ready to test
  - label: M5
    title: Hand-carry check
    text: The drone's estimate follows it as it is carried through the flight volume.
    state: Ready to test
  - label: M6
    title: First flight
    text: First Starling flights in Singapore, flown.
    state: Done
---

ST Engineering is bringing up AirStack on the Starling 2 Max in its Singapore hangar one step at a time.
**Who can stop a flight**, highest authority first: a safety pilot holding a radio stop switch, then
PX4's own failsafes on the drone (including loss of the link), then AirStack's software geofence.
