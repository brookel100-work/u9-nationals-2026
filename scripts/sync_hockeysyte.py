#!/usr/bin/env python3
import json,re,sys
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright

SEASON='https://ilha.hockeysyte.com/season/1130'
TEAM='https://ilha.hockeysyte.com/team/993'
GAME23='https://ilha.hockeysyte.com/news/343'
OUT=Path(__file__).resolve().parents[1]/'live-data.json'
TEAMS={'QUEENSLAND':'QLD','QLD':'QLD','VICTORIA':'VIC','VIC':'VIC','SOUTH AUSTRALIA':'SA','SA':'SA','NEW SOUTH WALES':'NSW','NSW':'NSW','TASMANIA':'TAS','TAS':'TAS'}
NAMES={'QLD':'Queensland','VIC':'Victoria','SA':'South Australia','NSW':'New South Wales','TAS':'Tasmania'}
SA_GAMES={23:('QLD','SA'),42:('SA','NSW'),65:('TAS','SA'),108:('SA','VIC')}

def norm_team(s):
    s=re.sub(r'\s+',' ',str(s)).strip().upper()
    if s in TEAMS:return TEAMS[s]
    for k,v in TEAMS.items():
        if len(k)>3 and k in s:return v
    return None

def tables(page):
    return page.locator('table').evaluate_all("""els => els.map(t => ({
      headers:[...t.querySelectorAll('thead th')].map(x=>x.innerText.trim()),
      rows:[...t.querySelectorAll('tbody tr')].map(r=>[...r.querySelectorAll('th,td')].map(x=>x.innerText.trim()))
    }))""")

def ints(s): return [int(x) for x in re.findall(r'(?<!\d)\d{1,3}(?!\d)', str(s))]

def parse_standings(tbls):
    out=[]
    for t in tbls:
        hs=[re.sub(r'[^A-Z%+/-]','',h.upper()) for h in t['headers']]
        if not ('GP' in hs and 'W' in hs and 'L' in hs): continue
        def idx(name):
            try:return hs.index(name)
            except:return -1
        igp,iw,il,ipts,igf,iga=map(idx,['GP','W','L','PTS','GF','GA'])
        for row in t['rows']:
            team=None
            for c in row[:3]:
                team=norm_team(c)
                if team:break
            if not team:continue
            def val(i):
                if i<0 or i>=len(row):return 0
                a=ints(row[i]); return a[0] if a else 0
            out.append({'team':team,'name':NAMES[team],'gp':val(igp),'w':val(iw),'l':val(il),'pts':val(ipts),'gf':val(igf),'ga':val(iga)})
        if len({x['team'] for x in out})>=5:break
    # de-dupe and order by table order
    seen=set(); clean=[]
    for x in out:
        if x['team'] not in seen: clean.append(x);seen.add(x['team'])
    return clean

def parse_results(tbls, body):
    found=[]
    # Tables: find rows containing two known team names and a plausible score pair.
    for t in tbls:
        for row in t['rows']:
            joined=' | '.join(row)
            teams=[]
            for c in row:
                tt=norm_team(c)
                if tt and tt not in teams: teams.append(tt)
            if len(teams)<2: continue
            # Prefer a cell formatted score, then adjacent numeric cells.
            score=None
            for c in row:
                m=re.search(r'(?<!\d)(\d{1,2})\s*[-–:]\s*(\d{1,2})(?!\d)',c)
                if m: score=(int(m.group(1)),int(m.group(2)));break
            if score is None:
                nums=[]
                for c in row:
                    if re.fullmatch(r'\s*\d{1,2}\s*',c): nums.append(int(c.strip()))
                if len(nums)>=2: score=(nums[-2],nums[-1])
            if score:
                found.append({'home':teams[0],'away':teams[1],'homeScore':score[0],'awayScore':score[1]})
    # fallback on visible text patterns
    lines=[re.sub(r'\s+',' ',x).strip() for x in body.splitlines() if x.strip()]
    for line in lines:
        m=re.search(r'(Queensland|Victoria|South Australia|New South Wales|Tasmania|QLD|VIC|SA|NSW|TAS).*?(\d{1,2})\s*[-–:]\s*(\d{1,2}).*?(Queensland|Victoria|South Australia|New South Wales|Tasmania|QLD|VIC|SA|NSW|TAS)',line,re.I)
        if m:
            a,b=norm_team(m.group(1)),norm_team(m.group(4))
            if a and b and a!=b: found.append({'home':a,'away':b,'homeScore':int(m.group(2)),'awayScore':int(m.group(3))})
    # de-dupe
    clean=[];seen=set()
    for r in found:
        key=(r['home'],r['away'],r['homeScore'],r['awayScore'])
        if key not in seen:clean.append(r);seen.add(key)
    return clean

def map_sa(results):
    mapped={}
    for gid,(home,away) in SA_GAMES.items():
        for r in results:
            if r['home']==home and r['away']==away:
                mapped[str(gid)]={'homeScore':r['homeScore'],'awayScore':r['awayScore']};break
            if r['home']==away and r['away']==home:
                mapped[str(gid)]={'homeScore':r['awayScore'],'awayScore':r['homeScore']};break
    return mapped

def main():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1600})
        all_tables=[]; bodies=[]
        for url in (SEASON,TEAM,GAME23):
            page.goto(url,wait_until='networkidle',timeout=90000)
            page.wait_for_timeout(2500)
            all_tables += tables(page)
            bodies.append(page.locator('body').inner_text())
        browser.close()
    standings=parse_standings(all_tables)
    results=parse_results(all_tables,'\n'.join(bodies))
    if len(standings)<5:
        raise RuntimeError(f'Could not safely parse all five U9 standings teams (got {len(standings)}). Refusing to overwrite last-known-good data.')
    payload={
      'source':'HockeySyte','sourceLabel':'HockeySyte · automatic sync',
      'updated':datetime.now(timezone.utc).isoformat(timespec='seconds'),
      'note':'Automatically synced from the official 2026 Nationals HockeySyte pages.',
      'standings':standings,'results':results,'scheduleResults':map_sa(results)
    }
    tmp=OUT.with_suffix('.tmp');tmp.write_text(json.dumps(payload,indent=2)+"\n");tmp.replace(OUT)
    print(f"Synced {len(standings)} standings rows, {len(results)} result rows, {len(payload['scheduleResults'])} SA games")
if __name__=='__main__': main()
