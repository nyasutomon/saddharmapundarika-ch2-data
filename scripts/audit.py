from pathlib import Path
import csv,json,re,itertools,hashlib,statistics,functools,ctypes,array,time,random
import os
REPO=Path(__file__).resolve().parents[1]
ROOT=REPO/'results/recomputed'
ROOT.mkdir(parents=True,exist_ok=True)
SOURCE=REPO/'work/legacy'
UTF=Path(os.environ['ASCJ_TRANSCRIPTIONS_DIR'])
MATRIX=REPO/'data/matrices/exported'
UNITS={1:'Verse',2:'Prose',3:'Whole',4:'G1',5:'G2',6:'G3',7:'G4',8:'G5',9:'G6',10:'Pr1',11:'Pr2',12:'Pr3'}
lib=ctypes.CDLL(os.environ['ASCJ_AUDIT_LIBRARY']);lib.lev.argtypes=[ctypes.c_void_p,ctypes.c_int,ctypes.c_void_p,ctypes.c_int];lib.lev.restype=ctypes.c_int
@functools.lru_cache(None)
def arr(s):
 a=array.array('I',map(ord,s));return a,a.buffer_info()[0]
@functools.lru_cache(None)
def sim(a,b):
 if a==b:return 1.
 x,xp=arr(a);y,yp=arr(b);d=lib.lev(xp,len(x),yp,len(y));assert d>=0
 return 1-d/max(len(a),len(b))
def ref(a,b):
 p=list(range(len(b)+1))
 for i,x in enumerate(a,1):
  q=[i]
  for j,y in enumerate(b,1):q.append(min(q[-1]+1,p[j]+1,p[j-1]+(x!=y)))
  p=q
 return p[-1]
for a,b,d in [('kitten','sitting',3),('buddhajñānaṃ','buddhayānaṃ',2),('','ś',1),('','',0)]:
 if a or b:assert abs(sim(a,b)-(1-d/max(len(a),len(b))))<1e-14
random.seed(20261010)
for n,m in [(8,5),(63,64),(67,65),(120,75)]:
 a=''.join(random.choices('abcśṭṃ',k=n));b=''.join(random.choices('abcśṭṃ',k=m));assert abs(sim(a,b)-(1-ref(a,b)/max(n,m)))<1e-14
print('Levenshtein reference checks passed',flush=True)
def parse(f,mode):
 text=f.read_bytes().decode('latin1' if mode=='legacy' else 'utf-8-sig');blocks=[];cur=None;marker=None
 for no,line in enumerate(text.splitlines(),1):
  if mode=='legacy': # splitlines() treats legacy NEL bytes as line breaks, so the byte newline is authoritative
   pass
 # preserve only LF physical lines in both encodings
 for no,line in enumerate(text.split('\n'),1):
  line=line.rstrip('\r');head='\xa4' if mode=='legacy' else '§'
  mt=re.match('^'+head+r'(\d+)',line)
  if mt:marker=int(mt[1]);continue
  if not line.strip():continue
  if '\t' not in line:raise ValueError((f.name,no,line[:80]))
  sig,v=line.split('\t',1);sig=sig.split()[0]
  if sig=='KN':cur={'ord':len(blocks)+1,'marker':marker,'rows':{},'lines':{}};blocks.append(cur);marker=None
  if cur is None:raise ValueError(('no KN start',f.name,no))
  if sig in cur['rows']:raise ValueError(('duplicate witness',f.name,no,sig))
  cur['rows'][sig]=v;cur['lines'][sig]=no
 return blocks
@functools.lru_cache(None)
def clean_legacy(t):
 t=t.replace("'",'').replace('"','');t=re.sub(r'\([^)]*\)','',t);t=re.sub(r'\[[^\]]*[0-9][^\]]*\]','',t)
 return re.sub(r'[ \t\r\n0-9\[\]\(\)\-\*\.,/:;?!\xa2\xa3\xaa\xc1\xca]','',t)
@functools.lru_cache(None)
def clean_utf(t):
 t=t.replace("'",'').replace('"','');t=re.sub(r'\([^)]*\)','',t);t=re.sub(r'\[[^\]]*[0-9][^\]]*\]','',t)
 return re.sub(r'[ \t\r\n0-9\[\]\(\)\-\*\.,/:;?!¢£™|\u00a0]','',t)
