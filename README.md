# Coop

*Because every flock needs one.*

Coop helps NYC restaurants, bars, and cafés turn their quiet nights into recurring group business, and gives local clubs (run clubs, book clubs, supper clubs and more) a regular place to meet.

## The site

A plain HTML/CSS site with no build step. Open `index.html` in a browser.

| File | Page |
|---|---|
| `index.html` | Home: the "Table for Twenty" flyer |
| `how.html` | How it works, pricing and FAQ |
| `join.html` | Pilot sign-up forms for venues and clubs |
| `styles.css` | All styles |
| `script.js` | Form handling |
| `preview-a/b/c.html` | Alternative home-page drawings, for comparison |
| `_backup-*`, `_draft-v0` | Earlier versions |

## Forms

The sign-up forms on `join.html` don't send anywhere yet. To receive submissions, create a form with a service such as Formspree and put its URL in the `data-endpoint=""` attribute on each `<form class="intake">`.
