#!/usr/bin/env python3
"""Sync SA U9 Nationals data from HockeySyte's rendered pages.

Designed for GitHub Actions. Each section is updated independently so one HockeySyte
layout change cannot wipe otherwise-good data. Diagnostic HTML/screenshots/tables are
written to diagnostics/ on every run and uploaded by the workflow when a run fails.
"""
import json, re, traceback
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'live-data.json'; DIAG=ROOT/'diagnostics'; DIAG.mkdir(exist_ok=True)
SEASON='https://ilha.hockeysyte.com/season/1130'; TEAM='https://ilha.hockeysyte.com/team/993'; GAME23='https://ilha.hockeysyte.com/news/343'
PLAYERS={
 '14592':('TJ Lodge','https://ilha.hockeysyte.com/player/14592'), '14593':('Ben Karapandzic','https://ilha.hockeysyte.com/player/14593'),
 '14594':('Rowan Broderick','https://ilha.hockeysyte.com/player/14594'), '14595':('Odin Grantham','https://ilha.hockeysyte.com/player/14595'),
 '14596':('Ethan Huang','https://ilha.hockeysyte.com/player/14596'), '14597':('Rylee Ruwette','https://ilha.hockeysyte.com/player/14597'),
 '14598':('Safira Giveen','https://ilha.hockeysyte.com/player/14598'), '14599':('Harrison Kelleher','https://ilha.hockeysyte.com/player/14599'),
 '14600':('Thomas Halsted','https://ilha.hockeysyte.com/player/14600'), '14601':('Beau Mumford','https://ilha.hockeysyte.com/player/14601'),
 '14602':('Jasiah Mumford','https://ilha.hockeysyte.com/player/14602')}
ALIASES={'HARRISON KELLEHER':['HARRISON KELLEHER','HARRY KELLEHER']}
TEAMS={'QUEENSLAND':'QLD','QLD':'QLD','VICTORIA':'VIC','VIC':'VIC','SOUTH AUSTRALIA':'SA','SA':'SA','NEW SOUTH WALES':'NSW','NSW':'NSW','TASMANIA':'TAS','TAS':'TAS'}
NAMES={'QLD':'Queensland','VIC':'Victoria','SA':'South Australia','NSW':'New South Wales','TAS':'Tasmania'}
SA_GAMES={23:('QLD','SA'),42:('SA','NSW'),65:('TAS','SA'),108:('SA','VIC')}

def clean(s): return re.sub(r'\s+',' ',str(s or '')).strip()
def key(s): return re.sub(r'[^A-Z0-9%+/-]','',clean(s).upper())
def norm_team(s):
    u=clean(s).upper()
    if u in TEAMS:return TEAMS[u]
    for k,v in TEAMS.items():
        if len(k)>3 and re.search(r'\b'+re.escape(k)+r'\b',u): return v
    return None

def nval(s):
    s=clean(s).replace(',','')
    m=re.search(r'-?\d+(?:\.\d+)?',s)
    if not m:return None
    v=float(m.group()); return int(v) if v.is_integer() else v

def table_data(page):
    return page.locator('table').evaluate_all("""els => els.map(t => ({
      headers:[...t.querySelectorAll('thead th')].map(x=>x.innerText.trim()),
      rows:[...t.querySelectorAll('tbody tr')].map(r=>[...r.querySelectorAll('th,td')].map(x=>x.innerText.trim())),
      text:t.innerText
    }))""")

def load(page,url,label):
    page.goto(url,wait_until='domcontentloaded',timeout=90000)
    try: page.wait_for_load_state('networkidle',timeout=30000)
    except Exception: pass
    page.wait_for_timeout(3500)
    body=page.locator('body').inner_text()
    tbl=table_data(page)
    (DIAG/f'{label}.txt').write_text(body,encoding='utf-8')
    (DIAG/f'{label}-tables.json').write_text(json.dumps(tbl,indent=2),encoding='utf-8')
    page.screenshot(path=str(DIAG/f'{label}.png'),full_page=True)
    return {'body':body,'tables':tbl,'url':page.url,'title':page.title()}