B={'legacy':{},'unicode':{}};M={};inventory=[];pairlabels=None;rank_differences=[]
for i,u in UNITS.items():
 for mode,base in [('legacy',SOURCE),('unicode',UTF)]:
  f=next(base.glob(f'({i}) *.txt'));bb=parse(f,mode);B[mode][u]=bb
  inventory.append({'unit':u,'mode':mode,'file':f.name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'blocks':len(bb),'all_rows_34':all(len(b['rows'])==34 for b in bb)})
 f=next((MATRIX/('Matrix Data (1)-(3)' if i<=3 else 'G1-6_P1-P3_20260921')).glob(f'correlation_matrix-({i}) *.csv'))
 r=list(csv.reader(f.open(encoding='utf-8-sig',newline='')));labels=r[0][1:];m={q[0]:dict(zip(labels,map(float,q[1:]))) for q in r[1:]};M[u]=m
 assert set(m)==set(labels) and len(labels)==34
 assert all(abs(m[x][y]-m[y][x])<1e-12 for x in labels for y in labels)
 assert all(0<=v<=1 for q in m.values() for v in q.values())
 if pairlabels is None:pairlabels=[x for x in labels if x!='KN']
 assert pairlabels==[x for x in labels if x!='KN']
 rf=f.with_name(f.name.replace('correlation_matrix','similarity_matrix'));rr=list(csv.reader(rf.open(encoding='utf-8-sig',newline='')))
 rankissues=[];entries=0
 for ci in range(1,len(rr[0]),2):
  x=rr[0][ci+1];prev=1.1;seen=set()
  for row in rr[1:]:
   if ci+1>=len(row) or not row[ci].strip():continue
   y=row[ci].strip();v=float(row[ci+1].strip().rstrip('%'))/100;entries+=1
   if y not in m[x] or y==x or y in seen or v>prev+0.000051:rankissues.append([x,y,'name/order'])
   if abs(v-m[x][y])>0.000051:rankissues.append([x,y,'value',v,m[x][y]])
   seen.add(y);prev=v
  if seen!={y for y in m if y not in {x,'KN'}}:rankissues.append([x,'','missing rank rows',sorted(set(m)-{x,'KN'}-seen)])
 rank_differences.append({'unit':u,'rank_entries':entries,'issues':rankissues})
 print(u,'blocks',len(B['legacy'][u]),'rank issues',len(rankissues),flush=True)
# Confirm identical row boundaries and map subdivision payloads to whole chapter.
correspondence=[]
for u in UNITS.values():
 la,un=B['legacy'][u],B['unicode'][u];assert len(la)==len(un)
 assert all(list(x['rows'])==list(y['rows']) and all(x['rows'][z].count('\t')==y['rows'][z].count('\t') for z in x['rows']) for x,y in zip(la,un))
for mode in B:
 lookup={}
 for b in B[mode]['Whole']:
  key=tuple(sorted(b['rows'].items()));lookup.setdefault(key,[]).append(b['ord'])
 for u in ['Verse','Prose']:
  blocks=B[mode][u]
  for b in blocks:
   candidates=lookup.get(tuple(sorted(b['rows'].items())),[])
   if len(candidates)!=1:raise ValueError(('whole match',mode,u,b['ord'],candidates))
   b['whole']=candidates[0]
  correspondence.append({'mode':mode,'unit':u,'blocks':len(blocks),'identical_to_whole':True,'whole_indices':[b['whole'] for b in blocks]})
 for u,parent,lo,hi in [('G1','Verse',0,14),('G2','Verse',14,42),('G3','Verse',42,58),('G4','Verse',58,74),('G5','Verse',74,82),('G6','Verse',82,300),('Pr1','Prose',0,22),('Pr2','Prose',22,56),('Pr3','Prose',56,159)]:
  blocks=B[mode][u];cleaner=clean_legacy if mode=='legacy' else clean_utf;changed=0
  for a,b in zip(blocks,B[mode][parent][lo:hi]):
   assert set(a['rows'])==set(b['rows'])
   for z in a['rows']:
    va,vb=a['rows'][z],b['rows'][z]
    assert va.count('\t')==vb.count('\t') and all(cleaner(x)==cleaner(y) for x,y in zip(va.split('\t'),vb.split('\t')))
    changed+=va!=vb
   a['whole']=b['whole']
  correspondence.append({'mode':mode,'unit':u,'blocks':len(blocks),'identical_to_whole':changed==0,'changed_whitespace_rows':changed,'clean_fields_identical':True,'whole_indices':[b['whole'] for b in blocks]})
