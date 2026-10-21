// All site copy lives here. Fee wording must stay exactly as PRODUCT.md allows.

export const TAGLINE = "Because every flock needs one.";

export const HERO_INTRO =
  "Coop brings NYC clubs and neighborhood spots together. Clubs find somewhere to keep coming back to, and restaurants, bars and cafés get a few more familiar faces on nights they could use a crowd.";

export const STEPS = [
  { color: "#3E7396", label: "1, the venue", alt: "1, the venue: a bar with four empty stools and an empty table on a slow night." },
  { color: "#C4572B", label: "2, the clubs", alt: "2, the clubs: knit, book, art, run, chess and talk, with nowhere regular to meet." },
  { color: "#7B7A2C", label: "3, the match", alt: "3, the match: the Coop house with the egg, right area, right size, right night." },
  { color: "#B8232F", label: "4, the regulars", alt: "4, the regulars: the long table with lamps lit, one chair saved for you." },
];

/** The plus-icon menu. Anchors point into the scrolling page. */
export const MENU = [
  { label: "How it works", href: "/how/#how" },
  { label: "For venues", href: "/how/#venues" },
  { label: "For clubs", href: "/how/#clubs" },
  { label: "A few numbers", href: "/how/#numbers" },
  { label: "Questions", href: "/how/#questions" },
];

export const MERRIER = {
  title: "The more, the merrier.",
  body: [
    "Run clubs. Book clubs. Chess nights. People who get together to knit, paint, talk, play, or just hang out.",
    "New York is full of little groups of people who make time for each other. And it’s full of lovely neighborhood spots that could use a few more people on a quiet Tuesday.",
    "We thought, why not introduce them? That’s really all Coop is about.",
  ],
};

export const HOW = [
  {
    sketch: "name-tags",
    caption: "Hello, my name is",
    title: "Tell us a little about yourself.",
    body: "Have a club looking for somewhere to meet? Or a space that could use a little more company? We’d love to hear about it.",
  },
  {
    sketch: "pilot-map",
    caption: "The right neighborhood",
    title: "We’ll see who might get along.",
    body: "We look for places and groups that make sense together. The right neighborhood, the right night, the right kind of crowd. Nothing gets booked until everyone’s happy with the plan.",
  },
  {
    sketch: "weekly-calendar",
    caption: "Their night, every week",
    title: "Make yourself at home.",
    body: "The first get-together is just the beginning. Hopefully, before long, it’s the spot everyone knows to show up to.",
  },
];

export const NUMBERS = {
  title: "A few numbers that got us thinking.",
  items: [
    {
      figure: "91%",
      text: "of young US adults surveyed said it matters that events help them feel connected to their local community.",
      source: "Eventbrite Social Study, 2026 (US adults 18–35, surveyed July 2025)",
      href: "https://www.eventbrite.com/blog/social-study-event-trends-neighborhood-revival/",
    },
    {
      figure: "45%",
      text: "of surveyed NYC hospitality establishments cited a lack of customers as a major challenge.",
      source: "NYC Hospitality Alliance, 2024 survey of 354 establishments",
      href: "https://myemail.constantcontact.com/DECLINING-SALES-AND-INDUSTRY-CONCERNS-AMID-SUMMER-2024-CHALLENGES.html?aid=A0cBf3hnp6Y&soid=1116674519904",
    },
    {
      figure: "233%",
      text: "growth in US attendance at coffee-and-running events on Eventbrite.",
      source: "Eventbrite US event data, Aug 2024–Jul 2025 vs. the prior 12 months",
      href: "https://www.eventbrite.com/social-study-trends/",
    },
  ],
  outro: "Lots of people looking to get together. Lots of neighborhood spots that could use the company. We thought we’d introduce them.",
  note: "Different populations and methods. These are industry findings, not Coop results.",
};

export const VENUES = {
  title: "Got a quiet night? We’ve got some ideas.",
  lead: "For the places that make a neighborhood: restaurants, bars and cafés.",
  tiles: [
    { sketch: "corner-booth", caption: "The corner nobody books" },
    { sketch: "floor-plan", caption: "A back room, empty" },
  ],
  body: [
    "Maybe Mondays are a little slow. Maybe there’s a back room that doesn’t get used much. Or maybe you’d just love to see a few more familiar faces coming through the door.",
    "We find local clubs looking for somewhere to meet regularly and introduce them to places like yours. You tell us what works for your space; we look for a group that fits. And if it feels right, maybe that quiet Wednesday becomes chess night. Every Wednesday.",
  ],
  rulesTitle: "Your space. Your rules.",
  rules: [
    "You decide which nights work and how many people you’re comfortable hosting.",
    "You set any spending expectations, and you always have the final say before anything is booked.",
    "No fee to join our pilot, and your first completed matched event is free of any Coop fee.",
    "After that, a small percentage for completed club nights, agreed together in advance.",
  ],
  cta: "Let’s bring some people in",
};

