import type { Metadata } from "next";
import { Clock } from "@/components/Clock";
import { Faq } from "@/components/Faq";
import { JoinButton } from "@/components/Join";
import { Tile } from "@/components/Tile";
import { TopBar } from "@/components/TopBar";
import { CLOSE, CLUBS, FIRST_FLOCK, HOW, MERRIER, NUMBERS, PRIVACY, TAGLINE, VENUES } from "@/content/coop";

export const metadata: Metadata = { title: "How it works — Coop" };

/** Tiles are numbered in reading order, like the IDs on Carl Hauser's sketches. */
const no = (k: number) => String(k).padStart(2, "0");

function Side({ id, side, data, first }: { id: string; side: "venue" | "club"; data: typeof VENUES; first: number }) {
  return (
    <article id={id} className={`card side ${side}`} aria-labelledby={`${id}-title`}>
      <h2 id={`${id}-title`}>{data.title}</h2>
      <p className="lead">{data.lead}</p>
      <div className="pair">
        {data.tiles.map((t, k) => (
          <Tile key={t.sketch} sketch={t.sketch} caption={t.caption} n={no(first + k)} />
        ))}
      </div>
      {data.body.map((p) => <p key={p.slice(0, 24)}>{p}</p>)}
      <h3>{data.rulesTitle}</h3>
      <ul className="ticks">
        {data.rules.map((r) => <li key={r}>{r}</li>)}
      </ul>
      <JoinButton side={side} className="pill">{data.cta}</JoinButton>
    </article>
  );
}

export default function How() {
  return (
    <>
      <div className="card bar"><TopBar /></div>
      <main className="sheet">
        <section className="card merrier" aria-labelledby="merrier-title">
          <h1 id="merrier-title">{MERRIER.title}</h1>
          <div className="merrier-body">
            {MERRIER.body.map((p) => <p key={p.slice(0, 24)}>{p}</p>)}
          </div>
        </section>

        <section id="how" className="card how" aria-labelledby="how-title">
          <h2 id="how-title">Here’s how it works.</h2>
          <ol className="how-steps">
            {HOW.map((s, k) => (
              <li key={s.sketch}>
                <Tile sketch={s.sketch} caption={s.caption} n={no(1 + k)} tall={k === 0} />
                <h3>{s.title}</h3>
                <p>{s.body}</p>
              </li>
            ))}
          </ol>
        </section>

        <section id="numbers" className="card numbers" aria-labelledby="numbers-title">
          <div className="numbers-head">
            <h2 id="numbers-title">{NUMBERS.title}</h2>
            <p>{NUMBERS.outro}</p>
            <p className="fine">{NUMBERS.note}</p>
          </div>
          <ul>
            {NUMBERS.items.map((n) => (
              <li key={n.figure}>
                <p><strong>{n.figure}</strong> {n.text}</p>
                <a href={n.href} target="_blank" rel="noopener noreferrer">{n.source}</a>
              </li>
            ))}
          </ul>
        </section>

        <div className="sides">
          <Side id="venues" side="venue" data={VENUES} first={4} />
          <Side id="clubs" side="club" data={CLUBS} first={6} />
        </div>

        <section id="flock" className="card flock" aria-labelledby="flock-title">
          <Tile sketch={FIRST_FLOCK.sketch.sketch} caption={FIRST_FLOCK.sketch.caption} n="08" />
          <div className="flock-copy">
            <h2 id="flock-title">{FIRST_FLOCK.title}</h2>
            {FIRST_FLOCK.body.map((p) => <p key={p.slice(0, 24)}>{p}</p>)}
            <JoinButton side="club" className="pill">{FIRST_FLOCK.cta}</JoinButton>
          </div>
        </section>

        <section id="questions" className="card questions" aria-labelledby="questions-title">
          <h2 id="questions-title">A few good questions.</h2>
          <Faq />
        </section>

        <section className="card closing" aria-labelledby="close-title">
          <h2 id="close-title">{CLOSE.title}</h2>
          <p>{CLOSE.body}</p>
          <div className="close-actions">
            <JoinButton side="club" className="pill">Find your people a place</JoinButton>
            <JoinButton side="venue" className="pill ghost">Bring a club to your venue</JoinButton>
          </div>
        </section>
      </main>

      <footer className="card site-foot">
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
