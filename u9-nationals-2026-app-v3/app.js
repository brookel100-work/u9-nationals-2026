const data = window.APP_DATA;
const app = document.getElementById('app');
const navButtons = [...document.querySelectorAll('.nav-item')];
let deferredInstallPrompt = null;

const esc = (s = '') => String(s)
  .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;').replaceAll("'", '&#039;');

function qldDate(date, time = '00:00') { return new Date(`${date}T${time}:00+10:00`); }
function countdownText() {
  const now = new Date();
  const start = new Date(data.meta.nationalsStart);
  const diff = start - now;
  if (diff <= 0) {
    const end = new Date(data.meta.nationalsEnd);
    if (now <= end) return 'Nationals are underway!';
    return 'Nationals complete';
  }
  const days = Math.ceil(diff / 86400000);
  return `${days} day${days === 1 ? '' : 's'} to Nationals`;
}
function getNextGame() {
  const now = new Date();
  return data.schedule.map(g => ({...g, when: qldDate(g.date, g.time)}))
    .filter(g => g.when >= now).sort((a,b) => a.when - b.when)[0] || null;
}
function sectionTitle(title, aside = '') {
  return `<div class="section-title"><h2>${esc(title)}</h2>${aside ? `<small>${esc(aside)}</small>` : ''}</div>`;
}
function nextGameCard(game) {
  if (!game) return `<div class="card empty">No upcoming round-robin games.</div>`;
  return `<article class="card next-game">
    <div class="game-kicker">NEXT U9 GAME · GAME ${esc(game.id)}</div>
    <div class="match-row"><div><h3>${esc(game.match)}</h3><p>${esc(game.dateLabel)} · ${esc(game.venue)}</p></div>
      <div class="match-time"><strong>${esc(game.timeLabel)}</strong><span>game time</span></div></div>
    <div class="match-meta"><span class="pill gold">Arrive ${esc(game.arrivalLabel)}</span><span class="pill">AEST</span></div>
  </article>`;
}
function facebookFeedBlock() {
  const href = encodeURIComponent(data.meta.facebookShareUrl);
  const plugin = `https://www.facebook.com/plugins/page.php?href=${href}&tabs=timeline&width=500&height=640&small_header=true&adapt_container_width=true&hide_cover=false&show_facepile=false`;
  return `<article class="card facebook-feed-card">
    <div class="facebook-title"><div class="fb-mark">f</div><div><strong>Official Nationals Updates</strong><span>Australian Inline Hockey National Championships</span></div></div>
    <div class="facebook-frame-wrap">
      <iframe class="facebook-frame" title="Official Nationals Facebook updates" src="${plugin}" width="500" height="640" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share"></iframe>
    </div>
    <div class="feed-fallback"><span>If Facebook does not display the feed on your device:</span><a href="${esc(data.meta.facebookShareUrl)}" target="_blank" rel="noopener noreferrer">Open official Facebook page</a></div>
  </article>`;
}
function renderHome() {
  const next = getNextGame();
  return `<section class="sa-hero">
      <img src="./assets/sa-u9-training-art.png" alt="South Australia U9 team artwork" class="hero-art" />
      <div class="hero-overlay"></div>
      <div class="hero-content"><div class="eyebrow">UNDER 9 · SOUTH AUSTRALIA</div><h1>Nationals 2026</h1>
      <p>27 September – 4 October · Queensland</p><div class="countdown">${esc(countdownText())}</div></div>
    </section>
    ${sectionTitle('Next game', data.meta.scheduleVersion)}${nextGameCard(next)}
    ${sectionTitle('Official Nationals feed')}
    ${facebookFeedBlock()}
    <p class="source-note">Schedule: Nationals Draw ${esc(data.meta.scheduleVersion)} · Updated ${esc(data.meta.lastUpdated)}</p>`;
}
function renderTeam() {
  return `<section class="team-banner"><div class="team-banner-copy"><div class="eyebrow">SOUTH AUSTRALIA</div><h1>SA U9 Team</h1><p>Play · Represent · Belong</p></div></section>
    <article class="image-card roster-card"><img src="./assets/u9-roster.jpeg" alt="Official South Australia U9 representative team roster" /></article>
    ${sectionTitle('Players')}
    <div class="team-grid">${data.team.map(p => `<article class="card person"><div class="avatar">${esc(p.badge || p.name.split(' ').map(x => x[0]).slice(0,2).join(''))}</div><div class="person-copy"><strong>${esc(p.name)}</strong><small>${esc(p.role)}</small></div>${p.badge ? `<span class="role-badge">${esc(p.badge)}</span>` : ''}</article>`).join('')}</div>
    ${sectionTitle('Team staff')}
    <div class="team-grid">${data.staff.map(p => `<article class="card person"><div class="avatar staff">${esc(p.name.split(' ').map(x => x[0]).slice(0,2).join(''))}</div><div class="person-copy"><strong>${esc(p.name)}</strong><small>${esc(p.role)}</small></div></article>`).join('')}</div>`;
}
function gameCard(g, conditional = false) {
  return `<article class="card schedule-card ${conditional ? 'conditional' : ''}"><div class="schedule-top"><div class="schedule-date">${esc(g.dateLabel)}</div><div class="schedule-id">Game ${esc(g.id)}</div></div>
    <div class="schedule-match">${esc(g.match)}</div><div class="schedule-details"><div class="schedule-detail"><span>Game</span><strong>${esc(g.timeLabel)}</strong></div><div class="schedule-detail"><span>Team arrival</span><strong>${esc(g.arrivalLabel)}</strong></div></div>${g.note ? `<div class="notice">${esc(g.note)}</div>` : ''}</article>`;
}
function renderSchedule() {
  return `<div class="page-hero compact"><div><div class="eyebrow">QUEENSLAND · AEST</div><h1>U9 Schedule</h1><p>Arrive one hour before each game.</p></div></div>
    ${sectionTitle('Round robin')}${data.schedule.map(g => gameCard(g)).join('')}
    ${sectionTitle('Play-in & finals', 'depends on standings')}${data.finals.map(g => gameCard(g, true)).join('')}
    <details class="training-details"><summary>Completed SA Nationals training <span>${data.training.length} sessions</span></summary><div class="training-body">${data.training.map(t => `<div class="training-row"><div><strong>${esc(t.dateLabel)}</strong><span>${esc(t.group)}</span></div><div class="training-time">${esc(t.timeLabel)} <b>✓</b></div></div>`).join('')}</div></details>
    <p class="source-note">Change-room allocations are not shown because the supplied v2.6 change-room sheet was blank.</p>`;
}
function renderChecklist() {
  return `<div class="page-hero compact"><div><div class="eyebrow">READY TO GO</div><h1>Nationals Checklist</h1><p>Quick family reference before Queensland.</p></div></div>
    ${data.checklist.map(item => `<article class="card check-item"><div class="check-icon">✓</div><div><h3>${esc(item.title)}</h3><p>${esc(item.detail)}</p></div></article>`).join('')}`;
}
function renderInfo() {
  return `<section class="event-banner"><div class="event-banner-copy"><div class="eyebrow">AUSTRALIAN INLINE HOCKEY</div><h1>2026 National Championships</h1><p>27 September – 4 October · Skate Paradise, Queensland</p></div></section>
    <article class="image-card poster"><img src="./assets/nationals-poster-full.png" alt="Official 2026 Australian Inline Hockey National Championships poster" /></article>
    ${sectionTitle('Useful links')}${data.links.map(l => `<a class="card link-card ${l.featured ? 'featured-link' : ''}" href="${esc(l.url)}" target="_blank" rel="noopener noreferrer"><div class="link-icon">${esc(l.icon)}</div><div class="link-copy"><strong>${esc(l.title)}</strong><span>${esc(l.description)}</span></div><div class="chevron">›</div></a>`).join('')}
    ${sectionTitle('Venue')}<article class="card venue-card"><strong>Skate Paradise</strong><p>${esc(data.meta.address)}</p><a class="secondary-link" href="https://www.google.com/maps/search/?api=1&query=Skate+Paradise+34-38+Johnson+Road+Hillcrest+QLD+4118" target="_blank" rel="noopener noreferrer">Open in Maps</a></article>
    ${sectionTitle('Quick Nationals rules')}<article class="card"><ul class="rule-list">${data.rules.map(r => `<li>${esc(r)}</li>`).join('')}</ul></article>`;
}
const views = { home: renderHome, schedule: renderSchedule, team: renderTeam, checklist: renderChecklist, info: renderInfo };
function showView(view, pushHash = true) {
  const currentView = views[view] ? view : 'home';
  app.innerHTML = views[currentView]();
  navButtons.forEach(b => b.classList.toggle('active', b.dataset.view === currentView));
  if (pushHash) history.replaceState(null, '', `#${currentView}`);
  window.scrollTo({ top: 0, behavior: 'instant' });
  app.focus({ preventScroll: true });
}
navButtons.forEach(btn => btn.addEventListener('click', () => showView(btn.dataset.view)));
window.addEventListener('hashchange', () => showView(location.hash.slice(1) || 'home', false));
showView(location.hash.slice(1) || 'home', false);
window.addEventListener('beforeinstallprompt', (event) => {
  event.preventDefault(); deferredInstallPrompt = event;
  const btn = document.getElementById('installBtn'); btn.hidden = false;
  btn.addEventListener('click', async () => { btn.hidden = true; deferredInstallPrompt.prompt(); await deferredInstallPrompt.userChoice; deferredInstallPrompt = null; }, { once: true });
});
if ('serviceWorker' in navigator) window.addEventListener('load', () => navigator.serviceWorker.register('./sw.js').catch(() => {}));
