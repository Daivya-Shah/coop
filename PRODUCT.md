# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Two audiences, given equal weight:

- **Venue owners and managers** of New York City restaurants, bars and cafés that have suitable space during quieter periods (a slow Monday, an unused back room). Their job: fill quiet nights with repeat customers without losing control of their space.
- **Organizers of established NYC clubs and recurring social groups** (run, book, chess, knitting, art, language exchange, game nights). Their job: find a dependable place their group can keep coming back to, instead of venue-hunting every week.

## Product Purpose

Coop introduces established clubs to neighborhood venues with room on quieter nights, checks fit, coordinates mutually approved bookings, and helps manage the ongoing arrangement. Groups get a dependable home; venues get the chance to welcome repeat customers.

Version one's goal is qualified inbound interest and the start of a real conversation with venues and clubs. Not payment, not self-service booking.

## Positioning

A founder-assisted matchmaker, not a booking marketplace. Coop sources and vets real groups, both sides approve every introduction, and Coop stays involved after the match (reminders, headcounts, schedule changes, finding another compatible group).

## Operating Context

- Founder-assisted NYC pilot, starting in one or two walkable neighborhood clusters (candidates on the forms: Chelsea, Flatiron, East Village, Lower East Side).
- Interest arrives through two separate forms (venue, club). Submissions go to a founder inbox or CRM; there are no accounts.
- Venues take customer food-and-drink payments through their own point of sale; Coop invoices the venue separately when a fee is due.

## Capabilities and Constraints

- Venues are the paying customers. Clubs join free: no membership fee. Venue food-and-drink minimums may apply, are the venue's, and are always explained before anything is agreed.
- Fees, the only public wording allowed: no fee to join the pilot; the first completed matched event has no Coop fee; after that, a small percentage for completed club nights, agreed together in advance. Never publish a number, percentage, subscription price, cap, calculator or pricing example.
- Venues control nights, capacity, activities, group approval and spending expectations. Nothing is booked without both sides' approval.
- Never promise guaranteed revenue, attendance, a full room, an immediate match, or a response deadline.
- Thank-you after a form: "Thanks for saying hi. We're reviewing our first NYC pilot matches and will reach out if we see a fit."
- Stack: existing Next.js 15 static-export app (React, TypeScript, Tailwind), Motion, Base UI, Sonner.
- Undecided: contact email, domain, form endpoint (Formspree planned), privacy policy text (needs review).

## Brand Commitments

- Name **Coop**, tagline exactly: "Because every flock needs one."
- Hand-drawn COOP wordmark; the second O is an egg with a yolk (`public/img/brand/wordmark.svg`).
- Voice: warm, lightly playful, conversational, genuinely New York; short sentences you could say out loud. A handwritten note from your favorite neighborhood café, not an enterprise software page.
- Illustration: delicate, visibly imperfect hand-drawn pen sketches, one colour per step (venue #3E7396, clubs #C4572B, match #7B7A2C, regulars #B8232F).
- Binding user direction: inspired by carlhauser.com (hello card, plus-icon menu, live clock, rounded sketch tiles with small meta labels); the landing is a single screen, with everything else opening as panels; plain white page for now.

## Evidence on Hand

- Sketches: `public/img/landing/step1-4.svg` (venue, clubs, match, regulars) and `public/img/sketches/*.svg` (name tags, pilot map, weekly calendar, corner booth, floor plan, club kit, no app needed).
- Three contextual industry statistics, allowed only with their source and qualifier shown:
  - 91% of surveyed US adults 18-35 said it matters that events help them feel connected to their local community (Eventbrite 2026 Social Study, survey July 2025). https://www.eventbrite.com/blog/social-study-event-trends-neighborhood-revival/
  - 45% of surveyed NYC hospitality establishments cited a lack of customers as a major challenge (NYC Hospitality Alliance, 2024 survey of 354 establishments). https://myemail.constantcontact.com/DECLINING-SALES-AND-INDUSTRY-CONCERNS-AMID-SUMMER-2024-CHALLENGES.html?aid=A0cBf3hnp6Y&soid=1116674519904
  - 233% growth in US coffee-and-running event attendance on Eventbrite, Aug 2024-Jul 2025 vs. the prior 12 months. https://www.eventbrite.com/social-study-trends/
- These are context, not Coop results. No testimonials, partner venues, customer counts or outcomes exist: never fabricate them.

## Product Principles

1. Both sides say yes first. Every surface makes explicit approval visible.
2. Honest and early. Say "pilot" and "starting small"; promise conversations, not outcomes.
3. Warm before clever. Plain, spoken language over marketing claims.
4. Venue control is the business case: their space, their rules.
5. Free for clubs, simple for venues. Fee wording never goes beyond the approved sentence.

## Accessibility & Inclusion

WCAG 2.2 AA: text contrast, keyboard-operable panels and tabs, visible focus, reduced-motion support, 16px+ form inputs on phones.
