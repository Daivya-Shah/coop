---
name: Coop
description: A neighborhood sketchbook for NYC clubs and the venues with room for them.
colors:
  ink: "#121212"
  yolk: "#ffc300"
  venue: "#3e7396"
  club: "#c4572b"
  match: "#7b7a2c"
  regulars: "#b8232f"
  page: "#ffffff"
  tile: "#f5f5f5"
  chip: "#f1f1f1"
  soft: "#4d4d4d"
  meta: "#666666"
  line: "#e2e2e2"
typography:
  display:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "clamp(44px, 5.4vw, 80px)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "-0.045em"
  display-tagline:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "clamp(44px, 4.4vw, 62px)"
    fontWeight: 700
    lineHeight: 0.98
    letterSpacing: "-0.04em"
  headline:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "clamp(34px, 3.6vw, 54px)"
    fontWeight: 700
    lineHeight: 1.02
    letterSpacing: "-0.04em"
  lede:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "clamp(19px, 1.7vw, 22px)"
    fontWeight: 600
    lineHeight: 1.25
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "20px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "17px"
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: "-0.01em"
  meta:
    fontFamily: "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"
    fontSize: "12px"
    fontWeight: 400
    fontFeature: "\"tnum\""
rounded:
  focus: "4px"
  toast: "14px"
  tile: "20px"
  pill: "999px"
spacing:
  tile-gap: "8px"
  gutter: "24px"
  tile-inset: "42px 22px 18px"
  section: "clamp(96px, 11vw, 168px)"
  wrap: "min(1320px, 100vw - 48px)"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.page}"
    rounded: "{rounded.pill}"
    padding: "13px 22px"
  button-primary-hover:
    backgroundColor: "{colors.yolk}"
    textColor: "{colors.ink}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "13px 22px"
  step-tab:
    backgroundColor: "{colors.chip}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    size: "46px"
  chip:
    backgroundColor: "{colors.chip}"
    textColor: "{colors.ink}"
    rounded: "{rounded.pill}"
    padding: "7px 13px"
  chip-selected:
    backgroundColor: "{colors.yolk}"
    textColor: "{colors.ink}"
  sketch-tile:
    backgroundColor: "{colors.tile}"
    rounded: "{rounded.tile}"
  input-underline:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "0px"
    padding: "8px 0"
  toast:
    backgroundColor: "{colors.yolk}"
    textColor: "{colors.ink}"
    rounded: "{rounded.toast}"
---

# Design System: Coop

## Overview

**Creative North Star: "The Neighborhood Sketchbook"**

Coop is a sketchbook someone keeps about their neighborhood: a hello card on top, then a stack of numbered pen drawings on pale grey tiles. The page is plain white and the type is near-black Inter set tight, so the drawings carry all of the warmth. Colour belongs to the sketches (one ink per step of the story) and to a single yolk yellow that answers the visitor whenever they touch something.

Density is low and calm. One screen on the landing; on the story page, generous gaps between sections and tight 8px gutters between tiles, so drawings read as a set laid on a table. Structure comes from hairlines and tiles, not boxes and shadows.

Motion is small and deliberate: a blur-bridged page turn between drawings, an ink-in reveal as a sketch enters view, a 55ms first-load stagger, press feedback, and hover nudges on fine pointers only. Nothing else moves.

