"""Quest mod v9.1.0: reward rework, new Ch1 quests (GT Not Hard research, Greenhouse, Soul Crusher),
and rebalance notes on the existing GT Not Hard / My Mods quests."""
import base64, json, os, struct, uuid, collections, copy

R = '/home/claude/qjar/x/assets/gtnhaddonquests'
STAGES = {100, 102, 104, 106, 108}
TIERBAG_STAGE = {2: 102, 4: 100, 6: 104, 8: 104, 42: 106, 44: 108}
stats = collections.Counter()

def bag(dmg, n=1):
    return {"Count:3": n, "Damage:2": dmg, "OreDict:8": "", "id:8": "enhancedlootbags:lootbag"}

def item(i, dmg=0, n=1):
    return {"Count:3": n, "Damage:2": dmg, "OreDict:8": "", "id:8": i}

def items_of(q):
    out = []
    for r in q.get('rewards:9', {}).values():
        if r['rewardID:8'] == 'bq_standard:item':
            out += list(r['rewards:9'].values())
    return out

def choices_of(q):
    out = []
    for r in q.get('rewards:9', {}).values():
        if r['rewardID:8'] == 'bq_standard:choice':
            out += list(r['choices:9'].values())
    return out

def is_finale(q):
    return any(i['id:8'] == 'enhancedlootbags:lootbag' and i['Damage:2'] in (110, 111) for i in items_of(q))

def tier_bag(q):
    for i in items_of(q):
        if i['id:8'] == 'enhancedlootbags:lootbag' and i['Damage:2'] in TIERBAG_STAGE:
            return i
    return None

def stage_bag(q, tb):
    for i in choices_of(q):
        if i['id:8'] == 'enhancedlootbags:lootbag' and i['Damage:2'] in STAGES:
            return i['Damage:2']
    return TIERBAG_STAGE.get(tb['Damage:2'], 100) if tb else 100

def set_rewards(q, item_list, choice_list=None):
    rw = {}
    if item_list:
        rw["0:10"] = {"index:3": 0, "ignoreDisabled:1": 0, "rewardID:8": "bq_standard:item",
                      "rewards:9": {f"{k}:10": v for k, v in enumerate(item_list)}}
    if choice_list:
        n = len(rw)
        rw[f"{n}:10"] = {"index:3": n, "ignoreDisabled:1": 0, "rewardID:8": "bq_standard:choice",
                        "choices:9": {f"{k}:10": v for k, v in enumerate(choice_list)}}
    q['rewards:9'] = rw

