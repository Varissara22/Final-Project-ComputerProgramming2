import pygame
from typing import Optional

SCREEN_W = 1000
SCREEN_H = 700

class GhostToPhantomAnimation:

    FRAME_PATHS = [f"GhostToPhanthom/Untitled_Artwork-{i}.png" for i in range(1, 8)]
    SOUND_PATH  = "SoundEffect/611675__genel__sprinkle.wav"
    FRAME_DELAY = 20

    def __init__(self):
        self.frames     : list[pygame.Surface] = []
        self.sound      : Optional[pygame.mixer.Sound] = None
        self.is_playing : bool = False
        self.finished   : bool = False
        self._frame_idx : int  = 0
        self._tick      : int  = 0
        self._loaded    : bool = False

    def _load(self):
        if self._loaded:
            return
        self._loaded = True

        for path in self.FRAME_PATHS:
            try:
                img = pygame.image.load(path).convert_alpha()
                img = pygame.transform.smoothscale(img, (SCREEN_W, SCREEN_H))
                self.frames.append(img)
                print(f"[PhantomAnim] Loaded: {path}")
            except (pygame.error, FileNotFoundError):
                print(f"[PhantomAnim] WARNING – missing frame: {path}")

        try:
            self.sound = pygame.mixer.Sound(self.SOUND_PATH)
            print(f"[PhantomAnim] Sound loaded: {self.SOUND_PATH}")
        except (pygame.error, FileNotFoundError):
            print(f"[PhantomAnim] WARNING – missing sound: {self.SOUND_PATH}")

    def start(self):
        self._load()
        if not self.frames:
            self.finished = True
            return
        self.is_playing = True
        self.finished   = False
        self._frame_idx = 0
        self._tick      = 0
        if self.sound:
            self.sound.play()

    def update(self):
        if not self.is_playing:
            return
        self._tick += 1
        if self._tick >= self.FRAME_DELAY:
            self._tick = 0
            self._frame_idx += 1
            if self._frame_idx >= len(self.frames):
                self.is_playing = False
                self.finished   = True

    def draw(self, screen: pygame.Surface):
        if not self.is_playing or not self.frames:
            return
        idx = min(self._frame_idx, len(self.frames) - 1)
        screen.blit(self.frames[idx], (0, 0))

    def reset(self):
        self.is_playing = False
        self.finished   = False
        self._frame_idx = 0
        self._tick      = 0