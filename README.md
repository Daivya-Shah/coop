# Coop

*Because every flock needs one.*

Coop helps NYC restaurants, bars, and cafés turn their quiet nights into recurring group business, and gives local clubs (run clubs, book clubs, supper clubs and more) a regular place to meet.

## The site

A single-page sketchbook in plain HTML/CSS/JS, with no build step. Open `index.html` in a browser.

| File | What it is |
|---|---|
| `index.html` | The page: a hello card, the sketch grid, and pop-up panels (the idea, how it works, venues, clubs, pricing, FAQ, sign-up) |
| `styles.css` | All styles |
| `script.js` | New York clock, panels, sketch lightbox, sign-up forms |
| `sketches/*.svg` | The pen sketches (light grey ink; the page inverts them to black) |
| `sketches/sketch.py` | The script that draws them: `python sketches/sketch.py sketches` |
| `_backup-*`, `_draft-v0` | Earlier versions |

## Forms

The sign-up forms don't send anywhere yet. To receive submissions, create a form with a service such as Formspree and put its URL in the `data-endpoint=""` attribute on each `<form class="intake">` in `index.html`.