def rework(q, row_end, nth):
    """nth: running count of normal quests in the chapter (every 5th gets a small choice)."""
    if is_finale(q):
        stats['finale'] += 1
        return
    tb = tier_bag(q)
    keep = [i for i in items_of(q) if i['id:8'] != 'enhancedlootbags:lootbag']
    base = keep + ([dict(tb, **{"Count:3": 1})] if tb else [])
    sb = stage_bag(q, tb)
    if row_end:
        set_rewards(q, base + [bag(sb + 1, 3)])
        stats['row_end'] += 1
        return
    choice = None
    if nth % 5 == 4:
        coin = next((dict(i) for i in choices_of(q) if i['id:8'].startswith('dreamcraft:Coin')), None)
        choice = [bag(sb)]
        if coin:
            coin['Count:3'] = max(1, coin['Count:3'] // 2)
            choice.append(coin)
        stats['seed_choice'] += 1
    set_rewards(q, base, choice)
    stats['normal'] += 1

def read_index(ch):
    rows = []
    for line in open(f'{R}/{ch}/index.tsv'):
        if line.startswith('#') or not line.strip():
            continue
        rows.append(line.rstrip('\n').split('\t'))
    return rows

def load(ch, f):
    return json.load(open(f'{R}/{ch}/quests/{f}'))

def save(ch, f, q):
    json.dump(q, open(f'{R}/{ch}/quests/{f}', 'w'), indent=2, ensure_ascii=False)

def desc_add(q, text):
    b = q['properties:10']['betterquesting:10']
    marker = '§cRebalanced§r'
    d = b['desc:8']
    if marker in d:
        d = d[:d.index('\n\n' + marker)] if ('\n\n' + marker) in d else d
    # put it before the Task line
    if '\n\n§aTask§r' in d:
        head, tail = d.split('\n\n§aTask§r', 1)
        b['desc:8'] = f"{head}\n\n{marker}: {text}\n\n§aTask§r{tail}"
    else:
        b['desc:8'] = f"{d}\n\n{marker}: {text}"

def set_desc(q, name, body, task):
    b = q['properties:10']['betterquesting:10']
    b['desc:8'] = f"§b{name}§r\n\n{body}\n\n§aTask§r: {task}"

# ------------------------------------------------------------------ rewards, every chapter
chapters = [l.split('\t')[0] for l in open(f'{R}/chapters.tsv') if not l.startswith('#') and l.strip()]
for ch in chapters:
    rows = read_index(ch)
    if ch == 'ch21-my-mods':
        for r in rows:
            q = load(ch, r[1]); q['rewards:9'] = {}; save(ch, r[1], q); stats['no_reward'] += 1
        continue
    quests = {r[1]: load(ch, r[1]) for r in rows}
    place = {r[1]: json.load(open(f'{R}/{ch}/placements/{r[2]}')) for r in rows}
    row_end = set()
    if ch == 'ch01-void-mining':
        groups = collections.OrderedDict()
        for r in rows:
            q = quests[r[1]]
            if not any(i['id:8'].startswith('gtneioreplugin') for i in items_of(q)):
                continue
            key = tuple((i['id:8'], i['Count:3']) for i in choices_of(q) if i['id:8'].startswith('dreamcraft'))
            groups.setdefault(key, []).append(r[1])
        for g in groups.values():
            row_end.add(g[-1])
    else:
        lanes = collections.defaultdict(list)
        for f, p in place.items():
            lanes[p['y:3']].append(f)
        for lane in lanes.values():
            last = max(lane, key=lambda f: place[f]['x:3'])
            if len(lane) > 1:
                row_end.add(last)
    nth = 0
    for r in rows:
        f = r[1]
        q = quests[f]
        fin = is_finale(q)
        rework(q, f in row_end, nth)
        if not fin and f not in row_end:
            nth += 1
        save(ch, f, q)

# ------------------------------------------------------------------ notes on existing quests
CH1 = 'ch01-void-mining'
notes = {
    '01-01.json': "An 11x11, 30-tall tower made in the Assembly Line after researching a Tier II Alien Artifact. Each mode needs its Singularity Module in an input bus (Ore first, then Dust, Ingot, Gem, Fluid, Pachinko, Ecosystem, Mod Item) and a high enough heating-coil core. Every run costs power and UU-Matter.",
    '01-07.json': "A 9x9, 30-tall tower made in the Assembly Line after researching a Tier I Alien Artifact. Singleblock machines only; an Array Module and the coil core set how many (16 to 64) and how high their tier. Each parallel costs a full machine's power.",
    '01-08.json': "A 9x9, 30-tall tower made in the Assembly Line after researching a Tier I Alien Artifact. Burns real fuel at 85% of the generators' efficiency, 1 amp per generator, no wireless mode. An Array Module and the coil core set how many generators (16 to 64).",
}
for f, t in notes.items():
    q = load(CH1, f); desc_add(q, t); save(CH1, f, q)

CH21 = 'ch21-my-mods'
notes21 = {
    'Seed Bags': "seed stats rise with the bag's stage (1/1/1 up to 6/6/6; Fortune bags double). Stage I-III seeds come unscanned. Rare Heirloom and Fortune Rare Heirloom are both 10/10/10.",
    'GT Not Hard: Singularity NEI': "Chaos, Origin and Singularity are now huge late-game towers unlocked with Alien Artifacts (space dungeon chests) and Ancient Books (dragon drops). See Chapter 1 and the Mod Guide.",
    'Singularity': "needs a Singularity Module, a coil core of Trinium or better, power and UU-Matter. Made in the Assembly Line.",
    'GTNH Greenhouse': "Harvest uses Distilled Water (Purified Water from ZPM) and Sewage, Pollination uses Mutagen, Growth is slow and uses fertilizer. Plants per slot go from 4 at LV to 32 at UIV. The mod also adds the Soul Crusher (Chapter 1).",
    'Breeding Greenhouse': "overclocks like GT now (4x power for 2x speed), and it needs an input hatch for its fluids.",
    'Seed Bed Hatch (LV)': "seed beds are made in the Assembler from LV to LuV and the Assembly Line from ZPM, each from the tier below.",
    'Rockbloom Seeds': "about 1 block per harvest, plus 1 for every 2 seed bed tiers above the Rockbloom's.",
    'Super Pattern Maker': "Blank Super Patterns are tiered HV to UMV: 10 recipes at HV, 50% more each tier. The * search unlocks at IV.",
    'Blank Super Pattern': "this quest now asks for an HV Blank Super Pattern, made in the Assembler from 8 AE2 blank patterns and HV parts.",
    'Super Pattern Terminal': "made in the Assembler with HV parts. Its tier slider stops at the best blank you carry.",
    'Maintaining Input Hatch (ME)': "now tiered: IV 3 slots, LuV 5, ZPM 7, UV 9. Made in the Assembler.",
    'Wildcard Pattern (NC edition)': "needs LuV parts to craft.",
    'Pattern Generator (NC edition)': "needs EV parts to craft.",
}
for r in read_index(CH21):
    q = load(CH21, r[1])
    name = q['properties:10']['betterquesting:10']['name:8']
    if name in notes21:
        desc_add(q, notes21[name])
        if name == 'Blank Super Pattern':
            for t in q['tasks:9'].values():
                for it in t.get('requiredItems:9', {}).values():
                    if it['id:8'] == 'superpatternmaker:super_pattern':
                        it['Damage:2'] = 3
        save(CH21, r[1], q)
        stats['note21'] += 1

# ------------------------------------------------------------------ new Ch1 quests
SEED = uuid.uuid5(uuid.NAMESPACE_URL, 'gtnhaddonquests/v9.1/ch01-rebalance')

def qid(key):
    u = uuid.uuid5(SEED, key)
    hi, lo = struct.unpack('>qq', u.bytes)
    return base64.urlsafe_b64encode(u.bytes).decode(), hi, lo

ids = {}
def existing_id(f):
    for r in read_index(CH1):
        if r[1] == f:
            hi, lo = struct.unpack('>qq', base64.urlsafe_b64decode(r[0]))
            return hi, lo

def task_have(it):
    return {"0:10": {"index:3": 0, "taskID:8": "bq_standard:retrieval", "autoConsume:1": 0, "consume:1": 0,
                     "groupDetect:1": 0, "ignoreNBT:1": 1, "partialMatch:1": 0, "requireOnlyOneItem:1": 0,
                     "requiredItems:9": {"0:10": it}}}

def task_check():
    return {"0:10": {"index:3": 0, "taskID:8": "bq_standard:checkbox"}}

NEW = [
    # key, file, x, y, name, icon, body, task(item or None), prereqs(keys or files), tierbag, row_end, mod
    ('art1', '01-60.json', 960, 380, 'Alien Artifact (Tier I)', item('gtnothard:material', 0),
     "Found in dungeon chests on the Moon, Mars, Phobos and Deimos. The first time anyone opens a chest in a space dimension it has a 1 in 4 chance to hold one. Research it in the Research Station to unlock the Chaos and Origin controllers and Array Module I.",
     item('gtnothard:material', 0), [], 42, False, 'gtnothard'),
    ('arr1', '01-61.json', 1000, 380, 'Array Module I', item('gtnothard:material', 20),
     "Goes in an input bus of Chaos or Origin and is never used up. With Naquadah Alloy coils it runs LV to EV machines or generators, 16 at a time. Modules II to IV each need the one before.",
     item('gtnothard:material', 20), ['art1'], 42, False, 'gtnothard'),
    ('art2', '01-62.json', 1040, 380, 'Alien Artifact (Tier II)', item('gtnothard:material', 1),
     "Found in dungeon chests on the asteroids, the gas giant moons and the inner planets. Unlocks the Singularity, Array Module II and the Void Ore module.",
     item('gtnothard:material', 1), ['art1'], 44, False, 'gtnothard'),
    ('sing1', '01-63.json', 1080, 380, 'Singularity Module: Void Ore', item('gtnothard:material', 30),
     "The first Singularity module. Void Ore needs a Trinium coil core and costs 1 L of UU-Matter per 16 ores. Every later module needs the one before it.",
     item('gtnothard:material', 30), ['art2'], 44, False, 'gtnothard'),
    ('art3', '01-64.json', 1120, 380, 'Alien Artifact (Tier III)', item('gtnothard:material', 2),
     "Found on the outer planets, around other stars and in the Amun-Ra systems. Unlocks Array Module III and the Void Dust and Void Ingot modules.",
     item('gtnothard:material', 2), ['art2'], 44, True, 'gtnothard'),
    ('word', '01-65.json', 960, 460, 'Ancient Word', item('gtnothard:material', 10),
     "Dragons have a 1 in 50 chance per kill to drop one, including kills in the Soul Crusher. 9 Words make a Line, 9 Lines a Paragraph, 9 Paragraphs a Page and 9 Pages a Book.",
     item('gtnothard:material', 10), [], 44, False, 'gtnothard'),
    ('book', '01-66.json', 1040, 460, 'Ancient Book', item('gtnothard:material', 14),
     "6,561 Ancient Words. Research it to unlock Array Module IV and the late Singularity modules (Gem, Fluid, Pachinko, Ecosystem, Mod Item). You will need Soul Crushers farming the dragon to get here.",
     item('gtnothard:material', 14), ['word'], 44, True, 'gtnothard'),
    ('gh', '01-70.json', 960, 560, 'Breeding Greenhouse', item('gregtech:gt.blockmachines', 17400),
     "Grows seeds in three modes. Harvest uses Distilled Water and MineFactory Sewage, Pollination uses Gendustry Mutagen, Growth is slow and uses fertilizer. It needs an input hatch for its fluids. Change mode with a screwdriver.",
     item('gregtech:gt.blockmachines', 17400), [], 4, False, 'gtnhgreenhouse'),
    ('bed', '01-71.json', 1000, 560, 'Seed Bed Hatch (LV)', item('gregtech:gt.blockmachines', 17401),
     "Made in the Assembler. Higher seed beds grow more plants per slot (4 at LV up to 32 at UIV), use less fluid and breed more reliably. From ZPM the greenhouse needs Purified Water; each grade adds 10% output.",
     item('gregtech:gt.blockmachines', 17401), ['gh'], 4, False, 'gtnhgreenhouse'),
    ('bedzpm', '01-72.json', 1040, 560, 'Seed Bed Hatch (ZPM)', item('gregtech:gt.blockmachines', 17407),
     "The first Assembly Line seed bed (research the LuV one). It needs Mana Glass and Void Metal, and the greenhouse switches to Purified Water.",
     item('gregtech:gt.blockmachines', 17407), ['bed'], 42, True, 'gtnhgreenhouse'),
    ('vessel1', '01-73.json', 960, 640, 'Basic Soul Vessel', item('gtnhgreenhouse:soul_vessel', 0),
     "Made on the Infusion Altar (HV). Keep it in your inventory and kill a Twilight Forest boss to capture its soul. A soul lasts 500 kills in the Soul Crusher.",
     item('gtnhgreenhouse:soul_vessel', 0), [], 6, False, 'gtnhgreenhouse'),
    ('crusher', '01-74.json', 1000, 640, 'Soul Crusher', item('gregtech:gt.blockmachines', 17412),
     "An 11x11, 15-tall caged arena that farms a captured boss soul. Each run is one kill with the boss's real loot. Summoning items go in an input bus, and a Looting sword makes kills faster. The captured boss floats inside as a hologram.",
     item('gregtech:gt.blockmachines', 17412), ['vessel1'], 6, False, 'gtnhgreenhouse'),
    ('vessel2', '01-75.json', 1040, 640, 'Advanced Soul Vessel', item('gtnhgreenhouse:soul_vessel', 1),
     "Made from a Dragon Egg, a Nether Star and all seven Twilight Forest trophies (farm them in the Soul Crusher). It catches the Wither and the Ender Dragon. Bring the dragon back with Draconic Evolution's resurrection ritual to catch it.",
     item('gtnhgreenhouse:soul_vessel', 1), ['crusher'], 8, False, 'gtnhgreenhouse'),
    ('rift', '01-76.json', 1080, 640, 'Rift Focus', item('gtnhgreenhouse:rift_focus', 0),
     "Use it as the focus of Blood Magic's Mark of the Falling Tower, in the End. The meteor opens a rift: an Ender Dragon and three Withers.",
     item('gtnhgreenhouse:rift_focus', 0), ['vessel2'], 42, False, 'gtnhgreenhouse'),
    ('vessel3', '01-77.json', 1120, 640, 'Draconic Soul Vessel', item('gtnhgreenhouse:soul_vessel', 2),
     "Drops when all four bosses from the rift are dead. It catches the Chaos Guardian, the hardest soul to farm.",
     item('gtnhgreenhouse:soul_vessel', 2), ['rift'], 44, True, 'gtnhgreenhouse'),
]
PRE_EXISTING = {'art1': ['01-07.json', '01-08.json'], 'art2': ['01-01.json']}

index_lines = open(f'{R}/{CH1}/index.tsv').read().rstrip('\n').split('\n')
for key, f, x, y, name, icon, body, task_item, pre, tb, rend, mod in NEW:
    b64, hi, lo = qid(key)
    ids[key] = (hi, lo)
for key, f, x, y, name, icon, body, task_item, pre, tb, rend, mod in NEW:
    hi, lo = ids[key]
    q = {"properties:10": {"betterquesting:10": {
        "autoClaim:1": 0, "globalShare:1": 0, "isMain:1": 0, "isSilent:1": 0, "lockedProgress:1": 0,
        "questLogic:8": "AND", "repeatTime:3": -1, "repeat_relative:1": 1, "simultaneous:1": 0,
        "snd_complete:8": "random.levelup", "snd_update:8": "random.levelup", "taskLogic:8": "AND",
        "visibility:8": "NORMAL", "name:8": name, "desc:8": "", "icon:10": icon}},
        "questIDHigh:4": hi, "questIDLow:4": lo, "tasks:9": task_have(task_item)}
    set_desc(q, name, body, "have one in your inventory. It is not consumed.")
    pr = {}
    for k, p in enumerate(pre):
        h, l = ids[p]
        pr[f"{k}:10"] = {"questIDHigh:4": h, "questIDLow:4": l}
    if pr:
        q["preRequisites:9"] = pr
    sb = TIERBAG_STAGE[tb]
    set_rewards(q, [bag(tb)] + ([bag(sb + 1, 3)] if rend else []))
    save(CH1, f, q)
    json.dump({"questIDHigh:4": hi, "questIDLow:4": lo, "sizeX:3": 24, "sizeY:3": 24, "x:3": x, "y:3": y},
              open(f'{R}/{CH1}/placements/{f}', 'w'), indent=2)
    b64 = qid(key)[0]
    line = f"{b64}\t{f}\t{f}\t{mod}"
    index_lines = [l for l in index_lines if f"\t{f}\t" not in l] + [line]
    stats['new'] += 1
open(f'{R}/{CH1}/index.tsv', 'w').write('\n'.join(index_lines) + '\n')

# Chaos / Origin need Artifact I, Singularity needs Artifact II
for key, files in PRE_EXISTING.items():
    h, l = ids[key]
    for f in files:
        q = load(CH1, f)
        pr = q.get('preRequisites:9', {})
        if not any(v['questIDHigh:4'] == h and v['questIDLow:4'] == l for v in pr.values()):
            pr[f"{len(pr)}:10"] = {"questIDHigh:4": h, "questIDLow:4": l}
        q['preRequisites:9'] = pr
        save(CH1, f, q)

# chapter description
ql = json.load(open(f'{R}/{CH1}/QuestLine.json'))
ql['properties:10']['betterquesting:10']['desc:8'] = (
    "Build Void Miners LV to IV and reach every planet from T0 to T10 for its planet block. On the right: "
    "the GT-Not-Hard research path (Alien Artifacts from space dungeons, Ancient Books from dragons), the "
    "Breeding Greenhouse and the Soul Crusher.")
json.dump(ql, open(f'{R}/{CH1}/QuestLine.json', 'w'), indent=2, ensure_ascii=False)
print(dict(stats))
