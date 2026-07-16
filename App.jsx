const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "embossDepth": 1.15,
  "zoomScale": 6.2,
  "butterflyHue": "oklch(0.62 0.13 55)",
  "headerScale": 0.36
}/*EDITMODE-END*/;

function ButterflyMark({ className = "" }) {
  return (
    <svg className={`butterfly ${className}`} viewBox="0 0 240 180" role="img" aria-label="Embossed butterfly logo mark">
      <defs>
        <linearGradient id="wingGold" x1="24" y1="20" x2="205" y2="150" gradientUnits="userSpaceOnUse">
          <stop offset="0" stopColor="oklch(0.88 0.08 80)" />
          <stop offset="0.42" stopColor="var(--ocd-tweak-butterfly-hue)" />
          <stop offset="1" stopColor="oklch(0.34 0.10 48)" />
        </linearGradient>
        <radialGradient id="wingGlow" cx="50%" cy="42%" r="68%">
          <stop offset="0" stopColor="oklch(0.98 0.03 92 / .96)" />
          <stop offset="0.55" stopColor="oklch(0.70 0.12 62 / .8)" />
          <stop offset="1" stopColor="oklch(0.28 0.08 42 / .78)" />
        </radialGradient>
        <filter id="emboss" x="-22%" y="-25%" width="144%" height="150%">
          <feGaussianBlur in="SourceAlpha" stdDeviation="2.4" result="blur" />
          <feSpecularLighting in="blur" surfaceScale="9" specularConstant=".9" specularExponent="25" lightingColor="#fff8df" result="spec">
            <fePointLight x="-90" y="-80" z="180" />
          </feSpecularLighting>
          <feComposite in="spec" in2="SourceAlpha" operator="in" result="specOut" />
          <feOffset in="SourceAlpha" dx="5" dy="8" result="offset" />
          <feGaussianBlur in="offset" stdDeviation="7" result="shadow" />
          <feMerge>
            <feMergeNode in="shadow" />
            <feMergeNode in="SourceGraphic" />
            <feMergeNode in="specOut" />
          </feMerge>
        </filter>
      </defs>
      <g filter="url(#emboss)">
        <path className="wing wing-left upper" d="M111 82C82 35 41 17 23 30 4 44 17 91 47 114c25 19 53 11 70-16 2-4-1-11-6-16Z" />
        <path className="wing wing-right upper" d="M129 82c29-47 70-65 88-52 19 14 6 61-24 84-25 19-53 11-70-16-2-4 1-11 6-16Z" />
        <path className="wing wing-left lower" d="M105 98c-30 2-62 18-66 42-3 18 17 30 39 22 23-8 39-30 43-52 1-7-8-13-16-12Z" />
        <path className="wing wing-right lower" d="M135 98c30 2 62 18 66 42 3 18-17 30-39 22-23-8-39-30-43-52-1-7 8-13 16-12Z" />
        <path className="body" d="M117 61c-9 14-11 32-7 54 2 13 6 27 10 40 4-13 8-27 10-40 4-22 2-40-7-54-2-3-4-3-6 0Z" />
        <path className="antenna" d="M115 67C104 45 90 34 75 31M125 67c11-22 25-33 40-36" />
        <circle cx="74" cy="31" r="4" className="tip" />
        <circle cx="166" cy="31" r="4" className="tip" />
      </g>
    </svg>
  );
}

