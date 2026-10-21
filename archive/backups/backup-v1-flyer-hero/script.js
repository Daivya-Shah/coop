// Hero: cycle the highlighted weekday ("Fill your quiet tuesdays.")
(() => {
  const el = document.querySelector('.rotator-word');
  if (!el || matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const words = el.dataset.words.split(',');
  let i = 0;

  setInterval(() => {
    el.classList.add('is-out');
    setTimeout(() => {
      i = (i + 1) % words.length;
      el.textContent = words[i];
      el.classList.remove('is-out');
    }, 300);
  }, 2400);
})();
