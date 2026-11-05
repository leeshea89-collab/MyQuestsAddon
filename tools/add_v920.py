"""Quest mod v9.2.0: quests for the mods added on 2026-11-04.

- Chapter 9 (Steam Revolution, GT Steam Reborn v2.1.9): turbine upgrades, processing cluster modules,
  the Mimetic Loom and the four released critical machines.
- Chapter 3 (MessTech 3.1): reactor coolant loop, essentia power, Large Processing Factory, Protocol Core,
  Comprehensive Mining Plant, Grand Space Elevator, Wireless Filtered Beam Output Hatch.
- New Chapter 22 (Blueprints & ME Tools): TenkeiTech and GT Miao Blueprint (+ MIAOKATZE Core camera).

Rewards follow 9.1.0 (tier bag; every 5th normal quest a small choice; last quest of a row tier bag + 3 Fortune
seed bags; finale Fortune Rare Heirloom + GTNH bag 14) and add Fair Play Iridium coins (fairplay:CoinIV):
1 as the coin option of the small choice, 1 on every row end, 3 on the finale.
Every new quest is gated by its mod id (4th index column).
Run from the repo root: python3 tools/add_v920.py
"""
import base64, json, os, struct, uuid

R = os.path.join(os.path.dirname(__file__), '..', 'jar-contents', 'assets', 'gtnhaddonquests')
SEED = uuid.uuid5(uuid.NAMESPACE_URL, 'gtnhaddonquests/v9.2/new-mods-2026-11-04')
TIERBAG = {0: 2, 1: 4, 2: 6, 3: 8, 4: 42, 5: 44, 6: 44}
TIERBAG_STAGE = {2: 102, 4: 100, 6: 104, 8: 104, 42: 106, 44: 108}
IRIDIUM = 'fairplay:CoinIV'
GT = 'gregtech:gt.blockmachines'


def bag(dmg, n=1):
    return {"Count:3": n, "Damage:2": dmg, "OreDict:8": "", "id:8": "enhancedlootbags:lootbag"}


def item(i, dmg=0, n=1):
    return {"Count:3": n, "Damage:2": dmg, "OreDict:8": "", "id:8": i}


def gt(meta):
    return item(GT, meta)


def qid(key):
    u = uuid.uuid5(SEED, key)
    hi, lo = struct.unpack('>qq', u.bytes)
    return base64.urlsafe_b64encode(u.bytes).decode(), hi, lo


def b64_to_ids(b64):
    return struct.unpack('>qq', base64.urlsafe_b64decode(b64))


def existing(ch, f):
    for line in open(f'{R}/{ch}/index.tsv'):
        p = line.rstrip('\n').split('\t')
        if len(p) >= 2 and p[1] == f:
            return b64_to_ids(p[0])
    raise KeyError(f'{ch}/{f}')


HAVE = "have one in your inventory. It is not consumed."
READ = "tick the box once you've read this."

