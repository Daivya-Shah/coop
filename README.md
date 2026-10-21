# Coop

*Because every flock needs one.*

Coop matches NYC social clubs (knit, book, run, chess, art, language…) with restaurants, bars and cafés that have empty seats on their slow nights. The club gets a table it can count on. The venue gets regulars.

## Folder layout

```
Coop/
├── src/
│   ├── app/
│   │   ├── page.tsx          Landing page: flip-through of the four steps
│   │   ├── how/page.tsx      How it works: three steps + For venues / For clubs
│   │   ├── layout.tsx        Font, metadata, join panel available everywhere
│   │   ├── globals.css       All styles
│   │   └── icon.svg          Favicon (the egg)
│   └── components/
│       ├── FlipThrough.tsx   The four sketches, the 1-2-3-4 buttons, auto-advance
│       ├── Join.tsx          Join panel (dialog) + JoinButton + venue/club switch
│       ├── IntakeForm.tsx    Venue and club sign-up forms
│       ├── TopBar.tsx, Tile.tsx, Reveal.tsx, Plus.tsx
├── public/img/
│   ├── brand/                COOP wordmark (dark + light)
│   ├── landing/              step1–4.svg, the flip-through sketches
│   └── sketches/             Sketches used on the How it works page
├── tools/sketch-engine/      Python scripts that draw every sketch (see below)
├── archive/
│   ├── backups/              Every saved version of the site (v1 → v15), each self-contained
│   ├── sketch-sets/          All sketch sets: grey, color, coral, classico, mono, story, v2
│   └── explorations/         Hero / landing experiments that weren't used
├── .env                      Secrets (git-ignored). See .env.example
└── .env.example              Template for .env
```

MCP servers (Figma, 21st.dev, Playwright) are registered in your Claude Code user config, not in this folder.

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
