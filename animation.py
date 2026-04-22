import re
import pygame
import os
import glob

ANIM_FOLDER = "AnimationEnded"
DEFAULT_FPS = 5
GAME_FPS    = 60

SCREEN_W, SCREEN_H = 1000, 700

SKIP_W, SKIP_H = 90, 38
SKIP_MARGIN    = 10
C_INK          = (62, 75, 130)
C_PAPER        = (248, 247, 244)
C_HOVER        = (220, 225, 255)

def _natural_key(path: str) -> list:
    return [int(c) if c.isdigit() else c.lower()
            for c in re.split(r'(\d+)', os.path.basename(path))]

def _load_frames(folder: str) -> list:
    if not os.path.isdir(folder):
        return []

    paths = []
    for pat in ("*.png", "*.PNG", "*.jpg", "*.JPG", "*.jpeg"):
        paths.extend(glob.glob(os.path.join(folder, pat)))

    paths.sort(key=_natural_key)

    frames = []
    for p in paths:
        try:
            frames.append(pygame.image.load(p).convert_alpha())
        except pygame.error:
            pass
    return frames

class BrewingAnimation:

    def __init__(self, anim_fps: int = DEFAULT_FPS):
        self._raw_frames    = []
        self._scaled_frames = []
        self._anim_fps        = anim_fps
        self._ticks_per_frame = max(1, GAME_FPS // anim_fps)
        self._scaled          = False
        self._loaded          = False

        self.is_playing = False
        self.finished   = False
        self._frame_idx = 0
        self._tick      = 0

        self._overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        self._overlay.fill((0, 0, 0, 160))

        self._skip_rect = pygame.Rect(
            SCREEN_W - SKIP_W - SKIP_MARGIN,
            SKIP_MARGIN,
            SKIP_W, SKIP_H,
        )
        self._font = None

    def _ensure_loaded(self):
        if not self._loaded:
            self._raw_frames = _load_frames(ANIM_FOLDER)
            self._loaded = True

    def _scale_frames(self):
        self._scaled_frames = []
        for raw in self._raw_frames:
            rw, rh = raw.get_size()
            scale  = min(SCREEN_W / rw, SCREEN_H / rh)
            nw, nh = int(rw * scale), int(rh * scale)
            self._scaled_frames.append(
                pygame.transform.smoothscale(raw, (nw, nh)))
        self._scaled = True

    def _get_font(self):
        if self._font is None:
            for name in ("Comic Sans MS", "Segoe Print", "Arial"):
                try:
                    self._font = pygame.font.SysFont(name, 18, bold=True)
                    break
                except Exception:
                    continue
            if self._font is None:
                self._font = pygame.font.Font(None, 22)
        return self._font

    @property
    def has_frames(self) -> bool:
        self._ensure_loaded()
        return bool(self._raw_frames)

    def start(self):
        self._ensure_loaded()
        if not self._raw_frames:
            self.finished   = True
            self.is_playing = False
            return
        if not self._scaled:
            self._scale_frames()
        self._frame_idx = 0
        self._tick      = 0
        self.finished   = False
        self.is_playing = True

    def skip(self):
        self.finished   = True
        self.is_playing = False

    def reset(self):
        self.is_playing = False
        self.finished   = False
        self._frame_idx = 0
        self._tick      = 0

    def update(self):
        if not self.is_playing or self.finished:
            return
        self._tick += 1
        if self._tick >= self._ticks_per_frame:
            self._tick = 0
            self._frame_idx += 1
            if self._frame_idx >= len(self._scaled_frames):
                self._frame_idx = len(self._scaled_frames) - 1
                self.finished   = True
                self.is_playing = False

    def draw(self, screen: pygame.Surface):
        if not self._scaled_frames:
            return

        screen.blit(self._overlay, (0, 0))

        frame      = self._scaled_frames[self._frame_idx]
        frame_rect = frame.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))

        pygame.draw.rect(screen, C_PAPER, frame_rect)

        screen.blit(frame, frame_rect)

        hovered = self._skip_rect.collidepoint(pygame.mouse.get_pos())
        fill    = C_HOVER if hovered else C_PAPER
        pygame.draw.rect(screen, fill,  self._skip_rect, border_radius=6)
        pygame.draw.rect(screen, C_INK, self._skip_rect, 2, border_radius=6)
        font  = self._get_font()
        label = font.render("SKIP  ››", True, C_INK)
        screen.blit(label, label.get_rect(center=self._skip_rect.center))

    def handle_event(self, event: pygame.event.Event) -> bool:
        if (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self._skip_rect.collidepoint(event.pos)):
            return True
        return False