# key, x, y, name, icon, task item (None = checkbox), body, tier, prereqs (new keys or (chapter, file)), mod, finale
CH9 = 'ch09-steam-revolution'
GTSR = [
    ('coolhatch', 360, 1260, 'Steam Cooling Hatch', gt(14955), gt(14955),
     "Takes the spent steam from the Mega Steam Turbine Array and condenses it back into water instead of venting it. "
     "Put it where the array lists an Output Hatch / Steam Cooling Hatch.", 2, [(CH9, '09-12.json')], 'gtsr', False),
    ('ophatch', 432, 1260, 'Mega Overpressure Steam Input Hatch', gt(14963), gt(14963),
     "Takes vast amounts of steam of every type through steam singularities. It only fits the Mega Steam Turbine Array "
     "and the Steam Singularity Entangler, and is the way to feed a fully stacked array.", 2, ['coolhatch'], 'gtsr', False),
    ('cyclechip', 900, 1260, 'Steam Turbine Cycle Overlimit Chip', item('gtsr:SteamTurbineCycleOverlimitChip'),
     item('gtsr:SteamTurbineCycleOverlimitChip'),
     "Goes in the Mega Steam Turbine Array's controller slot and only works with all 4 extra stack groups built. "
     "Superheated and supercritical steam (dense too) then cools straight into distilled water, and the steam efficiency "
     "factors stack within each steam family. A Critical Steam Entangled Singularity in the input bus gives x5 power for 200 s.",
     5, ['coolhatch', (CH9, '09-30.json')], 'gtsr', False),

    ('crusher', 540, 1332, 'Processing Cluster Crusher Module', gt(15052), gt(15052),
     "The Steam-Powered Mineral Processing Logistics Engineering Cluster does nothing on its own: each processing step is "
     "a module you link to it in the terminal. The Crusher is the first step of every ore line.", 3,
     [(CH9, '09-17.json')], 'gtsr', False),
    ('washer', 612, 1332, 'Processing Cluster Ore Washing Module', gt(15053), gt(15053),
     "Washes crushed ore for the next step. Chain modules in the order your ore line needs them; the Centrifuge, "
     "Thermal Centrifuge, Sifting, Magnetic Separation and Smelting modules work the same way.", 3, ['crusher'], 'gtsr', False),
    ('logistics', 540, 1404, 'Processing Cluster Logistics Module', gt(15064), gt(15064),
     "Sets the cluster's logistics base, which decides how many parallels it runs and how long items spend moving "
     "between modules. Throughput = parallels / time per batch.", 3, [(CH9, '09-17.json')], 'gtsr', False),
    ('parallel', 612, 1404, 'Processing Cluster Parallel Booster Module', gt(15059), gt(15059),
     "Each booster adds parallels (+5/10/30/40% pressure by tier, more for each extra booster of the same kind) but raises "
     "the steam bill. The Speed, Primary Output, Secondary Output and Efficiency boosters work the same way.", 3,
     ['logistics'], 'gtsr', False),

    ('loom', 900, 1476, 'Mimetic Loom', gt(14904), gt(14904),
     "The builder for critical machines. Build the 15x36x15 loom first (by hand or with a projector), feed it materials "
     "through real GT input buses and hatches, then pick one of the four released kinds: Solar, Turbine, Star or Battery. "
     "The kind locks once construction starts, and missing materials or power pause the build. Leave up to 80x162x80 free "
     "for the machine.", 5, [(CH9, '09-30.json')], 'gtsr', False),
    ('csolar', 972, 1476, 'Dimensional Irradiance Coupling Boiler', gt(14905), gt(14905),
     "The critical solar boiler: makes steam from distilled water (or recovers Sanzu steam) using a coolant and an "
     "exciter fluid. Only one can own a dimension.", 5, ['loom'], 'gtsr', False),
    ('csun', 1044, 1476, 'Artificial Stellar Confinement Core', gt(14909), gt(14909),
     "An artificial star that runs GregTech fusion recipes: ignition, upkeep and fusion take 400 ticks each, with up to "
     "8196 parallels limited by power, inputs and output space. It keeps burning helium-3 and power while paused.",
     5, ['loom'], 'gtsr', True),
    ('cturbine', 972, 1548, 'Supercritical Steam Pulse Power Core', gt(14906), gt(14906),
     "The critical turbine: all six steam families cascade from steam back to water at 100-2000% efficiency, and the "
     "power goes straight to its owner team's wireless EU network.", 5, ['loom'], 'gtsr', False),
    ('cbattery', 1044, 1548, 'Multiphase Thermochemical Reaction Core', gt(14911), gt(14911),
     "The critical battery: zinc-acid electrochemical generation, with energy stored in the structure.", 5, ['loom'],
     'gtsr', False),
]

