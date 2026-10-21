---
version: 1
slug: "src-app-page-tsx"
primary_target: "src/app/page.tsx"
related_targets: ["src/app/how/page.tsx"]
---

# Coop site (landing + scrolling story page)

Mode: Persuade. Code-led (no image generation available). Direction pinned by the user: carlhauser.com template, existing hand-drawn sketches, white page, Inter (the template's face). No concept roll: a pinned direction beats it.

Audience: NYC venue owners and club organizers, equal weight. Action: open the venue or club interest form. Proof: the sketches dramatize the mechanism; three sourced context statistics; no fabricated outcomes.

Constraints: landing is exactly one screen (desktop); everything else scrolls on /how/. Fee wording only as PRODUCT.md allows.

## Direction contract

THESIS: Coop as a sketchbook left open on a grey table: Carl Hauser's hello card and rounded cards, rearranged so the four story drawings are a real pile of pages you can flick, and every other drawing is drawn in front of you. Not a hero over a row of feature cards.

OWN-WORLD: #e6e6e6 table, #f5f5f5 rounded cards (24px), white paper tiles (16px) holding pen sketches, ink #121212 Inter at tight tracking, one ink per part of the story (venue #3E7396, clubs #C4572B, match #7B7A2C, regulars #B8232F), yolk #FFC300 for what answers the visitor and for the closing card, #2e2e2e footer card; plus-icon menu; tiny grey "No. NN" tile labels; live New York clock.

STORY: the visitor flicks through venue, clubs, match, regulars; on the scrolling page sees how a club and a venue meet (cards, overlap, same time next week), each side's problem and answer, the sourced numbers, the first neighborhoods; opens the form for their side.

FIRST VIEWPORT: left, the hello card: wordmark, plus menu, venue/club links; tagline at up to 84px; intro; "Starting small, right here in NYC." and the clock at the foot. Right, on the bare table: the pile of four sketch pages, numbered tabs 1-4 and a one-line caption.

FORM: Carl Hauser hello card + tile grid (user-pinned, position 1; the roll was run and set aside because a user-pinned direction beats it). seed:1d83436c5b198c93

Sketch map (each drawing appears once): landing pile = step1-4; how it works = intro-cards, who-gets-along, weekly-calendar (match green); venues = corner-booth, floor-plan (venue blue); clubs = group-chat, reserved-card (club orange); first flock = pilot-map (regulars red); join panel = name-tags.

Signature interaction and motion: the story pile (adapted from the 21st.dev Motion "Card stack": drag with momentum or tap to send the top page to the back, tabs to jump, auto-turn that pauses on hover, focus and hidden tab); on the scrolling page each sketch below the fold draws itself stroke by stroke and then its colour washes in (the 21st.dev "Line Draw SVG" technique, in CSS). Beyond that: a 60ms first-load stagger, press feedback, small hover nudges on fine pointers only.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
