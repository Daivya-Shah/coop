"use client";

// Adapted from the 21st.dev "Card stack" component (Motion's official examples catalog):
// a pile of pages where the top one is flicked away and goes to the back.
import { useEffect, useRef, useState } from "react";
import { animate, motion, useMotionValue, useReducedMotion, useTransform } from "motion/react";
import { Tabs } from "@base-ui/react/tabs";
import { STEPS } from "@/content/coop";

const EVERY = 5200;
const N = STEPS.length;
const wrap = (v: number) => ((v % N) + N) % N;

function Page({ k, current, onNext, minDistance }: { k: number; current: number; onNext: () => void; minDistance: number }) {
  const depth = wrap(k - current); // 0 = on top
  const top = depth === 0;
  const rest = 3.2 * Math.sin(k * 1.7); // every page sits a little crooked, like a real pile
  const x = useMotionValue(0);
  const rotate = useTransform(x, [-400, 0, 400], [rest - 9, rest, rest + 9]);

  // Momentum dismissal: a quick flick is enough, no distance threshold needed.
  const onDragEnd = () => {
    const far = Math.abs(x.get()) > minDistance;
    const fast = Math.abs(x.getVelocity()) > 400;
    if (far || fast) onNext();
    animate(x, 0, { type: "spring", stiffness: far || fast ? 520 : 320, damping: 42 });
  };

  return (
    <motion.li
      className="page"
      style={{ x, rotate, zIndex: N - depth }}
      initial={false}
      animate={{ scale: 1 - depth * 0.045, y: depth * -14, opacity: depth > 2 ? 0 : 1 }}
      transition={{ type: "spring", stiffness: 380, damping: 34 }}
      drag={top ? "x" : false}
      dragSnapToOrigin={false}
      dragElastic={0.7}
      onDragEnd={onDragEnd}
      onTap={top ? onNext : undefined}
      whileTap={top ? { scale: 0.985 } : undefined}
      aria-hidden={!top}
    >
      <img src={`/img/landing/step${k + 1}.svg`} alt={top ? STEPS[k].alt : ""} draggable={false} width={900} height={900} />
    </motion.li>
  );
}

export function StoryStack() {
  const [current, setCurrent] = useState(0);
  const [paused, setPaused] = useState(false);
  const [hidden, setHidden] = useState(false);
  const [tick, setTick] = useState(0);
  const [minDistance, setMinDistance] = useState(200);
  const ref = useRef<HTMLUListElement>(null);
  const still = useReducedMotion();

  useEffect(() => {
    if (ref.current) setMinDistance(ref.current.offsetWidth * 0.35);
    const onVis = () => setHidden(document.hidden);
    document.addEventListener("visibilitychange", onVis);
    return () => document.removeEventListener("visibilitychange", onVis);
  }, []);

  useEffect(() => {
    if (still || paused || hidden) return;
    const t = setInterval(() => setCurrent((c) => wrap(c + 1)), EVERY);
    return () => clearInterval(t);
  }, [still, paused, hidden, tick]);

  const go = (k: number) => { setCurrent(wrap(k)); setTick((t) => t + 1); };
  const step = STEPS[current];

  return (
    <section
      className="story-stack"
      aria-label="How Coop works, in four drawings"
      onPointerEnter={() => setPaused(true)}
      onPointerLeave={() => setPaused(false)}
      onFocus={() => setPaused(true)}
      onBlur={() => setPaused(false)}
    >
      <ul className="pile" ref={ref} aria-live="polite">
        {STEPS.map((s, k) => (
          <Page key={s.label} k={k} current={current} onNext={() => go(current + 1)} minDistance={minDistance} />
        ))}
      </ul>
      <div className="pile-foot">
        <Tabs.Root value={current} onValueChange={(v) => go(v as number)}>
          <Tabs.List className="pile-tabs" style={{ "--c": step.color } as React.CSSProperties} aria-label="Jump to a drawing">
            {STEPS.map((s, k) => (
              <Tabs.Tab key={s.label} value={k} aria-label={s.label}>{k + 1}</Tabs.Tab>
            ))}
            <Tabs.Indicator className="pile-dot" />
          </Tabs.List>
        </Tabs.Root>
        <p className="pile-caption"><b>{step.name}.</b> <span>Swipe or tap the page.</span></p>
      </div>
    </section>
  );
}