CH3 = 'ch03-messtech'
MESS = [
    ('coolin', 108, 1260, 'Reactor Coolant Input Hatch', gt(32432), gt(32432),
     "A screwdriver on the Nuclear Reactor's controller switches it to fluid (wet) mode, which needs one coolant input "
     "hatch and one hot coolant output hatch. 1 mB of coolant carries 1 HU of heat.", 2, [(CH3, '03-01.json')],
     'MessTech', False),
    ('coolout', 180, 1260, 'Reactor Hot Coolant Output Hatch', gt(32435), gt(32435),
     "Hot coolant comes out here as fast as cold coolant goes in. It is a through-put, not a heat sink: keep both sides "
     "flowing or the loop carries no heat away.", 2, ['coolin'], 'MessTech', False),
    ('leg', 108, 1332, 'Large Essentia Generator', gt(32437), gt(32437),
     "Turns stored essentia into EU. The dynamo hatch sets the voltage and amperage; EU per essentia = fuel value x "
     "stable points / 25, and the cells only add stable points.", 2, [], 'MessTech', False),
    ('smeltery', 288, 1332, 'Small Essentia Smeltery', gt(32478), gt(32478),
     "A compact essentia smeltery that melts items and fluids into essentia with no vis nodes, pollution or flux. The 7 "
     "cells on its centre axis must all be one tier. Feed its output to the Large Essentia Generator.", 3, ['leg'],
     'MessTech', False),
    ('lpf', 108, 1404, 'Large Processing Factory', gt(32436), gt(32436),
     "Nine single-block machines in one frame. The machine mode (Metal, Fluid, Misc) and the circuit pick the recipe pool.",
     2, [], 'MessTech', False),
    ('protocol', 108, 1476, 'Protocol Core', gt(32480), gt(32480),
     "A 16x52x16 beacon tower with no energy hatch of its own. It drains the placer's wireless network 1:1 and charges "
     "every wired, laser and multi-amp energy hatch owned by the placer's team at full amperage, even while they are offline.",
     2, [], 'MessTech', False),
    ('cmp', 468, 1548, 'Comprehensive Mining Plant', gt(32479), gt(32479),
     "A void miner and void pump in one: each ore parallel takes 64 ores a second from this dimension's ore pool, and the "
     "fluid parallels pump its oil field. No energy hatch; each parallel draws 32,768 EU/t from your wireless network.",
     4, [], 'MessTech', False),
    ('elevator', 468, 1620, 'Grand Space Elevator', gt(32438), gt(32438),
     "GregTech's Space Elevator on one 95x122x78 structure with 64 project module bays. Use the Blueprint to preview it.",
     4, [], 'MessTech', False),
    ('filtbeam', 720, 1692, 'Wireless Filtered Beam Output Hatch', gt(32472), gt(32472),
     "The wireless beam output hatch with the particle blacklist. Like the others, it pairs with the input hatch of the "
     "same dye colour.", 5, [(CH3, '03-24.json')], 'MessTech', False),
]

