[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b18-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b18-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

A dense front-page image summing up the world's news of Monday 23 November 2026:
31 stories across 6 regions, led by the day's three biggest stories — the AI rout
hitting Asia (KOSPI -3.3%), Guterres urging the world to regulate AI before it is
too late, and the US lead over China falling to a record low (Asia Power Index gap 5.3).

## How it is built

`draw.py` (PIL, stdlib-only drawing) renders `entry.png` (1024×1024, < 1 MiB):
masthead, kanon number strip (-3.3% / 5.3 / 11,762 / 10T won / 2% / $450M / 165 /
107.3B), region bar, THE DAY IN UTC strip, 3 hero scenes, 10 small illustrated
cards, a world map with 31 numbered pins, an ALSO list, a DATE CHECK box
(wires read up to 23:00 UTC; excluded items dated; not-yet items listed), and a
sources + certainty-chip legend.

`main.py` copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`, verifying the
1024×1024 size, the 1 MiB limit, and the sha256 checksum. It never writes
anything next to itself.

## Verification

- `python3 draw.py` → `entry.png` (199,398 bytes, sha256 `dab1d9ede5468e79b3bc041090d4e56cfc81c50eeb64df60ad012858e6efb40a`)
- `main.py` run twice from a different cwd with `MAKEFUN_OUTPUT_DIR` pointed at
  an empty dir: byte-identical output, exit 0
- `main.py` run twice against a read-only copy of the repo: exit 0, repo unchanged

## License

MIT — see `LICENSE`. SPDX-License-Identifier: MIT.
