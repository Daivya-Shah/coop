"use client";

import Link from "next/link";
import { useCallback, useEffect, useRef, useState } from "react";
import { motion, useReducedMotion, type Variants } from "motion/react";
import { Plus } from "./Plus";

const STEPS = [
  { color: "#3E7396", label: "1, the venue", alt: "1, the venue: a bar with four empty stools and an empty table on a slow night." },
  { color: "#C4572B", label: "2, the clubs", alt: "2, the clubs: knit, book, art, run, chess and talk, with nowhere regular to meet." },
  { color: "#7B7A2C", label: "3, the match", alt: "3, the match: the Coop house with the egg, right area, right size, right night." },
  { color: "#B8232F", label: "4, the regulars", alt: "4, the regulars: the long table with lamps lit, one chair saved for you." },
];

const EVERY = 4200;

const intro: Variants = {
  hidden: { opacity: 0, y: 14 },
  shown: (k: number) => ({ opacity: 1, y: 0, transition: { delay: 0.08 * k, duration: 0.6, ease: [0.2, 0.7, 0.2, 1] } }),
};

const page: Variants = {
  on: { opacity: 1, y: 0, rotate: 0, scale: 1, transition: { type: "spring", stiffness: 140, damping: 20, mass: 0.9 } },
  // the page being left lifts away; the next one settles in from just below
  before: { opacity: 0, y: -14, rotate: 0.6, scale: 0.99, transition: { duration: 0.35, ease: "easeIn" } },
  after: { opacity: 0, y: 16, rotate: -0.8, scale: 0.985, transition: { duration: 0.35, ease: "easeIn" } },
};

export function FlipThrough() {
  const [i, setI] = useState(0);
  const [paused, setPaused] = useState(false);
  const still = useReducedMotion();
  const timer = useRef<ReturnType<typeof setInterval>>(undefined);

  const restart = useCallback(() => {
    clearInterval(timer.current);
    if (!still && !paused) timer.current = setInterval(() => setI((k) => (k + 1) % STEPS.length), EVERY);
  }, [still, paused]);

  useEffect(() => {
    restart();
    return () => clearInterval(timer.current);
  }, [restart]);

  const show = (k: number) => {
    setI((k + STEPS.length) % STEPS.length);
    restart();
  };

  const m = still ? { initial: false as const } : { initial: "hidden", animate: "shown", variants: intro };

  return (
    <main className="flip">
      <div className="flip-copy">
        <motion.h1 className="tagline" custom={0} {...m}>Because every flock needs one.</motion.h1>
        <motion.p className="intro" custom={1} {...m}>
          We match social clubs with restaurants, bars and cafés that have empty seats on their slow nights. The club
          gets a table it can count on. The venue gets regulars.
        </motion.p>
        <motion.div className="flip-tabs" role="tablist" aria-label="How Coop works, in four steps" custom={2} {...m}>
          {STEPS.map((s, k) => (
            <motion.button
              key={s.label}
              role="tab"
              aria-selected={k === i}
              aria-label={s.label}
              onClick={() => show(k)}
              whileHover={still ? undefined : { y: -2 }}
              whileTap={still ? undefined : { scale: 0.92 }}
            >
              {k === i && (
                <motion.span
                  className="dot"
                  layoutId="flip-dot"
                  initial={false}
                  animate={{ backgroundColor: s.color }}
                  transition={still ? { duration: 0 } : { type: "spring", stiffness: 420, damping: 32 }}
                />
              )}
              <span>{k + 1}</span>
            </motion.button>
          ))}
        </motion.div>
        <motion.div custom={3} {...m}>
          <Link className="plus-link" href="/how/"><Plus />How it works</Link>
        </motion.div>
      </div>

      <motion.figure
        className="flip-stage"
        aria-live="polite"
        onClick={() => show(i + 1)}
        onMouseEnter={() => setPaused(true)}
        onMouseLeave={() => setPaused(false)}
        initial={still ? false : { opacity: 0, scale: 0.97 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.8, delay: 0.15, ease: [0.2, 0.7, 0.2, 1] }}
      >
        {STEPS.map((s, k) => (
          <motion.img
            key={s.label}
            src={`/img/landing/step${k + 1}.svg`}
            width={900}
            height={900}
            alt={k === i ? s.alt : ""}
            aria-hidden={k !== i}
            variants={page}
            initial={false}
            animate={k === i ? "on" : k < i ? "before" : "after"}
            transition={still ? { duration: 0 } : undefined}
          />
        ))}
      </motion.figure>
    </main>
  );
}
