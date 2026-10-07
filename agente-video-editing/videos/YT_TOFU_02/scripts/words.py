import json,sys
d=json.load(open('data/transcript2.json'))
W=[]
for seg in d['transcription']:
    for tk in seg['tokens']:
        t=tk['text']
        if t.startswith('[_') or t.strip()=='' : continue
        W.append((tk['offsets']['from']/1000.0, tk['offsets']['to']/1000.0, t))
if __name__=='__main__':
    a,b=float(sys.argv[1]),float(sys.argv[2])
    for s,e,t in W:
        if e<a or s>b: continue
        print(f"{s:8.2f} {e:8.2f}  {t!r}")
