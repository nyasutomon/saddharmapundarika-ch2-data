from pathlib import Path
import json,csv,statistics,re,itertools
# Read the audited input definitions and accelerated scorer, stopping before full analysis.
s=(Path(__file__).parent/'audit.py').read_text();exec(s[:s.index('# Confirm identical row boundaries')])
rows=list(csv.DictReader((ROOT/'pair_checks.csv').open(encoding='utf-8-sig')));rowmap={(r['unit'],r['witness1'],r['witness2']):r for r in rows}
policies=['raw_nonblank','strip_all_editorial','raw_both_nonblank']
out=[];diagnostic_summary=[]
for u in UNITS.values():
 for x,y in itertools.combinations(pairlabels,2):
  if M[u][x][y]<=0:continue
  values={k:[] for k in policies}
  for b in B['legacy'][u]:
   va,vb=b['rows'][x],b['rows'][y]
   if va.strip()=='<LAC>' or vb.strip()=='<LAC>':continue
   aa,bb=va.split('\t'),vb.split('\t')
   if len(aa)!=len(bb):continue
   vv={k:[] for k in policies}
   for a,c in zip(aa,bb):
    if '<LAC' in a+c:continue
    ca,cc=clean_legacy(a),clean_legacy(c)
    v=sim(*sorted([ca,cc])) if ca or cc else 1
    if a.strip() or c.strip():vv['raw_nonblank'].append(v)
    if ca or cc:vv['raw_both_nonblank'].append(v)
    elif a.strip() and c.strip():vv['raw_both_nonblank'].append(1)
    # Conventional alternative: remove brackets but retain parenthetical contents.
    sa=re.sub(r'[\[\]\(\)]','',re.sub(r'\[[^\]]*[0-9][^\]]*\]','',a));sc=re.sub(r'[\[\]\(\)]','',re.sub(r'\[[^\]]*[0-9][^\]]*\]','',c))
    sa,sc=clean_legacy(sa),clean_legacy(sc)
    if sa or sc:vv['strip_all_editorial'].append(sim(*sorted([sa,sc])))
   for k in policies:
    if vv[k]:values[k].append(statistics.mean(vv[k]))
  for k in policies:
   v=statistics.mean(values[k])*100 if values[k] else 0
   out.append({'unit':u,'witness1':x,'witness2':y,'policy':k,'export_pct':M[u][x][y]*100,'recomputed_pct':v,'difference_pp':v-M[u][x][y]*100,'matches':abs(v-M[u][x][y]*100)<1e-8})
 for k in policies:
  rr=[r for r in out if r['unit']==u and r['policy']==k and not {r['witness1'],r['witness2']}&{'F','M'}]
  diagnostic_summary.append({'unit':u,'policy':k,'positive_pairs':len(rr),'matched':sum(r['matches'] for r in rr),'max_abs_diff_pp':max(abs(r['difference_pp']) for r in rr)})
# Fully inspect the rank export; numbers are correct but some order inversions are present.
rank_issues=[];rank_recomputed=[];ppt_rank=[]
for i,u in UNITS.items():
 f=next((MATRIX/('Matrix Data (1)-(3)' if i<=3 else 'G1-6_P1-P3_20260921')).glob(f'similarity_matrix-({i}) *.csv'));rr=list(csv.reader(f.open(encoding='utf-8-sig')))
 lex_columns=0
 for ci in range(1,len(rr[0]),2):
  x=rr[0][ci+1];seq=[(rank,row[ci],float(row[ci+1].rstrip('%'))) for rank,row in enumerate(rr[1:],1) if row[ci].strip()]
  for a,b in zip(seq,seq[1:]):
   if b[2]>a[2]+0.0051:rank_issues.append({'unit':u,'witness':x,'previous_rank':a[0],'previous_partner':a[1],'previous_pct':a[2],'following_rank':b[0],'following_partner':b[1],'following_pct':b[2]})
  strings=[row[ci+1] for row in rr[1:] if row[ci].strip()];lex_columns+=strings==sorted(strings,reverse=True)
  choices=sorted([(y,v*100) for y,v in M[u][x].items() if y not in {'KN','F','M',x} and v>0],key=lambda r:(-r[1],r[0]))
  for rank,(y,v) in enumerate(choices,1):rank_recomputed.append({'unit':u,'witness':x,'rank':rank,'partner':y,'similarity_pct':v})
 print('LEX',u,lex_columns,'of',33)
 if u not in {'Whole','Verse','Prose'}:
  rr=[r for r in rank_recomputed if r['unit']==u and r['witness']=='P3' and r['partner']=='T8'];ppt_rank+=rr
co=list(csv.DictReader((ROOT/'aggregate_coherence.csv').open(encoding='utf-8-sig')))
print('COHERENCE COUNTS',[(a,e,sum(r['aggregate']==a and not {r['witness1'],r['witness2']}&e for r in co)) for a in ['Verse','Prose','Whole'] for e in [set(),{'F'},{'F','M'}]])
print('COHERENCE LARGEST WITHOUT FM',sorted([r for r in co if not {r['witness1'],r['witness2']}&{'F','M'}],key=lambda r:-float(r['difference_outside_pp']))[:10])
print('LEGACY WORST WITHOUT FM')
for u in UNITS.values():
 rr=sorted([r for r in rows if r['unit']==u and float(r['export_pct'])>0 and not {r['witness1'],r['witness2']}&{'F','M'}],key=lambda r:-abs(float(r['legacy_strict_difference_pp'])))
 print(u,[(r['witness1'],r['witness2'],round(float(r['export_pct']),5),round(float(r['legacy_strict_pct']),5),r['legacy_unequal_blocks']) for r in rr[:2]])
print('PPT ranks',ppt_rank)
for name,data in [('blank_policy_checks.csv',out),('blank_policy_summary.csv',diagnostic_summary),('rank_order_inversions.csv',rank_issues),('numeric_ranks_excluding_F_M.csv',rank_recomputed),('P3_T8_rank_check.csv',ppt_rank)]:
 with (ROOT/name).open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(data[0]));w.writeheader();w.writerows(data)
print('BLANK POLICIES',diagnostic_summary)
