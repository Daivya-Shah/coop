"use client";

// The pen-drawing reveal follows the 21st.dev "Line Draw SVG" technique (animate each stroke's dash
// offset from its full length to zero), applied to every stroke of our hand-drawn sketches, in CSS.
import { memo, useEffect, useRef, useState } from "react";

type Props = { sketch: string; caption: string; n: string; alt?: string; tall?: boolean };

const cache = new Map<string, Promise<string>>();
const load = (src: string) => {
  if (!cache.has(src)) cache.set(src, fetch(src).then((r) => r.text()));
  return cache.get(src)!;
};

/** Prepare a sketch so every stroke can be drawn: unit path length, dashes hidden, staggered start. */
function prepare(svgText: string) {
  const doc = new DOMParser().parseFromString(svgText, "image/svg+xml");
  const svg = doc.documentElement;
  svg.removeAttribute("width");
  svg.removeAttribute("height");
  const groups = svg.querySelectorAll(":scope > g");
  const ink = groups[groups.length - 1];
  const strokes = ink ? Array.from(ink.querySelectorAll("path")) : [];
  const span = 1500; // ms over which the pen starts its strokes
  strokes.forEach((p, i) => {
    p.setAttribute("pathLength", "1");
    p.setAttribute("style", `--d:${Math.round((i / Math.max(1, strokes.length - 1)) * span)}ms`);
  });
  if (groups.length > 1) groups[0].setAttribute("class", "wash");
  ink?.setAttribute("class", "ink");
  return new XMLSerializer().serializeToString(svg);
}

/** Kept stable across re-renders, so React never swaps the strokes out mid-drawing. */
const Drawing = memo(function Drawing({ html, label }: { html: string; label: string }) {
  return <div className="drawing" role="img" aria-label={label} dangerouslySetInnerHTML={{ __html: html }} />;
});

/**
 * A sketch on a paper tile with Carl Hauser's small caption and number.
 * Below the fold, the sketch draws itself stroke by stroke the first time it scrolls into view.
 * The plain image stays as the default (no JS, reduced motion, or already on screen at load).
 */
export function Tile({ sketch, caption, n, alt, tall }: Props) {
  const ref = useRef<HTMLElement>(null);
  const src = `/img/sketches/${sketch}.svg`;
  const [svg, setSvg] = useState<string | null>(null);
  const [drawn, setDrawn] = useState(false);

  useEffect(() => {
    const el = ref.current;
    if (!el || matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    if (el.getBoundingClientRect().top < innerHeight * 0.6) return; // already in plain view: leave it be
    let alive = true;
    const near = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return;
      near.disconnect();
      load(src).then((t) => alive && setSvg(prepare(t)));
    }, { rootMargin: "600px 0px" });
    near.observe(el);
    return () => { alive = false; near.disconnect(); };
  }, [src]);

  useEffect(() => {
    const el = ref.current;
    if (!svg || !el) return;
    const io = new IntersectionObserver(([e]) => {
      if (!e.isIntersecting) return;
      io.disconnect();
      // Let the browser paint the hidden strokes first, or there is nothing to transition from.
      void el.getBoundingClientRect();
      requestAnimationFrame(() => requestAnimationFrame(() => setDrawn(true)));
    }, { threshold: 0.35 });
    io.observe(el);
    return () => io.disconnect();
  }, [svg]);

  return (
    <figure ref={ref} className={tall ? "tile tall" : "tile"} data-drawn={svg ? drawn : undefined}>
      <figcaption className="meta"><span>{caption}</span><span>No. {n}</span></figcaption>
      {svg ? (
        <Drawing html={svg} label={alt ?? caption} />
      ) : (
        <img src={src} alt={alt ?? caption} loading="lazy" decoding="async" />
      )}
    </figure>
  );
}
