# Plan: Interactive Geometry Viewer for GitHub Pages

## Goal

Convert the Python matplotlib interactive tool (`hippie-hideout-interactive.py`) into a browser-based page that can be hosted on GitHub Pages. One slider controls roof pitch (20°–35°) and both views — cross-section and floor plan — update in real time.

## What Already Exists

- **`dome-viewer.html`** — Full 3D Three.js viewer with wing parameters, camera presets, cutaway mode. Already has `wingAngle`, `wingWidth`, `wingDepth`, wall heights, etc. as adjustable parameters.
- **`hippie-hideout-interactive.py`** — Python dual-view (cross-section + floor plan) driven by a roof pitch slider. This is what we're porting to the web.

## Approach: Single HTML File with Canvas

Keep it simple like `dome-viewer.html` — one self-contained HTML file, no build tools, no dependencies beyond what's loaded from CDN.

### Tech Stack

- **HTML5 Canvas** (2D) — no need for Three.js, these are 2D diagrams
- **Vanilla JS** — all geometry logic ports directly from the Python (it's just trig)
- **HTML range input** — for the roof pitch slider
- **No framework** — stays consistent with the existing `dome-viewer.html` pattern

### Page Layout

```
┌──────────────────────────────────────────────────────┐
│  Hippie Hideout — Roof Pitch Geometry Explorer        │
├──────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────────┐    ┌─────────────────┐          │
│  │                 │    │                 │          │
│  │  Cross-Section  │    │   Floor Plan    │          │
│  │  (Side View)    │    │  (Top Down)     │          │
│  │                 │    │                 │          │
│  └─────────────────┘    └─────────────────┘          │
│                                                      │
│  ═══════════════════════════════════════════          │
│  Roof Pitch: [====●===========] 25°                  │
│                                                      │
│  ┌──────────────────────────────────────────┐        │
│  │ Summary:                                  │        │
│  │   Wing room: 17.2'  |  Extension: 8.6'   │        │
│  │   Total span: 25.7' |  Rafter: 28.4'     │        │
│  └──────────────────────────────────────────┘        │
│                                                      │
│  [Export PNG]  [Export PDF]  [Share Link]             │
└──────────────────────────────────────────────────────┘
```

### Implementation Steps

#### 1. Geometry Engine (JS)

Port `compute_geometry()` from Python — it's just five lines of trig:

```javascript
function computeGeometry(pitchDeg) {
    const rad = pitchDeg * Math.PI / 180;
    const horizSpan = 12 / Math.tan(rad);
    const wallX = 8 / Math.tan(rad);
    const rafterLen = 12 / Math.sin(rad);
    const rightSection = horizSpan - wallX;
    return { pitchDeg, rad, horizSpan, wallX, rafterLen, rightSection };
}
```

#### 2. Cross-Section Renderer

Port `draw_cross_section()` to Canvas 2D:
- Ground line, left wall (20'), right post (8'), roof line, interior wall (12')
- Dimension arrows and labels
- Angle arc at top-left corner
- Grid lines

#### 3. Floor Plan Renderer

Port `draw_floorplan()` to Canvas 2D:
- Dome circle (r=16.5)
- Right wing: connection point at 20° above horizontal, 30' back wall at -25°, perpendicular wing wall (dynamic length), extension to post (dynamic length), wall back to dome (quadratic intersection)
- Left wing: mirror of right
- Front entry rectangle + arc between posts
- All dimension labels update with pitch

#### 4. Slider + Live Update

```html
<input type="range" min="20" max="35" step="0.5" value="20" id="pitch-slider">
```

On `input` event: recompute geometry, clear both canvases, redraw both views, update summary text.

#### 5. Export Features

- **Export PNG**: `canvas.toBlob()` → download link (one for each canvas, or stitch both into one)
- **Share Link**: Encode pitch angle in URL hash (`#pitch=25`) so links are shareable
- **Print**: CSS `@media print` styles for clean output

#### 6. Mobile Responsive

- Stack canvases vertically on narrow screens
- Touch-friendly slider
- Canvas sizes adapt to viewport

### File Structure

```
domes/
├── dome-viewer.html              # existing 3D viewer
├── geometry-explorer.html        # NEW — the 2D interactive page
├── hippie-hideout-interactive.py # Python source (reference)
├── hippie-hideout-floorplan.py   # Python source (reference)
├── hippie-hideout-crosssection.py# Python source (reference)
└── ...
```

### GitHub Pages Setup

1. Create a GitHub repo (or add remote to existing local repo)
2. Enable GitHub Pages from Settings → Pages → Deploy from branch `main`
3. `geometry-explorer.html` is accessible at `https://<user>.github.io/domes/geometry-explorer.html`
4. Optionally add an `index.html` that links to both the 3D viewer and the geometry explorer

### Constants (from Python)

| Constant | Value | Description |
|----------|-------|-------------|
| `LEFT_WALL_H` | 20.0 | Dome wall height (feet) |
| `RIGHT_POST_H` | 8.0 | Post height (feet) |
| `ROOF_DROP` | 12.0 | Height difference |
| `INTERIOR_WALL_H` | 12.0 | Interior wall height |
| `BACK_WALL_LEN` | 30.0 | Back wall length (fixed) |
| `DOME_R` | 16.5 | Dome radius |
| `CONN_ANGLE` | 20° | Wing attachment angle above horizontal |
| `WALL_ANGLE` | -25° | Back wall angle below horizontal |

### Key Derived Values by Pitch

| Pitch | Wing Room | Extension | Total Span | Rafter | Bottom Wall |
|-------|-----------|-----------|------------|--------|-------------|
| 20° | 22.0' | 11.0' | 33.0' | 35.1' | 28.8' |
| 25° | 17.2' | 8.6' | 25.7' | 28.4' | ~23' |
| 30° | 13.9' | 6.9' | 20.8' | 24.0' | ~18' |
| 35° | 11.4' | 5.7' | 17.1' | 20.9' | ~15' |

### Nice-to-Haves (later)

- Side-by-side comparison of two pitch angles
- Area calculation for each wing
- Integration with the 3D dome-viewer (link to open same config in 3D)
- Animated sweep (CSS transition on redraw for smooth sliding)
