## Paint App (Tkinter)

Jednoduchý rastrový paint program v Pythonu podobný Microsoft paint. Aplikace vykresluje tvary vlastními algoritmy (bez externích grafických knihoven pro kreslení), drží seznam objektů a renderuje je do pixelového rastru.

## Spuštění

Požadavky:
- Python 3.10+
- Tkinter (běžně součást standardní instalace Pythonu)

Spuštění:

```bash
python3 main.pyw
```

## Technický popis

### Architektura projektu

- `ui/`
	- `app.py`: hlavní třída `PaintApp`, správa canvasu, event bindingy, přepínání nástrojů, plánování renderu.
	- `toolbar.py`: horní panel (výběr nástroje, tloušťka, barva, clear).
- `models/`
	- datové modely: `Point`, `Shape`, `Line`, `Rectangle`, `Oval`, `Polygon`, `Fill`.
	- `LineStyle` (SOLID, DOTTED, DASHED).
- `tools/`
	- logika interakce uživatele (klik, tah, klávesy) pro jednotlivé nástroje.
- `rasterizers/`
	- převod modelu tvaru na pixely (`LineRasterizer`, `RectangleRasterizer`, `OvalRasterizer`, `PolygonRasterizer`, `FillRasterizer`).
	- `CanvasRasterizer`: skládání všech tvarů, cache pixelů, hit-test, fill operace.
- `rasters/`
	- `Raster`: správa RGB bufferu (`bytearray`), `set_pixel/get_pixel`, export do `PhotoImage` přes dočasný PPM soubor.

### Render pipeline

1. Nástroj vytvoří nebo upraví model tvaru
2. `CanvasRasterizer.mark_dirty()` označí změněný tvar
3. `PaintApp.render()` naplánuje render přes `after_idle` (omezování zbytečných překreslení)
4. `CanvasRasterizer.render_all()` přerasterizuje pouze dirty tvary do cache
5. Všechny cachované segmenty pixelů se složí do bufferu rastru
6. Buffer se převede na `PhotoImage` a nastaví se do Tkinter canvasu

## Uživatelský návod

### Základní ovládání myší

- Levé tlačítko: kreslení/umístění bodů/akce aktivního nástroje.
- Tah s levým tlačítkem: průběžné úpravy (např. délka čáry, velikost obdélníku, přesun).
- Pravé tlačítko: uzavření polygonu (když má alespoň 3 body).

### Panel nástrojů

- `Tools`: výběr aktivního nástroje.
- `Size`: tloušťka stopy/čáry (1-20).
- `Color`: předdefinovaná paleta, vlastní výběr (`Pick Color`), poslední vlastní barva (`Last Custom`).
- `Clear`: vyčistí plátno.

### Klávesové zkratky nástrojů

- `L` -> Line
- `R` -> Rectangle
- `O` -> Oval
- `P` -> Polygon
- `F` -> Fill
- `E` -> Erase
- `M` -> Move

### Klávesové Modifikátory

- `Ctrl`: tečkovaný styl čáry
- `Alt`: přerušovaný styl čáry
- `Shift`: perfektní zarovnání (čára se zarovnává po 45°, z oválu se stane perfektní kruh, z libovolného obdélníku se stane čtverec, ...)

#### Erase

- Bez `Ctrl`: mazání celého objektu pod kurzorem
- S držením `Ctrl`: maže pixely

#### Move

- Bez `Ctrl`: přesun celého objektu
- S držením `Ctrl`: modifikace bodů/rohů

### Polygon workflow

1. Zvolit `Polygon` (`P`)
2. Levým klikem přidávat vrcholy
3. Dokončení:
	 - pravým klikem, nebo
	 - levým klikem blízko prvního bodu
	 - při opuštění nástroje se polygon s >=3 body uzavře automaticky
