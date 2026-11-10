"""Quest mod v9.3.0 / v9.4.0: Chapter 23 "Planetary Exploitation" for the Planetary Exploiter mod.

- Machine row: the guide, the controller, the Modification Hatch, fuel and spark plugs, the tier 2-6 rings.
- v9.4.0: every planet lane starts with its Fuel quest (have 1,000 L of that tier's fuel) and Spark Plug quest (have
  that tier's fuel rod); the lane's planets need both, so you unlock the fuel and the rod before the planets.
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
# The pack's own planet dusts (NewHorizonsCoreMod 2.9.84 ids; GT dusts for Earth, Nether and End).
# Planets missing here have no dust in the pack, so their quest is a visit only.
GT_META = 'gregtech:gt.metaitem.01'
DUSTS = {
    'Ow': (GT_META, 2299, 'dustStone', 'Stone Dust'), 'Ne': (GT_META, 2807, 'dustNetherrack', 'Netherrack Dust'),
    'ED': (GT_META, 2808, 'dustEndstone', 'End Stone Dust'), 'EA': (GT_META, 2808, 'dustEndstone', 'End Stone Dust'),
    'Mo': ('dreamcraft:MoonStoneDust', 0, '', 'Moon Stone Dust'),
    'De': ('dreamcraft:DeimosStoneDust', 0, '', 'Deimos Stone Dust'),
    'Ma': ('dreamcraft:MarsStoneDust', 0, '', 'Mars Stone Dust'),
    'Ph': ('dreamcraft:PhobosStoneDust', 0, '', 'Phobos Stone Dust'),
    'As': ('dreamcraft:AsteroidsStoneDust', 0, '', 'Asteroids Stone Dust'),
    'Ca': ('dreamcraft:CallistoStoneDust', 0, '', 'Callisto Stone Dust'),
    'Ce': ('dreamcraft:CeresStoneDust', 0, '', 'Ceres Stone Dust'),
    'Eu': ('dreamcraft:EuropaStoneDust', 0, '', 'Europa Stone Dust'),
    'Ga': ('dreamcraft:GanymedeStoneDust', 0, '', 'Ganymede Stone Dust'),
    'Io': ('dreamcraft:IoStoneDust', 0, '', 'Io Stone Dust'),
    'Me': ('dreamcraft:MercuryStoneDust', 0, '', 'Mercury Stone Dust'),
    'Ve': ('dreamcraft:VenusStoneDust', 0, '', 'Venus Stone Dust'),
    'En': ('dreamcraft:EnceladusStoneDust', 0, '', 'Enceladus Stone Dust'),
    'Mi': ('dreamcraft:MirandaStoneDust', 0, '', 'Miranda Stone Dust'),
    'Ob': ('dreamcraft:OberonStoneDust', 0, '', 'Oberon Stone Dust'),
    'Ti': ('dreamcraft:TitanStoneDust', 0, '', 'Titan Stone Dust'),
    'Pr': ('dreamcraft:ProteusStoneDust', 0, '', 'Proteus Stone Dust'),
    'Tr': ('dreamcraft:TritonStoneDust', 0, '', 'Triton Stone Dust'),
    'Ha': ('dreamcraft:HaumeaStoneDust', 0, '', 'Haumea Stone Dust'),
    'MM': ('dreamcraft:MakeMakeStoneDust', 0, '', 'Makemake Stone Dust'),
    'Pl': ('dreamcraft:PlutoStoneDust', 0, '', 'Pluto Stone Dust'),
    'BE': ('dreamcraft:BarnardaEStoneDust', 0, '', 'Barnarda E Stone Dust'),
    'BF': ('dreamcraft:BarnardaFStoneDust', 0, '', 'Barnarda F Stone Dust'),
    'CB': ('dreamcraft:CentauriAStoneDust', 0, '', 'Centauri A Stone Dust'),
    'TE': ('dreamcraft:TCetiEStoneDust', 0, '', 'T Ceti E Stone Dust'),
    'VB': ('dreamcraft:VegaBStoneDust', 0, '', 'Vega B Stone Dust'),
}
CONTROLLER, MOD_HATCH, EATER, REFINERY = 31774, 31775, 31776, 31777
PLUG = 'planetaryexploiter:sparkPlug'
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
ROD = {0: 'Thorium', 1: 'Uranium', 2: 'MOX', 3: 'Plutonium', 4: 'Naquadah', 5: 'Naquadria',
       6: 'Naquadria', 7: 'Tiberium', 8: 'The Core', 9: 'Stellar', 10: 'Eternal'}
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


def fluid_task(name, amount):
    return {"taskID:8": "bq_standard:fluid", "autoConsume:1": 0, "consume:1": 0, "groupDetect:1": 0, "partialMatch:1": 0,
            "ignoreNBT:1": 1, "requiredFluids:9": {"0:10": {"FluidName:8": name, "Amount:3": amount}}}


# Fuel fluid (registry name, shown name) and spark plug items per planet tier, checked against the pack's log.
FUEL_FLUID = {0: ('rocket_fuel', 'Rocket Fuel'), 1: ('rocket_fuel', 'Rocket Fuel'),
              2: ('fluid.rocketfuelmixb', 'RP-1 Rocket Fuel'), 3: ('fluid.rocketfuelmixd', 'Dense Hydrazine Fuel Mixture'),
              4: ('fluid.rocketfuelmixc', 'CN3H7O3 Rocket Fuel'), 5: ('plasma.helium', 'Helium Plasma'),
              6: ('plasma.nitrogen', 'Nitrogen Plasma'), 7: ('plasma.iron', 'Iron Plasma'),
              8: ('plasma.nickel', 'Nickel Plasma'), 9: ('rawstarmatter', 'Condensed Raw Stellar Plasma Mixture'),
              10: ('molten.spacetime', 'Molten SpaceTime')}
ROD_ITEMS = {0: ['gregtech:gt.rodThorium'], 1: ['gregtech:gt.rodUranium', 'IC2:reactorUraniumSimple'],
             2: ['gregtech:gt.rodMOX', 'IC2:reactorMOXSimple'],
             3: ['gregtech:gt.rodHighDensityPlutonium', 'gregtech:gt.rodExcitedPlutonium'],
             4: ['gregtech:gt.rodNaquadah'], 5: ['gregtech:gt.rodNaquadria'], 6: ['gregtech:gt.rodNaquadria'],
             7: ['gregtech:gt.rodTiberium'], 8: ['gregtech:gt.rodNaquadah32'], 9: [(PLUG, 0)], 10: [(PLUG, 1)]}
ROD_NAME = {0: 'Thorium', 1: 'Uranium', 2: 'MOX', 3: 'Plutonium', 4: 'Naquadah', 5: 'Naquadria', 6: 'Naquadria',
            7: 'Tiberium', 8: 'The Core', 9: 'Stellar Spark Plug', 10: 'Eternal Spark Plug'}
FUEL_LITRES = 1000


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
     "21x21 solid steel floor, a titanium plinth that holds every hatch, and a fusion-sized ring of "
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
     "charge: Thorium for T0, Uranium T1, MOX T2, Plutonium T3 and on up to The Core for T8. Tiers 9 and 10 need the "
     "mod's own Stellar and Eternal Spark Plugs. A better rod burns less.", 2, ['modhatch']),
    ('tier2', 288, 0, 'Tier 2 Ring', item('gregtech:gt.blockcasings5', 4), [checkbox()],
     "Build the second ring round and above the first, without taking anything down: a wider solid steel floor, a "
     "tube of Robust Tungstensteel round HSS-G coils with coil bands wound round it, four IV emitters and "
     "tungstensteel legs. It needs 2A of IV and reaches T2 planets. Easier planets now get a bigger aim.", 3,
     ['controller']),
    ('tier3', 360, 0, 'Tier 3 Ring', item('gregtech:gt.blockcasings5', 5), [checkbox()],
     "The third ring, wider and higher again: LuV machine casing round Naquadah coils with coil bands wound round it, "
     "eight emitters and HSS-G legs. It needs 4A of LuV (multi-amp or laser hatches work) and reaches T3 planets.", 3,
     ['tier2']),
    ('tier4', 432, 0, 'Tier 4 Ring', item('gregtech:gt.blockcasings5', 6), [checkbox()],
     "ZPM machine casing round Naquadah Alloy coils, eight emitters and naquadah legs. 8A of ZPM; reaches T4 planets.",
     4, ['tier3']),
    ('tier5', 504, 0, 'Tier 5 Ring', item('gregtech:gt.blockcasings5', 10), [checkbox()],
     "UV machine casing round Trinium coils, twelve Fusion Machine Casing emitters and naquadah alloy legs. 16A of UV; "
     "reaches T5 planets.", 4, ['tier4']),
    ('tier6', 576, 0, 'Tier 6 Ring', item('gregtech:gt.blockcasings5', 7), [checkbox()],
     "Fusion Machine Casing Mk-II round Electrum Flux coils, twelve Fusion Coil emitters and neutronium legs, on an "
     "81x81 floor. 32A of UHV; reaches T6 planets.", 5, ['tier5']),
    ('tier7', 648, 0, 'Tier 7 Ring', item('gregtech:gt.blockcasings5', 8), [checkbox()],
     "The endgame rings step out 5 blocks at a time and carry sixteen lasers each. Tier 7: Fusion Machine Casing "
     "Mk-III round Awakened Draconium coils, with cosmic neutronium legs (the guide book and the Structure "
     "Projector show the exact casings in your pack). 64A of UEV; reaches T7 planets.", 5, ['tier6']),
    ('tier8', 720, 0, 'Tier 8 Ring', item('gregtech:gt.blockcasings5', 11), [checkbox()],
     "Molecular Casing round Infinity coils, Advanced Molecular Casing emitters and infinity legs. 128A of UIV; "
     "reaches T8 planets.", 6, ['tier7']),
    ('tier9', 792, 0, 'Tier 9 Ring', item('gregtech:gt.blockcasings5', 12), [checkbox()],
     "Spacetime Altering Casing round Hypogen coils, spacetime-boundary emitters and SpaceTime legs. 256A of UMV; "
     "reaches T9 planets with a Stellar Spark Plug.", 6, ['tier8']),
    ('tier10', 864, 0, 'Tier 10 Ring', item('gregtech:gt.blockcasings5', 13), [checkbox()],
     "The crown of the funnel, 121 blocks across: Reinforced Temporal Structure Casing round Eternal coils, spatial "
     "structure emitters and transcendent metal legs. 512A of UXV; reaches the Deep Dark with an Eternal Spark Plug.",
     6, ['tier9']),
    ('eater', 144, 48, 'Planet Eater', item(GT, EATER), [retrieval([item(GT, EATER)], False)],
     "A 5x5 EV drilling rig. It strips the 3x3 chunks round it, a layer at a time from under the machine down to "
     "bedrock, and keeps only the planet's own rock (moon turf and regolith count). Ores, soil and sand stay put, and "
     "every hole is back-filled with cobblestone. Off-world only.\n\nPut a drill tip in the controller: EV for T1 "
     "planets and one voltage higher per planet tier. Each tier better doubles the speed and makes the tip last four "
     "times longer. The rock it digs is exactly what the planet quests want macerated.", 2, ['guide']),
    ('refinery', 216, 48, 'Regolith Refinery', item(GT, REFINERY), [retrieval([item(GT, REFINERY)], False)],
     "A 7x7 IV refinery that crushes and centrifuges planet rock in one step, with GregTech's own macerator and "
     "centrifuge recipes. Only planet surface blocks go in.\n\nAny turbine rotor in the controller is the "
     "crusher, and it wears down as it works. Bigger rotors do more blocks at once (tool speed x size / 2: Small x1, "
     "Normal x2, Large x3, Huge x4), and the material sets the highest recipe voltage (tool quality + 2).", 3, ['eater']),
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
            out.append((meta, abbr, name, dim, t, flavour, 144 + k * 60, y, k == len(lane) - 1))
    return out


def planet_quest(meta, abbr, name, dim, tier, flavour):
    tasks = []
    visit = dim is not None and abbr != 'Ow'
    if visit:
        tasks.append(location(name if abbr != 'EA' else 'The End (for End Asteroids)', dim))
    dust = DUSTS.get(abbr)
    n = f"{STACKS} stacks ({STACKS * 64:,})"
    if dust:
        reg, dmg, ore, dname = dust
        tasks.append(retrieval([{"Count:3": STACKS * 64, "Damage:2": dmg, "OreDict:8": ore, "id:8": reg}], True))
        if abbr == 'EA':
            what = (f"End Asteroids share The End's dimension, so visit The End, then hand in {n} of "
                    f"§e{dname}§r from the asteroids' end stone.")
        elif visit:
            what = f"Visit {name}, then hand in {n} of §e{dname}§r."
        else:
            what = f"Hand in {n} of §e{dname}§r."
        how = (f"Macerate {name}'s rock to make it. A Planet Eater on {name} strips whole layers of rock for you, "
               f"and a Regolith Refinery turns it into dust and more.\n\n") if abbr not in ('Ow', 'Ne', 'ED', 'EA', 'TF', 'Eg') \
            else f"Macerate {name}'s rock to make it.\n\n"
    else:
        what = f"Visit {name}. There is no {name} dust in the pack, so the visit is enough."
        how = ""
    mt = machine_tier_for(tier)
    body = (f"{flavour}\n\n§bTier {tier}§r planet. {what}\n\n{how}"
            f"Reward: the §e{name} planet block§r. Put it in a tier {mt} (or better) Planetary Exploiter "
            f"({VOLT[tier]} power, {FUEL[tier]}, a {ROD[tier]} spark plug or better) to mine {name} from home.")
    return tasks, body


def main():
    os.makedirs(f'{R}/{CH}/quests', exist_ok=True)
    os.makedirs(f'{R}/{CH}/placements', exist_ok=True)
    index = ['# quest UUID (base64url)\tquest file\tplacement file\tmod id']
    keys = [m[0] for m in MACHINES] + [f'planet-{p[0]}' for p in PLANETS] + \
        [f'fuel-{t}' for t in range(11)] + [f'rod-{t}' for t in range(11)]
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
            if hidden_pre is True or (hidden_pre and r in hidden_pre):
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

    def machine_key(planet_tier):
        mt = min(10, machine_tier_for(planet_tier))
        return 'controller' if mt <= 1 else f'tier{mt}'

    lane_tiers = sorted({p[3] for p in PLANETS})
    for tier in lane_tiers:
        y = 96 + tier * 60
        reg, fname = FUEL_FLUID[tier]
        band = quest_band(tier)
        write(f'fuel-{tier}', 0, y, f'T{tier} Fuel: {fname}', item('IC2:itemFluidCell'),
              [fluid_task(reg, FUEL_LITRES)],
              f"§bT{tier} Fuel§r\n\nThe Planetary Exploiter burns §e{fname}§r (or any better fuel) from an input "
              f"hatch while it mines a tier {tier} planet, {['10', '20', '40', '80', '160', '320', '640', '1,280', '2,560', '5,120', '10,240'][tier]} L "
              f"a second (three times that for ore + fluid).\n\n§aTask§r: have {FUEL_LITRES:,} L of it in a container in "
              f"your inventory. It is not consumed.", band, [machine_key(tier)], '', hidden_pre=True)
        nth += 1
        rods = ROD_ITEMS[tier]
        if rods:
            stacks = [item(r) if isinstance(r, str) else item(r[0], r[1]) for r in rods]
            rod_tasks = [dict(retrieval(stacks, False), **{"requireOnlyOneItem:1": 1})]
            rod_icon = stacks[0]
            if tier >= 9:
                made_by = ("Assembler, UMV: Field Generator, 2 Sensors and 2 Emitters (UMV) with 1,000 L of raw star "
                           "matter." if tier == 9 else
                           "Assembler, UXV: a Stellar Spark Plug, a Field Generator, 2 Sensors and 2 Emitters (UXV) "
                           "with 1,440 L of molten SpaceTime.")
                rod_text = (f"No fuel rod in the pack reaches tier {tier}, so the Planetary Exploiter has its own: the "
                            f"§e{ROD_NAME[tier]}§r. It goes in the Modification Hatch's Plug slot and burns charge "
                            f"like any rod.\n\n{made_by}\n\n§aTask§r: have one in your inventory. It is not "
                            f"consumed.")
            else:
                rod_text = (f"Moving the lasers to a new square burns the spark plug: a §e{ROD_NAME[tier]}§r fuel rod "
                            f"(or better) in the Modification Hatch's Plug slot. A rod of the planet's own tier burns "
                            f"10% per square, and each tier above burns less.\n\n§aTask§r: have one in your inventory. "
                            f"It is not consumed.")
        else:
            rod_tasks = [checkbox()]
            rod_icon = item('minecraft:blaze_rod')
            rod_text = ("No fuel rod in the pack reaches this tier yet; a spark plug for it is coming with a later "
                        "version of the Planetary Exploiter.\n\n§aTask§r: tick the box once you've read this.")
        write(f'rod-{tier}', 60, y, f'T{tier} Spark Plug' if tier >= 9 else f'T{tier} Spark Plug: {ROD_NAME[tier]}',
              rod_icon, rod_tasks, f"§bT{tier} Spark Plug§r\n\n{rod_text}", band, [f'fuel-{tier}'], '')
        nth += 1

    for meta, abbr, name, dim, tier, flavour, x, y, lane_end in planet_entries():
        tasks, body = planet_quest(meta, abbr, name, dim, tier, flavour)
        pre = [machine_key(tier), f'rod-{tier}']
        band = quest_band(tier)
        kind = 'finale' if abbr == 'DD' else 'row end' if lane_end else ''
        block = item(f'gtneioreplugin:blockDimensionDisplay_{abbr}')
        # The first planet of a lane shows its line from the spark plug; the rest stay tidy.
        hidden = {pre[0]} if x == 144 else set(pre)
        write(f'planet-{abbr}', x, y, name, block, tasks, f"§b{name}§r\n\n{body}", band, pre, kind,
              extra_items=[block], hidden_pre=hidden)
        if kind == '':
            nth += 1

    open(f'{R}/{CH}/index.tsv', 'w').write('\n'.join(index) + '\n')
    cb64, chi, clo = qid('chapter-23')
    json.dump({"properties:10": {"betterquesting:10": {
        "bg_image:8": "", "bg_size:3": 256,
        "desc:8": "The Planetary Exploiter: a ring machine that mines planets from afar through a 9x9 survey map. "
                  "Visit each planet and bring back its stone dust to earn its planet block.",
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