export const CLUBS = {
  title: "Your people deserve a place.",
  lead: "For the people who keep showing up: clubs, communities and little gatherings.",
  tiles: [
    { sketch: "club-kit", caption: "What each club brings" },
    { sketch: "no-app-needed", caption: "Members just get a text" },
  ],
  body: [
    "You’ve already done the lovely part. You’ve brought people together. Finding somewhere to fit everyone shouldn’t be the hard part.",
    "Maybe your book club keeps hopping between cafés. Maybe your run club needs somewhere to wind down. Or maybe the group chat keeps asking, “So where are we meeting this week?” Tell us what you’re looking for, and we’ll help you find a spot you can come back to again and again.",
  ],
  rulesTitle: "No membership fee.",
  rules: [
    "Coop is free for clubs to join.",
    "No venue-hunting every week. Just a place for your people.",
    "Some places may have a minimum food or drink spend. You’ll know the details before agreeing to anything.",
    "Weekly, every other week or monthly: whatever works for your group.",
  ],
  cta: "Let’s find your spot",
};

export const FIRST_FLOCK = {
  title: "Our first flock is coming together.",
  body: [
    "We’re starting Coop with a handful of clubs and neighborhood spots around New York City.",
    "It’s early days, which means we’re getting to know people, figuring out what works, and doing our best to make some really lovely introductions. No big commitments just to say hello.",
  ],
  cta: "Come say hi",
};

export const FAQ = [
  {
    q: "Does it cost anything for my club?",
    a: "Nope. Coop is free for clubs to join. Some venues may ask your group to agree to a minimum food or drink spend, and we’ll always talk that through before anything is confirmed. Any cancellation or shortfall terms will be clear in advance too.",
  },
  {
    q: "What kinds of clubs can join?",
    a: "Pretty much any group that gets together regularly. Running, reading, chess, crafts, language exchanges, game nights, you name it. If you’ve got people who love showing up, we’d love to meet you.",
  },
  {
    q: "Does my group have to be a certain size?",
    a: "Not really. Some places have room for a long table, others have an entire back room. Tell us how many people usually come, and we’ll see what’s possible.",
  },
  {
    q: "Do we have to meet every week?",
    a: "Not at all. Weekly, every other week, monthly: tell us what works for your group. The idea is to find somewhere you can keep coming back to.",
  },
  {
    q: "I’m a venue owner. What will this cost me?",
    a: "Nothing to join the pilot, and your first completed matched event has no Coop fee. After that, there’s a small percentage-based fee for completed club nights. We’ll explain the details and agree on them with you before any booking is confirmed. No surprises.",
  },
  {
    q: "Can I choose which clubs come to my venue?",
    a: "Of course. It’s your space. You’ll get to know the kind of group we’re suggesting, when they’d like to come, how many people to expect, and any spending arrangements. Nothing gets confirmed without your approval.",
  },
  {
    q: "What if we need to cancel or change a date?",
    a: "Things happen. Give us as much notice as you can, and we’ll help figure it out. Any cancellation terms will be agreed in advance, so everyone knows where they stand.",
  },
  {
    q: "Where is Coop available?",
    a: "We’re starting in NYC, one neighborhood and one introduction at a time. If you’re based here, we’d love to hear from you.",
  },
];

export const CLOSE = {
  title: "Good things happen when people get together.",
  body: "A few new friends. A favorite table. A Wednesday you start looking forward to. Here’s to more of those.",
  footer: "Made with love for the little communities that make New York, New York.",
};

export const THANKS = "Thanks for saying hi. We’re reviewing our first NYC pilot matches and will reach out if we see a fit.";

export const PRIVACY =
  "We only use what you send to talk to you about the Coop pilot. We don’t sell it or share it for advertising. Ask us any time and we’ll delete it.";

export const NEIGHBORHOODS = ["Chelsea", "Flatiron", "East Village", "Lower East Side", "Somewhere else"];
export const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];
