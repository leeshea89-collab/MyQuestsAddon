"""Quest mod v9.3.0: new Chapter 23 "Planetary Exploitation" for the Planetary Exploiter mod.

- Machine row: the guide, the controller, the Modification Hatch, fuel and spark plugs, the tier 2 and tier 3 rings.
- One quest per planet (the same 43 as Chapter 1), in a lane per planet tier. Each quest asks you to visit the
  planet AND hand in 128 stacks (8,192) of its Planet Dust (planetaryexploiter:planet_dust, meta = planet index).
  The Overworld skips the visit (you live there); End Asteroids is visited through The End (same dimension).
  Reward: the planet block plus the tier bag. Deep Dark is the legendary finale.
- Every quest is gated by the mod id planetaryexploiter (4th index column), so the chapter is empty without the mod.
- Chapter 1 is left as it is (the user disables it in game).

Rewards follow 9.2.0 (tier bag; every 5th normal quest a small choice; last quest of a lane tier bag + 3 Fortune
seed bags + an Iridium coin; finale Fortune Rare Heirloom + GTNH bag 14 + 3 Iridium coins).
Run from the repo root: python3 tools/add_v930.py
"""
import base64, json, os, struct, uuid

R = os.path.join(os.path.dirname(__file__), '..', 'jar-contents', 'assets', 'gtnhaddonquests')
CH = 'ch23-planetary-exploitation'
MOD = 'planetaryexploiter'
SEED = uuid.uuid5(uuid.NAMESPACE_URL, 'gtnhaddonquests/v9.3/ch23-planetary-exploitation')
TIERBAG = {0: 2, 1: 4, 2: 6, 3: 8, 4: 42, 5: 44, 6: 44}
TIERBAG_STAGE = {2: 102, 4: 100, 6: 104, 8: 104, 42: 106, 44: 108}
IRIDIUM = 'fairplay:CoinIV'
GT = 'gregtech:gt.blockmachines'
DUST = 'planetaryexploiter:planet_dust'
CONTROLLER, MOD_HATCH = 31774, 31775
STACKS = 128

# meta order of ItemPlanetDust.PLANETS: (abbr, name, dimension id or None, planet tier, flavour)
PLANETS = [
    ('Ow', 'Overworld', None, 0, 'Home.'), ('Ne', 'Nether', -1, 0, 'Fire and brimstone.'),
    ('TF', 'Twilight Forest', 7, 0, 'Forever dusk.'), ('ED', 'The End', 1, 0, 'Where the dragon sleeps.'),
    ('EA', 'End Asteroids', 1, 0, 'Rocks drifting far out from the End island.'),
    ('Eg', 'Toxic Everglades', 227, 0, 'Poisoned swamps.'), ('Mo', 'Moon', 28, 1, 'Our first step off the world.'),
    ('De', 'Deimos', 40, 2, "Mars's smaller moon."), ('Ma', 'Mars', 29, 2, 'The red planet.'),
    ('Ph', 'Phobos', 38, 2, "Mars's larger moon."), ('As', 'Asteroid Belt', 30, 3, 'Rubble between Mars and Jupiter.'),
    ('Ca', 'Callisto', 45, 3, "Jupiter's cratered moon."), ('Ce', 'Ceres', 42, 3, 'The dwarf planet in the belt.'),
    ('Eu', 'Europa', 35, 3, 'Ice over a hidden ocean.'), ('Ga', 'Ganymede', 43, 3, 'The largest moon.'),
    ('Rb', 'Ross 128 b', 64, 3, 'A world around another star.'), ('Io', 'Io', 36, 4, 'Volcanoes everywhere.'),
    ('Me', 'Mercury', 37, 4, 'Scorched by the sun.'), ('Ve', 'Venus', 39, 4, 'Crushing acid clouds.'),
    ('En', 'Enceladus', 41, 5, "Saturn's icy geysers."), ('Mi', 'Miranda', 86, 5, "Uranus's patchwork moon."),
    ('Ob', 'Oberon', 46, 5, "Uranus's outer moon."), ('Ti', 'Titan', 44, 5, 'Methane lakes under orange skies.'),
    ('Ra', 'Ross 128 ba', 63, 5, "Ross 128 b's moon."), ('Pr', 'Proteus', 47, 6, "Neptune's dark moon."),
    ('Tr', 'Triton', 48, 6, "Neptune's backwards moon."), ('Ha', 'Haumea', 83, 7, 'A spinning egg of ice.'),
    ('KB', 'Kuiper Belt', 33, 7, 'The frozen edge of the system.'), ('MM', 'Makemake', 25, 7, 'A far dwarf planet.'),
    ('Pl', 'Pluto', 49, 7, 'Small, cold and far.'), ('BC', 'Barnard C', 32, 8, "Barnard's Star, world C."),
    ('BE', 'Barnard E', 81, 8, "Barnard's Star, world E."), ('BF', 'Barnard F', 82, 8, "Barnard's Star, world F."),
    ('CB', 'Alpha Centauri Bb', 31, 8, 'Our nearest neighbour star.'), ('TE', 'Tau Ceti E', 85, 8, 'A sun-like star.'),
    ('VB', 'Vega B', 84, 8, 'Around bright Vega.'), ('An', 'Anubis', 92, 9, 'Amun-Ra system.'),
    ('Ho', 'Horus', 93, 9, 'Amun-Ra system.'), ('Mh', 'Maahes', 91, 9, 'Amun-Ra system.'),
    ('MB', 'Mehen Belt', 95, 9, 'Amun-Ra asteroid belt.'), ('Np', 'Neper', 90, 9, 'Amun-Ra system.'),
    ('Se', 'Seth', 94, 9, 'Amun-Ra system.'), ('DD', 'Deep Dark', 100, 10, 'The bottom of everything.'),
]
FUEL = {0: 'Rocket Fuel', 1: 'Rocket Fuel', 2: 'RP-1 Rocket Fuel', 3: 'Dense Hydrazine Fuel Mixture',
        4: 'CN3H7O3 or H8N4C2O4 Rocket Fuel', 5: 'helium plasma', 6: 'nitrogen or oxygen plasma', 7: 'iron plasma',
        8: 'nickel plasma', 9: 'Raw Star Matter', 10: 'Molten SpaceTime'}
