"use client";

import { useEffect, useState } from "react";

const time = new Intl.DateTimeFormat("en-US", {
  timeZone: "America/New_York",
  hour: "numeric",
  minute: "2-digit",
  second: "2-digit",
});
const zone = new Intl.DateTimeFormat("en-US", { timeZone: "America/New_York", timeZoneName: "short" });

/** Carl Hauser's live clock, set to New York. Renders nothing until mounted to avoid a hydration mismatch. */
export function Clock() {
  const [now, setNow] = useState<Date | null>(null);

  useEffect(() => {
    setNow(new Date());
    const t = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  const tz = now ? zone.formatToParts(now).find((p) => p.type === "timeZoneName")?.value : "";
  return (
    <p className="clock">
      <span>New York {tz}</span>
      <time suppressHydrationWarning dateTime={now?.toISOString()}>{now ? time.format(now) : " "}</time>
    </p>
  );
}