**Key Characteristics:**
- White page, #f5f5f5 rounded tiles holding hand-drawn pen sketches.
- Near-black Inter at tight negative tracking for every heading.
- One ink colour per story step; yolk only as the answering colour.
- Plus-in-a-circle icon as the system's one glyph: menu bullets, accordion toggles, close button.
- Tiny grey tabular meta labels (caption + "No. 01") on every tile.
- Hairline rules (#e2e2e2) instead of cards for lists, stats and FAQ.

## Colors

A monochrome ink-on-white page lit by four sketch inks and one egg-yolk yellow.

### Primary
- **Pen Ink** (ink): every heading, the primary pill, input underlines, focus rings, the plus icon fill. The page's voice.

### Secondary
- **Egg Yolk** (yolk): the answering colour. Pill hover, chosen chip, the venue/club switch indicator, input focus underline, link hover underline, text selection, toasts. Also the yolk in the wordmark's egg.

### Tertiary
- **Harbor Blue** (venue): step 1, the venue sketch; tick bullets on the venue side.
- **Brick Orange** (club): step 2, the clubs sketch; tick bullets on the club side.
- **Olive Moss** (match): step 3, the match sketch.
- **Lamp Red** (regulars): step 4, the regulars sketch; also the invalid-field underline and outline.

### Neutral
- **Paper White** (page): page ground and the join panel surface.
- **Tile Grey** (tile): the sketch tile ground; also the stroke of the plus glyph's cross.
- **Chip Grey** (chip): resting step tabs, form chips, the switch track.
- **Pencil Grey** (soft): secondary copy: intro, story paragraphs, footer.
- **Caption Grey** (meta): tile meta labels, field labels, source links, fine print.
- **Hairline** (line): 1px rules between list rows, FAQ items, and above the footer.

### Named Rules
**The One Ink Per Step Rule.** Each of the four story steps owns one ink, used for its drawing and for that side's accents (the sliding step dot, tick bullets). Never mix step inks inside one drawing or swap them between steps.

**The Yolk Answers Rule.** Yolk appears only as a response: hover, selection, focus, the chosen state, a toast. It is never a resting fill for a section, a heading, or decoration (the wordmark egg is the one fixed instance).

## Typography

**Display Font:** Inter (with system-ui, -apple-system, Segoe UI fallback)
**Body Font:** Inter
**Label/Mono Font:** Inter with tabular numerals for meta, clock and statistics.

**Character:** One family doing every job, distinguished by weight and tracking. Headings are bold and tightly packed so they sit like a hand-lettered title beside the drawings; body stays regular and grey so it never competes with the ink.

### Hierarchy
- **Display** (700, clamp 44-80px, 0.98): the story page's opening line only.
- **Display Tagline** (700, clamp 44-62px, 0.98; 42px under 640px): the landing tagline.
- **Headline** (700, clamp 34-54px, 1.02): section titles on the story page; side titles drop to clamp 30-44px, the closing line rises to clamp 38-68px with a 16ch cap.
- **Lede** (600, clamp 19-22px, 1.25): the join panel's first line; statistic rows use a close cousin (500, clamp 21-27px, 1.32, 34ch).
- **Title** (600, 20px, 1.2): step and rule-list titles.
- **Body** (400, 17px, 1.5, max 62ch): story paragraphs in Pencil Grey; the landing intro is 500 / 18px / 1.38 at 460px.
- **Label** (600, 17px, -0.01em): plus-menu items, FAQ triggers (clamp 17-19px); buttons and chips use 600 at 14-15px.
- **Meta** (400, 12-13px, tabular): tile captions and numbers, field labels, source links, fine print.

### Named Rules
**The Tight Ink Rule.** Every heading is 600-700 with negative tracking (-0.02em to -0.045em) and line-height at or under 1.2; balance-wrapped. Body text is never tracked.

**The Tabular Count Rule.** Anything that counts (tile numbers, step tabs, the clock, statistic figures) uses tabular numerals.

## Layout

Content sits in a single centred wrap (min(1320px, 100vw - 48px); 100vw - 32px under 640px). The landing is exactly one screen on desktop: a three-row grid (top bar, flip-through, footer row) at min-height 100svh. The top bar is a 1fr / auto / 1fr grid: wordmark left, the plus menu centre as a two-column, three-row list, venue/club text links right-aligned.

The story page is a single column of sections separated by clamp(96px, 11vw, 168px). Sections are asymmetric two-column splits (roughly 0.85fr copy to 1.15fr tiles or rows) with clamp(32px, 5vw, 80px) gaps. The three how-it-works tiles step down the page (0, 64px, 128px offsets) like cards dealt onto a table. Tiles group with 8px gaps.

Breakpoints: 1080px moves the plus menu to a second row; 980px stacks the join panel with its sketch on top; 860px collapses every split to one column and removes the step offsets; 640px narrows the wrap, drops the tile radius to 16px, and stacks tile pairs.

## Elevation & Depth

Flat. Depth comes from the tile grey against white and from hairlines, never from lifted surfaces. The single exception is the join panel, a modal that floats over a white frosted backdrop.

### Shadow Vocabulary
- **Panel float** (`box-shadow: 0 30px 80px -40px rgba(0,0,0,.35), 0 0 0 1px rgba(0,0,0,.04)`): the join panel only.
- **Ghost ring** (`box-shadow: inset 0 0 0 2px var(--ink)`): the ghost pill's outline; turns yolk on hover. A stroke, not elevation.

### Named Rules
**The Paper Stays Flat Rule.** Tiles, lists and sections never carry a shadow. Only an overlay that sits above the page (the join panel) may float.

## Shapes

Two corner families: soft rounded rectangles for tiles and the panel (20px, 16px on phones) and full pills or circles for everything pressable (buttons, step tabs, chips, the switch). Inputs are the exception: no box at all, just a 1.5px underline. Lists are open rows divided by 1px hairlines. The recurring glyph is a filled circle with a cross, which rotates 90 degrees on hover and sits at 45 degrees as the close button.

## Components

### Buttons
Confident ink pills that turn yolk under the pointer.
- **Shape:** full pill (999px).
- **Primary:** Pen Ink fill, white text, 600 at 15px, 13px 22px padding.
- **Hover / Focus:** fill becomes Egg Yolk with ink text (fine pointers only); focus is a 2px ink outline at 3px offset; press scales to 0.97 over 160ms on the strong ease-out.
- **Ghost:** transparent with a 2px inset ink ring; the ring turns yolk on hover. Used for the second of a venue/club pair.
- **Disabled:** 50% opacity, progress cursor.

### Step Tabs
- **Style:** 46px circles in Chip Grey with tabular 600 numerals. A coloured dot slides beneath the active tab (300ms in-out) and takes the current step's ink; the active numeral turns white. Unselected hover darkens to #e6e6e6.

### Chips
- **Style:** Chip Grey pills, 600 at 14px, 7px 13px padding, wrapping with 6px gaps.
- **State:** checked turns Egg Yolk; keyboard focus draws a 2px ink outline.

### Switch
- **Style:** Chip Grey pill track with 4px padding; a yolk pill indicator slides under the chosen side (250ms in-out).

### Cards / Containers
- **Corner Style:** 20px (16px under 640px).
- **Background:** Tile Grey for sketch tiles; Paper White for the join panel.
- **Shadow Strategy:** none on tiles; the panel uses the panel float (see Elevation).
- **Border:** none.
- **Internal Padding:** tiles inset their drawing 42px top, 22px sides, 18px bottom to leave room for the meta row; the panel pads clamp(24px, 3vw, 40px).

### Inputs / Fields
- **Style:** no box; transparent ground, 1.5px ink underline, 500 at 17px (never below 16px on phones). Labels sit above in Caption Grey at 13px.
- **Focus:** the underline turns Egg Yolk; no outline.
- **Error:** the underline (or checkbox outline) turns Lamp Red.

### Navigation
- **Plus menu:** 600 at 17px (16px on phones), each item led by a 22px plus glyph that rotates 90 degrees on hover. No underline.
- **Side links:** 600 at 16px, underlined at 1.5px with a 3px offset; underline turns yolk on hover.
- **Mobile:** the menu drops below the wordmark row, three then two columns.

### Sketch Tile (signature)
A Tile Grey rounded square holding one pen sketch, with a meta row across the top: caption left, "No. 01" right, in 12px tabular Caption Grey. Tiles are numbered in reading order. On first entry into view the drawing inks in left to right with a clip-path reveal (1100ms in-out); on fine-pointer hover the drawing scales 1.03 and tilts -0.4 degrees.

### Flip-Through (signature)
The landing's four step drawings stacked in one square stage up to 740px. A page turn crossfades them: the outgoing drawing leaves in 200ms, the incoming settles over 500-650ms with a 2px blur bridging the two and a slight rotate. It advances every 4.2s and pauses on hover, keyboard focus and hidden tabs.

## Do's and Don'ts

### Do:
- **Do** put every sketch on a Tile Grey tile with its caption and tabular "No." number, numbered in reading order.
- **Do** keep each story step in its own ink (venue, club, match, regulars) and let that side's accents inherit it.
- **Do** use Egg Yolk only as a response: hover, focus, selected, toast.
- **Do** set headings in Inter 600-700 with negative tracking; keep body regular in Pencil Grey under 62ch.
- **Do** separate list rows, statistics and FAQ items with 1px hairlines rather than cards.
- **Do** use the two custom curves for motion (ease-out for entrances and presses, in-out for things that slide or reveal), gate hover effects to fine pointers, and keep fades but drop movement under reduced motion.

### Don't:
- **Don't** add shadows to tiles, sections or buttons; only the join panel floats.
- **Don't** use Egg Yolk as a section background or heading colour.
- **Don't** box the form inputs; they stay underlines.
- **Don't** introduce a second icon glyph or icon font; the plus-in-a-circle carries menu, accordion and close.
- **Don't** animate anything beyond the page turn, the ink-in, the first-load stagger, press feedback and fine-pointer hover nudges.
