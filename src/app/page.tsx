import { Clock } from "@/components/Clock";
import { StoryStack } from "@/components/StoryStack";
import { TopBar } from "@/components/TopBar";
import { HERO_INTRO, TAGLINE } from "@/content/coop";

/** The landing: one screen. Carl Hauser's hello card on the left, the story as a pile of pages on the right. */
export default function Home() {
  return (
    <main className="landing">
      <section className="card hello">
        <TopBar />
        <div className="hello-words">
          <h1 className="tagline rise" style={{ "--i": 0 } as React.CSSProperties}>{TAGLINE}</h1>
          <p className="intro rise" style={{ "--i": 1 } as React.CSSProperties}>{HERO_INTRO}</p>
        </div>
        <footer className="hello-foot rise" style={{ "--i": 2 } as React.CSSProperties}>
          <p>Starting small, right here in NYC.</p>
          <Clock />
        </footer>
      </section>
      <StoryStack />
    </main>
  );
}
