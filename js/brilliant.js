/* Brilliant design system — behaviour helpers (no dependencies, ~6 KB).
 *
 *   <script src="js/brilliant.js" defer></script>
 *
 * Auto-wires on DOMContentLoaded:
 *   · [data-theme-toggle]           cycles light/dark on <html data-theme>, remembered per browser
 *   · .segmented                    moves the thumb (--i) and aria-selected
 *   · [data-chip-group]             single-select chips / CTA toggles (aria-pressed)
 *   · .tabs                         aria-selected underline tabs
 *   · [role=radiogroup] .choice     single-select answer tiles (aria-checked) + "select" sound
 *   · input.slider                  keeps --value in sync for the filled track + detent ticks
 *   · sounds on presses (Brilliant-like soft wooden taps); opt out with data-sfx="none"
 *
 * Exposes window.B = { sfx, reveal, setTheme }:
 *   B.sfx.correct() / wrong() / select() / tap() / reveal() / unlock() / complete() / open() / close()
 *   B.reveal(container) → shows the next [hidden] .beat inside container; returns how many remain
 *
 * Sound engine adapted from the author's AI Engineering Blueprint (src/sound.js): synthesized
 * with Web Audio, soft and low, always the result of a user action. Muted when the OS asks
 * for reduced motion is NOT assumed; respect a user setting via B.sfx.enabled = false.
 */