CH22 = 'ch22-blueprints-me-tools'
NEW22 = [
    ('tk_buffer', 360, 0, 'ME Super Pattern Buffer', gt(32600), gt(32600),
     "A multiblock item input that works like the ME Crafting Input Buffer with more pattern sets and a programmed "
     "circuit per slot. The ME Pattern Buffer Copy and Cut Tools copy or move a buffer's patterns.", 2, [],
     'tenkeitech', False),
    ('tk_proxy', 432, 0, 'ME Super Pattern Buffer Proxy', gt(32601), gt(32601),
     "Shares the inputs of a linked Super Pattern Buffer with another machine. Link it with a data stick; a screwdriver "
     "changes the recipe order.", 2, ['tk_buffer'], 'tenkeitech', False),
    ('tk_auto', 360, 72, 'Auto Template ME Input Bus', gt(32604), gt(32604),
     "Provides Extruder or Fluid Solidifier patterns by itself: craft it with a shape or mold to bind the template. "
     "The Mirror version shares its materials with another machine.", 2, ['tk_buffer'], 'tenkeitech', False),
    ('tk_wire', 432, 72, 'Wiremill Template ME Input Bus', gt(32606), gt(32606),
     "Ingot-to-wire patterns with seven circuits, each with its own inputs and settings. The Bender Template ME Input "
     "Bus does the same for plates and foil.", 2, ['tk_auto'], 'tenkeitech', False),
    ('tk_core', 360, 144, 'Wireless ME Network Core', gt(32602), gt(32602),
     "Connects GT ME hatches to a network without cables. Right-click to name the network; you and your ServerUtilities "
     "team can use it. Keep both ends loaded.", 2, ['tk_buffer'], 'tenkeitech', False),
    ('tk_bookmark', 432, 144, 'Wireless ME Network Bookmark', gt(32603), gt(32603),
     "Pick one of your or your team's wireless networks, then sneak-place GT ME hatches to bind them to it.", 2,
     ['tk_core'], 'tenkeitech', False),
    ('tk_requester', 360, 216, 'Better ME Requester', item('tenkeitech:better_level_maintainer'),
     item('tenkeitech:better_level_maintainer'),
     "Keeps chosen items and fluids stocked by ordering crafts from your network. Set target, batch size and check "
     "interval for each entry (k/m/g/t shorthand works); it keeps its settings when broken.", 2, ['tk_buffer'],
     'tenkeitech', False),
    ('tk_blocking', 360, 288, 'Blocking Filter Card', item('tenkeitech:blocking_filter_card_precise'),
     item('tenkeitech:blocking_filter_card_precise'),
     "An ME Interface upgrade: blocking mode only waits for the items this card filters, so other leftovers no longer "
     "stall the interface. The Ignore NBT version matches any NBT.", 2, ['tk_buffer'], 'tenkeitech', False),
    ('tk_extract', 432, 288, 'Automatic Extraction Card', item('tenkeitech:auto_extraction_card'),
     item('tenkeitech:auto_extraction_card'),
     "An ME Interface upgrade that pulls finished outputs back out of the machine it faces into the network.", 2,
     ['tk_blocking'], 'tenkeitech', False),
    ('tk_reso', 504, 288, 'Resonating Pattern', item('tenkeitech:resonating_pattern'),
     item('tenkeitech:resonating_pattern'),
     "A pattern whose inputs are bound with the Resonating Binding Card. AE waits until every bound input is in place "
     "before it pushes the craft.", 2, ['tk_blocking'], 'tenkeitech', False),

    ('mb_proj', 180, 432, 'Neko Blueprint Hologram Projector', item('gtmb:neko_hologram_projector'),
     item('gtmb:neko_hologram_projector'),
     "GT Miao Blueprint's one tool. Right-click opens it. It previews multiblocks as holograms, saves and shares "
     "blueprints, and builds, replaces or dismantles structures from your materials. Its own tutorial (? in the UI) has "
     "eight lessons.", 1, [], 'gtmb', False),
    ('mb_import', 252, 432, 'Import a Machine', None, item('gregtech:gt.blockmachines', 1000),
     "Right-click a real controller with the projector to import its whole structure, then right-click again to lock the "
     "green preview. A second right-click opens the material check, and only then do you confirm the build. Ctrl-click "
     "picks single cells, Shift-drag picks a volume.", 1, ['mb_proj'], 'gtmb', False),
    ('mb_modes', 180, 504, 'Refill, Replace, Dismantle', None, item('gtmb:neko_hologram_projector'),
     "Refill places what's missing, Replace swaps hatches and casings for the targets you picked, and Dismantle takes a "
     "structure down from the top and returns the items (Esc cancels). Number keys 1/2/3 switch mode; switching never "
     "builds anything on its own.", 1, ['mb_proj'], 'gtmb', False),
    ('mb_library', 252, 504, 'The Blueprint Library', None, item('minecraft:book'),
     "Save blueprints to your client library or the server's public one, export them as JSON to share, and place them "
     "from the library. Alt-right-click quick-places the last blueprint. Shared blueprints are de-identified so other "
     "players' networks and owners don't come along.", 1, ['mb_proj'], 'gtmb', False),
    ('mb_cut', 180, 576, 'Cut and Move', None, item('minecraft:shears'),
     "Shift-right-click picks Blueprint, Cut or Demolish mode. Cut lifts a complete structure (blocks, machines and their "
     "contents) into storage so you can place it somewhere else; Alt-right-click undoes the last cut.", 1, ['mb_proj'],
     'gtmb', False),
    ('mb_materials', 252, 576, 'Materials and AE Orders', None, item('appliedenergistics2:tile.BlockInterface'),
     "Building takes materials from your main inventory, backpack containers and an ME terminal in the order you set. "
     "If something is missing, the material screen can order the missing items as an AE crafting job, or place only what "
     "you have.", 1, ['mb_proj'], 'gtmb', False),
    ('mb_voucher', 180, 648, 'Miao Decoration Voucher', item('gtmb:decoration_voucher'), item('gtmb:decoration_voucher'),
     "Decoration-only blueprints can use one voucher to cover their building-mod materials. Industrial devices and "
     "internal resources are still paid for in full.", 1, ['mb_proj'], 'gtmb', False),
    ('mb_pixel', 252, 648, 'Text and Image Blueprints', None, item('minecraft:painting'),
     "The text and image tools turn typed text, or a PNG/JPG put in .minecraft/MiaoBlueprintPicture, into LittleTiles "
     "pixel art you can attach to a blueprint.", 1, ['mb_proj'], 'gtmb', False),
    ('mb_camera', 180, 720, 'Blueprint Camera', None, item('minecraft:compass'),
     "From MIAOKATZE Core: the editor's camera can rotate, zoom, switch to isometric view and X-ray. The height slice "
     "view needs a newer Angelica and is switched off in this pack.", 1, ['mb_proj'], 'miaokatzecore', False),
]


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


