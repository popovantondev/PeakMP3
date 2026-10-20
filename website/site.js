(() => {
  const menu = document.querySelector('.menu-toggle');
  menu?.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    document.querySelector('#site-menu').classList.toggle('open', open);
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && menu) {
      menu.setAttribute('aria-expanded', 'false');
      document.querySelector('#site-menu').classList.remove('open');
    }
  });
  document.querySelectorAll('.languages a').forEach(a => a.addEventListener('click', () => {
    try { localStorage.setItem('studio.site.language', a.lang); } catch (_) {}
  }));
})();

// Keep cross-product navigation inside the two local review sites.
(() => {
 if (!['127.0.0.1','localhost'].includes(location.hostname)) return;
 for (const link of document.querySelectorAll('a[href]')) {
  const url = new URL(link.href, location.href);
  if (url.origin !== 'https://popovantondev.github.io') continue;
  const target = url.pathname.match(/^\/(PeakMP3|YouTubeDownloader)\/(.*)$/);
  if (!target) continue;
  link.href = 'http://' + location.hostname + ':' + (target[1] === 'PeakMP3' ? '8768' : '8767') + '/' + target[2] + url.search + url.hash;
 }
})();