(() => {
  const store = {
    get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } },
  };

  // ── sound ──
  const sfx = (() => {
    let ctx = null, out = null, noiseBuf = null, lastTick = 0, lastTap = 0;
    function ensure() {
      if (!S.enabled) return null;
      if (navigator.userActivation && !navigator.userActivation.hasBeenActive) return null;
      try {
        if (!ctx) {
          const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null;
          ctx = new AC();
          const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 2600; lp.Q.value = .5;
          const comp = ctx.createDynamicsCompressor(); comp.threshold.value = -3; comp.knee.value = 2; comp.ratio.value = 20; comp.attack.value = .002; comp.release.value = .12;
          out = ctx.createGain(); out.gain.value = 1.4;
          out.connect(lp); lp.connect(comp); comp.connect(ctx.destination);
          noiseBuf = ctx.createBuffer(1, Math.floor(ctx.sampleRate * .3), ctx.sampleRate);
          const d = noiseBuf.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
        }
        if (ctx.state === 'suspended') ctx.resume();
        return ctx;
      } catch (e) { return null; }
    }
    function env(g, s, peak, a, dur) { g.gain.setValueAtTime(.0001, s); g.gain.exponentialRampToValueAtTime(peak, s + a); g.gain.exponentialRampToValueAtTime(.0001, s + dur); }
    function osc(f, t, dur, { type = 'sine', gain = .12, attack = .004, to = null, lp = null } = {}) {
      const c = ensure(); if (!c) return;
      const s = c.currentTime + t, o = c.createOscillator(), g = c.createGain();
      o.type = type; o.frequency.setValueAtTime(f, s); if (to) o.frequency.exponentialRampToValueAtTime(to, s + dur * .8);
      env(g, s, gain, attack, dur);
      let n = o; if (lp) { const f2 = c.createBiquadFilter(); f2.type = 'lowpass'; f2.frequency.value = lp; o.connect(f2); n = f2; }
      n.connect(g); g.connect(out); o.start(s); o.stop(s + dur + .03);
    }
    function noise(t, dur, { gain = .04, freq = 600, q = .7, to = null, type = 'lowpass' } = {}) {
      const c = ensure(); if (!c) return;
      const s = c.currentTime + t, src = c.createBufferSource(); src.buffer = noiseBuf;
      const f = c.createBiquadFilter(); f.type = type; f.frequency.setValueAtTime(freq, s); f.Q.value = q; if (to) f.frequency.exponentialRampToValueAtTime(to, s + dur);
      const g = c.createGain(); env(g, s, gain, .008, dur);
      src.connect(f); f.connect(g); g.connect(out); src.start(s); src.stop(s + dur + .03);
    }
    function mallet(f, t = 0, dur = .5, gain = .13) { osc(f, t, dur, { gain, attack: .003 }); osc(f * 3.98, t, .07, { gain: gain * .18, attack: .002 }); osc(f * 2, t, dur * .35, { gain: gain * .12, attack: .003 }); }
    const S = {
      enabled: store.get('b-sfx') !== 'off',
      tap() { const n = performance.now(); if (n - lastTap < 50) return; lastTap = n; osc(560, 0, .075, { gain: .22, to: 340 }); noise(0, .03, { gain: .05, freq: 1400 }); },
      toggle() { osc(470, 0, .065, { gain: .17, to: 300 }); },
      select() { osc(380, 0, .11, { gain: .22, to: 640, attack: .002 }); },
      tick(frac = .5) { const n = performance.now(); if (n - lastTick < 60) return; lastTick = n; osc(320 + frac * 260, 0, .03, { gain: .07, to: 260 }); },
      reveal() { noise(0, .15, { gain: .05, freq: 500, to: 1200, type: 'bandpass', q: .6 }); mallet(523.25, .02, .3, .1); },
      correct() { mallet(523.25, 0, .5, .16); mallet(659.25, .1, .5, .16); mallet(783.99, .2, .8, .17); },
      wrong() { osc(294, 0, .15, { type: 'triangle', gain: .2, lp: 800 }); osc(220, .12, .26, { type: 'triangle', gain: .18, lp: 650, to: 196 }); },
      unlock() { mallet(659.25, 0, .55, .12); },
      open() { noise(0, .26, { gain: .05, freq: 350, to: 1100, type: 'bandpass', q: .5 }); mallet(392, .05, .4, .1); },
      close() { noise(0, .22, { gain: .045, freq: 1100, to: 350, type: 'bandpass', q: .5 }); },
      complete() { [523.25, 659.25, 783.99, 1046.5].forEach((f, k) => mallet(f, k * .11, .6, .13)); [261.63, 329.63, 392, 523.25].forEach(f => osc(f, .55, 1.1, { gain: .05, attack: .05 })); },
      setEnabled(v) { S.enabled = !!v; store.set('b-sfx', v ? 'on' : 'off'); },
    };
    return S;
  })();

  // ── theme ──
  function setTheme(t) { document.documentElement.dataset.theme = t; store.set('b-theme', t); }
  const saved = store.get('b-theme');
  if (saved && !document.documentElement.hasAttribute('data-theme-locked')) document.documentElement.dataset.theme = saved;

  // ── beats ──
  function reveal(container) {
    const next = container.querySelector('.beat[hidden]');
    if (next) { next.hidden = false; sfx.reveal(); next.scrollIntoView({ block: 'nearest', behavior: 'smooth' }); }
    return container.querySelectorAll('.beat[hidden]').length;
  }

  function wire(root = document) {
    root.querySelectorAll('[data-theme-toggle]').forEach(b => b.addEventListener('click', () =>
      setTheme(document.documentElement.dataset.theme === 'dark' ? 'light' : 'dark')));
    root.querySelectorAll('.segmented').forEach(seg => {
      const btns = [...seg.querySelectorAll('button')];
      seg.style.setProperty('--n', btns.length);
      btns.forEach((b, i) => b.addEventListener('click', () => {
        btns.forEach(x => x.setAttribute('aria-selected', x === b)); seg.style.setProperty('--i', i); sfx.toggle();
      }));
    });
    root.querySelectorAll('[data-chip-group]').forEach(g => g.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
      g.querySelectorAll('button').forEach(x => x.setAttribute('aria-pressed', x === b)); sfx.toggle();
    })));
    root.querySelectorAll('.tabs').forEach(t => t.querySelectorAll('.tab').forEach(b => b.addEventListener('click', () => {
      t.querySelectorAll('.tab').forEach(x => x.setAttribute('aria-selected', x === b)); sfx.toggle();
    })));
    root.querySelectorAll('[role=radiogroup]').forEach(g => g.querySelectorAll('.choice').forEach(c => c.addEventListener('click', () => {
      if (c.disabled) return;
      g.querySelectorAll('.choice').forEach(x => { x.setAttribute('aria-checked', x === c); x.removeAttribute('data-state'); });
      sfx.select(); g.dispatchEvent(new CustomEvent('choice', { detail: c, bubbles: true }));
    })));
    root.querySelectorAll('input.slider').forEach(r => {
      const sync = () => { const min = +r.min || 0, max = +r.max || 100; r.style.setProperty('--value', ((+r.value - min) / ((max - min) || 1) * 100) + '%'); };
      sync(); r.addEventListener('input', () => { sync(); const min = +r.min || 0, max = +r.max || 100; sfx.tick((+r.value - min) / ((max - min) || 1)); });
    });
    root.querySelectorAll('details.deeper').forEach(d => d.addEventListener('toggle', () => d.open ? sfx.open() : sfx.close()));
  }

  // generic press sound for buttons/links styled as buttons
  document.addEventListener('click', e => {
    const t = e.target.closest && e.target.closest('.btn3d, .btn, .icon-btn, .step-arrow, .level-header, .path__item, .card--lip');
    if (!t || t.disabled || t.dataset.sfx === 'none') return;
    sfx.tap();
  }, true);

  window.B = { sfx, reveal, setTheme, wire };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', () => wire()); else wire();
})();
