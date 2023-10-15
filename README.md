# Hero Siege Stats

This is a simple tool that tracks the requests made between the game and the server and displays them in a nice way.

### App preview

![App preview](/assets/readme/preview.jpg)

## How to use

1. Download the latest release from the [releases page]() and run it.

2. Start the game and play a bit. Some stats only update after changing maps.

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