ROD = {0: 'Thorium', 1: 'Uranium', 2: 'MOX', 3: 'Plutonium', 4: 'Naquadah', 5: 'Enriched Naquadah',
       6: 'Naquadria', 7: 'Tiberium', 8: 'The Core', 9: 'a tier 9 rod', 10: 'a tier 10 rod'}
VOLT = ['EV', 'EV', 'IV', 'LuV', 'ZPM', 'UV', 'UHV', 'UEV', 'UIV', 'UMV', 'UXV']


def quest_band(planet_tier):
    """Reward band 0-6 (steam ... UIV+) from the voltage the planet needs."""
    return {0: 2, 1: 2, 2: 3, 3: 3, 4: 4, 5: 4, 6: 5, 7: 5}.get(planet_tier, 6)


def bag(dmg, n=1):
    return {"Count:3": n, "Damage:2": dmg, "OreDict:8": "", "id:8": "enhancedlootbags:lootbag"}


def item(i, dmg=0, n=1):
    return {"Count:3": n, "Damage:2": dmg, "OreDict:8": "", "id:8": i}


def qid(key):
    u = uuid.uuid5(SEED, key)
    hi, lo = struct.unpack('>qq', u.bytes)
    return base64.urlsafe_b64encode(u.bytes).decode(), hi, lo


def set_rewards(q, items, choices=None):
    rw = {}
    if items:
        rw["0:10"] = {"index:3": 0, "ignoreDisabled:1": 0, "rewardID:8": "bq_standard:item",
                      "rewards:9": {f"{k}:10": v for k, v in enumerate(items)}}
    if choices:
        n = len(rw)
        rw[f"{n}:10"] = {"index:3": n, "ignoreDisabled:1": 0, "rewardID:8": "bq_standard:choice",
                        "choices:9": {f"{k}:10": v for k, v in enumerate(choices)}}
    q['rewards:9'] = rw


def retrieval(items, consume):
    return {"taskID:8": "bq_standard:retrieval", "autoConsume:1": 0, "consume:1": 1 if consume else 0,
            "groupDetect:1": 0, "ignoreNBT:1": 1, "partialMatch:1": 0, "requireOnlyOneItem:1": 0,
            "requiredItems:9": {f"{k}:10": v for k, v in enumerate(items)}}


def location(name, dim):
    return {"taskID:8": "bq_standard:location", "name:8": name, "dimension:3": dim, "posX:3": 0, "posY:3": 64,
            "posZ:3": 0, "range:3": -1, "biome:3": -1, "structure:8": "", "visible:1": 0, "hideInfo:1": 0,
            "invert:1": 0, "taxiCabDist:1": 0}


def checkbox():
    return {"taskID:8": "bq_standard:checkbox"}


def machine_tier_for(planet_tier):
    return max(1, planet_tier)


