/** A sketch in a Carl Hauser-style rounded tile, with a small caption and number on top. */
export function Tile({ src, caption, n }: { src: string; caption: string; n: string }) {
  return (
    <figure className="tile">
      <span className="meta"><span>{caption}</span><span>{n}</span></span>
      <img src={`/img/sketches/${src}.svg`} alt={caption} loading="lazy" />
    </figure>
  );
}
