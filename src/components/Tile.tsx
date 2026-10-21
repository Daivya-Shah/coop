"use client";

import { useEffect, useRef, useState } from "react";
import clsx from "clsx";

type Props = { src: string; caption: string; n: string; big?: boolean; alt?: string };

/**
 * A sketch in a Carl Hauser-style rounded tile, with a small caption and number on top.
 * The drawing inks in from left to right the first time it scrolls into view.
 * Visible by default: it is only hidden once we know it is below the fold.
 */
export function Tile({ src, caption, n, big, alt }: Props) {
  const ref = useRef<HTMLElement>(null);
  const [ink, setInk] = useState<"idle" | "waiting" | "in">("idle");

  useEffect(() => {
    const el = ref.current;
    if (!el || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    const io = new IntersectionObserver(
      ([e]) => {
        if (e.isIntersecting) {
          setInk((s) => (s === "waiting" ? "in" : s));
          io.disconnect();
        } else {
          setInk("waiting");
        }
      },
      { rootMargin: "0px 0px -12% 0px" },
    );
    io.observe(el);
    return () => io.disconnect();
  }, []);

  return (
    <figure ref={ref} className={clsx("tile", big && "big")} data-ink={ink}>
      <figcaption className="meta"><span>{caption}</span><span>No. {n}</span></figcaption>
      <img src={src} alt={alt ?? caption} loading="lazy" decoding="async" />
    </figure>
  );
}
