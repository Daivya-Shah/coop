import { Clock } from "@/components/Clock";
import { FlipThrough } from "@/components/FlipThrough";
import { TopBar } from "@/components/TopBar";

/** The landing: one screen, Carl Hauser's hello card with the four drawings at its heart. */
export default function Home() {
  return (
    <main className="hello">
      <TopBar />
      <FlipThrough />
      <footer className="hello-foot">
        <p>Starting small, right here in NYC.</p>
        <Clock />
      </footer>
    </main>
  );
}
