# 📊 Air Presenter v5.2 — Single-Slide Precision Maestro

A high-reliability spatial gesture controller built for **Microsoft PowerPoint**, **Google Slides**, and **PDF presentations**.

---

## 🖐️ Core Gestures

1. ✌️ **Show 2 FINGERS (Index + Middle / Peace Sign)**:
   - Advances **strictly ONE slide forward** (`Right Arrow`).
   - Hard lock: will **never** skip multiple slides!
   - To advance the next slide, lower your fingers or close your hand, then show 2 fingers again.

2. 🤟 **Show 3 FINGERS (Index + Middle + Ring)**:
   - Rewinds **strictly ONE slide backward** (`Left Arrow`).
   - Lower fingers to reset for the next slide.

3. 👍 **Show THUMBS UP**:
   - **Immediately ends the PowerPoint presentation / slideshow** (`Escape` key).
   - Confident, natural gesture to wrap up keynotes with style!

4. 🖐️ **Show FULL PALM (5 Fingers) [Hold 0.7s]**:
   - Launches PowerPoint Slideshow / Fullscreen (`F5`).

5. ✊ **CLOSED FIST (0 Fingers) [Hold 0.6s]**:
   - Toggles **Speaker Focus** (Blacks out the screen with PowerPoint's `'B'` key to draw audience attention to you).

---

## ⌨️ Hotkeys & Shortcuts

- **`[P]`**: **Toggle Picture-in-Picture (PiP) Mini Mode** (Shrinks into a corner widget so PowerPoint is completely visible)
- **`[T]`**: **Toggle Always-On-Top** (Pins the widget floating on top of PowerPoint)
- **`[D]`**: Toggle Built-in Demo Deck / Desktop Only View
- **`[M]`**: Mute / Unmute synthesized sound effects
- **`[H]`**: Toggle Hand Skeleton Landmark Overlay
- **`[Space]`** or **`[N]`**: Manual keyboard passthrough to advance slide
- **`[Q]`** or **`[Esc]`**: Exit cleanly

---

## 🚀 How to Run

1. Open your presentation in **Microsoft PowerPoint**.
2. Run from your terminal:
   ```bash
   & .venv\Scripts\python.exe air_presenter.py
   ```
   *(Or double-click [run_presenter.bat](file:///c:/Users/shash/Documents/antigravity/run_presenter.bat))*
3. Press **`[P]`** on Air Presenter to shrink it to the corner, and press **`[T]`** to keep it on top.
4. Controls:
   - Show **2 fingers ✌️** to go forward 1 slide.
   - Show **3 fingers 🤟** to go back 1 slide.
   - Show **Thumbs Up 👍** to end the presentation!