function App() {
  const [progress, setProgress] = React.useState(0);
  const [isNarrow, setIsNarrow] = React.useState(false);

  React.useEffect(() => {
    const update = () => {
      const max = Math.max(1, document.documentElement.scrollHeight - window.innerHeight);
      setProgress(Math.min(1, Math.max(0, window.scrollY / Math.min(max, 920))));
      setIsNarrow(window.innerWidth < 820);
    };
    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => {
      window.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, []);

  const takeover = Math.min(1, Math.max(0, (progress - 0.12) / 0.34));
  const settle = Math.min(1, Math.max(0, (progress - 0.56) / 0.34));
  const headerOpacity = Math.min(1, Math.max(0, (progress - 0.7) / 0.22));
  const heroFade = 1 - Math.min(1, Math.max(0, progress / 0.2));
  const heroScale = 1 - takeover * 0.18;
  const zoomScale = 1 + takeover * (TWEAK_DEFAULTS.zoomScale - 1);
  const finalScale = TWEAK_DEFAULTS.headerScale;
  const scale = zoomScale * (1 - settle) + finalScale * settle;
  const restingX = isNarrow ? 0 : 18;
  const restingY = isNarrow ? 42 : 34;
  const takeoverX = restingX * (1 - takeover);
  const takeoverY = restingY * (1 - takeover);
  const x = takeoverX * (1 - settle) + -42 * settle;
  const y = takeoverY * (1 - settle) + (-38 * settle);
  const rotate = -2 + takeover * 7 - settle * 5;

  return (
    <main className="page" style={{ "--progress": progress }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT,WONK@9..144,500..800,35,1&family=Manrope:wght@500;650;800&display=swap');
        :root {
          --ocd-tweak-emboss-depth: ${TWEAK_DEFAULTS.embossDepth};
          --ocd-tweak-zoom-scale: ${TWEAK_DEFAULTS.zoomScale};
          --ocd-tweak-butterfly-hue: ${TWEAK_DEFAULTS.butterflyHue};
          --ocd-tweak-header-scale: ${TWEAK_DEFAULTS.headerScale};
          --ink: oklch(0.18 0.03 60);
          --muted: oklch(0.45 0.04 63);
          --paper: oklch(0.94 0.025 82);
          --cream: oklch(0.89 0.045 82);
          --line: oklch(0.63 0.06 70 / .34);
          --cocoa: oklch(0.25 0.045 48);
          font-family: Avenir Next, Trebuchet MS, Segoe UI, sans-serif;
        }
        * { box-sizing: border-box; }
        html { scroll-behavior: smooth; }
        body { margin: 0; background: var(--paper); color: var(--ink); overflow-x: hidden; }
        button { font: inherit; }
        .page {
          min-height: 230vh;
          background:
            radial-gradient(circle at 78% 8%, oklch(0.81 0.09 64 / .5), transparent 25rem),
            radial-gradient(circle at 8% 36%, oklch(0.78 0.08 105 / .38), transparent 28rem),
            linear-gradient(135deg, oklch(0.96 0.032 88), oklch(0.86 0.045 74));
          position: relative;
          isolation: isolate;
        }
        .page:before {
          content: "";
          position: fixed;
          inset: 0;
          pointer-events: none;
          opacity: .08;
          z-index: 0;
          background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 180 180' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.75' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='180' height='180' filter='url(%23n)' opacity='.7'/%3E%3C/svg%3E");
          mix-blend-mode: multiply;
        }
        .site-header {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 7;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: clamp(1rem, 2vw, 1.6rem) clamp(1rem, 4vw, 3.25rem);
          background: linear-gradient(to bottom, oklch(0.95 0.03 83 / .88), oklch(0.95 0.03 83 / .32), transparent);
          backdrop-filter: blur(10px);
          opacity: calc(.25 + ${headerOpacity} * .75);
        }
        .brand {
          display: inline-flex;
          align-items: center;
          gap: .65rem;
          min-width: 10rem;
          font-weight: 800;
          letter-spacing: -.04em;
        }
        .brand-slot {
          width: 2.25rem;
          height: 2.25rem;
          border-radius: 999px;
          background: oklch(0.95 0.032 84 / .62);
          border: 1px solid var(--line);
          box-shadow: inset 1px 1px 1px oklch(1 0 0 / .8), inset -1px -1px 2px oklch(0.35 0.05 52 / .22);
        }
        .header-actions { display: flex; align-items: center; gap: .7rem; }
        .ghost, .solid {
          border: 1px solid var(--line);
          border-radius: 999px;
          padding: .78rem 1rem;
          color: var(--ink);
          background: oklch(0.96 0.03 85 / .52);
          box-shadow: inset 0 1px 0 oklch(1 0 0 / .58);
        }
        .solid { background: var(--cocoa); color: oklch(0.96 0.03 84); border-color: oklch(0.22 0.04 50); }
        .hero {
          min-height: 100vh;
          padding: clamp(6.5rem, 12vw, 9rem) clamp(1.2rem, 5vw, 5rem) 5rem;
          display: grid;
          grid-template-columns: minmax(0, 1.02fr) minmax(18rem, .8fr);
          gap: clamp(2rem, 7vw, 7rem);
          align-items: start;
          position: sticky;
          top: 0;
          z-index: 2;
          transform: scale(${heroScale});
          transform-origin: 42% 28%;
        }
        .copy {
          max-width: 48rem;
          padding-top: clamp(1rem, 6vh, 4.5rem);
          opacity: ${heroFade};
          transition: opacity .08s linear;
        }
        .eyebrow {
          display: inline-flex;
          align-items: center;
          gap: .55rem;
          color: var(--muted);
          font-weight: 800;
          letter-spacing: .11em;
          text-transform: uppercase;
          font-size: .77rem;
        }
        .eyebrow:before { content: ""; width: 2.6rem; height: 1px; background: var(--line); }
        h1 {
          font-family: Georgia, Charter, serif;
          font-size: clamp(3.45rem, 9.8vw, 9.4rem);
          line-height: .86;
          letter-spacing: -.08em;
          margin: 1.1rem 0 1.35rem;
          max-width: 11ch;
        }
        .lede {
          max-width: 39rem;
          color: oklch(0.32 0.045 58);
          font-size: clamp(1.03rem, 1.55vw, 1.32rem);
          line-height: 1.65;
          margin: 0 0 1.6rem;
        }
        .cta-row { display: flex; flex-wrap: wrap; gap: .85rem; align-items: center; }
        .primary, .secondary {
          border: 0;
          border-radius: 999px;
          padding: 1rem 1.24rem;
          font-weight: 800;
          cursor: pointer;
          transition: transform .18s ease, box-shadow .18s ease;
        }
        .primary { background: var(--ink); color: var(--paper); box-shadow: 0 1rem 2.4rem oklch(0.22 0.04 55 / .20); }
        .secondary { background: transparent; color: var(--ink); outline: 1px solid var(--line); }
        .primary:hover, .secondary:hover { transform: translateY(-2px); }
        .butterfly-stage {
          min-height: 58vh;
          display: flex;
          align-items: end;
          justify-content: center;
          padding-top: clamp(3rem, 12vh, 9rem);
          position: relative;
          z-index: 1;
        }
        .orbit-note {
          position: absolute;
          right: 2vw;
          bottom: 7vh;
          max-width: 13rem;
          color: var(--muted);
          font-size: .88rem;
          line-height: 1.55;
          border-left: 1px solid var(--line);
          padding-left: 1rem;
        }
        .floating-mark {
          position: fixed;
          left: 50%;
          top: 50%;
          width: min(42vw, 24rem);
          height: auto;
          z-index: 5;
          transform: translate(calc(-50% + ${x}vw), calc(-50% + ${y}vh)) scale(${scale}) rotate(${rotate}deg);
          transform-origin: center;
          pointer-events: none;
          will-change: transform;
          filter: drop-shadow(0 2rem 3rem oklch(0.22 0.06 50 / .2));
        }
        .butterfly .wing { fill: url(#wingGold); stroke: oklch(0.20 0.055 45 / .35); stroke-width: 1.2; }
        .butterfly .upper { fill: url(#wingGlow); }
        .butterfly .lower { opacity: .94; }
        .butterfly .body { fill: oklch(0.18 0.045 47); }
        .butterfly .antenna { fill: none; stroke: oklch(0.18 0.045 47); stroke-width: 3.4; stroke-linecap: round; }
        .butterfly .tip { fill: oklch(0.18 0.045 47); }
        .content {
          position: relative;
          z-index: 4;
          margin-top: 12vh;
          padding: 0 clamp(1.2rem, 5vw, 5rem) 8rem;
        }
        .panel {
          max-width: 72rem;
          margin: 0 auto;
          border: 1px solid var(--line);
          border-radius: clamp(1.6rem, 3vw, 3rem);
          padding: clamp(1.4rem, 4vw, 4rem);
          background: oklch(0.96 0.03 84 / .74);
          backdrop-filter: blur(18px);
          box-shadow: inset 0 1px 0 oklch(1 0 0 / .68), 0 3rem 7rem oklch(0.28 0.05 52 / .14);
          display: grid;
          grid-template-columns: .9fr 1.1fr;
          gap: clamp(1.5rem, 5vw, 5rem);
        }
        .panel h2 {
          font-family: Georgia, Charter, serif;
          font-size: clamp(2rem, 5vw, 5.2rem);
          line-height: .96;
          letter-spacing: -.06em;
          margin: 0;
        }
        .panel p { color: var(--muted); line-height: 1.7; font-size: 1.03rem; margin-top: 0; }
        .steps { display: grid; gap: .85rem; }
        .step { padding: 1rem 0; border-top: 1px solid var(--line); display: flex; justify-content: space-between; gap: 1rem; }
        .step strong { font-size: .92rem; }
        .step span { color: var(--muted); max-width: 26rem; line-height: 1.45; }
        :focus-visible { outline: 3px solid oklch(0.67 0.13 68); outline-offset: 4px; }
        @media (max-width: 820px) {
          .site-header { padding-inline: 1rem; }
          .header-actions .ghost { display: none; }
          .hero { grid-template-columns: 1fr; min-height: 108vh; padding-top: 6.5rem; gap: 1rem; }
          .copy { padding-top: 1rem; }
          h1 { font-size: clamp(3.2rem, 17vw, 6.2rem); }
          .butterfly-stage { min-height: 34vh; padding-top: 0; align-items: center; }
          .floating-mark { width: min(76vw, 22rem); }
          .orbit-note { display: none; }
          .panel { grid-template-columns: 1fr; }
        }
        @media (prefers-reduced-motion: reduce) {
          html { scroll-behavior: auto; }
          .floating-mark { transition: none; transform: translate(-50%, -22%) scale(var(--ocd-tweak-header-scale)); left: 8.8rem; top: 2.4rem; }
          .copy { opacity: 1; }
          .hero { transform: none; position: relative; }
        }
      `}</style>

      <header className="site-header" aria-label="Index page header">
        <div className="brand">
          <span className="brand-slot" aria-hidden="true" />
          <span>Butterfly</span>
        </div>
        <div className="header-actions">
          <button className="ghost" type="button">View sequence</button>
          <button className="solid" type="button">Open index</button>
        </div>
      </header>

      <ButterflyMark className="floating-mark" />

      <section className="hero" aria-labelledby="hero-title">
        <div className="copy">
          <span className="eyebrow">Index page motion study</span>
          <h1 id="hero-title">Embossed logo takeover</h1>
          <p className="lede">
            The collage has been replaced by a single embossed butterfly icon. Before scrolling, the hero text and buttons stay clear while the mark sits below as the visual anchor.
          </p>
          <div className="cta-row" aria-label="Hero actions">
            <button className="primary" type="button">Start below the fold</button>
            <button className="secondary" type="button">Inspect motion path</button>
          </div>
        </div>
        <div className="butterfly-stage" aria-hidden="true">
          <p className="orbit-note">Scroll: the mark zooms forward, washes over the page, then settles into the header identity.</p>
        </div>
      </section>

      <section className="content" aria-labelledby="motion-title">
        <div className="panel">
          <h2 id="motion-title">One icon, three readable states.</h2>
          <div>
            <p>
              The butterfly begins below the copy, expands into a full-page transition, and resolves into a compact header mark so the navigation inherits the logo rather than competing with it.
            </p>
            <div className="steps" aria-label="Animation stages">
              <div className="step"><strong>01 Resting</strong><span>Hero copy remains unobstructed; the icon is visually below the button row.</span></div>
              <div className="step"><strong>02 Takeover</strong><span>The embossed wings scale up and create the replacement for the removed collage.</span></div>
              <div className="step"><strong>03 Header</strong><span>The mark contracts into the brand slot as the user reaches page content.</span></div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />);