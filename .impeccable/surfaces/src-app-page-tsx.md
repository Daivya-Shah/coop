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

THESIS: Coop as a sketchbook someone keeps about their neighborhood: a hello card and a stack of numbered drawings, not a startup hero over a row of cards.

OWN-WORLD: white ground, #f5f5f5 rounded tiles (20px) holding pen sketches, ink #121212 type in Inter at tight tracking, one ink colour per step (#3E7396, #C4572B, #7B7A2C, #B8232F), yolk #FFC300 only for selection, toasts and the chosen state; plus-icon menu; tiny grey meta labels (No. / caption) on tiles; live New York clock.

STORY: the visitor sees an empty bar, clubs with nowhere to go, the match, the regulars; understands both sides approve; opens the form for their side.

FIRST VIEWPORT: top row: COOP wordmark left, plus-icon menu centre (How it works, For venues, For clubs, A few numbers, Questions, Say hi), venue/club links right. Middle: tagline (60px) and intro left with 1-4 step tabs; flip-through sketch right at up to 760px square. Bottom row: "Starting small, right here in NYC." left; live "New York EDT 7:42:10 PM" clock right.

FORM: Carl Hauser hello card + tile grid (user-pinned, position 1). seed: none (unavailable)

Signature interaction and motion: the landing page-turn between the four sketches (CSS, blur-bridged crossfade); on /how/ each sketch inks in once with a left-to-right clip-path reveal as it enters view. Nothing else moves except press feedback.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
