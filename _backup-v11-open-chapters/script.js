// ---------- New York clock ----------
(() => {
  const clock = document.getElementById('clock');
  const tz = document.getElementById('tz');
  const time = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', hour: 'numeric', minute: '2-digit', second: '2-digit' });
  const zone = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', timeZoneName: 'short' });

  function tick() {
    const now = new Date();
    clock.textContent = time.format(now);
    tz.textContent = zone.formatToParts(now).find((p) => p.type === 'timeZoneName').value;
  }
  tick();
  setInterval(tick, 1000);
})();

// ---------- Panels: [data-open="name"] opens #p-name ----------
const panels = {};
document.querySelectorAll('dialog.panel').forEach((d) => {
  panels[d.id.replace(/^p-/, '')] = d;
  d.addEventListener('click', (e) => { if (e.target === d) d.close(); });            // backdrop click
  d.querySelectorAll('[data-close]').forEach((b) => b.addEventListener('click', () => d.close()));
});

function openPanel(name) {
  const d = panels[name];
  if (!d) return;
  document.querySelectorAll('dialog[open]').forEach((o) => o !== d && o.close());
  if (!d.open) d.showModal();
  d.querySelector('.panel-card').scrollTop = 0;
}

document.querySelectorAll('[data-open]').forEach((btn) => {
  btn.addEventListener('click', () => {
    if (btn.dataset.side) selectSide(btn.dataset.side);
    openPanel(btn.dataset.open);
  });
});

// Deep links like coop.nyc/#faq or #join
const hash = location.hash.slice(1);
if (panels[hash]) openPanel(hash);

// ---------- Join: venue / club switch ----------
const tabs = [...document.querySelectorAll('.switch [role="tab"]')];

function selectSide(side, focus) {
  tabs.forEach((tab) => {
    const on = tab.id === `tab-${side}`;
    tab.setAttribute('aria-selected', on);
    tab.tabIndex = on ? 0 : -1;
    document.getElementById(tab.getAttribute('aria-controls')).hidden = !on;
    if (on && focus) tab.focus();
  });
}

tabs.forEach((tab, i) => {
  tab.addEventListener('click', () => selectSide(tab.id.slice(4)));
  tab.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
    selectSide(tabs[(i + 1) % tabs.length].id.slice(4), true);
  });
});

// ---------- Lightbox for the sketches ----------
(() => {
  const box = document.getElementById('lightbox');
  const img = document.getElementById('lb-img');
  const title = document.getElementById('lb-title');
  const id = document.getElementById('lb-id');
  const tiles = [...document.querySelectorAll('.tile')];
  let current = 0;

  function show(i) {
    current = (i + tiles.length) % tiles.length;
    const t = tiles[current];
    img.src = t.dataset.src;
    img.alt = t.querySelector('img').alt;
    title.textContent = t.dataset.title;
    id.textContent = t.dataset.id;
  }

  tiles.forEach((t, i) => t.addEventListener('click', () => { show(i); box.showModal(); }));
  document.getElementById('lb-prev').addEventListener('click', () => show(current - 1));
  document.getElementById('lb-next').addEventListener('click', () => show(current + 1));
  box.addEventListener('click', (e) => { if (e.target === box) box.close(); });
  box.querySelector('[data-close]').addEventListener('click', () => box.close());
  box.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') show(current - 1);
    if (e.key === 'ArrowRight') show(current + 1);
  });
})();

// ---------- Intake forms ----------
// With no data-endpoint set, submissions stay in the browser (nothing is sent).
document.querySelectorAll('.intake').forEach((form) => {
  const done = form.querySelector('.done');

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    let ok = true;
    form.querySelectorAll('[required]').forEach((input) => {
      const bad = !input.value.trim() || (input.type === 'email' && !input.validity.valid);
      input.setAttribute('aria-invalid', bad);
      if (bad && ok) { input.focus(); ok = false; }
    });
    if (!ok) return;

    const endpoint = form.dataset.endpoint;
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;

    try {
      if (endpoint) {
        const res = await fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
        if (!res.ok) throw new Error(res.statusText);
      } else {
        console.warn('Coop intake form has no data-endpoint; submission was not sent.', Object.fromEntries(new FormData(form)));
      }
      const name = form.elements.name.value.trim().split(' ')[0];
      done.textContent = `Thanks, ${name}, got it. We'll be in touch about the pilot.`;
      done.hidden = false;
      form.reset();
    } catch {
      done.textContent = 'Something went wrong sending that. Please try again in a minute.';
      done.hidden = false;
    } finally {
      button.disabled = false;
    }
  });
});
