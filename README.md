# GTNH Quest Chapter Injectors

Independent Better Questing chapter injectors for GTNH 2.9.0 RC2.

## Chapter 2 — Fission-Evolved

Latest local test build: `GTNH-Chapter02-Fission-Evolved-v3.4.0-REAL-ITEM-FIX-TEST.jar`.

- Independent Chapter 2 questline (11 quests) with fixed chapter and quest identifiers.
- Designed to preserve existing Chapter 1 data and player quest progress.
- Actual Fission-Evolved controller and fuel-rod items for icons and non-consuming retrieval tasks.
- Rewards: food lootbag and a choice of Technician or Neko coins.

**Testing status:** The build has not been confirmed fully working in-game after the v3.4 item-ID fix. Back up world data before testing. Do not run `/bq_admin default load`.

This repository is being initialized for the chapter injector source. Binary artifacts should be uploaded as GitHub Release assets when available.

## GTNH Addon Quests 9.1.0

`jar-contents/` is the unpacked 9.1.0 jar (quest JSON, placements and the merge classes). The original Python
generator from earlier versions was never pushed; `tools/rebalance.py` is the script that turned 9.0.0 into 9.1.0:

- Rewards: normal quests give their tier bag only, every fifth one adds a small choice (stage seed bag or half the
  coins), the last quest in each row gives the tier bag plus 3 Fortune seed bags, finales are unchanged, and
  Chapter 21 (My Mods) has no rewards.
- Chapter 1: new quests for the GT-Not-Hard research path (Alien Artifacts, Array Module, Singularity module,
  Ancient Word and Book), the Breeding Greenhouse and the Soul Crusher. Chaos and Origin need the Tier I artifact
  quest, the Singularity the Tier II one.
- Rebalance notes on the GT-Not-Hard and My Mods quests.

To rebuild the jar: `cd jar-contents && zip -qr -X ../GTNH-Addon-Quests-v9.1.0.jar .`
