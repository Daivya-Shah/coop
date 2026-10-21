"use client";

import { motion, useReducedMotion } from "motion/react";

type Props = {
  as?: "div" | "section" | "article" | "figure";
  delay?: number;
  className?: string;
  children: React.ReactNode;
} & React.AriaAttributes;

/** Fades and lifts its children in the first time they scroll into view. */
export function Reveal({ as = "div", delay = 0, children, ...rest }: Props) {
  const still = useReducedMotion();
  const Tag = motion[as];
  return (
    <Tag
      initial={still ? false : { opacity: 0, y: 24 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "0px 0px -12% 0px" }}
      transition={{ duration: 0.7, delay, ease: [0.2, 0.7, 0.2, 1] }}
      {...rest}
    >
      {children}
    </Tag>
  );
}
