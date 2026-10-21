"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { MotionConfig, motion, useReducedMotion } from "motion/react";
import { Plus } from "./Plus";
import { ClubForm, VenueForm } from "./IntakeForm";

export type Side = "venue" | "club";

const JoinContext = createContext<(side: Side) => void>(() => {});

/** Wraps the site so any "I run a venue / club" button can open the join panel. */
export function JoinProvider({ children }: { children: React.ReactNode }) {
  const dialog = useRef<HTMLDialogElement>(null);
  const card = useRef<HTMLDivElement>(null);
  const [side, setSide] = useState<Side>("venue");
  const [open, setOpen] = useState(false);
  const still = useReducedMotion();

  const openJoin = useCallback((s: Side) => {
    setSide(s);
    const d = dialog.current;
    if (d && !d.open) d.showModal();
    if (card.current) card.current.scrollTop = 0;
    setOpen(true);
  }, []);

  // Closing plays the exit animation first, then closes the native dialog.
  const close = useCallback(() => setOpen(false), []);

  // Deep link: coop.nyc/#join
  useEffect(() => {
    if (location.hash === "#join") openJoin("venue");
  }, [openJoin]);

  return (
    <JoinContext.Provider value={openJoin}>
      <MotionConfig reducedMotion="user">{children}</MotionConfig>
      <dialog
        className="panel"
        ref={dialog}
        aria-labelledby="t-join"
        onCancel={(e) => { e.preventDefault(); close(); }}
        onClick={(e) => { if (e.target === dialog.current) close(); }}
      >
        <motion.div
          className="panel-card"
          ref={card}
          initial={false}
          animate={open ? { opacity: 1, y: 0, scale: 1 } : { opacity: 0, y: 18, scale: 0.985 }}
          transition={still ? { duration: 0 } : { type: "spring", stiffness: 380, damping: 34, mass: 0.8 }}
          onAnimationComplete={() => { if (!open) dialog.current?.close(); }}
        >
          <button className="close" onClick={close} aria-label="Close"><Plus /></button>
          <div className="panel-body">
            <div>
              <h2 id="t-join">Join the Pilot</h2>
              <p className="lede">Two minutes. No account.</p>
              <SideSwitch side={side} onChange={setSide} />
              {side === "venue" ? <VenueForm /> : <ClubForm />}
            </div>
            <img className="panel-sketch" src="/img/sketches/name-tags.svg" alt="" />
          </div>
        </motion.div>
      </dialog>
    </JoinContext.Provider>
  );
}

export function JoinButton({ side, className, children }: { side: Side; className?: string; children: React.ReactNode }) {
  const openJoin = useContext(JoinContext);
  return <button className={className} onClick={() => openJoin(side)}>{children}</button>;
}

const SIDES: { id: Side; label: string; color: string }[] = [
  { id: "venue", label: "I run a venue", color: "var(--ink)" },
  { id: "club", label: "I run a club", color: "var(--yolk)" },
];

function SideSwitch({ side, onChange }: { side: Side; onChange: (s: Side) => void }) {
  const refs = useRef<(HTMLButtonElement | null)[]>([]);
  return (
    <div className="switch" role="tablist" aria-label="Which side are you on?">
      {SIDES.map((s, i) => {
        const on = s.id === side;
        return (
          <button
            key={s.id}
            ref={(el) => { refs.current[i] = el; }}
            role="tab"
            id={`tab-${s.id}`}
            aria-controls={`form-${s.id}`}
            aria-selected={on}
            tabIndex={on ? 0 : -1}
            onClick={() => onChange(s.id)}
            onKeyDown={(e) => {
              if (e.key !== "ArrowRight" && e.key !== "ArrowLeft") return;
              const next = SIDES[(i + 1) % SIDES.length];
              onChange(next.id);
              refs.current[(i + 1) % SIDES.length]?.focus();
            }}
          >
            {on && (
              <motion.span
                className="dot"
                layoutId="switch-dot"
                initial={false}
                animate={{ backgroundColor: s.color }}
                transition={{ type: "spring", stiffness: 500, damping: 38 }}
              />
            )}
            {s.label}
          </button>
        );
      })}
    </div>
  );
}