def build(ch, entries, file_prefix, start_no, row_ends=None):
    ids = {e[0]: qid(e[0]) for e in entries}
    lanes = {}
    for e in entries:
        lanes.setdefault((e[2]), []).append(e)
    row_end = set()
    # a lane's last quest (by x) is a row end when the lane has more than one quest (new or existing)
    existing_place = [json.load(open(os.path.join(R, ch, 'placements', f)))
                      for f in os.listdir(os.path.join(R, ch, 'placements'))]
    for y, lane in lanes.items():
        old = [p for p in existing_place if p['y:3'] == y]
        last = max(lane, key=lambda e: e[1])
        if len(lane) + len(old) > 1 and all(p['x:3'] < last[1] for p in old):
            row_end.add(last[0])
    if row_ends is not None:  # chapters laid out as one row per mod
        row_end = set(row_ends)
    index_lines = open(f'{R}/{ch}/index.tsv').read().rstrip('\n').split('\n')
    nth = 0
    made = []
    for no, e in enumerate(entries, start_no):
        key, x, y, name, icon, task_item, body, tier, pre, mod, finale = e
        if icon is None:  # info quest: (None, icon) means a checkbox task with that icon
            icon, task_item = task_item, None
        b64, hi, lo = ids[key]
        f = f'{file_prefix}-{no:02d}.json'
        p = {"autoClaim:1": 0, "globalShare:1": 0, "isMain:1": 0, "isSilent:1": 0, "lockedProgress:1": 0,
             "questLogic:8": "AND", "repeatTime:3": -1, "repeat_relative:1": 1, "simultaneous:1": 0,
             "snd_complete:8": "random.levelup", "snd_update:8": "random.levelup", "taskLogic:8": "AND",
             "visibility:8": "NORMAL", "name:8": name,
             "desc:8": f"§b{name}§r\n\n{body}\n\n§aTask§r: {HAVE if task_item else READ}", "icon:10": icon}
        q = {"properties:10": {"betterquesting:10": p}, "questIDHigh:4": hi, "questIDLow:4": lo}
        if task_item:
            q["tasks:9"] = {"0:10": {"index:3": 0, "taskID:8": "bq_standard:retrieval", "autoConsume:1": 0,
                                     "consume:1": 0, "groupDetect:1": 0, "ignoreNBT:1": 1, "partialMatch:1": 0,
                                     "requireOnlyOneItem:1": 0, "requiredItems:9": {"0:10": task_item}}}
        else:
            q["tasks:9"] = {"0:10": {"index:3": 0, "taskID:8": "bq_standard:checkbox"}}
        pr = {}
        for k, r in enumerate(pre):
            h, l = (ids[r][1], ids[r][2]) if isinstance(r, str) else existing(*r)
            pr[f"{k}:10"] = {"questIDHigh:4": h, "questIDLow:4": l}
        if pr:
            q["preRequisites:9"] = pr
        tb = TIERBAG[tier]
        stage = TIERBAG_STAGE[tb]
        base = [bag(tb, 2 if tier == 6 else 1)]
        if finale:
            kind = 'finale'
            set_rewards(q, base + [bag(111), bag(14), item(IRIDIUM, 0, 3)])
        elif key in row_end:
            kind = 'row end'
            set_rewards(q, base + [bag(stage + 1, 3), item(IRIDIUM)])
        else:
            kind = 'choice' if nth % 5 == 4 else ''
            set_rewards(q, base, [bag(stage), item(IRIDIUM)] if kind else None)
            nth += 1
        json.dump(q, open(f'{R}/{ch}/quests/{f}', 'w'), indent=2, ensure_ascii=False)
        json.dump({"questIDHigh:4": hi, "questIDLow:4": lo, "sizeX:3": 24, "sizeY:3": 24, "x:3": x, "y:3": y},
                  open(f'{R}/{ch}/placements/{f}', 'w'), indent=2)
        index_lines = [l for l in index_lines if f"\t{f}\t" not in l] + [f"{b64}\t{f}\t{f}\t{mod}"]
        made.append((ch[:4], f, name, tier, kind))
    open(f'{R}/{ch}/index.tsv', 'w').write('\n'.join(index_lines) + '\n')
    return made


