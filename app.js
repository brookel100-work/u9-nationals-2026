const data = window.APP_DATA;
const app = document.getElementById('app');
const navButtons = [...document.querySelectorAll('.nav-item')];
let currentView = 'home';
let deferredInstallPrompt = null;

const esc = (s = '') => String(s)
  .replaceAll('&', '&amp;')
  .replaceAll('<', '&lt;')
  .replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;')
  .replaceAll("'", '&#039;');

function qldDate(date, time = '00:00') {
  return new Date(`${date}T${time}:00+10:00`);
}

function countdownText() {
  const now = new Date();
  const start = new Date(data.meta.nationalsStart);
  const diff = start - now;
  if (diff <= 0) {
    const end = new Date(data.meta.nationalsEnd);
    if (now <= end) return 'Nationals are underway! 🏒';
    return 'Nationals complete 💙💛';
  }
  const days = Math.ceil(diff / 86400000);
  return `${days} day${days === 1 ? '' : 's'} to Nationals`;
}

function getNextGame() {
  const now = new Date();
  return data.schedule
    .map(g => ({...g, when: qldDate(g.date, g.time)}))
    .filter(g => g.when >= now)
    .sort((a,b) => a.when - b.when)[0] || null;
}

function sectionTitle(title, aside = '') {
  return `<div class="section-title"><h2>${esc(title)}</h2>${aside ? `<small>${esc(aside)}</small>` : ''}</div>`;
}

function nextGameCard(game) {
  if (!game) return `<div class="card empty">No upcoming round-robin games.</div>`;
  return `
    <article class="card next-game">
      <div class="match-row">
        <div>
          <div class="eyebrow" style="color:#667085">NEXT U9 GAME · GAME ${esc(game.id)}</div>
          <h3 style="margin-top:6px;font-size:22px">${esc(game.match)}</h3>
          <p>${esc(game.dateLabel)} · ${esc(game.venue)}</p>
        </div>
        <div class="match-time"><strong>${esc(game.timeLabel)}</strong><span>game time</span></div>
      </div>
      <div class="match-meta">
        <span class="pill gold">⏰ Arrive ${esc(game.arrivalLabel)}</span>
        <span class="pill">🕒 ${esc(data.meta.timezoneLabel)}</span>
      </div>
    </article>`;
}

function renderHome() {
  const next = getNextGame();
  return `
    <section class="hero">
      <div class="eyebrow">South Australia · Under 9</div>
      <h1>Nationals 2026</h1>
      <p>${esc(data.meta.subtitle)}<br>${esc(data.meta.location)}</p>
      <div class="countdown">🏒 ${esc(countdownText())}</div>
    </section>

    ${sectionTitle('Next up', data.meta.scheduleVersion)}
    ${nextGameCard(next)}

    ${sectionTitle('Latest updates')}
    ${data.updates.map(u => `
      <article class="card update-card">
        <div class="date-badge">${esc(u.date)}</div>
        <div><h3>${esc(u.title)}</h3><p>${esc(u.body)}</p></div>
      </article>`).join('')}

    <p class="source-note">Schedule shown from Nationals Draw ${esc(data.meta.scheduleVersion)} · Last updated ${esc(data.meta.lastUpdated)}</p>
  `;
}

function renderTeam() {
  return `
    <div class="section-title" style="margin-top:4px"><h2>SA U9 Team</h2><small>${data.team.length} players</small></div>
    <div class="team-grid">
      ${data.team.map(p => `
        <article class="card person">
          <div class="avatar">${esc(p.badge || p.name.split(' ').map(x => x[0]).slice(0,2).join(''))}</div>
          <div class="person-copy"><strong>${esc(p.name)}</strong><small>${esc(p.role)}</small></div>
          ${p.badge ? `<span class="role-badge">${esc(p.badge)}</span>` : ''}
        </article>`).join('')}
    </div>

    ${sectionTitle('Team staff')}
    <div class="team-grid">
      ${data.staff.map(p => `
        <article class="card person">
          <div class="avatar">${esc(p.name.split(' ').map(x => x[0]).slice(0,2).join(''))}</div>
          <div class="person-copy"><strong>${esc(p.name)}</strong><small>${esc(p.role)}</small></div>
        </article>`).join('')}
    </div>

    <div class="notice">This family-facing Team page intentionally does not display private contact, payment or registration information.</div>
  `;
}