# ---------------------------------------------------------------------------------------------------------------
# Machine row: key, x, y, name, icon, tasks, body, band, prereqs, finale
# ---------------------------------------------------------------------------------------------------------------
MACHINES = [
    ('guide', 0, 0, 'Planetary Exploiter Guide', item('minecraft:written_book'), [checkbox()],
     "Craft the guide book from a Book and a Compass (shapeless). It covers building every tier, the hatches, the "
     "map, parts, fuel and spark plugs, and what each warning means.", 2, []),
    ('controller', 72, 0, 'Planetary Exploiter', item(GT, CONTROLLER), [retrieval([item(GT, CONTROLLER)], False)],
     "One controller for every tier. Build tier 1 round it (the Structure Projector with stack size 1 shows it): a "
     "19x19 solid steel floor, a titanium plinth that holds every hatch, and a fusion-sized ring of "
     "Frost Proof casing round a core of TPV coils, with four laser arms. It needs 1A of EV.\n\n"
     "Put a planet block in the controller (sneak + right-click), then right-click it to open the map.", 2,
     ['guide']),
    ('modhatch', 144, 0, 'Modification Hatch', item(GT, MOD_HATCH), [retrieval([item(GT, MOD_HATCH)], False)],
     "Goes on the plinth. It holds the spark plug (a fuel rod), a drill tip, an Electric Pump, a scanner (Sensor or "
     "Electric Prospector's Scanner), a Field Generator and the lenses. Each slot only takes its own part, nothing "
     "above the machine's voltage, and lens slots open 2 per machine tier.", 2, ['controller']),
    ('fuel', 216, 0, 'Fuel and Spark Plugs', item('minecraft:blaze_rod'), [checkbox()],
     "The machine burns rocket fuel from an input hatch while it mines: Rocket Fuel for T0-T1 planets, RP-1 for T2, "
     "Dense Hydrazine for T3, and on through plasmas to SpaceTime. Moving the lasers to a new square burns spark plug "
     "charge: Thorium for T0, Uranium T1, MOX T2, Plutonium T3. A better rod burns less.", 2, ['modhatch']),
    ('tier2', 288, 0, 'Tier 2 Ring', item('gregtech:gt.blockcasings5', 4), [checkbox()],
     "Build the second ring round the first, without taking anything down: a wider solid steel floor, a waving ring of "
     "Robust Tungstensteel round HSS-G coils with more coils snaking over and under it, four IV emitters and "
     "tungstensteel legs. It needs 2A of IV and reaches T2 planets. Easier planets now get a bigger aim.", 3,
     ['controller']),
    ('tier3', 360, 0, 'Tier 3 Ring', item('gregtech:gt.blockcasings5', 5), [checkbox()],
     "The third ring: a 41x41 floor, a ring of LuV machine casing round Naquadah coils with snaking coils, eight "
     "emitters and HSS-G legs. It needs 4A of LuV (multi-amp or laser hatches work) and reaches T3 planets.", 3,
     ['tier2']),
]


def planet_entries():
    """Planet quests in tier lanes below the machine row."""
    lanes = {}
    for meta, (abbr, name, dim, tier, flavour) in enumerate(PLANETS):
        lanes.setdefault(tier, []).append((meta, abbr, name, dim, tier, flavour))
    out = []
    for tier, lane in sorted(lanes.items()):
        y = 96 + tier * 60
        for k, (meta, abbr, name, dim, t, flavour) in enumerate(lane):
            out.append((meta, abbr, name, dim, t, flavour, k * 60, y, k == len(lane) - 1 and len(lane) > 1))
    return out


def planet_quest(meta, abbr, name, dim, tier, flavour):
    dust = item(DUST, meta, STACKS * 64)
    tasks = []
    visit = dim is not None and abbr != 'Ow'
    if visit:
        tasks.append(location(name if abbr != 'EA' else 'The End (for End Asteroids)', dim))
    tasks.append(retrieval([dust], True))
    mt = machine_tier_for(tier)
    what = (f"Visit {name}, then hand in {STACKS} stacks ({STACKS * 64:,}) of {name} Dust."
            if visit else f"Hand in {STACKS} stacks ({STACKS * 64:,}) of {name} Dust.")
    if abbr == 'EA':
        what = (f"End Asteroids share The End's dimension, so visit The End, then hand in {STACKS} stacks "
                f"({STACKS * 64:,}) of End Asteroids Dust.")
    body = (f"{flavour}\n\n§bTier {tier}§r planet. {what}\n\n"
            f"Make the dust by macerating {name}'s surface rock with §eProgrammed Circuit 23§r. The Planet Eater "
            f"(coming) will strip whole layers of rock for you.\n\n"
            f"Reward: the §e{name} planet block§r. Put it in a tier {mt} (or better) Planetary Exploiter "
            f"({VOLT[tier]} power, {FUEL[tier]}, a {ROD[tier]} spark plug or better) to mine {name} from home.")
    return tasks, body