# UTF and legacy mappings must identify the same chapter positions.
assert all([b.get('whole',b['ord']) for b in B['legacy'][u]]==[b.get('whole',b['ord']) for b in B['unicode'][u]] for u in UNITS.values())
PAIRS=list(itertools.combinations(pairlabels,2));assert len(PAIRS)==528
# Policy: exclude a wholly lost row and physically lost corresponding fields; keep one-sided blanks.
# On unequal field counts, strict mode makes no score. Zip is a separately labelled diagnostic.
cache={};unequal=[];start=time.monotonic()
for mode,cleaner in [('legacy',clean_legacy),('unicode',clean_utf)]:
 for bi,b in enumerate(B[mode]['Whole']):
  for x,y in PAIRS:
   va,vb=b['rows'][x],b['rows'][y]
   aa,bb=va.split('\t'),vb.split('\t');bad=len(aa)!=len(bb)
   full_lac=va.strip()=='<LAC>' or vb.strip()=='<LAC>'
   if full_lac:cache[mode,b['ord'],x,y]=(None,None,None,0,0,0,False,0);continue
   if bad and mode=='legacy':unequal.append([b['ord'],b['marker'],x,y,len(aa),len(bb),b['lines'][x],b['lines'][y]])
   vals=[];both=0;ones=0;lost=0
   for a,c in zip(aa,bb):
    if '<LAC' in a+c:lost+=1;continue
    a,c=cleaner(a),cleaner(c)
    if not(a or c):both+=1;continue
    ones+=not a or not c;vals.append(sim(*sorted([a,c])))
   v=statistics.mean(vals) if vals else None
   vbth=(sum(vals)+both)/(len(vals)+both) if vals or both else None
   cache[mode,b['ord'],x,y]=(v if not bad else None,v,vbth,len(vals) if not bad else 0,len(vals),ones,bad,both)
  if (bi+1)%100==0:print(mode,bi+1,'elapsed',round(time.monotonic()-start,1),'scores',sim.cache_info(),flush=True)
results=[];summaries=[]
for u in UNITS.values():
 ids=[b.get('whole',b['ord']) for b in B['legacy'][u]]
 for x,y in PAIRS:
  out={'unit':u,'witness1':x,'witness2':y,'export_pct':M[u][x][y]*100}
  for mode in ['legacy','unicode']:
   rs=[cache[mode,k,x,y] for k in ids]
   for policy,index in [('strict',0),('zip_diagnostic',1),('both_blank_counted',2)]:
    vals=[r[index] for r in rs if r[index] is not None];v=statistics.mean(vals)*100 if vals else 0
    out[f'{mode}_{policy}_pct']=v;out[f'{mode}_{policy}_difference_pp']=v-out['export_pct'];out[f'{mode}_{policy}_matches']=abs(v-out['export_pct'])<1e-8
   out[f'{mode}_retained_blocks']=sum(r[0] is not None for r in rs);out[f'{mode}_retained_fields']=sum(r[3] for r in rs);out[f'{mode}_unequal_blocks']=sum(r[6] for r in rs);out[f'{mode}_one_empty_fields']=sum(r[5] for r in rs);out[f'{mode}_both_empty_fields']=sum(r[7] for r in rs)
  results.append(out)
 for selection,exclude in [('all',set()),('without_F',{'F'}),('without_F_M',{'F','M'})]:
  rr=[r for r in results if r['unit']==u and not({r['witness1'],r['witness2']}&exclude)]
  item={'unit':u,'selection':selection,'pairs':len(rr),'positive_exports':sum(r['export_pct']>0 for r in rr),'blocks':len(ids)}
  for mode in ['legacy','unicode']:
   for policy in ['strict','zip_diagnostic','both_blank_counted']:
    item[f'{mode}_{policy}_all_match']=sum(r[f'{mode}_{policy}_matches'] for r in rr)
    positive=[r for r in rr if r['export_pct']>0]
    item[f'{mode}_{policy}_positive_match']=sum(r[f'{mode}_{policy}_matches'] for r in positive)
    item[f'{mode}_{policy}_max_difference_pp']=max(abs(r[f'{mode}_{policy}_difference_pp']) for r in positive) if positive else 0
  summaries.append(item)
# Aggregation coherence using known row payload matches, without relying on the reconstructed policy.
coherence=[]
for aggregate,children in [('Verse',['G1','G2','G3','G4','G5','G6']),('Prose',['Pr1','Pr2','Pr3']),('Whole',['Verse','Prose'])]:
 for x,y in PAIRS:
  vs=[M[k][x][y]*100 for k in children if M[k][x][y]>0];t=M[aggregate][x][y]*100
  if vs and t>0 and (t<min(vs)-1e-8 or t>max(vs)+1e-8):coherence.append({'aggregate':aggregate,'witness1':x,'witness2':y,'aggregate_pct':t,'subunit_min_pct':min(vs),'subunit_max_pct':max(vs),'difference_outside_pp':max(min(vs)-t,t-max(vs))})
