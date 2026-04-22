# PanoSphere — 360° Virtual Tour Studio

A fully offline Flask web app for creating interactive 360° virtual tours
with the Photo Sphere Viewer library and all its plugins.

## Features

- **Upload Manager** — drag-and-drop 360° panoramas (JPG/PNG/WEBP, up to 200MB each)
- **Full PSV Viewer** — all plugins: Virtual Tour, Markers, Compass, Auto-rotate, Gallery
- **Matrix Room Planner** — visually arrange panoramas in a grid; auto-generates
  directional links (N/S/E/W arrows) between adjacent cells
- **Manual Link Editor** — fine-tune any link's target, yaw, and pitch
- **Persistent storage** — tour saved as `tour_data.json` on disk

## Setup

```bash
# 1. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the server
python app.py
```

Then open **http://localhost:5000** in Chrome or Edge.

> Firefox works too, but Chrome/Edge give the best WebGL performance for PSV.

## How to build a tour

### Step 1 — Upload panoramas
- Click the **Panos** tab (globe icon in the sidebar)
- Drag your equirectangular 360° images into the drop zone, or click to browse
- Each panorama appears in the library list; click its name to rename it

### Step 2 — Arrange in Matrix (recommended)
- Click the **Matrix** tab (grid icon)
- Set the number of rows and columns for your floor plan
- Drag panoramas from the library onto grid cells, or click a cell then click a panorama
- Click **Save Links** — the app automatically links adjacent rooms with directional arrows

### Step 3 — Fine-tune links (optional)
- Click the **Links** tab (chain icon)
- With a panorama loaded in the viewer, edit any link's yaw/pitch to position arrows precisely
- Add or delete manual links as needed

### Step 4 — Launch the tour
- Click the **Tour** button (play icon) to enter fullscreen tour mode
- Use the PSV gallery (bottom bar) to jump between panoramas
- The compass and auto-rotate controls are in the navbar

## File structure

```
psv-tour/
├── app.py              ← Flask backend
├── requirements.txt
├── tour_data.json      ← auto-created, stores tour state
├── templates/
│   └── index.html      ← full frontend
└── static/
    └── uploads/        ← your panorama images stored here
```

## Notes on panorama images

- Images must be **equirectangular** format (2:1 aspect ratio, e.g. 4096×2048)
- Most 360° cameras export this automatically (Ricoh Theta, Insta360, GoPro Max)
- For phone photos, use PTGui, Hugin, or Google Street View app to stitch
- Recommended size: 4096×2048 for quality, 2048×1024 for faster loading
