![Release Version](https://img.shields.io/github/v/release/guilhermefaga/hero-siege-stats) ![Total Downloads](https://img.shields.io/github/downloads/guilhermefaga/hero-siege-stats/total.svg)

# Hero Siege Stats

This is a simple tool that tracks the requests made between the game and the server and displays them in a nice way.

### App preview

![App preview](/assets/readme/preview.jpg)

## Features

- Session time
- Mailbox notification
- Gold earned and gold per hour
- XP earned and XP per hour
- Items picked up (Angelic, Heroic and Satanic) (Blue number means Magic Find drops)
 
## Limitations

- Gold picked up from mailbox is counted as gold earned
- XP earned can be wrong when leveling up (would need the max XP for each level)
- Items moved between inventories are counted as picked up
- Items dropped by players are counted as picked up

## How to use

1. On Windows make sure that WinPcap is installed in your system. [Npcap downloads page](https://npcap.com/#download) | [Direct link](https://npcap.com/dist/npcap-1.77.exe).

2. Download the latest release from the [releases page](https://github.com/GuilhermeFaga/hero-siege-stats/releases) and run it.

3. Start the game and play a bit. Some stats only update after changing maps.

## Roadmap

- [X] Support for all login regions
  - [x] Mevius (America)
  - [x] Inoya (Europe 1)
  - [x] Damien (Europe 2)
  - [X] Karponia (Asia)
- [ ] Session reset button
- [x] Items drop counter
- [ ] XP percentage

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

## Author

- [Guilherme Faga](https://faga.dev)

Thanks to **Shalwkz** for helping me with finding the game server address.

Highly inspired by [Albion Online Stats](https://github.com/mazurwiktor/albion-online-stats).
