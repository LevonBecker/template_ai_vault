---
applyTo: "topics/travel/**"
---
# Travel Instructions

This file is an example of a **topic-scoped preferences file** — instructions that only apply
when working inside one topic (`applyTo` above), as opposed to `.github/instructions/project.instructions.md`
which applies everywhere. Replace the placeholder content below with your own travel preferences
so the AI can tailor trip planning without you repeating yourself in every chat.

## Travel Style Preferences

When suggesting activities, food, nightlife, and daily plans for any trip topic, describe what you
actually want, e.g.:

- **Pace**: relaxed vs. packed itinerary; how many major activities per day
- **Nightlife**: bars/live music vs. quiet evenings; any hard no's (dress codes, bottle service, etc.)
- **Food**: foodie vs. food-as-fuel; cuisines you love or avoid; dietary constraints
- **Sightseeing style**: deep dives at fewer sites vs. quick stops at many
- **Trip cadence**: how often you travel and typical trip length
- **Flight preferences**: nonstop vs. stopovers, max acceptable leg length, cabin class
- **Climate preference**: what temperature/humidity range you enjoy
- **Luggage style**: carry-on only vs. checked bags

## Travelers

Document who you're planning for and what the AI should know to tailor suggestions:

**Home Base:** _City, State/Country_
**Home Airport:** _Airport code_

| | Traveler 1 | Traveler 2 |
|---|---|---|
| Fitness level | | |
| Mobility notes (relevant to trip planning only) | | |
| Interests | | |
| Activities to avoid | | |
| Dietary preferences | | |

**Activity guidance:**
- Note pacing constraints (e.g. don't over-schedule back-to-back physical activity)
- Note anything that should shape day-by-day planning

## Future Destinations of Interest

- **Destination** — why it's on the list
- **Destination** — why it's on the list

## Trip Docs Structure

Standard folder structure for each trip subtopic:

```
trips/<year_destination>/
├── chats/
├── docs/
│   ├── destinations/     # Per-city must-see/do files
│   ├── itinerary.md      # Day-by-day trip skeleton
│   └── pricing.csv       # Flights, hotels, totals
├── AGENTS.md
└── CLAUDE.md
```
