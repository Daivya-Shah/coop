"use client";

import { motion, useReducedMotion } from "motion/react";

type Props = {
  as?: "div" | "section" | "article" | "figure";
  delay?: number;
  className?: string;
  children: React.ReactNode;
} & React.AriaAttributes;

const EASE_OUT = [0.23, 1, 0.32, 1] as const;

/** Fades and lifts its children in the first time they scroll into view. */
export function Reveal({ as = "div", delay = 0, children, ...rest }: Props) {
  const Tag = motion[as];
  const still = useReducedMotion(); // reduced motion: fade only, no movement
  return (
    // Full transform strings (not x/y shorthands) so Motion can hand the work to the compositor.
    <Tag
      initial={{ opacity: 0, transform: still ? "none" : "translateY(16px)" }}
      whileInView={{ opacity: 1, transform: still ? "none" : "translateY(0px)" }}
      viewport={{ once: true, margin: "0px 0px -10% 0px" }}
      transition={{ duration: 0.6, delay, ease: EASE_OUT }}
      {...rest}
    >
      {children}
    </Tag>
  );
}
