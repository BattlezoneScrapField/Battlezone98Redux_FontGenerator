# Battlezone 98 Redux Font Sheet Generator
A lightweight tool for modders to create custom `bzone.png` font atlases.

Developed by **GrizzlyOne95**.

## Features
- **Dual Font Support:** Use one font for letters and another for numbers/symbols.
- **Auto-Alignment:** Automatically sit characters on the correct baseline for the BZ98 engine.
- **Modern Resolution:** Generates a 1024x1024 RGBA texture from scratch.
- **Drag-and-Drop Ready:** Outputs as `bzone.png` for immediate use in game assets.

## How to Use
### For Users
1. Download the latest `bz_generator.exe` from the [Releases](../../releases) section.
2. Run the application.
3. Select your desired `.ttf` or `.otf` font files.
4. Click **Generate BZONE.PNG**.
5. Copy the resulting `bzone.png` into your mod's texture directory.

### For Developers
If you want to run from source:
1. Clone this repo.
2. Install dependencies: `pip install -r requirements.txt`.
3. Run: `python bz_generator.py`.

## Credits
- **Tool Development:** GrizzlyOne95
- **Default Font:** Orbitron (Open Font License)
- **Engine Compatibility:** Battlezone 98 Redux

## License
MIT License - See [LICENSE](LICENSE) for details.