function gameCard(g, conditional = false) {
  return `
    <article class="card schedule-card ${conditional ? 'conditional' : ''}">
      <div class="schedule-top">
        <div class="schedule-date">${esc(g.dateLabel)}</div>
        <div class="schedule-id">Game ${esc(g.id)}</div>
      </div>
      <div class="schedule-match">${esc(g.match)}</div>
      <div class="schedule-details">
        <div class="schedule-detail"><span>Game</span><strong>${esc(g.timeLabel)}</strong></div>
        <div class="schedule-detail"><span>Team arrival</span><strong>${esc(g.arrivalLabel)}</strong></div>
      </div>
      ${g.note ? `<div class="notice">${esc(g.note)}</div>` : ''}
    </article>`;
}

function renderSchedule() {
  return `
    <div class="section-title" style="margin-top:4px"><h2>U9 Schedule</h2><small>${esc(data.meta.scheduleVersion)}</small></div>
    <div class="notice" style="margin-top:0">All times are <strong>Queensland time (AEST)</strong>. Team arrival is shown one hour before game time.</div>

    ${sectionTitle('Round robin')}
    ${data.schedule.map(g => gameCard(g, false)).join('')}

    ${sectionTitle('Play-in & finals', 'depends on standings')}
    ${data.finals.map(g => gameCard(g, true)).join('')}

    <p class="source-note">Change-room allocations are not shown because they were not populated in the supplied v2.6 change-room sheet.</p>
  `;
}

function renderChecklist() {
  return `
    <div class="section-title" style="margin-top:4px"><h2>Nationals Checklist</h2><small>Family reference</small></div>
    <div class="notice" style="margin-top:0">This is a quick-reference list. Your Team Manager is separately tracking team administration.</div>
    ${data.checklist.map(item => `
      <article class="card check-item">
        <div class="check-icon">✓</div>
        <div><h3>${esc(item.title)}</h3><p>${esc(item.detail)}</p></div>
      </article>`).join('')}
  `;
}

function renderInfo() {
  return `
    <div class="section-title" style="margin-top:4px"><h2>Info & Links</h2><small>one place, no scrolling</small></div>
    ${data.links.map(l => `
      <a class="card link-card" href="${esc(l.url)}" target="_blank" rel="noopener noreferrer">
        <div class="link-icon">${esc(l.icon)}</div>
        <div class="link-copy"><strong>${esc(l.title)}</strong><span>${esc(l.description)}</span></div>
        <div class="chevron">›</div>
      </a>`).join('')}

    ${sectionTitle('Quick Nationals rules')}
    <article class="card"><ul class="rule-list">${data.rules.map(r => `<li>${esc(r)}</li>`).join('')}</ul></article>

    <p class="source-note">Venue: Skate Paradise, 34–38 Johnson Road, Hillcrest QLD 4118.</p>
  `;
}

const views = { home: renderHome, team: renderTeam, schedule: renderSchedule, checklist: renderChecklist, info: renderInfo };

function showView(view, pushHash = true) {
  currentView = views[view] ? view : 'home';
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
  event.preventDefault();
  deferredInstallPrompt = event;
  const btn = document.getElementById('installBtn');
  btn.hidden = false;
  btn.addEventListener('click', async () => {
    btn.hidden = true;
    deferredInstallPrompt.prompt();
    await deferredInstallPrompt.userChoice;
    deferredInstallPrompt = null;
  }, { once: true });
});

if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => navigator.serviceWorker.register('./sw.js').catch(() => {}));
}
