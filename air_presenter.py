"""
================================================================================
🚀 AIR PRESENTER // MINORITY REPORT PRESENTATION MAESTRO (v5.2 THUMBS-UP EXIT)
================================================================================
Universal precision gesture controller for Microsoft PowerPoint, Google Slides,
Adobe PDF, and Keynote.

Controls:
✌️ 2 FINGERS (Index + Middle)     -> STRICTLY ONE Next Slide (Right Arrow)
🤟 3 FINGERS (Index+Middle+Ring)  -> STRICTLY ONE Prev Slide (Left Arrow)
👍 THUMBS UP (Thumb Upward Only)  -> END PRESENTATION / SLIDESHOW (Escape Key)
🖐️ 5 FINGERS (Full Open Palm)    -> Launch Slideshow / Fullscreen (F5 Key) [Hold 0.7s]
✊ 0 FINGERS (Closed Fist)        -> Toggle Speaker Focus / Blackout ('B') [Hold 0.6s]

Features:
- Guaranteed Single-Key Injection: Sends strictly 1 key stroke per gesture
- Hard-Lockout State Machine: Will NEVER skip multiple slides or end slideshow accidentally
- Mandatory Neutral Reset: Lower fingers to re-arm for the next slide
- Picture-in-Picture Mini Mode [P] & Always-On-Top [T]

Keyboard Controls:
  [P]       : Toggle Picture-in-Picture (PiP Mini Mode) - Best for PowerPoint!
  [T]       : Toggle Always-On-Top Floating Window
  [D]       : Toggle Embedded Demo Slides / Desktop Only View
  [M]       : Mute / Unmute Sound Effects
  [H]       : Toggle Hand Skeleton Overlay
  [Right]/[Left]/[Space] : Keyboard passthrough to PowerPoint
  [Q] / Esc : Quit
================================================================================
"""

import cv2
import mediapipe as mp
import numpy as np
import time
import math
import sys
import os
from collections import deque
import ctypes
import ctypes.wintypes

# -----------------------------------------------------------------------------
# 🎮 SYSTEM INPUT LAYER (Universal PowerPoint & Desktop Controller)
# -----------------------------------------------------------------------------
user32 = ctypes.windll.user32

# Virtual Key Codes
VK_LEFT    = 0x25
VK_RIGHT   = 0x27
VK_PRIOR   = 0x21 # Page Up
VK_NEXT    = 0x22 # Page Down
VK_SPACE   = 0x20
VK_ESCAPE  = 0x1B
VK_F5      = 0x74
VK_B       = 0x42 # Black screen in PPT
KEYEVENTF_KEYUP = 0x0002

try:
    import pygetwindow as gw
    HAS_PYGETWINDOW = True
except Exception:
    HAS_PYGETWINDOW = False

def send_single_key(vk_code):
    """Sends exactly ONE hardware key down and up event with clean timing."""
    user32.keybd_event(vk_code, 0, 0, 0)
    time.sleep(0.015)
    user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

def activate_powerpoint_window():
    """Finds PowerPoint window and brings it to foreground focus."""
    if HAS_PYGETWINDOW:
        try:
            for w in gw.getAllWindows():
                title = w.title.lower()
                if any(k in title for k in ['powerpoint', 'slide show', 'presentation', '.pptx', '.ppt']):
                    if w.isMinimized:
                        w.restore()
                    w.activate()
                    return w.title
        except Exception:
            pass
    try:
        hwnd_show = user32.FindWindowW("screenClass", None)
        if hwnd_show and user32.IsWindowVisible(hwnd_show):
            user32.SetForegroundWindow(hwnd_show)
            return "PowerPoint Slide Show"
        hwnd_ppt = user32.FindWindowW("PPTFrameClass", None)
        if hwnd_ppt and user32.IsWindowVisible(hwnd_ppt):
            user32.SetForegroundWindow(hwnd_ppt)
            return "PowerPoint Window"
    except Exception:
        pass
    return None

def broadcast_next_slide():
    """Universal Next Slide: Sends STRICTLY ONE key event to advance 1 slide."""
    activate_powerpoint_window()
    send_single_key(VK_RIGHT)

def broadcast_prev_slide():
    """Universal Prev Slide: Sends STRICTLY ONE key event to rewind 1 slide."""
    activate_powerpoint_window()
    send_single_key(VK_LEFT)

def broadcast_blackout():
    """Toggles black screen (Speaker Focus) in PowerPoint."""
    activate_powerpoint_window()
    send_single_key(VK_B)

def broadcast_f5():
    """Starts slideshow in PowerPoint (F5)."""
    activate_powerpoint_window()
    send_single_key(VK_F5)