def parse_standings(tbls):
    candidates=[]
    for t in tbls:
        hs=[key(h) for h in t['headers']]
        if not all(x in hs for x in ('GP','W','L')): continue
        def ix(*names):
            for name in names:
                if name in hs:return hs.index(name)
            return -1
        for row in t['rows']:
            team=next((norm_team(c) for c in row if norm_team(c)),None)
            if not team:continue
            def get(*names):
                i=ix(*names); return nval(row[i]) if 0<=i<len(row) else None
            candidates.append({'team':team,'name':NAMES[team],'gp':get('GP'),'w':get('W'),'l':get('L'),'pts':get('PTS','POINTS'),'gf':get('GF'),'ga':get('GA')})
    best={}
    for x in candidates:
        if x['gp'] is not None and (x['team'] not in best or x['gp']>=best[x['team']].get('gp',-1)):best[x['team']]=x
    rows=list(best.values())
    rows.sort(key=lambda x:(-(x.get('pts') or 0),-(x.get('w') or 0),-((x.get('gf') or 0)-(x.get('ga') or 0)),x['name']))
    return rows

def score_in(cells):
    for c in cells:
        m=re.search(r'(?<!\d)(\d{1,2})\s*[-–:]\s*(\d{1,2})(?!\d)',c)
        if m:return int(m.group(1)),int(m.group(2))
    return None

def parse_results(pages):
    found=[]
    for pg in pages:
      for t in pg['tables']:
        for row in t['rows']:
            teams=[]
            for c in row:
                tt=norm_team(c)
                if tt and tt not in teams:teams.append(tt)
            score=score_in(row)
            if score and len(teams)>=2:found.append({'home':teams[0],'away':teams[1],'homeScore':score[0],'awayScore':score[1]})
            # SA team Game Log omits "South Australia" because it is implicit.
            if score and len(teams)==1 and teams[0]!='SA':
                text=' '.join(row).upper(); opp=teams[0]
                if re.search(r'\bAT\b',text): found.append({'home':opp,'away':'SA','homeScore':score[0],'awayScore':score[1]})
                elif re.search(r'\bVS\b',text): found.append({'home':'SA','away':opp,'homeScore':score[0],'awayScore':score[1]})
      # article/body fallback: QLD/Queensland vs SA/South Australia around a score
      text=pg['body']
      for a,sa,sb,b in re.findall(r'(Queensland|Victoria|South Australia|New South Wales|Tasmania|QLD|VIC|SA|NSW|TAS)[^\n]{0,120}?(\d{1,2})\s*[-–:]\s*(\d{1,2})[^\n]{0,120}?(Queensland|Victoria|South Australia|New South Wales|Tasmania|QLD|VIC|SA|NSW|TAS)',text,re.I):
          aa,bb=norm_team(a),norm_team(b)
          if aa and bb and aa!=bb:found.append({'home':aa,'away':bb,'homeScore':int(sa),'awayScore':int(sb)})
    cleanout=[];seen=set()
    for r in found:
        k=(r['home'],r['away'],r['homeScore'],r['awayScore'])
        if k not in seen:cleanout.append(r);seen.add(k)
    return cleanout

def map_sa(results):
    mapped={}
    for gid,(home,away) in SA_GAMES.items():
        for r in results:
            if (r['home'],r['away'])==(home,away):mapped[str(gid)]={'homeScore':r['homeScore'],'awayScore':r['awayScore']};break
            if (r['home'],r['away'])==(away,home):mapped[str(gid)]={'homeScore':r['awayScore'],'awayScore':r['homeScore']};break
    return mapped

def parse_named_rows(tbls,display_name):
    wanted=ALIASES.get(display_name.upper(),[display_name.upper()]); matches=[]
    for t in tbls:
        hs=[clean(h) for h in t['headers']]
        for row in t['rows']:
            joined=' '.join(row).upper()
            if not any(n in joined for n in wanted):continue
            rec={}
            for i,c in enumerate(row):
                if i<len(hs) and hs[i]:rec[hs[i]]=clean(c)
            if rec:matches.append(rec)
    return matches

