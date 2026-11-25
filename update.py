import json, urllib.request, datetime, pathlib, time, calendar
ROOT=pathlib.Path(__file__).resolve().parent
cfg=json.loads((ROOT/'config.json').read_text())
def get(path):
    req=urllib.request.Request('https://fantasy.premierleague.com/api/'+path,headers={'User-Agent':'SmithmanInvitationalDashboard/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req,timeout=25) as r:return json.load(r)
        except Exception:
            if attempt==2:raise
            time.sleep(2*(attempt+1))
league=get(f"leagues-classic/{cfg['league_id']}/standings/?page_standings=1")
rows=list(league.get('standings',{}).get('results',[])); has_next=league.get('standings',{}).get('has_next',False);page=1
while has_next and page<30:
    page+=1;chunk=get(f"leagues-classic/{cfg['league_id']}/standings/?page_standings={page}").get('standings',{})
    rows+=chunk.get('results',[]);has_next=chunk.get('has_next',False)
bootstrap=get('bootstrap-static/');events=bootstrap.get('events',[])
finished={int(e['id']) for e in events if e.get('finished') and e.get('data_checked')}
months={int(e['id']):e['deadline_time'][:7] for e in events}
players=[]
for r in rows:
    entry=r.get('entry');hist=[]
    if entry:
        try:hist=get(f'entry/{entry}/history/').get('current',[])
        except Exception as ex:print('History unavailable',entry,str(ex))
    players.append({'id':entry,'manager':r.get('player_name',''),'team':r.get('entry_name',''),'rank':r.get('rank'),'total':r.get('total',0),'event_total':r.get('event_total',0),'history':[{'gw':x.get('event'),'points':x.get('points',0),'total':x.get('total_points',0)} for x in hist]})
# Only award weekly prizes for fully checked, finished gameweeks.
awards=[]
for gw in sorted(finished):
    scores=[(p,next((h['points'] for h in p['history'] if h['gw']==gw),None)) for p in players]
    scores=[(p,v) for p,v in scores if v is not None]
    if len(scores)!=len(players) or not scores:continue
    top=max(v for p,v in scores);winners=[p for p,v in scores if v==top]
    for w in winners:awards.append({'type':'Gameweek','period':str(gw),'id':w['id'],'amount':round(cfg['weekly_prize']/len(winners),4),'points':top})
# Group gameweeks by deadline calendar month. Change this if league uses a custom monthly schedule.
for month in sorted(set(months.values())):
    gws=[gw for gw,m in months.items() if m==month]
    if not gws or not set(gws).issubset(finished):continue
    totals=[]
    for p in players:
        values=[next((h['points'] for h in p['history'] if h['gw']==gw),None) for gw in gws]
        if any(v is None for v in values):break
        totals.append((p,sum(values)))
    if len(totals)!=len(players):continue
    top=max(v for p,v in totals);winners=[p for p,v in totals if v==top]
    for w in winners:awards.append({'type':'Month','period':month,'id':w['id'],'amount':round(cfg['monthly_prize']/len(winners),4),'points':top})
for p in players:
    p['earned']=round(sum(a['amount'] for a in awards if a['id']==p['id']),2)
output={'league':league.get('league',{}).get('name','Smithman Invitational'),'season':cfg['season'],'updated':datetime.datetime.now(datetime.timezone.utc).isoformat(),'gameweek':next((e['id'] for e in events if e.get('is_current')),None),'players':players,'awards':awards,'prize_config':cfg,'notice':'Provisional tracker. Cup, season-end and special prizes require validation; monthly awards use deadline calendar months.'}
(ROOT/'data/dashboard.json').write_text(json.dumps(output,indent=2,ensure_ascii=False))
print('Updated',len(players),'managers',len(awards),'awards')
