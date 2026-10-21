"use client";

import { useEffect, useState } from "react";
import { Tabs } from "@base-ui/react/tabs";
import { useReducedMotion } from "motion/react";
import clsx from "clsx";
import { HERO_INTRO, STEPS, TAGLINE } from "@/content/coop";

const EVERY = 4200;

export function FlipThrough() {
  const [i, setI] = useState(0);
  const [hovered, setHovered] = useState(false);
  const [focused, setFocused] = useState(false);
  const [hidden, setHidden] = useState(false);
  const [tick, setTick] = useState(0); // bumps on every manual change, restarting the timer
  const still = useReducedMotion();

  // Pause while the tab is in the background, like Sonner pauses its timers.
  useEffect(() => {
    const onVis = () => setHidden(document.hidden);
    document.addEventListener("visibilitychange", onVis);
    return () => document.removeEventListener("visibilitychange", onVis);
  }, []);

  const playing = !still && !hovered && !focused && !hidden;
  useEffect(() => {
    if (!playing) return;
    const t = setInterval(() => setI((k) => (k + 1) % STEPS.length), EVERY);
    return () => clearInterval(t);
  }, [playing, tick]);

  const show = (k: number) => {
    setI((k + STEPS.length) % STEPS.length);
    setTick((t) => t + 1);
  };

  return (
    <div className="flip">
      <div className="flip-copy">
        <h1 className="tagline rise" style={{ "--i": 0 } as React.CSSProperties}>{TAGLINE}</h1>
        <p className="intro rise" style={{ "--i": 1 } as React.CSSProperties}>{HERO_INTRO}</p>
        <Tabs.Root value={i} onValueChange={(v) => show(v as number)}>
          <Tabs.List
            className="flip-tabs rise"
            style={{ "--i": 2, "--c": STEPS[i].color } as React.CSSProperties}
            aria-label="How Coop works, in four drawings"
            onFocus={(e) => setFocused(e.target.matches(":focus-visible"))}
            onBlur={() => setFocused(false)}
          >
            {STEPS.map((s, k) => (
              <Tabs.Tab key={s.label} value={k} aria-label={s.label} aria-controls="flip-stage">
                {k + 1}
              </Tabs.Tab>
            ))}
            <Tabs.Indicator className="flip-dot" />
          </Tabs.List>
        </Tabs.Root>
      </div>

      <figure
        className="flip-stage rise"
        id="flip-stage"
        aria-live="polite"
        style={{ "--i": 2 } as React.CSSProperties}
        onClick={() => show(i + 1)}
        onMouseEnter={() => setHovered(true)}
        onMouseLeave={() => setHovered(false)}
      >
        {STEPS.map((s, k) => (
          <img
            key={s.label}
            className={clsx(k === i ? "on" : k < i ? "before" : "after")}
            src={`/img/landing/step${k + 1}.svg`}
            width={900}
            height={900}
            alt={k === i ? s.alt : ""}
            aria-hidden={k !== i}
            fetchPriority={k === 0 ? "high" : "low"}
          />
        ))}
      </figure>
    </div>
  );
}