def compact_stats(rows):
    """Return useful numeric fields without assuming HockeySyte's exact header spelling."""
    if not rows:return {}
    aliases={'GP':['GP','GAMES','GAMES PLAYED'],'G':['G','GOAL','GOALS'],'A':['A','ASSIST','ASSISTS'],'PTS':['PTS','POINTS'],'PIM':['PIM','PM','PENALTY','PENALTY MINUTES'],
             'MP':['MP','MIN','MINUTES','MINUTES PLAYED'],'SA':['SA','SHOTS AGAINST'],'GA':['GA','GOALS AGAINST'],'GAA':['GAA'],'S':['S','SV','SAVES'],'SV%':['SV PCT','SV%','SAVE%','SAVE PCT']}
    out={}
    # Prefer the row with the most numeric content.
    row=max(rows,key=lambda r:sum(nval(v) is not None for v in r.values()))
    normalized={key(k):v for k,v in row.items()}
    for dest,names in aliases.items():
        for nm in names:
            kk=key(nm)
            if kk in normalized:
                v=nval(normalized[kk]);
                if v is not None:out[dest]=v
                break
    return out

def merge(old,new):
    out=dict(old or {})
    for k,v in (new or {}).items():
        if v not in (None,[],{}):out[k]=v
    return out

def main():
    old=json.loads(OUT.read_text()) if OUT.exists() else {}
    status={}; pages={}; player_pages={}
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--disable-dev-shm-usage'])
        ctx=browser.new_context(viewport={'width':1440,'height':1600},user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140 Safari/537.36')
        page=ctx.new_page()
        for label,url in [('season',SEASON),('team',TEAM),('game23',GAME23)]:
            try: pages[label]=load(page,url,label);status[label]='ok'
            except Exception as e: status[label]=f'error: {e}'
        for pid,(name,url) in PLAYERS.items():
            try: player_pages[pid]=load(page,url,f'player-{pid}');status[f'player-{pid}']='ok'
            except Exception as e: status[f'player-{pid}']=f'error: {e}'
        browser.close()
    all_tables=[t for pg in pages.values() for t in pg['tables']]
    standings=parse_standings(all_tables)
    results=parse_results(list(pages.values()))
    schedule=map_sa(results)
    pstats={}
    for pid,(name,url) in PLAYERS.items():
        rows=[]
        if pid in player_pages:rows += parse_named_rows(player_pages[pid]['tables'],name)
        rows += parse_named_rows(all_tables,name)
        stats=compact_stats(rows)
        pstats[pid]={'name':name,'url':url,'stats':stats}
    now=datetime.now(timezone.utc).isoformat(timespec='seconds')
    payload=dict(old)
    payload.update({'source':'HockeySyte','sourceLabel':'HockeySyte · automatic sync','updated':now,
                    'note':'Official HockeySyte data. Each section keeps its last-known-good value if a refresh cannot be verified.',
                    'syncStatus':status})
    if len(standings)>=5: payload['standings']=standings
    if results: payload['results']=results
    if schedule: payload['scheduleResults']=merge(old.get('scheduleResults',{}),schedule)
    # URLs are always safe to refresh; stats update independently per player.
    oldps=old.get('playerStats',{})
    merged={}
    for pid,item in pstats.items():
        prev=oldps.get(pid,{})
        merged[pid]={'name':item['name'],'url':item['url'],'stats':merge(prev.get('stats',{}),item['stats'])}
    payload['playerStats']=merged
    (DIAG/'sync-summary.json').write_text(json.dumps({'status':status,'parsedStandings':standings,'parsedResults':results,'parsedSchedule':schedule,'parsedPlayerStats':pstats},indent=2),encoding='utf-8')
    tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(payload,indent=2)+'\n');tmp.replace(OUT)
    print(f"standings={len(standings)} results={len(results)} SA_results={len(schedule)} player_pages={len(player_pages)} players_with_stats={sum(bool(x['stats']) for x in pstats.values())}")

if __name__=='__main__':
    try: main()
    except Exception:
        (DIAG/'fatal-error.txt').write_text(traceback.format_exc(),encoding='utf-8');raise
