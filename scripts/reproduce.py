"""Verify the release, restore documented legacy units, and repeat the audit.

Python 3.10+ standard library and a local C compiler are required.
No network access, account credentials, or original author's local paths are used.
"""
from pathlib import Path
import argparse,csv,gzip,hashlib,json,math,os,shutil,subprocess,sys
REPO=Path(__file__).resolve().parents[1]
def digest(data):return hashlib.sha256(data).hexdigest()

def verify_release(transcriptions):
    for item in json.loads((REPO/'metadata/input_manifest.json').read_text(encoding='utf-8')):
        source=(transcriptions/Path(item['path']).name) if item['path'].startswith('data/transcriptions/') else (REPO/item['path'])
        if digest(source.read_bytes())!=item['sha256']:
            raise ValueError('Input checksum mismatch: '+item['path'])
    print('Verified 24 public matrix exports and 12 externally supplied private UTF8 inputs.',flush=True)

def restore_legacy(transcriptions,annotations):
    mapping=json.loads((REPO/'data/encoding/legacy_character_map.json').read_text(encoding='utf-8'))
    dest=REPO/'work/legacy';dest.mkdir(parents=True,exist_ok=True)
    count=0
    for file in sorted(annotations.glob('*-legacy-spans.json.gz')):
        obj=json.loads(gzip.decompress(file.read_bytes()))
        rawutf=(transcriptions/obj['utf8_file']).read_bytes()
        if digest(rawutf)!=obj['utf8_sha256']:raise ValueError('UTF8 input mismatch')
        text=rawutf.decode('utf-8');chunks=[];pos=0
        for offset,length,oldhex in obj['spans']:
            if offset<pos or text[offset:offset+length]!=mapping[oldhex]:
                raise ValueError('Encoding annotation mismatch: '+obj['unit'])
            chunks.append(text[pos:offset].encode('ascii'));chunks.append(bytes([int(oldhex,16)]));pos=offset+length
        chunks.append(text[pos:].encode('ascii'));data=b''.join(chunks)
        if digest(data)!=obj['legacy_sha256']:raise ValueError('Restored legacy checksum mismatch')
        (dest/obj['legacy_file']).write_bytes(data);count+=1
    if count!=12:raise ValueError('Expected 12 encoding annotations')
    print('Restored all 12 original font-unit inputs; all legacy SHA256 values match.',flush=True)

def compile_scorer():
    compiler=os.environ.get('CC') or shutil.which('cc') or shutil.which('clang') or shutil.which('gcc')
    if not compiler:raise RuntimeError('A local C compiler is required (cc, clang or gcc).')
    dest=REPO/'work';dest.mkdir(exist_ok=True)
    lib=dest/('lev.dylib' if sys.platform=='darwin' else 'lev.so')
    flags=['-dynamiclib'] if sys.platform=='darwin' else ['-shared','-fPIC']
    subprocess.run([compiler,'-O3',*flags,str(REPO/'scripts/lev.c'),'-o',str(lib)],check=True)
    return lib

def compare_reference():
    reference=REPO/'results/reference';new=REPO/'results/recomputed'
    checked=0
    for file in sorted(reference.glob('*.csv')):
        with file.open(encoding='utf-8-sig',newline='') as f:a=list(csv.reader(f))
        with (new/file.name).open(encoding='utf-8-sig',newline='') as f:b=list(csv.reader(f))
        if len(a)!=len(b) or a[0]!=b[0]:raise ValueError('CSV shape mismatch: '+file.name)
        for rowno,(x,y) in enumerate(zip(a,b),1):
            if len(x)!=len(y):raise ValueError('CSV column mismatch')
            for left,right in zip(x,y):
                if left==right:continue
                try:equal=math.isclose(float(left),float(right),rel_tol=0,abs_tol=1e-8)
                except ValueError:equal=False
                if not equal:raise ValueError(f'Reference mismatch: {file.name} row {rowno}')
        checked+=1
    for file in reference.glob('*.json'):
        if json.loads(file.read_text(encoding='utf-8'))!=json.loads((new/file.name).read_text(encoding='utf-8')):
            raise ValueError('JSON reference mismatch: '+file.name)
    print(f'All {checked} reference CSV files and all reference JSON files reproduced.',flush=True)
    print('This repeats the audit, not the original production program. Ten export units remain unresolved.',flush=True)

def main():
    parser=argparse.ArgumentParser(description='Repeat the numerical audit using lawfully obtained private SMSR II inputs. Transcriptions and text-specific annotations are not distributed.')
    parser.add_argument('--transcriptions-dir',type=Path,help='External private folder containing the 12 matching UTF8 inputs')
    parser.add_argument('--encoding-dir',type=Path,help='External private folder containing the 12 matching legacy-spans.json.gz annotations')
    parser.add_argument('--check-inputs-only',action='store_true',help='Validate and privately restore inputs, without running the audit')
    args=parser.parse_args()
    if args.transcriptions_dir is None or args.encoding_dir is None:
        parser.error('SMSR II inputs are excluded. Supply --transcriptions-dir and --encoding-dir from lawfully obtained private copies; no text is downloaded.')
    transcriptions=args.transcriptions_dir.expanduser().resolve()
    annotations=args.encoding_dir.expanduser().resolve()
    for folder in [transcriptions,annotations]:
        if not folder.is_dir():parser.error('Private input directory does not exist: '+str(folder))
        if folder==REPO or REPO in folder.parents:
            parser.error('Keep private inputs outside this public repository.')
    verify_release(transcriptions);restore_legacy(transcriptions,annotations)
    if args.check_inputs_only:return
    library=compile_scorer()
    env=dict(os.environ);env['ASCJ_AUDIT_LIBRARY']=str(library);env['ASCJ_TRANSCRIPTIONS_DIR']=str(transcriptions)
    for script in ['audit.py','diagnostics.py']:
        log=REPO/'work'/f'{script[:-3]}.log'
        with log.open('w',encoding='utf-8') as f:
            run=subprocess.run([sys.executable,str(REPO/'scripts'/script)],env=env,stdout=f,stderr=subprocess.STDOUT)
        if run.returncode:
            print(log.read_text(encoding='utf-8'),file=sys.stderr)
            raise RuntimeError('Audit failed; see '+log.name)
    compare_reference()
if __name__=='__main__':main()