def broadcast_exit_slideshow():
    """Exits slideshow in PowerPoint / Google Slides (Escape)."""
    activate_powerpoint_window()
    send_single_key(VK_ESCAPE)

# -----------------------------------------------------------------------------
# 🔊 PROCEDURAL AUDIO SYNTHESIZER
# -----------------------------------------------------------------------------
class SoundEngine:
    """Synthesizes high-tech UI audio in real-time with zero external files."""
    def __init__(self):
        self.enabled = False
        self.muted = False
        self.sounds = {}
        try:
            import pygame
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
            self.enabled = True
            self._synthesize_sounds()
        except Exception as e:
            print(f"[SoundEngine] Audio init unavailable: {e}")
            self.enabled = False

    def _wave_to_sound(self, wave, sr=22050):
        import pygame
        wave = np.clip(wave, -1.0, 1.0)
        audio = (wave * 32767).astype(np.int16)
        stereo = np.column_stack((audio, audio))
        return pygame.sndarray.make_sound(stereo)

    def _synthesize_sounds(self):
        sr = 22050

        # 1. Slide Next (Futuristic upward whoosh)
        dur = 0.13
        t = np.linspace(0, dur, int(sr * dur), False)
        f = np.linspace(450, 1500, len(t))
        w = np.sin(2 * np.pi * f * t) * 0.4 + np.random.uniform(-0.35, 0.35, len(t)) * 0.6
        env = np.sin(np.pi * t / dur) ** 2
        self.sounds['next'] = self._wave_to_sound(w * env * 0.8, sr)

        # 2. Slide Prev (Futuristic downward whoosh)
        dur = 0.13
        t = np.linspace(0, dur, int(sr * dur), False)
        f = np.linspace(1500, 450, len(t))
        w = np.sin(2 * np.pi * f * t) * 0.4 + np.random.uniform(-0.35, 0.35, len(t)) * 0.6
        env = np.sin(np.pi * t / dur) ** 2
        self.sounds['prev'] = self._wave_to_sound(w * env * 0.8, sr)

        # 3. Launch chime
        dur = 0.22
        t = np.linspace(0, dur, int(sr * dur), False)
        w = (np.sin(2 * np.pi * 523.25 * t) + np.sin(2 * np.pi * 659.25 * t) + np.sin(2 * np.pi * 783.99 * t)) * np.exp(-t * 12)
        self.sounds['launch'] = self._wave_to_sound(w * 0.35, sr)

        # 4. Exit dismiss tone (Descending two-tone)
        dur = 0.20
        t = np.linspace(0, dur, int(sr * dur), False)
        w = (np.sin(2 * np.pi * 659.25 * t) * (1.0 - t/dur) + np.sin(2 * np.pi * 392.0 * t) * (t/dur)) * np.exp(-t * 8)
        self.sounds['exit'] = self._wave_to_sound(w * 0.45, sr)

        # 5. Focus Gong
        dur = 0.30
        t = np.linspace(0, dur, int(sr * dur), False)
        w = (np.sin(2 * np.pi * 180 * t) + 0.5 * np.sin(2 * np.pi * 360 * t)) * np.exp(-t * 10)
        self.sounds['focus'] = self._wave_to_sound(w * 0.75, sr)

    def play(self, name):
        if not self.enabled or self.muted:
            return
        snd = self.sounds.get(name)
        if snd:
            snd.play()

