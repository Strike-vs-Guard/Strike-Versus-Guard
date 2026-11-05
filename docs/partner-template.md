---
# ─────────────────────────────────────────────────────────────────────────────
# Template for a partner file. Copy this whole file to content/partners/<NAME>.md
# and replace ABC with the name. Images go in content/partners/<NAME>/, team
# photos in content/partners/<NAME>/people/. Field rules: CONTRIBUTING.md §2 and
# src/content.config.ts. Delete optional lines you do not use.
# A NEW partner also needs (ST Engineering): its id (file name in lower case) in
# PARTNER_IDS in src/content.config.ts, and lines in .github/CODEOWNERS.
# ─────────────────────────────────────────────────────────────────────────────
short: ABC                                   # 24 characters; cards and navigation
institution: Full Institution Name
lab: ABC Lab                                 # optional
labFull: Lab name written out in full        # optional, if lab is an acronym
labBlurb: >-
  We are the ... lab in ... at .... We work on .... In Strike vs Guard we ....
# labBlurb: optional, 420 characters, three sentences in "we" voice ("About the lab")
lead: Prof Firstname Lastname                # optional; "Principal investigator" in the page head
role: Partner                                # Funding sponsor | Lead partner | Partner
contribution: What you contribute, in a few words
# contribution: 70 characters, shown on the card
summary: >-
  One or two sentences for the home page card.
# summary: 320 characters
work:                                        # one line per layer you work on, 90 characters each
  strategy: "What you do on the strategy layer."
  # safety: "..."
  # flight: "..."
  # localisation: "..."
  # drones: "..."
  # integration: "..."
logo: ./ABC/logo.png                         # required; must exist
logoMark: ./ABC/mark.png                     # optional square emblem for the Partners menu
labLogo: ./ABC/lab-logo.png                  # optional
logoAlt: Full Institution Name               # optional; defaults to institution
website: https://example.org                 # optional, full https:// address
contact: someone@example.org                 # optional, public
order: 6                                     # partner order: ST Engineering 2, NUS 3, UPenn 4, CMU 5
# page: false                                # only for a card with no page (the funder)
updated: 2026-11-05                          # YYYY-MM-DD of your last edit
people:
  - name: Prof Firstname Lastname
    role: Professor, Department
    photo: ./ABC/people/firstname-lastname.jpg   # 400 px square JPG, 80 KB or less
    lead: true
    bio: >-
      Firstname Lastname is a Professor in ... at ... and leads the ... Lab.
      They study ...; PhD in ... from ....
    # bio: 300 characters, third person, two sentences, no awards
    link: https://example.org/people/firstname-lastname
  - name: Second Person
    role: PhD student
    photo: ./ABC/people/second-person.jpg
  - name: Third Person
    group: Interns                           # optional; own small heading after everyone else
publications: []
# publications:
#   - title: A paper title
#     authors: Surname, Surname, Surname
#     venue: IROS 2026
#     year: 2026
#     status: accepted                       # published | accepted | preprint | workshop
#     link: https://arxiv.org/abs/0000.00000
#     pdf: https://example.org/paper.pdf
#     image: ./ABC/paper-first-page.jpg
---

## What we're trying

Write as "we". Name people and dates, give one number per claim with its conditions.

## What we've flown

![Describe the photo for someone who cannot see it](./ABC/flight.jpg)

## Where it breaks

What did not work, or is still open.
