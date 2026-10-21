# Coop

*Because every flock needs one.*

Coop matches NYC social clubs (knit, book, run, chess, art, language…) with restaurants, bars and cafés that have empty seats on their slow nights. The club gets a table it can count on. The venue gets regulars.

## Folder layout

```
Coop/
├── src/
│   ├── app/
│   │   ├── page.tsx          Landing: one screen, Carl Hauser-style hello card + flip-through
│   │   ├── how/page.tsx      The scrolling page: story, how it works, numbers, venues, clubs, FAQ
│   │   ├── layout.tsx        Font, metadata, join panel available everywhere
│   │   ├── globals.css       All styles
│   │   └── icon.svg          Favicon (the egg)
│   ├── content/coop.ts       Every word on the site (edit copy here)
│   └── components/
│       ├── FlipThrough.tsx   The four sketches, the 1-2-3-4 buttons, auto-advance
│       ├── Join.tsx          Join panel (dialog) + JoinButton + venue/club switch
│       ├── IntakeForm.tsx    Venue and club sign-up forms
│       ├── TopBar.tsx        Wordmark, plus-icon menu, venue/club links
│       ├── Clock.tsx         Live New York clock
│       ├── Faq.tsx           Questions (Base UI Accordion)
│       ├── Tile.tsx, Plus.tsx
├── public/img/
│   ├── brand/                COOP wordmark (dark + light)
│   ├── landing/              step1–4.svg, the flip-through sketches
│   └── sketches/             Sketches used on the How it works page
├── tools/sketch-engine/      Python scripts that draw every sketch (see below)
├── archive/
│   ├── backups/              Every saved version of the site (v1 → v15), each self-contained
│   ├── sketch-sets/          All sketch sets: grey, color, coral, classico, mono, story, v2
│   └── explorations/         Hero / landing experiments that weren't used
├── PRODUCT.md                Product truth for Impeccable (users, facts, fee wording)
├── .impeccable/              Impeccable surface brief (design direction)
├── .mcp.json                 MCP servers: Figma, 21st.dev, Playwright, Motion
├── .claude/
│   ├── skills/               /motion, Emil Kowalski's skills, /impeccable
│   └── agents/               motion-reviewer, impeccable-* (design review helpers)
├── .env                      Secrets (git-ignored). See .env.example
└── .env.example              Template for .env
```

Everything Claude Code uses lives in this folder. Open Claude Code **in the Coop folder** and approve the servers once when asked:

- **figma**: read Figma designs into code, push pages into Figma. Signs in with your Figma account.
- **21st**: search and add 21st.dev components (`/ui ...`). Reads `API_KEY_21ST` from your environment.
- **playwright**: drives Chrome to open, click and screenshot the site. Output goes to `.playwright-mcp/` (git-ignored).
- **motion**: searches the official Motion (Framer Motion) docs and examples. Free, no account.

Skills (type `/name` in Claude Code): `/motion`, plus Emil Kowalski's `/emil-design-eng`, `/animate`, `/review-animations`, `/improve-animations`, `/find-animation-opportunities`, `/animation-performance`, `/animation-vocabulary`, `/apple-design`, `/pick-ui-library`, `/prototype`, `/mobile-native`, `/break-ui` (MIT, from github.com/emilkowalski/skills), and `/impeccable` (Paul Bakaus's design skill pack, Apache-2.0).

**Impeccable** also installs a design checker that runs automatically after Claude edits UI files (hooks in `.claude/settings.local.json`). Its 19 MB program is git-ignored; on a new computer run `npx impeccable@4.6.0 install -y --providers=claude --scope=project`. Check the site any time with `npx impeccable detect out/` after a build.

**Components follow Emil's picks:** Base UI for the join dialog and the tabs, Sonner for the confirmation toast, Motion for scroll reveals, clsx for class names.

## Running it

Next.js 15 (React, TypeScript, Tailwind) with [Motion](https://motion.dev) (Framer Motion) for animation.

```
npm install
npm run dev        # http://localhost:3000
npm run build      # static site written to out/, ready for any host
```

The last plain-HTML version is in `archive/backups/backup-v15-static-html/` (git tag `checkpoint-static-html`).

## Redrawing sketches

```
cd tools/sketch-engine
python landing_steps.py ../../public/img/landing        # the four flip-through sketches
python sketch.py OUT_DIR --color --ink=#3E7396 NAME     # any single sketch in one colour
```

`sketch.py` is the pen engine (wobbly doubled lines, hatching, marker fills, handwriting). The other scripts build on it.

## Secrets

Keys live in `.env` (never committed). Claude Code reads `API_KEY_21ST` from your Windows user environment, so after changing a key in `.env`, also run:

```
[Environment]::SetEnvironmentVariable('API_KEY_21ST', '<new key>', 'User')
```

## Forms

The venue and club sign-up forms don't send anywhere yet. To receive submissions, create a form with a service such as Formspree and put its URLs in `.env.local`:

```
NEXT_PUBLIC_FORM_VENUE=https://formspree.io/f/...
NEXT_PUBLIC_FORM_CLUB=https://formspree.io/f/...
```

Then rebuild. Until then, submissions are only logged in the browser console.
