import Link from "next/link";
import { MENU } from "@/content/coop";
import { JoinButton } from "./Join";
import { Plus } from "./Plus";

/** Carl Hauser's hello-card top row: wordmark, plus-icon menu, and the two ways in. */
export function TopBar() {
  return (
    <header className="topbar">
      <Link className="brand" href="/" aria-label="Coop, home">
        <img src="/img/brand/wordmark.svg" alt="" width={990} height={340} />
      </Link>
      <nav className="plus-menu" aria-label="Coop">
        {MENU.map((m) => (
          <Link key={m.href} href={m.href}><Plus />{m.label}</Link>
        ))}
        <JoinButton side="club"><Plus />Say hi</JoinButton>
      </nav>
      <nav className="side-links" aria-label="Join the pilot">
        <JoinButton side="venue">I run a venue</JoinButton>
        <JoinButton side="club">I run a club</JoinButton>
      </nav>
    </header>
  );
}