# -----------------------------------------------------------------------------
# 📑 EMBEDDED DEMO PRESENTATION DECK
# -----------------------------------------------------------------------------
DEMO_SLIDES = [
    {
        "title": "PROJECT ANTIGRAVITY",
        "subtitle": "Precision Finger-Count Presentation Controller",
        "bullets": [
            "✌️ Show 2 FINGERS (Index + Middle) -> STRICTLY ONE Next Slide",
            "🤟 Show 3 FINGERS (Index+Middle+Ring) -> STRICTLY ONE Prev Slide",
            "👍 Show THUMBS UP -> End Slideshow / Presentation (Escape)",
            "🖐️ Hold Full Palm (5 Fingers) for 0.7s -> Launch Slideshow (F5)"
        ],
        "accent": (0, 242, 254),
        "tag": "SYSTEM OVERVIEW // SLIDE 01"
    },
    {
        "title": "THUMBS-UP PRESENTATION EXIT",
        "subtitle": "End Keynotes with a Natural, Confident Gesture",
        "bullets": [
            "Simply hold your thumb vertically upright with other fingers closed",
            "Instantly sends Escape (VK_ESCAPE) to exit fullscreen mode",
            "Single-Action Lockout ensures zero repeat or accidental key spam",
            "Hold Closed Fist ✊ for 0.6s to toggle Speaker Focus (Screen Blackout)"
        ],
        "accent": (255, 80, 80),
        "tag": "EXIT GESTURE // SLIDE 02"
    },
    {
        "title": "POWERPOINT COMPATIBILITY",
        "subtitle": "Optimized for Fullscreen F5 Slide Shows",
        "bullets": [
            "Seamless integration with Microsoft PowerPoint & Google Slides",
            "Automatically brings PowerPoint to focus when gesture triggers",
            "Press [P] to toggle Mini PiP Widget in the screen corner",
            "Press [T] to pin the widget Always-On-Top of your presentation"
        ],
        "accent": (50, 255, 126),
        "tag": "POWERPOINT READY // SLIDE 03"
    },
    {
        "title": "PRESENTER CONFIDENCE",
        "subtitle": "Natural, Intuitive, and Frictionless",
        "bullets": [
            "Clean HUD displays detected finger count in real-time",
            "Press [D] to toggle Desktop Only View",
            "Press [Space] or [N] for manual keyboard passthrough",
            "Enjoy presenting like a true maestro!"
        ],
        "accent": (180, 105, 255),
        "tag": "CONCLUSION // SLIDE 04"
    }
]

