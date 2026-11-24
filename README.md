[![make.fun · news-image-20261123](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/akbare12/news-23-b18-front-page-dense/rank.svg)](https://make.fun/bounty/news-image-20261123/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/akbare12/news-23-b18-front-page-dense/reward.svg)](https://make.fun/bounty/news-image-20261123?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261123)

# THE WORLD TODAY — Monday 23 November 2026

A one-page front page summing up 23 November's world news in a single image:
31 stories across 6 regions, with a number strip, three hero scenes, ten
story cards, a world map with numbered pins, an ALSO list, and a DATE CHECK
box that keeps out stories from other days.

## The day in brief

- **AI rout hits Asia** — the Kospi falls 3.3% to 4,708.54, shedding 161 points
  (intraday low −5.8%); Samsung −3.1%, SK Hynix −2.5%.
- **Guterres: regulate AI before it's too late** — at the Bridgetown summit,
  150 delegates back a risk framework (a blueprint, not a treaty).
- **US lead over China at record low** — Asia Power Index 2026: US 78.9,
  China 73.6, a gap of 5.3, the narrowest since 2018; India third at 40.5.

Also inside: Anthropic's $107.3B IPO (raised at $83 a share), Skubal's $450M
Mets deal, the FBI's NCIC hack probe, Poland's claim that three Russian
Kh-101 missiles crossed its airspace, and 18 more stories from Paris to Seoul.

Chips: **REPORTED** = confirmed by wires · **CLAIM** = one side's claim, not
independently confirmed · **ONGOING** = still developing. Scenes are drawn
illustrations, not photographs.

## Build

`draw.py` (PIL) renders `entry.png` (1024×1024). `main.py` (stdlib only)
validates the PNG header and copies it to `$MAKEFUN_OUTPUT_DIR/entry.png`:

```sh
python3 draw.py
MAKEFUN_OUTPUT_DIR=out python3 main.py
```