# Aggregate evidence: group statistics and the G3/G5 common population / G5 shared masks.
N=[x for x in pairlabels if x not in {'D1','D2','D3','O','F','M'}];groupstats=[]
for u in UNITS.values():
 for group,ps in [('N-N',itertools.combinations(N,2)),('O-N',(('O',x) for x in N)),('D-N',((d,x) for d in ['D1','D2','D3'] for x in N))]:
  ps=list(ps)
  for mode in ['export','legacy','unicode']:
   vv=[]
   for x,y in ps:
    if not M[u][x][y]>0:continue
    if mode=='export':v=M[u][x][y]*100
    else:
     r=next(r for r in results if r['unit']==u and {r['witness1'],r['witness2']}=={x,y});v=r[f'{mode}_strict_pct']
    vv.append(v)
   groupstats.append({'unit':u,'group':group,'basis':mode,'pairs':len(vv),'min':min(vv) if vv else None,'max':max(vv) if vv else None,'median':statistics.median(vv) if vv else None})
common=[(x,y) for x,y in PAIRS if M['G3'][x][y]>0 and M['G5'][x][y]>0];assert len(common)==378
sensitivity=[]
def calc_line(b,x,y,mode,method,mask):
 cleaner=clean_legacy if mode=='legacy' else clean_utf
 aa,bb=b['rows'][x].split('\t'),b['rows'][y].split('\t');assert len(aa)==len(bb)
 vals=[]
 for j,(a,c) in enumerate(zip(aa,bb)):
  if j in mask or '<LAC' in a+c:continue
  a,c=cleaner(a),cleaner(c)
  if a or c:vals.append((a,c,sim(*sorted([a,c])),max(len(a),len(c))))
 if not vals:return None,0
 if method=='equal':v=statistics.mean(z[2] for z in vals)
 elif method=='length':v=sum(z[2]*z[3] for z in vals)/sum(z[3] for z in vals)
 else:v=sim(*sorted([''.join(z[0] for z in vals),''.join(z[1] for z in vals)]))
 return v*100,len(vals)
for mode in ['legacy','unicode']:
 for method in ['equal','length','joined']:
  means={}
  for u in ['G3','G5']:
   vals=[statistics.mean(calc_line(b,x,y,mode,method,set())[0] for b in B[mode][u]) for x,y in common];means[u]=vals
  sensitivity.append({'mode':mode,'method':method,'pairs':len(common),'G3_mean':statistics.mean(means['G3']),'G5_mean':statistics.mean(means['G5']),'difference_pp':statistics.mean(means['G5'])-statistics.mean(means['G3']),'G5_lower_pairs':sum(c<a for a,c in zip(means['G3'],means['G5']))})
tri=[]
for mode in ['legacy','unicode']:
 for masktype in ['pairwise','shared_N3_lacuna']:
  for method in ['equal','length','joined']:
   for x,y in [('P3','T8'),('P3','N3'),('T8','N3'),('P3','A3'),('P3','C2'),('P3','A2'),('P3','C1')]:
    vals=[];fields=0
    for b in B[mode]['G5']:
     mask={j for z in ['P3','T8','N3'] for j,v in enumerate(b['rows'][z].split('\t')) if '<LAC' in v} if masktype=='shared_N3_lacuna' else set()
     v,n=calc_line(b,x,y,mode,method,mask);assert v is not None;vals.append(v);fields+=n
    tri.append({'mode':mode,'mask':masktype,'method':method,'witness1':x,'witness2':y,'blocks':len(vals),'fields':fields,'score_pct':statistics.mean(vals)})
def write(name,rows):
 if not rows:return
 with (ROOT/name).open('w',newline='',encoding='utf-8-sig') as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
write('pair_checks.csv',results);write('unit_summary.csv',summaries);write('aggregate_coherence.csv',coherence);write('group_statistics.csv',groupstats);write('G3_G5_sensitivity.csv',sensitivity);write('G5_shared_mask.csv',tri)
with (ROOT/'unequal_fields.csv').open('w',newline='',encoding='utf-8-sig') as f:w=csv.writer(f);w.writerow(['whole_block','marker','witness1','witness2','fields1','fields2','line1','line2']);w.writerows(unequal)
(ROOT/'source_correspondence.json').write_text(json.dumps(correspondence,ensure_ascii=False,indent=2));(ROOT/'reconstruction_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2));(ROOT/'rank_checks.json').write_text(json.dumps(rank_differences,ensure_ascii=False,indent=2))
summary={'unit_summary':[r for r in summaries if r['selection']=='without_F_M'],'coherence_counts':{k:sum(r['aggregate']==k for r in coherence) for k in ['Verse','Prose','Whole']},'unequal_usable_whole_blocks':sorted(set(r[0] for r in unequal)),'G3_G5_sensitivity':sensitivity,'cache':str(sim.cache_info()),'elapsed':time.monotonic()-start}
(ROOT/'audit_summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
