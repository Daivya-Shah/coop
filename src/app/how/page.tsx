import type { Metadata } from "next";
import { Clock } from "@/components/Clock";
import { Faq } from "@/components/Faq";
import { JoinButton } from "@/components/Join";
import { Tile } from "@/components/Tile";
import { TopBar } from "@/components/TopBar";
import { CLOSE, CLUBS, FIRST_FLOCK, HOW, MERRIER, NUMBERS, PRIVACY, TAGLINE, VENUES } from "@/content/coop";

export const metadata: Metadata = { title: "How it works — Coop" };

const sketch = (name: string) => `/img/sketches/${name}.svg`;

/** Tiles are numbered in reading order, like the IDs on Carl Hauser's sketches. */
const no = (k: number) => String(k).padStart(2, "0");

function Side({ id, side, data, first }: { id: string; side: "venue" | "club"; data: typeof VENUES; first: number }) {
  return (
    <article id={id} className={`side ${side}`} aria-labelledby={`${id}-title`}>
      <h2 id={`${id}-title`}>{data.title}</h2>
      <p className="lead">{data.lead}</p>
      <div className="side-tiles">
        {data.tiles.map((t, k) => (
          <Tile key={t.sketch} src={sketch(t.sketch)} caption={t.caption} n={no(first + k)} />
        ))}
      </div>
      {data.body.map((p) => <p key={p.slice(0, 24)}>{p}</p>)}
      <h3>{data.rulesTitle}</h3>
      <ul className="ticks">
        {data.rules.map((r) => <li key={r}>{r}</li>)}
      </ul>
      <JoinButton side={side} className={side === "venue" ? "pill" : "pill ghost"}>{data.cta}</JoinButton>
    </article>
  );
}

export default function How() {
  return (
    <>
      <TopBar />
      <main className="story">
        <section className="merrier" aria-labelledby="merrier-title">
          <div className="merrier-copy">
            <h1 id="merrier-title">{MERRIER.title}</h1>
            {MERRIER.body.map((p) => <p key={p.slice(0, 24)}>{p}</p>)}
          </div>
          <div className="merrier-tiles">
            <Tile src="/img/landing/step2.svg" caption="Nowhere regular to meet" n="01" big alt="Clubs, knit, book, art, run, chess and talk, with nowhere regular to meet." />
            <Tile src="/img/landing/step1.svg" caption="Empty on slow nights" n="02" alt="A bar with four empty stools and an empty table on a slow night." />
          </div>
        </section>

        <section id="how" className="how" aria-labelledby="how-title">
          <h2 id="how-title">Here’s how it works.</h2>
          <ol className="how-steps">
            {HOW.map((s, k) => (
              <li key={s.sketch}>
                <Tile src={sketch(s.sketch)} caption={s.caption} n={no(3 + k)} />
                <h3>{s.title}</h3>
                <p>{s.body}</p>
              </li>
            ))}
          </ol>
        </section>

        <section id="numbers" className="numbers" aria-labelledby="numbers-title">
          <h2 id="numbers-title">{NUMBERS.title}</h2>
          <ul>
            {NUMBERS.items.map((n) => (
              <li key={n.figure}>
                <p><strong>{n.figure}</strong> {n.text}</p>
                <a href={n.href} target="_blank" rel="noopener noreferrer">{n.source}</a>
              </li>
            ))}
          </ul>
          <p className="numbers-outro">{NUMBERS.outro}</p>
          <p className="fine">{NUMBERS.note}</p>
        </section>

        <section className="sides" aria-label="For venues and for clubs">
          <Side id="venues" side="venue" data={VENUES} first={6} />
          <Side id="clubs" side="club" data={CLUBS} first={8} />
        </section>

        <section id="flock" className="flock" aria-labelledby="flock-title">
          <Tile src="/img/landing/step4.svg" caption="One chair saved for you" n="10" big alt="The long table with lamps lit, one chair saved for you." />
          <div className="flock-copy">
            <h2 id="flock-title">{FIRST_FLOCK.title}</h2>
            {FIRST_FLOCK.body.map((p) => <p key={p.slice(0, 24)}>{p}</p>)}
            <JoinButton side="club" className="pill">{FIRST_FLOCK.cta}</JoinButton>
          </div>
        </section>

        <section id="questions" className="questions" aria-labelledby="questions-title">
          <h2 id="questions-title">A few good questions.</h2>
          <Faq />
        </section>

        <section className="closing" aria-labelledby="close-title">
          <h2 id="close-title">{CLOSE.title}</h2>
          <p>{CLOSE.body}</p>
          <div className="close-actions">
            <JoinButton side="club" className="pill">Find your people a place</JoinButton>
            <JoinButton side="venue" className="pill ghost">Bring a club to your venue</JoinButton>
          </div>
        </section>
      </main>

      <footer className="site-foot">
        <div>
          <p className="foot-tag"><b>coop.</b> {TAGLINE}</p>
          <p>{CLOSE.footer}</p>
        </div>
        <p className="fine">{PRIVACY}</p>
        <Clock />
      </footer>
    </>
  );
}
