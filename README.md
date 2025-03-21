![Release Version](https://img.shields.io/github/v/release/guilhermefaga/hero-siege-stats) ![Total Downloads](https://img.shields.io/github/downloads/guilhermefaga/hero-siege-stats/total.svg)

# Hero Siege Stats

This is a simple tool that tracks the requests made between the game and the server and displays them in a nice way.

### App preview

![App preview](/assets/readme/preview.png)

## Features

- Session time and session reset button
- Mailbox notification
- Gold earned and gold per hour
- XP earned and XP per hour
- Items picked up (Angelic, Heroic and Satanic) (Blue number means Magic Find drops)
- Shows Satanic Zone with Buffs(Hover over Buff icons for tooltip with Buffdescriptions)
- Adapt to game server IP changes

## Limitations

- Gold picked up from mailbox is counted as gold earned
- XP earned can be wrong when leveling up (would need the max XP for each level)
- Items moved between inventories are counted as picked up
- Items dropped by players are counted as picked up

## Is this allowed?

![image](https://github.com/GuilhermeFaga/hero-siege-stats/assets/32572430/56a116cb-66b1-45de-afa9-3d3dc7a2ea6c)


## How to use

1. On Windows make sure that WinPcap is installed in your system. [Npcap downloads page](https://npcap.com/#download) | [Direct link](https://npcap.com/dist/npcap-1.77.exe).

2. Download the latest release from the [releases page](https://github.com/GuilhermeFaga/hero-siege-stats/releases) and run it.

3. Start the game and play a bit. Some stats only update after changing maps.

## Roadmap

- [X] Items drop counter
  - [X] Angelic items
  - [X] Unholy items
  - [X] Heroic items
  - [X] Satanic items
- [ ] XP percentage
- [ ] Fortune mission counter
- [ ] Mercenary alive status

# Instructions for developers

## Running from source

### Requirements

- [Python 3.11](https://www.python.org/downloads/release/python-3116/)
- [Poetry](https://python-poetry.org/)

### Steps

1. Clone the repository
2. Run `poetry install`
3. Run `poetry run python hero-siege-stats.py`

## Building from source

### Requirements

Same as running from source.

### Steps

1. Clone the repository
2. Run `poetry install`
3. Run `poetry run py build.py`
4. The executable will be in the `dist` folder

## Contributors

- [Guilherme Faga](https://faga.dev)
- [Skijearz](https://github.com/Skijearz)
- [Elliot Chen](https://github.com/keoy7am)

Thanks to **Shalwkz** for helping me with finding the game server address.

Highly inspired by [Albion Online Stats](https://github.com/mazurwiktor/albion-online-stats).
