// ---------- Footer marquee: duplicate the lettering so the loop is seamless ----------
(() => {
  const track = document.querySelector('.footer-track');
  if (track) track.append(track.firstElementChild.cloneNode(true));
})();

// ---------- Venue / club tabs (also reachable via #venues and #clubs links) ----------
(() => {
  const tabs = [...document.querySelectorAll('.tab')];
  const section = document.getElementById('sides');
  if (!tabs.length) return;

  function select(id, focus) {
    tabs.forEach((tab) => {
      const on = tab.getAttribute('aria-controls') === id;
      tab.setAttribute('aria-selected', on);
      tab.tabIndex = on ? 0 : -1;
      document.getElementById(tab.getAttribute('aria-controls')).hidden = !on;
      if (on && focus) tab.focus();
    });
  }

  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab.getAttribute('aria-controls')));
    tab.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const next = tabs[(i + (e.key === 'ArrowRight' ? 1 : tabs.length - 1)) % tabs.length];
      select(next.getAttribute('aria-controls'), true);
    });
  });

  // Links to #venues / #clubs open the right tab, then scroll to the section.
  document.querySelectorAll('a[href="#venues"], a[href="#clubs"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const id = link.getAttribute('href').slice(1);
      select(id);
      section.scrollIntoView({ behavior: 'smooth' });
      history.replaceState(null, '', '#' + id);
    });
  });
  if (location.hash === '#clubs' || location.hash === '#venues') {
    select(location.hash.slice(1));
    section.scrollIntoView();
  }
})();

// ---------- Build a match ----------
(() => {
  const form = document.getElementById('match-form');
  if (!form) return;

  // Illustrative venue profiles per kind of group. Not real venues.
  const PROFILES = {
    book:     { label: 'book club',         venue: 'a wine bar with a quiet back room',           seat: 'one long table, low music',   spend: [20, 30], time: '7:00 PM' },
    run:      { label: 'run club',          venue: 'an all-day café near the river path',          seat: 'high tops + standing room',   spend: [12, 18], time: '8:15 PM, after the run' },
    craft:    { label: 'craft night',       venue: 'a café with big tables and good light',        seat: 'tables with elbow room',      spend: [12, 20], time: '6:30 PM' },
    game:     { label: 'game night',        venue: 'a bar with booths and a games-friendly manager', seat: 'booths for 4–6',            spend: [18, 28], time: '7:30 PM' },
    language: { label: 'language exchange', venue: 'a neighborhood bistro with a communal table',  seat: 'communal table + bar seats',  spend: [15, 25], time: '7:00 PM' },
    supper:   { label: 'supper club',       venue: 'a restaurant with a semi-private back room',   seat: 'seated, family-style',        spend: [35, 55], time: '7:30 PM' },
    writing:  { label: 'writing group',     venue: 'a quiet café that stays open late',            seat: 'small tables, outlets',       spend: [10, 16], time: '6:30 PM' },
    wellness: { label: 'wellness group',    venue: 'a coffee & juice spot with an open floor',     seat: 'a space that clears easily',  spend: [10, 18], time: '10:00 AM' },
  };

  const $ = (id) => document.getElementById(id);
  let slipNo = 41;

  function render() {
    const data = new FormData(form);
    const p = PROFILES[data.get('club')];
    const size = Number(data.get('size'));
    const day = data.get('day');
    const area = data.get('area');
    const time = data.get('club') === 'wellness' && day !== 'Sunday' ? '7:30 AM' : p.time;

    $('size-out').textContent = size;
    $('slip-no').textContent = String(++slipNo).padStart(4, '0');
    $('slip-when').textContent = `Every ${day} · ${time}`;
    $('slip-group').textContent = `Your ${p.label}, ~${size} people`;
    $('slip-venue').textContent = `${p.venue} in ${area}`;
    $('slip-seat').textContent = size > 30 ? 'a private room or a section to yourselves' : p.seat;
    $('slip-spend').textContent = `$${p.spend[0]}–${p.spend[1]} a person`;

    const checks = [
      ['✓', `${day} is one of the venue’s quiet nights`],
      ['✓', `room for ${size}, plus a few extra`],
      ['✓', `within ~15 min of ${area}`],
      ['✓', 'your activity fits the house rules'],
      ['◌', 'spend terms to confirm with both sides'],
    ];
    $('slip-checks').replaceChildren(
      ...checks.map(([mark, text]) => {
        const li = document.createElement('li');
        const b = document.createElement('b');
        b.textContent = mark;
        li.append(b, text);
        return li;
      })
    );
  }

  form.addEventListener('input', render);
  render();
})();

// ---------- Intake forms ----------
// With no data-endpoint set, submissions stay in the browser (nothing is sent).
(() => {
  document.querySelectorAll('.intake').forEach((form) => {
    const done = form.querySelector('.intake-done');

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
      const button = form.querySelector('button');
      button.disabled = true;

      try {
        if (endpoint) {
          const res = await fetch(endpoint, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
          if (!res.ok) throw new Error(res.statusText);
        } else {
          console.warn('Coop intake form has no data-endpoint; submission was not sent.', Object.fromEntries(new FormData(form)));
        }
        const name = form.elements.name.value.trim().split(' ')[0];
        done.textContent = `Thanks, ${name} — got it. We’ll be in touch about the pilot.`;
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
})();
