import json,os,sys,collections
R='/home/claude/qjar/x/assets/gtnhaddonquests'
def rew(q):
    out=[]
    for k,r in q.get('rewards:9',{}).items():
        rid=r['rewardID:8']
        if rid=='bq_standard:item':
            out.append(('item',[(i['id:8'],i['Damage:2'],i['Count:3']) for i in r['rewards:9'].values()]))
        elif rid=='bq_standard:choice':
            out.append(('choice',[(i['id:8'],i['Damage:2'],i['Count:3']) for i in r['choices:9'].values()]))
        else: out.append((rid,None))
    return out
ch=sys.argv[1]
for line in open(f'{R}/{ch}/index.tsv'):
    if line.startswith('#'):continue
    p=line.rstrip('\n').split('\t')
    q=json.load(open(f'{R}/{ch}/quests/{p[1]}'))
    pl=json.load(open(f'{R}/{ch}/placements/{p[2]}'))
    b=q['properties:10']['betterquesting:10']
    print(p[1],pl['x:3'],pl['y:3'],b['name:8'][:40],rew(q))