def next_no(ch, prefix):
    nos = [int(f[len(prefix) + 1:-5]) for f in os.listdir(f'{R}/{ch}/quests') if f.startswith(prefix + '-')]
    return max(nos) + 1


if __name__ == '__main__':
    out = []
    out += build(CH9, GTSR, '09', next_no(CH9, '09'))
    out += build(CH3, MESS, '03', next_no(CH3, '03'))
    os.makedirs(f'{R}/{CH22}/quests', exist_ok=True)
    os.makedirs(f'{R}/{CH22}/placements', exist_ok=True)
    if not os.path.exists(f'{R}/{CH22}/index.tsv'):
        open(f'{R}/{CH22}/index.tsv', 'w').write('# quest UUID (base64url)\tquest file\tplacement file\tmod id\n')
    out += build(CH22, NEW22, '22', 1, row_ends={'tk_reso', 'mb_pixel'})
    cb64, chi, clo = qid('chapter-22')
    json.dump({"properties:10": {"betterquesting:10": {
        "bg_image:8": "", "bg_size:3": 256,
        "desc:8": "TenkeiTech's ME helpers (pattern buffers, template buses, wireless ME networks, the ME Requester and "
                  "interface cards) and GT Miao Blueprint's hologram projector (import, save, share, cut, build and "
                  "dismantle multiblocks). Each row only appears when its mod is installed.",
        "icon:10": item('gtmb:neko_hologram_projector'), "name:8": "Chapter 22: Blueprints & ME Tools",
        "visibility:8": "NORMAL"}}, "questLineIDHigh:4": chi, "questLineIDLow:4": clo},
        open(f'{R}/{CH22}/QuestLine.json', 'w'), indent=2, ensure_ascii=False)
    lines = open(f'{R}/chapters.tsv').read().rstrip('\n').split('\n')
    if not any(l.startswith(CH22 + '\t') for l in lines):
        lines.append(f'{CH22}\t{cb64}\t21')
    open(f'{R}/chapters.tsv', 'w').write('\n'.join(lines) + '\n')
    for m in out:
        print(*m, sep='\t')
    print(len(out), 'quests')
