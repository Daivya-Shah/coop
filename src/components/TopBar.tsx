import Link from "next/link";
import { JoinButton } from "./Join";
import { Plus } from "./Plus";

export function TopBar({ page }: { page: "landing" | "how" }) {
  return (
    <header className={page === "landing" ? "topbar landing" : "topbar"}>
      <Link className="brand" href="/">
        <img src="/img/brand/wordmark.svg" alt="Coop" width={990} height={340} />
      </Link>
      {page === "how" && (
        <Link className="plus-link on" href="/how/" aria-current="page">
          <Plus />
          How it works
        </Link>
      )}
      <nav className="side-links" aria-label="Join">
        <JoinButton side="venue">I run a venue</JoinButton>
        <JoinButton side="club">I run a club</JoinButton>
      </nav>
    </header>
  );
}
