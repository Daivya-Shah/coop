import type { Metadata } from "next";
import { JoinButton } from "@/components/Join";
import { Reveal } from "@/components/Reveal";
import { Tile } from "@/components/Tile";
import { TopBar } from "@/components/TopBar";

export const metadata: Metadata = { title: "How it works — Coop" };

const STEPS = [
  {
    n: "01",
    sketch: "name-tags",
    caption: "Hello, my name is",
    title: "Tell us a little about yourself.",
    body: "Have a club looking for somewhere to meet? Or a space that could use a little more company? We’d love to hear about it.",
  },
  {
    n: "02",
    sketch: "pilot-map",
    caption: "The right neighborhood",
    title: "We’ll see who might get along.",
    body: "We look for places and groups that make sense together: the right neighborhood, the right night, the right kind of crowd. Nothing gets booked until everyone’s happy with the plan.",
  },
  {
    n: "03",
    sketch: "weekly-calendar",
    caption: "Their night, every week",
    title: "Make yourself at home.",
    body: "The first get-together is just the beginning. Hopefully, before long, it’s the spot everyone knows to show up to.",
  },
];

export default function How() {
  return (
    <>
      <TopBar page="how" />
      <main className="how-main">
        <Reveal as="section" className="how-intro">
          <h1>Here’s how it works.</h1>
          <p>
            New York is full of little groups of people who make time for each other, and lovely neighborhood spots
            that could use a few more people on a quiet night. We thought, why not introduce them?
          </p>
        </Reveal>

        <section className="how-steps3" aria-label="Three steps">
          {STEPS.map((s, k) => (
            <Reveal as="article" key={s.n} delay={0.1 * k}>
              <Tile src={s.sketch} caption={s.caption} n={s.n} />
              <h2><b>{s.n}</b> {s.title}</h2>
              <p>{s.body}</p>
            </Reveal>
          ))}
        </section>

        <section className="sides" aria-label="For venues and for clubs">
          <Reveal as="article" className="side venue">
            <p className="kicker">Restaurants, bars &amp; cafés</p>
            <h2>Got a quiet night? We’ve got some ideas.</h2>
            <div className="side-tiles">
              <Tile src="corner-booth" caption="The corner nobody books" n="V.1" />
              <Tile src="floor-plan" caption="A back room, empty" n="V.2" />
            </div>
            <p>
              Maybe Mondays are a little slow. Maybe there’s a back room that doesn’t get used much. We find local clubs
              looking for somewhere to meet regularly and introduce them to places like yours.
            </p>
            <h3>Your space. Your rules.</h3>
            <ul className="ticks">
              <li>You decide which nights work and how many people you’re comfortable hosting.</li>
              <li>You set any spending expectations, and you always have the final say before anything is booked.</li>
              <li>No fee to join the pilot, and your first completed matched event is free of any Coop fee.</li>
              <li>After that, a small percentage for completed club nights, agreed together in advance.</li>
            </ul>
            <JoinButton side="venue" className="pill">Let’s bring some people in →</JoinButton>
          </Reveal>

          <Reveal as="article" className="side club" delay={0.12}>
            <p className="kicker">Clubs, communities &amp; little gatherings</p>
            <h2>Your people deserve a place.</h2>
            <div className="side-tiles">
              <Tile src="club-kit" caption="What each club brings" n="C.1" />
              <Tile src="no-app-needed" caption="Members just get a text" n="C.2" />
            </div>
            <p>
              Maybe your book club keeps hopping between cafés, or your run club needs somewhere to wind down. Tell us
              what you’re looking for and we’ll help you find a neighborhood spot you can come back to again and again.
            </p>
            <h3>No membership fee.</h3>
            <ul className="ticks">
              <li>Coop is free for clubs to join.</li>
              <li>No venue-hunting every week. Just a place for your people.</li>
              <li>Some places may have a minimum food or drink spend; you’ll know the details before agreeing to anything.</li>
              <li>Weekly, every other week or monthly: whatever works for your group.</li>
            </ul>
            <JoinButton side="club" className="pill ghost">Let’s find your spot →</JoinButton>
          </Reveal>
        </section>

        <Reveal as="section" className="how-end">
          <p className="tagline">Because every flock needs one.</p>
          <p>We’re starting small, right here in NYC. Come be part of it.</p>
        </Reveal>
      </main>
    </>
  );
}