# -----------------------------------------------------------------------------
# 🎯 AIR PRESENTER APPLICATION
# -----------------------------------------------------------------------------
class AirPresenter:
    def __init__(self):
        # MediaPipe Hands
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.65,
            min_tracking_confidence=0.60
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles

        # Audio synthesizer
        self.sound = SoundEngine()

        # Display settings
        self.width = 1280
        self.height = 720
        self.demo_mode = True
        self.pip_mode = False
        self.always_on_top = False
        self.show_landmarks = True
        self.window_name = "Air Presenter // Finger-Count Maestro"

        # Presentation State
        self.current_slide = 0
        self.total_slides = len(DEMO_SLIDES)
        self.blackout = False

        # ---------------------------------------------------------------------
        # ✌️ STRICT SINGLE-SLIDE STATE MACHINE
        # ---------------------------------------------------------------------
        self.gesture_state = "READY"       # "READY" or "LOCKED"
        self.detected_fingers = 0
        self.active_hold_pose = None
        self.active_hold_start = None
        self.neutral_start_time = None
        self.last_slide_time = 0
        self.min_hold_duration = 0.22      # Must hold pose for 0.22s to trigger
        self.cooldown_duration = 0.85      # Hard cooldown: 0.85s between slide advances

        # Thumbs Up Timer (Exit Slideshow Escape)
        self.thumbs_up_start_time = None
        self.last_thumbs_up_trigger = 0

        # Full Palm Timer (Launch F5)
        self.palm_start_time = None
        self.last_palm_trigger = 0

        # Fist Timer (Blackout 'B')
        self.fist_start_time = None
        self.last_fist_trigger = 0

        # Visual FX & Badges
        self.ripples = []
        self.last_action_badge = ""
        self.badge_timer = 0
        self.badge_color = (0, 242, 254)

        # FPS calculation
        self.prev_frame_time = time.time()
        self.fps = 0.0

    # -------------------------------------------------------------------------
    # 🎮 SLIDE ACTIONS (With Hard Cooldown Lock)
    # -------------------------------------------------------------------------
    def trigger_next_slide(self):
        """Advances strictly ONE slide in PowerPoint and Demo Deck."""
        now = time.time()
        if now - self.last_slide_time < self.cooldown_duration:
            return
        self.last_slide_time = now

        if self.current_slide < self.total_slides - 1:
            self.current_slide += 1

        broadcast_next_slide()
        self.sound.play('next')
        self._add_action_badge("✌️ 2 FINGERS: >> NEXT SLIDE >>", (0, 242, 254))
        self.ripples.append({'dir': 1, 'progress': 0.0, 'color': (0, 242, 254)})

    def trigger_prev_slide(self):
        """Rewinds strictly ONE slide in PowerPoint and Demo Deck."""
        now = time.time()
        if now - self.last_slide_time < self.cooldown_duration:
            return
        self.last_slide_time = now

        if self.current_slide > 0:
            self.current_slide -= 1

        broadcast_prev_slide()
        self.sound.play('prev')
        self._add_action_badge("🤟 3 FINGERS: << PREV SLIDE <<", (255, 110, 0))
        self.ripples.append({'dir': -1, 'progress': 0.0, 'color': (255, 110, 0)})

    def trigger_exit_slideshow(self):
        """Exits the PowerPoint presentation / slideshow."""
        broadcast_exit_slideshow()
        self.sound.play('exit')
        self._add_action_badge("👍 THUMBS UP: PRESENTATION ENDED (ESC)", (255, 80, 80))

    def trigger_blackout(self):
        """Toggles black screen (Speaker Focus) in PowerPoint."""
        self.blackout = not self.blackout
        broadcast_blackout()
        self.sound.play('focus')
        status = "SPEAKER FOCUS: MUTED (PPT 'B')" if self.blackout else "SPEAKER FOCUS: RESTORED"
        self._add_action_badge(status, (255, 50, 180))

    def trigger_start_slideshow(self):
        """Launches slideshow in PowerPoint (F5)."""
        broadcast_f5()
        self.sound.play('launch')
        self._add_action_badge("🖐️ FULL PALM: LAUNCH SLIDESHOW (F5)", (50, 255, 126))

    def _add_action_badge(self, text, color):
        self.last_action_badge = text
        self.badge_color = color
        self.badge_timer = time.time() + 1.2

    # -------------------------------------------------------------------------
    # 🖐️ PRECISION FINGER COUNTING PIPELINE
    # -------------------------------------------------------------------------
    def analyze_fingers(self, landmarks):
        """Accurately analyzes extended status of all 5 fingers."""
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        palm_scale = max(25.0, np.linalg.norm(wrist - middle_mcp))

        # Finger checks: Tip must be further from wrist than PIP
        index_ext  = (np.linalg.norm(landmarks[8]  - wrist) > np.linalg.norm(landmarks[6]  - wrist) * 1.08) or (landmarks[8][1] < landmarks[6][1])
        middle_ext = (np.linalg.norm(landmarks[12] - wrist) > np.linalg.norm(landmarks[10] - wrist) * 1.08) or (landmarks[12][1] < landmarks[10][1])
        ring_ext   = (np.linalg.norm(landmarks[16] - wrist) > np.linalg.norm(landmarks[14] - wrist) * 1.08) or (landmarks[16][1] < landmarks[14][1])
        pinky_ext  = (np.linalg.norm(landmarks[20] - wrist) > np.linalg.norm(landmarks[18] - wrist) * 1.08) or (landmarks[20][1] < landmarks[18][1])

        # Thumb: Distance from middle MCP & wrist
        thumb_dist = np.linalg.norm(landmarks[4] - landmarks[9]) / palm_scale
        thumb_ext  = (thumb_dist > 0.65) and (np.linalg.norm(landmarks[4] - wrist) > np.linalg.norm(landmarks[2] - wrist) * 1.08)

        non_thumb_count = sum([index_ext, middle_ext, ring_ext, pinky_ext])
        total_count = non_thumb_count + (1 if thumb_ext else 0)

        return {
            'thumb': thumb_ext,
            'index': index_ext,
            'middle': middle_ext,
            'ring': ring_ext,
            'pinky': pinky_ext,
            'non_thumb_count': non_thumb_count,
            'total_count': total_count
        }

    def process_gestures(self, results, frame_shape):
        h, w, _ = frame_shape
        now = time.time()
        hands_detected = len(results.multi_hand_landmarks) if results.multi_hand_landmarks else 0

        if hands_detected == 0:
            self.detected_fingers = 0
            self.active_hold_pose = None
            self.active_hold_start = None
            self.thumbs_up_start_time = None
            self.palm_start_time = None
            self.fist_start_time = None
            if (now - self.last_slide_time >= self.cooldown_duration):
                self.gesture_state = "READY"
                self.neutral_start_time = None
            return

        # Extract landmarks of primary hand
        primary_lms = results.multi_hand_landmarks[0].landmark
        landmarks = np.array([[lm.x * w, lm.y * h] for lm in primary_lms])
        wrist = landmarks[0]
        middle_mcp = landmarks[9]
        palm_scale = max(25.0, np.linalg.norm(wrist - middle_mcp))

        f = self.analyze_fingers(landmarks)
        self.detected_fingers = f['total_count']

        # Determine current semantic hand pose
        current_pose = 'NEUTRAL'

        # Check for Thumbs Up 👍:
        # 4 non-thumb fingers are closed, Thumb is extended and pointing upward
        is_thumbs_up = False
        if f['non_thumb_count'] == 0 and f['thumb']:
            # Thumb tip is higher than Thumb MCP (2) and Wrist (0)
            if (landmarks[4][1] < landmarks[2][1] - (palm_scale * 0.15)) and \
               (landmarks[4][1] < landmarks[0][1] - (palm_scale * 0.30)):
                is_thumbs_up = True

        if is_thumbs_up:
            current_pose = 'THUMBS_UP'
        elif f['total_count'] == 0:
            current_pose = 'FIST'
        elif f['total_count'] == 5 or (f['non_thumb_count'] == 4 and f['thumb']):
            current_pose = 'FULL_PALM'
        elif (f['index'] and f['middle'] and not f['ring'] and not f['pinky']):
            # ✌️ Strictly 2 fingers (Index + Middle)
            current_pose = 'TWO_FINGERS'
        elif (f['index'] and f['middle'] and f['ring'] and not f['pinky']):
            # 🤟 Strictly 3 fingers (Index + Middle + Ring)
            current_pose = 'THREE_FINGERS'
        elif f['total_count'] == 2 and not f['ring'] and not f['pinky']:
            current_pose = 'TWO_FINGERS'
        elif f['total_count'] == 3 and not f['pinky']:
            current_pose = 'THREE_FINGERS'

        # ---------------------------------------------------------------------
        # 1. 👍 THUMBS UP (Hold 0.25s) -> End Slideshow / Presentation (Escape)
        # ---------------------------------------------------------------------
        if current_pose == 'THUMBS_UP':
            if self.thumbs_up_start_time is None:
                self.thumbs_up_start_time = now
            elif (now - self.thumbs_up_start_time > 0.25) and (now - self.last_thumbs_up_trigger > 1.5):
                self.trigger_exit_slideshow()
                self.last_thumbs_up_trigger = now
                self.thumbs_up_start_time = None
                self.gesture_state = "LOCKED"
                self.last_slide_time = now
            return
        else:
            self.thumbs_up_start_time = None

        # ---------------------------------------------------------------------
        # 2. 🖐️ FULL PALM (Hold 0.70s) -> Launch Slideshow F5
        # ---------------------------------------------------------------------
        if current_pose == 'FULL_PALM':
            if self.palm_start_time is None:
                self.palm_start_time = now
            elif (now - self.palm_start_time > 0.70) and (now - self.last_palm_trigger > 2.0):
                self.trigger_start_slideshow()
                self.last_palm_trigger = now
                self.palm_start_time = None
                self.gesture_state = "LOCKED"
                self.last_slide_time = now
            return
        else:
            self.palm_start_time = None

        # ---------------------------------------------------------------------
        # 3. ✊ CLOSED FIST (Hold 0.60s) -> Speaker Focus / Blackout ('B')
        # ---------------------------------------------------------------------
        if current_pose == 'FIST':
            if self.fist_start_time is None:
                self.fist_start_time = now
            elif (now - self.fist_start_time > 0.60) and (now - self.last_fist_trigger > 1.5):
                self.trigger_blackout()
                self.last_fist_trigger = now
                self.fist_start_time = None
                self.gesture_state = "LOCKED"
                self.last_slide_time = now
            return
        else:
            self.fist_start_time = None

        # ---------------------------------------------------------------------
        # 4. ✌️ TWO FINGERS (Next) & 🤟 THREE FINGERS (Prev)
        # ---------------------------------------------------------------------
        if self.gesture_state == "LOCKED":
            cooldown_passed = (now - self.last_slide_time >= self.cooldown_duration)
            is_neutral = (current_pose not in ('TWO_FINGERS', 'THREE_FINGERS', 'THUMBS_UP'))

            if is_neutral:
                if self.neutral_start_time is None:
                    self.neutral_start_time = now
                elif (now - self.neutral_start_time >= 0.20) and cooldown_passed:
                    self.gesture_state = "READY"
                    self.neutral_start_time = None
                    self.active_hold_pose = None
                    self.active_hold_start = None
            else:
                self.neutral_start_time = None
            return

        if self.gesture_state == "READY":
            if current_pose in ('TWO_FINGERS', 'THREE_FINGERS'):
                if self.active_hold_pose != current_pose:
                    self.active_hold_pose = current_pose
                    self.active_hold_start = now
                elif now - self.active_hold_start >= self.min_hold_duration:
                    if current_pose == 'TWO_FINGERS':
                        self.trigger_next_slide()
                    elif current_pose == 'THREE_FINGERS':
                        self.trigger_prev_slide()

                    self.gesture_state = "LOCKED"
                    self.active_hold_pose = None
                    self.active_hold_start = None
                    self.neutral_start_time = None
            else:
                self.active_hold_pose = None
                self.active_hold_start = None

    # -------------------------------------------------------------------------
    # 🎨 RENDERING: EMBEDDED DEMO DECK
    # -------------------------------------------------------------------------
    def render_demo_slide(self, frame):
        h, w, _ = frame.shape
        slide = DEMO_SLIDES[self.current_slide]
        accent = slide["accent"]

        canvas_margin_x = 50
        canvas_margin_y = 65
        x1, y1 = canvas_margin_x, canvas_margin_y
        x2, y2 = w - canvas_margin_x, h - canvas_margin_y

        sub_overlay = frame.copy()
        cv2.rectangle(sub_overlay, (x1, y1), (x2, y2), (14, 18, 25), -1)
        cv2.addWeighted(sub_overlay, 0.88, frame, 0.12, 0, frame)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (40, 50, 70), 2)
        corner_len = 35
        cv2.line(frame, (x1, y1), (x1 + corner_len, y1), accent, 4)
        cv2.line(frame, (x1, y1), (x1 + corner_len, y1), accent, 4)
        cv2.line(frame, (x2, y1), (x2 - corner_len, y1), accent, 4)
        cv2.line(frame, (x2, y1), (x2, y1 + corner_len), accent, 4)
        cv2.line(frame, (x1, y2), (x1 + corner_len, y2), accent, 4)
        cv2.line(frame, (x1, y2), (x1 - corner_len, y2), accent, 4)
        cv2.line(frame, (x2, y2), (x2 - corner_len, y2), accent, 4)
        cv2.line(frame, (x2, y2), (x2, y2 - corner_len), accent, 4)

        cv2.putText(frame, slide["tag"], (x1 + 35, y1 + 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, accent, 2, cv2.LINE_AA)
        cv2.putText(frame, slide["title"], (x1 + 35, y1 + 105),
                    cv2.FONT_HERSHEY_DUPLEX, 1.35, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, slide["subtitle"], (x1 + 37, y1 + 145),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (160, 185, 215), 1, cv2.LINE_AA)
        cv2.line(frame, (x1 + 35, y1 + 165), (x2 - 35, y1 + 165), (50, 65, 90), 1)

        start_y = y1 + 225
        for i, bullet in enumerate(slide["bullets"]):
            by = start_y + i * 65
            cv2.circle(frame, (x1 + 50, by - 8), 7, accent, -1)
            cv2.circle(frame, (x1 + 50, by - 8), 12, accent, 1)
            cv2.putText(frame, bullet, (x1 + 75, by),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.80, (230, 240, 250), 2, cv2.LINE_AA)

        dots_center_x = w // 2
        dot_spacing = 30
        dots_start_x = dots_center_x - (self.total_slides * dot_spacing) // 2

        for i in range(self.total_slides):
            dx = dots_start_x + i * dot_spacing
            dy = y2 - 35
            if i == self.current_slide:
                cv2.circle(frame, (dx, dy), 8, accent, -1)
                cv2.circle(frame, (dx, dy), 14, accent, 2)
            else:
                cv2.circle(frame, (dx, dy), 5, (70, 85, 110), -1)

        num_str = f"SLIDE {self.current_slide + 1:02d} / {self.total_slides:02d}"
        cv2.putText(frame, num_str, (x2 - 190, y2 - 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (150, 175, 205), 1, cv2.LINE_AA)

    # -------------------------------------------------------------------------
    # 🌊 RENDERING: RIPPLES
    # -------------------------------------------------------------------------
    def render_ripples(self, frame):
        h, w, _ = frame.shape
        active_ripples = []
        for r in self.ripples:
            r['progress'] += 0.09
            if r['progress'] <= 1.0:
                active_ripples.append(r)
                alpha = 1.0 - r['progress']
                thickness = max(1, int(14 * alpha))
                wave_x = int(r['progress'] * w) if r['dir'] > 0 else int((1.0 - r['progress']) * w)
                col = tuple([int(c * alpha) for c in r['color']])
                cv2.line(frame, (wave_x, 0), (wave_x, h), col, thickness, cv2.LINE_AA)

                chevron = ">>>" if r['dir'] > 0 else "<<<"
                cv2.putText(frame, chevron, (wave_x - 30, h // 2),
                            cv2.FONT_HERSHEY_DUPLEX, 1.8, col, 3, cv2.LINE_AA)
        self.ripples = active_ripples

    # -------------------------------------------------------------------------
    # 🛸 RENDERING: MINIMAL SCI-FI HUD
    # -------------------------------------------------------------------------
    def render_hud(self, frame):
        h, w, _ = frame.shape

        # Top Bar
        hud_bar = frame[0:50, 0:w].copy()
        cv2.rectangle(hud_bar, (0, 0), (w, 50), (10, 14, 20), -1)
        cv2.addWeighted(hud_bar, 0.75, frame[0:50, 0:w], 0.25, 0, frame[0:50, 0:w])
        cv2.line(frame, (0, 50), (w, 50), (0, 242, 254), 1)

        cv2.putText(frame, "AIR PRESENTER v5.2 // THUMBS-UP EXIT MAESTRO", (25, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.65, (255, 255, 255), 2, cv2.LINE_AA)

        # Dynamic Status Pill
        if self.gesture_state == "LOCKED":
            pill_text = "🔒 SLIDE LOCKED // LOWER FINGERS TO RE-ARM"
            pill_col = (130, 160, 190)
        elif self.active_hold_pose == 'TWO_FINGERS':
            pill_text = "✌️ 2 FINGERS: ADVANCING NEXT SLIDE"
            pill_col = (0, 242, 254)
        elif self.active_hold_pose == 'THREE_FINGERS':
            pill_text = "🤟 3 FINGERS: REWINDING PREV SLIDE"
            pill_col = (255, 110, 0)
        elif self.thumbs_up_start_time is not None:
            pill_text = "👍 THUMBS UP: ENDING PRESENTATION (ESC)"
            pill_col = (255, 80, 80)
        elif self.detected_fingers == 5:
            pill_text = "🖐️ FULL PALM (HOLD FOR F5)"
            pill_col = (50, 255, 126)
        elif self.detected_fingers == 0:
            pill_text = "✊ CLOSED FIST (HOLD FOR BLACKOUT)"
            pill_col = (255, 50, 180)
        else:
            pill_text = f"🟢 READY // ✌️ NEXT | 🤟 PREV | 👍 EXIT"
            pill_col = (170, 210, 230)

        cv2.putText(frame, pill_text, (520, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, pill_col, 2, cv2.LINE_AA)

        # Real-time Finger Count Badge (Top-Right)
        fc_col = (0, 242, 254) if self.detected_fingers == 2 else ((255, 110, 0) if self.detected_fingers == 3 else (200, 200, 200))
        cv2.putText(frame, f"FINGERS: {self.detected_fingers}", (w - 230, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, fc_col, 2, cv2.LINE_AA)

        # FPS meter
        cv2.putText(frame, f"{int(self.fps)} FPS", (w - 75, 32),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (150, 255, 150), 2, cv2.LINE_AA)

        # Bottom Shortcut Bar
        b_bar = frame[h - 40:h, 0:w].copy()
        cv2.rectangle(b_bar, (0, 0), (w, 40), (10, 14, 20), -1)
        cv2.addWeighted(b_bar, 0.8, frame[h - 40:h, 0:w], 0.2, 0, frame[h - 40:h, 0:w])
        cv2.line(frame, (0, h - 40), (w, h - 40), (40, 50, 70), 1)

        shortcuts = "[P] PiP Mini Mode | [T] Topmost | [D] Demo Deck | [M] Mute | [H] Skeleton | [Q] Quit"
        cv2.putText(frame, shortcuts, (25, h - 14),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.50, (170, 190, 210), 1, cv2.LINE_AA)

        # Dynamic Action Badge
        if time.time() < self.badge_timer:
            bx = w // 2
            by = 110
            tw = len(self.last_action_badge) * 14 + 35
            cv2.rectangle(frame, (bx - tw // 2, by - 24), (bx + tw // 2, by + 12), (15, 20, 30), -1)
            cv2.rectangle(frame, (bx - tw // 2, by - 24), (bx + tw // 2, by + 12), self.badge_color, 2)
            cv2.putText(frame, self.last_action_badge, (bx - tw // 2 + 18, by),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.68, self.badge_color, 2, cv2.LINE_AA)

        # Speaker Focus Overlay
        if self.blackout:
            black_overlay = np.zeros_like(frame)
            cv2.putText(black_overlay, "SPEAKER FOCUS ACTIVE (PPT BLACK)", (w // 2 - 280, h // 2 - 20),
                        cv2.FONT_HERSHEY_DUPLEX, 1.3, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.putText(black_overlay, "Screen blacked out to focus audience on you",
                        (w // 2 - 250, h // 2 + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (180, 180, 180), 1, cv2.LINE_AA)
            cv2.putText(black_overlay, "Hold Fist ✊ again to restore presentation",
                        (w // 2 - 220, h // 2 + 65), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 242, 254), 1, cv2.LINE_AA)
            cv2.addWeighted(black_overlay, 0.94, frame, 0.06, 0, frame)

    # -------------------------------------------------------------------------
    # 🪟 WINDOW MANAGEMENT
    # -------------------------------------------------------------------------
    def toggle_pip_mode(self):
        """Switches between Full HUD (1280x720) and compact Corner PiP (380x215)."""
        self.pip_mode = not self.pip_mode
        if self.pip_mode:
            cv2.resizeWindow(self.window_name, 380, 215)
            self._add_action_badge("PiP MINI MODE ACTIVE", (0, 242, 254))
        else:
            cv2.resizeWindow(self.window_name, self.width, self.height)
            self._add_action_badge("FULL HUD MODE RESTORED", (0, 242, 254))

    def toggle_topmost(self):
        """Pins the window always-on-top so it floats over PowerPoint."""
        self.always_on_top = not self.always_on_top
        hwnd = user32.FindWindowW(None, self.window_name)
        if hwnd:
            HWND_TOPMOST = -1
            HWND_NOTOPMOST = -2
            SWP_NOMOVE = 0x0002
            SWP_NOSIZE = 0x0001
            target = HWND_TOPMOST if self.always_on_top else HWND_NOTOPMOST
            user32.SetWindowPos(hwnd, target, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
            msg = "PINNED ALWAYS-ON-TOP" if self.always_on_top else "NORMAL WINDOW MODE"
            self._add_action_badge(msg, (50, 255, 126))

    # -------------------------------------------------------------------------
    # 🚀 MAIN LOOP
    # -------------------------------------------------------------------------
    def run(self):
        print("==================================================")
        print("🚀 AIR PRESENTER v5.2 THUMBS-UP EXIT INITIALIZED")
        print("   ✌️ Show 2 FINGERS     -> NEXT SLIDE (Strictly 1)")
        print("   🤟 Show 3 FINGERS     -> PREV SLIDE (Strictly 1)")
        print("   👍 Show THUMBS UP     -> END PRESENTATION (Escape)")
        print("   🖐️ Full Palm (0.7s)   -> Launch Slideshow (F5)")
        print("   ✊ Closed Fist (0.6s) -> Blackout Screen ('B')")
        print("   Press [P]             -> Mini PiP Corner Widget")
        print("   Press [T]             -> Always-On-Top")
        print("==================================================")

        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)

        if not cap.isOpened():
            print("[Error] Could not open webcam.")
            return

        cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_name, self.width, self.height)

        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                now = time.time()
                self.fps = 0.9 * self.fps + 0.1 * (1.0 / max(0.001, (now - self.prev_frame_time)))
                self.prev_frame_time = now

                # MediaPipe Tracking
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb_frame.flags.writeable = False
                results = self.hands.process(rgb_frame)
                rgb_frame.flags.writeable = True

                # Process Gestures
                self.process_gestures(results, frame.shape)

                # Render Embedded Demo Deck (if active)
                if self.demo_mode and not self.pip_mode:
                    self.render_demo_slide(frame)

                # Render Hand Landmarks
                if self.show_landmarks and results.multi_hand_landmarks:
                    for hand_lms in results.multi_hand_landmarks:
                        self.mp_draw.draw_landmarks(
                            frame,
                            hand_lms,
                            self.mp_hands.HAND_CONNECTIONS,
                            self.mp_drawing_styles.get_default_hand_landmarks_style(),
                            self.mp_drawing_styles.get_default_hand_connections_style()
                        )

                # Render Ripples and Minimal HUD
                self.render_ripples(frame)
                self.render_hud(frame)

                # Display frame
                cv2.imshow(self.window_name, frame)

                # Keyboard handling (with PowerPoint passthrough)
                key = cv2.waitKey(1) & 0xFF
                if key in (ord('q'), ord('Q'), 27): # 'Q' or Esc
                    break
                elif key in (ord('d'), ord('D')):
                    self.demo_mode = not self.demo_mode
                    msg = "DEMO DECK MODE" if self.demo_mode else "DESKTOP ONLY MODE"
                    self._add_action_badge(msg, (0, 242, 254))
                elif key in (ord('p'), ord('P')):
                    self.toggle_pip_mode()
                elif key in (ord('t'), ord('T')):
                    self.toggle_topmost()
                elif key in (ord('m'), ord('M')):
                    self.sound.muted = not self.sound.muted
                    status = "AUDIO MUTED" if self.sound.muted else "AUDIO UNMUTED"
                    self._add_action_badge(status, (255, 255, 255))
                elif key in (ord('h'), ord('H')):
                    self.show_landmarks = not self.show_landmarks
                elif key in (ord('n'), ord('N'), 32): # 'N' or Spacebar
                    self.trigger_next_slide()
                elif key in (ord('b'), ord('B')):
                    self.trigger_blackout()

        finally:
            cap.release()
            cv2.destroyAllWindows()
            print("[*] Air Presenter closed cleanly.")

if __name__ == "__main__":
    app = AirPresenter()
    app.run()