def main():
    os.makedirs(f'{R}/{CH}/quests', exist_ok=True)
    os.makedirs(f'{R}/{CH}/placements', exist_ok=True)
    index = ['# quest UUID (base64url)\tquest file\tplacement file\tmod id']
    keys = [m[0] for m in MACHINES] + [f'planet-{p[0]}' for p in PLANETS]
    ids = {k: qid(k) for k in keys}
    made = []
    nth = 0
    no = 1

    def write(key, x, y, name, icon, tasks, desc, band, pre, kind, extra_items=(), hidden_pre=False):
        nonlocal no
        b64, hi, lo = ids[key]
        f = f'23-{no:02d}.json'
        no += 1
        p = {"autoClaim:1": 0, "globalShare:1": 0, "isMain:1": 1 if kind == 'finale' else 0, "isSilent:1": 0,
             "lockedProgress:1": 0, "questLogic:8": "AND", "repeatTime:3": -1, "repeat_relative:1": 1,
             "simultaneous:1": 0, "snd_complete:8": "random.levelup", "snd_update:8": "random.levelup",
             "taskLogic:8": "AND", "visibility:8": "NORMAL", "name:8": name, "desc:8": desc, "icon:10": icon}
        q = {"properties:10": {"betterquesting:10": p}, "questIDHigh:4": hi, "questIDLow:4": lo,
             "tasks:9": {f"{k}:10": dict(t, **{"index:3": k}) for k, t in enumerate(tasks)}}
        pr = {}
        for k, r in enumerate(pre):
            e = {"questIDHigh:4": ids[r][1], "questIDLow:4": ids[r][2]}
            if hidden_pre:
                e["type:1"] = 2
            pr[f"{k}:10"] = e
        if pr:
            q["preRequisites:9"] = pr
        tb = TIERBAG[band]
        stage = TIERBAG_STAGE[tb]
        base = list(extra_items) + [bag(tb, 2 if band == 6 else 1)]
        if kind == 'finale':
            set_rewards(q, base + [bag(111), bag(14), item(IRIDIUM, 0, 3)])
        elif kind == 'row end':
            set_rewards(q, base + [bag(stage + 1, 3), item(IRIDIUM)])
        else:
            choice = nth % 5 == 4
            set_rewards(q, base, [bag(stage), item(IRIDIUM)] if choice else None)
        json.dump(q, open(f'{R}/{CH}/quests/{f}', 'w'), indent=2, ensure_ascii=False)
        json.dump({"questIDHigh:4": hi, "questIDLow:4": lo, "sizeX:3": 24, "sizeY:3": 24, "x:3": x, "y:3": y},
                  open(f'{R}/{CH}/placements/{f}', 'w'), indent=2)
        index.append(f"{b64}\t{f}\t{f}\t{MOD}")
        made.append((f, name, band, kind))

    for key, x, y, name, icon, tasks, body, band, pre in MACHINES:
        done = "tick the box once you've read this." if tasks[0]["taskID:8"] == "bq_standard:checkbox" else \
            "have one in your inventory. It is not consumed."
        kind = 'row end' if key == 'tier3' else ''
        write(key, x, y, name, icon, tasks, f"§b{name}§r\n\n{body}\n\n§aTask§r: {done}", band, pre, kind)
        if kind == '':
            nth += 1

    for meta, abbr, name, dim, tier, flavour, x, y, lane_end in planet_entries():
        tasks, body = planet_quest(meta, abbr, name, dim, tier, flavour)
        mt = machine_tier_for(tier)
        pre = ['controller'] if mt <= 1 else ['tier2'] if mt == 2 else ['tier3']
        band = quest_band(tier)
        kind = 'finale' if abbr == 'DD' else 'row end' if lane_end else ''
        block = item(f'gtneioreplugin:blockDimensionDisplay_{abbr}')
        write(f'planet-{abbr}', x, y, name, block, tasks, f"§b{name}§r\n\n{body}", band, pre, kind,
              extra_items=[block], hidden_pre=True)
        if kind == '':
            nth += 1

    open(f'{R}/{CH}/index.tsv', 'w').write('\n'.join(index) + '\n')
    cb64, chi, clo = qid('chapter-23')
    json.dump({"properties:10": {"betterquesting:10": {
        "bg_image:8": "", "bg_size:3": 256,
        "desc:8": "The Planetary Exploiter: a ring machine that mines planets from afar through a 9x9 survey map. "
                  "Visit each planet and bring back its dust to earn its planet block.",
        "icon:10": item(GT, CONTROLLER), "name:8": "Chapter 23: Planetary Exploitation",
        "visibility:8": "NORMAL"}}, "questLineIDHigh:4": chi, "questLineIDLow:4": clo},
        open(f'{R}/{CH}/QuestLine.json', 'w'), indent=2, ensure_ascii=False)
    lines = open(f'{R}/chapters.tsv').read().rstrip('\n').split('\n')
    if not any(l.startswith(CH + '\t') for l in lines):
        lines.append(f'{CH}\t{cb64}\t22')
    open(f'{R}/chapters.tsv', 'w').write('\n'.join(lines) + '\n')
    for m in made:
        print(*m, sep='\t')
    print(len(made), 'quests')


if __name__ == '__main__':
    main()
