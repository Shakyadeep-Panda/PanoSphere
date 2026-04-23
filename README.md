<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:00d4ff,100:ff6b35&height=200&section=header&text=PanoSphere&fontSize=72&fontColor=ffffff&fontAlignY=38&desc=360°%20Virtual%20Tour%20Studio&descAlignY=58&descSize=20&animation=fadeIn" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.10%2B-00d4ff?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-ff6b35?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![PSV](https://img.shields.io/badge/Photo%20Sphere%20Viewer-5.x-7fff6b?style=for-the-badge&logo=javascript&logoColor=black)](https://photo-sphere-viewer.js.org)
[![License](https://img.shields.io/badge/License-MIT-white?style=for-the-badge)](LICENSE)

<br/>

> **Build immersive, interactive 360° virtual tours — entirely in your browser. No cloud. No subscription. Just drop your panoramas and go.**

<br/>

[🚀 Live Demo](#-live-demo) • [✨ Features](#-features) • [⚡ Quick Start](#-quick-start) • [🗺️ How It Works](#️-how-it-works) • [📁 Project Structure](#-project-structure) • [🛠️ Tech Stack](#️-tech-stack)

<br/>

</div>

---

## 🌐 Live Demo

> 🔗 **[panosphere.onrender.com](https://panosphere.onrender.com)** *(may take ~30s to wake from sleep on free tier)*

<br/>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🖼️ Upload Manager
- Drag-and-drop 360° panoramas
- Supports JPG, PNG, WEBP, GIF
- Up to **200MB per image**
- Auto-generates unique room IDs

</td>
<td width="50%">

### 🧭 Full PSV Viewer
- Powered by **Photo Sphere Viewer v5**
- Virtual Tour, Markers, Compass plugins
- Auto-rotate & Gallery support
- Smooth WebGL rendering

</td>
</tr>
<tr>
<td width="50%">

### 🗺️ Matrix Room Planner
- Visual grid-based floor planner
- Drag panoramas onto grid cells
- **Auto-generates N/S/E/W links** between adjacent rooms
- One click to save the entire layout

</td>
<td width="50%">

### 🔗 Manual Link Editor
- Fine-tune any link's `yaw` and `pitch`
- Add or remove directional arrows
- Mix auto-links with hand-crafted ones
- Per-node link management

</td>
</tr>
<tr>
<td width="50%">

### 📦 Export & Import Tours
- Download any tour as a single **ZIP file**
- ZIP includes all panoramas + tour data
- Import a ZIP to instantly restore a full tour
- Share tours with anyone — one file, zero setup

</td>
<td width="50%">

### ✏️ Tour & Panorama Renaming
- Click any panorama name to rename it inline
- Rename tours directly from the topbar input
- Press **Enter** or click away to save
- Press **Escape** to cancel

</td>
</tr>
<tr>
<td width="50%">

### 📱 Mobile Responsive
- Fully functional on phones and tablets
- Smart stacked layout: Nav → Viewer → Panel
- **⚙ Gear button** opens a slide-up drawer with all tour controls
- All features accessible on mobile

</td>
<td width="50%">

### 🔒 Session Isolation
- Each browser tab gets its own unique session tour
- Multiple users never share or overwrite each other's uploads
- Session persists on refresh, resets on tab close

</td>
</tr>
</table>

---

## ⚡ Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/panosphere.git
cd panosphere

# 2. Create & activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open **[http://localhost:5000](http://localhost:5000)** in Chrome or Edge.

> 💡 Firefox works too, but Chrome/Edge give the best WebGL performance for PSV.

---

## 🗺️ How It Works

```
┌─────────────────────────────────────────────────────────┐
│                     PanoSphere Flow                     │
├──────────────┬──────────────┬──────────────┬────────────┤
│  1. UPLOAD   │  2. ARRANGE  │  3. LINK     │  4. TOUR   │
│              │              │              │            │
│  Drop your   │  Place rooms │  Auto-gen    │  Walk      │
│  equirect-   │  on a grid   │  N/S/E/W     │  through   │
│  angular     │  floor plan  │  arrows or   │  your      │
│  panoramas   │  matrix      │  manual tune │  space!    │
└──────────────┴──────────────┴──────────────┴────────────┘
```

### Step 1 — Upload Panoramas
Click the **Panos** tab (🌐 globe icon) → drag your equirectangular 360° images into the drop zone.

### Step 2 — Arrange in Matrix
Click the **Matrix** tab (⊞ grid icon) → set rows/columns → drag panoramas onto cells.

### Step 3 — Save Links
Click **Save Links** — adjacent rooms are automatically connected with directional arrows.

### Step 4 — Launch Tour
Click the **Tour** button (▶ play icon) to enter fullscreen immersive mode.

### Step 5 — Export & Share *(new)*
Click **⬇ Export** to download the entire tour as a ZIP. Anyone can **⬆ Import** it to instantly load all panoramas and links.

---

## 📁 Project Structure

```
panosphere/
│
├── app.py                  ← Flask backend (API + file handling)
├── requirements.txt        ← Python dependencies
├── render.yaml             ← Render deployment config
│
├── templates/
│   └── index.html          ← Full frontend (PSV + UI)
│
├── static/
│   └── uploads/            ← User-uploaded panorama images
│
└── tours/
    └── *.json              ← Saved tour data (nodes + matrix)
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.10+, Flask 3.0 |
| **Frontend** | Vanilla JS, CSS3 |
| **360° Viewer** | [Photo Sphere Viewer v5](https://photo-sphere-viewer.js.org) |
| **Plugins** | Virtual Tour, Markers, Compass, Auto-rotate, Gallery |
| **Export/Import** | Python `zipfile` + `io.BytesIO` |
| **Storage** | Local filesystem (ephemeral on Render free tier) |
| **Hosting** | [Render](https://render.com) |

---

## 📸 Panorama Image Requirements

| Property | Requirement |
|---|---|
| **Format** | Equirectangular (2:1 aspect ratio) |
| **Recommended size** | 4096×2048 (quality) or 2048×1024 (fast) |
| **File types** | JPG, PNG, WEBP, GIF |
| **Max size** | 200MB per image |

> 📷 Most 360° cameras export this automatically — Ricoh Theta, Insta360, GoPro Max.  
> 🖥️ For phone photos, use **PTGui**, **Hugin**, or the **Google Street View** app to stitch.

---

## 🚀 Deploy to Render

<details>
<summary><b>Click to expand deployment steps</b></summary>

<br/>

**1. Add `gunicorn` to `requirements.txt`:**
```
flask>=3.0.0
werkzeug>=3.0.0
gunicorn>=21.0.0
```

**2. Create `render.yaml`:**
```yaml
services:
  - type: web
    name: panosphere
    runtime: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn app:app --workers 2 --bind 0.0.0.0:$PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

**3. Push to GitHub → Connect on [render.com](https://render.com) → Deploy ✅**

> ⚠️ Free tier uses ephemeral storage — uploads reset on restart. Use the **Export ZIP** feature to save your tours locally before the server sleeps.

</details>

---

## 💡 Tips

- **Session isolation** — each browser tab has its own tour. Open a new tab for a fresh workspace.
- **Saving your work** — always hit **⬇ Export** before closing. The free Render tier resets files on sleep.
- **Renaming** — click directly on any panorama name or the tour rename input to edit inline.
- **Mobile** — tap ⚙ in the top bar to access all tour controls in the slide-up drawer.

---

## 👥 Author

> Built as a Personal Final Year Project at **GITA Autonomous College, Bhubaneswar**

| Name | Role |
|---|---|
| Shakyadeep Panda | Aspiring Full Stack Developer |

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify, and distribute.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:ff6b35,100:00d4ff&height=120&section=footer" width="100%"/>

**Made with ❤️ using Flask + Photo Sphere Viewer**

⭐ *If you found this useful, consider giving it a star!* ⭐

</div>
