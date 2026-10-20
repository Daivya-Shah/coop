// ---------- Intake forms (join.html) ----------
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
        done.textContent = `Thanks, ${name}, got it. We’ll be in touch about the pilot.`;
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
