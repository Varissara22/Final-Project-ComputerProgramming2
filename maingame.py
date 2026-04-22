import pygame
import sys
import csv
import os
import datetime
from typing import Optional

from ghost               import Ghost
from teapot              import Teapot
from save_system         import save_game, delete_save
from how_to_play         import run_how_to_play
from tutorial            import run_tutorial
from manager_message     import run_manager_message
from animation           import BrewingAnimation
from ghost_to_phantom    import GhostToPhantomAnimation
from daily_letter        import run_daily_letter
from hint_card           import draw_hint_text_card, handle_hint_card_event
from ending_screen       import run_ending_screen

SCREEN_W, SCREEN_H = 1000, 700
BG_W        = 1420
MAX_SCROLL  = BG_W - SCREEN_W
SCROLL_SPEED = 8
EDGE_MARGIN  = 100
FPS = 60

BTN_W, BTN_H         = 53,  52
KETTLE_W, KETTLE_H   = 175, 100
BASE_W,   BASE_H     = 53,  100
TEABAG_W, TEABAG_H   = 50,   50
TOPPING_W, TOPPING_H = 50,   60
SUBMIT_W, SUBMIT_H   = 120,  60
DELETE_W, DELETE_H   = 150, 120

ICON_BTN_SIZE = 42
ICON_MARGIN   = 8

EMOTION_COLORS = {
    'h': (255, 223,   0),
    's': ( 30, 144, 255),
    'a': (255,  69,   0),
    'f': (138,  43, 226),
}

WARNING_FRAMES = 120
GHOSTS_PER_DAY = 5
TOTAL_DAYS     = 7

C_INK    = ( 62,  75, 130)
C_PAPER  = (248, 247, 244)
C_ICON   = (240, 240, 255)
C_ACCENT = (220, 225, 255)
C_FAINT  = (150, 155, 180)

def log_game_data(session_id, day, ghost_no, total_ghost_no,
                  accuracy,
                  water, teabag, topping,
                  duration_sec, click_count):

    fname = 'soul_steep_data.csv'
    write_header = not os.path.isfile(fname)
    with open(fname, mode='a', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        if write_header:
            w.writerow([
                'Session_ID', 'Day', 'Ghost_No', 'Total_Ghost_No',
                'Accuracy_Score',
                'Water', 'TeaBag', 'Topping',
                'Diagnostic_Duration_Sec', 'Click_Count',
                'Timestamp',
            ])
        w.writerow([
            session_id, day, ghost_no, total_ghost_no,
            f"{accuracy:.2f}",
            water, teabag, topping,
            f"{duration_sec:.2f}", click_count,
            datetime.datetime.now(),
        ])

def safe_load(path: str, fallback_size=(100, 100),
              fallback_color=(200, 50, 200)):
    try:
        return pygame.image.load(path).convert_alpha()
    except (pygame.error, FileNotFoundError):
        s = pygame.Surface(fallback_size)
        s.fill(fallback_color)
        return s

def score_accuracy(ghost: Ghost, teapot: Teapot):
    emotions = ('happiness', 'sadness', 'anger', 'fear')
    gv = [getattr(ghost,  e) for e in emotions]
    tv = [getattr(teapot, e) for e in emotions]
    diff = sum(abs(g - t) for g, t in zip(gv, tv))
    return max(0.0, 100.0 - (diff / (sum(gv) or 100) * 100))

def get_font(size: int, bold: bool = False):
    for name in ("Comic Sans MS", "Bradley Hand ITC", "Segoe Print",
                 "Chalkboard SE", "Arial"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)

def build_rects():
    return {
        'hint_happiness': pygame.Rect(520, 160, BTN_W,    BTN_H),
        'hint_sadness':   pygame.Rect(600, 160, BTN_W,    BTN_H),
        'hint_anger':     pygame.Rect(680, 160, BTN_W,    BTN_H),
        'hint_fear':      pygame.Rect(760, 160, BTN_W,    BTN_H),
        'water_h':  pygame.Rect(200, 300, BASE_W,   BASE_H),
        'water_s':  pygame.Rect(260, 300, BASE_W,   BASE_H),
        'water_a':  pygame.Rect(320, 300, BASE_W,   BASE_H),
        'water_f':  pygame.Rect(380, 300, BASE_W,   BASE_H),
        'teabag_h': pygame.Rect(510, 332, TEABAG_W, TEABAG_H),
        'teabag_s': pygame.Rect(605, 332, TEABAG_W, TEABAG_H),
        'teabag_a': pygame.Rect(700, 332, TEABAG_W, TEABAG_H),
        'teabag_f': pygame.Rect(795, 332, TEABAG_W, TEABAG_H),
        'topping_h': pygame.Rect( 950, 140, TOPPING_W, TOPPING_H),
        'topping_s': pygame.Rect(1100, 220, TOPPING_W, TOPPING_H),
        'topping_a': pygame.Rect(1000, 300, TOPPING_W, 50),
        'topping_f': pygame.Rect(1050, 370, TOPPING_W, 52),
        'kettle': pygame.Rect(  2, 285, KETTLE_W, KETTLE_H),
        'submit': pygame.Rect(1250, 300, SUBMIT_W, SUBMIT_H),
        'delete': pygame.Rect(  20, 550, DELETE_W, DELETE_H),
    }

def sr(world: pygame.Rect, cam):
    return pygame.Rect(world.x - cam, world.y, world.width, world.height)

def _make_ghost_hints(ghost):
    return {
        emotion: (emotion,) + ghost.get_hint_clue(emotion)
        for emotion in ('happiness', 'sadness', 'anger', 'fear')
    }

def _update_bgm(state, bgm):
    scores = state['day_accuracy_scores']
    avg = (sum(scores) / len(scores)) if scores else 50.0
    if avg < 33:
        track = "tense"
    elif avg <= 70:
        track = "main"
    else:
        track = "calm"
    bgm.playMusic(track)

def _reset_ghost_tracking(state):
    state['ghost_spawn_time'] = pygame.time.get_ticks()
    state['click_count']      = 0

class WarningSystem:
    def __init__(self, font: pygame.font.Font):
        self.font  = font
        self.msg   = ""
        self.timer = 0

    def show(self, text):
        self.msg   = text
        self.timer = WARNING_FRAMES

    def draw(self, screen: pygame.Surface):
        if self.timer <= 0:
            return

        alpha = 255 if self.timer > 40 else int(255 * (self.timer / 40))

        surf = self.font.render(self.msg, True, C_INK)
        rect = surf.get_rect(center=(SCREEN_W // 2, 130))
        pad  = pygame.Rect(rect.x - 16, rect.y - 10, rect.w + 32, rect.h + 20)

        card = pygame.Surface((pad.width, pad.height), pygame.SRCALPHA)
        card.fill((248, 247, 244, min(alpha, 230)))

        pygame.draw.rect(card, (*C_INK, alpha), card.get_rect(), 2, border_radius=6)

        pygame.draw.rect(card, (*C_INK, alpha),
                         pygame.Rect(0, 0, 5, pad.height), border_radius=3)
        screen.blit(card, (pad.x, pad.y))

        text_surf = self.font.render(self.msg, True, (*C_INK,))
        text_surf.set_alpha(alpha)
        screen.blit(text_surf, rect)

        self.timer -= 1

class HUD:
    def __init__(self):
        self.font_day    = get_font(36, bold=True)
        self.font_spirit = get_font(20)
        self.font_label  = get_font(14)

    def draw(self, screen: pygame.Surface,
             current_day, ghosts_today, total_ghosts):
        
        card = pygame.Rect(10, 10, 190, 92)
        pygame.draw.rect(screen, C_PAPER,  card, border_radius=8)
        pygame.draw.rect(screen, C_INK,    card, 2,  border_radius=8)
        
        pygame.draw.rect(screen, C_INK,
                         pygame.Rect(10, 10, 190, 8), border_radius=8)

        
        day_surf = self.font_day.render(f"DAY  {current_day}", True, C_INK)
        screen.blit(day_surf, (22, 24))

        
        pygame.draw.line(screen, (*C_INK, 120), (20, 66), (192, 66), 1)

        
        spirit_txt = f"Spirit:  {ghosts_today + 1} / {total_ghosts}"
        sp_surf = self.font_spirit.render(spirit_txt, True, C_INK)
        screen.blit(sp_surf, (22, 72))

class SoundManager:
    DEFAULT_LIBRARY = {
        "main":    "GameSoundBg/winter-waltz-by-scott-buckley.mp3",
        "calm":    "GameSoundBg/hyperfun-by-kevin-macleod.mp3",
        "tense":   "GameSoundBg/source-damour-by-arthur-marie-brillouin.mp3",
    }

    def __init__(self, bgmVolume = 0.3, library: Optional[dict] = None):
        self.bgmVolume  = max(0.0, min(1.0, bgmVolume))
        self.library    = library if library is not None else dict(self.DEFAULT_LIBRARY)
        self._current   = None    

        if not pygame.mixer.get_init():
            try:
                pygame.mixer.init()
            except pygame.error as e:
                print(f"[SoundManager] Mixer init failed: {e}")

    def playMusic(self, track_name: str = "main"):
        if track_name == self._current and pygame.mixer.music.get_busy():
            return   

        path = self.library.get(track_name)
        if path is None:
            print(f"[SoundManager] Unknown track: {track_name!r}")
            return

        try:
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(self.bgmVolume)
            pygame.mixer.music.play(loops=-1)
            self._current = track_name
            print(f"[SoundManager] Playing: {path}")
        except pygame.error as e:
            print(f"[SoundManager] Could not play {path!r}: {e}")

    def stopMusic(self):
        pygame.mixer.music.stop()
        self._current = None

    def setVolume(self, v):
        self.bgmVolume = max(0.0, min(1.0, v))
        pygame.mixer.music.set_volume(self.bgmVolume)

class IconButton:
    def __init__(self, label: str, rect: pygame.Rect, font: pygame.font.Font):
        self.label = label
        self.rect  = rect
        self.font  = font

    def draw(self, screen: pygame.Surface):
        hov  = self.rect.collidepoint(pygame.mouse.get_pos())
        fill = C_ACCENT if hov else C_ICON
        pygame.draw.rect(screen, fill,  self.rect, border_radius=6)
        pygame.draw.rect(screen, C_INK, self.rect, 2, border_radius=6)
        surf = self.font.render(self.label, True, C_INK)
        screen.blit(surf, surf.get_rect(center=self.rect.center))

    def clicked(self, event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))

def run_pause_menu(screen, clock, background, cam_x, bgm=None) -> str:
    font_h  = get_font(30, bold=True)
    font_b  = get_font(22)
    font_sm = get_font(16)

    options = [("RESUME",        "resume"),
               ("EXIT TO TITLE", "title"),
               ("EXIT GAME",     "exit")]

    panel_w, panel_h = 360, 380
    px = (SCREEN_W - panel_w) // 2
    py = (SCREEN_H - panel_h) // 2

    btn_rects = [pygame.Rect(px + 30, py + 190 + i * 62, panel_w - 60, 48)
                 for i in range(len(options))]

    SLIDER_X  = px + 30
    SLIDER_Y  = py + 110
    SLIDER_W  = panel_w - 60
    SLIDER_H  = 8
    THUMB_R   = 10

    volume = bgm.bgmVolume if bgm else 0.3
    dragging = False

    def vol_to_x(v):
        return SLIDER_X + int(v * SLIDER_W)

    def x_to_vol(x):
        return max(0.0, min(1.0, (x - SLIDER_X) / SLIDER_W))

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return 'resume'

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                tx = vol_to_x(volume)
                thumb_rect = pygame.Rect(tx - THUMB_R, SLIDER_Y - THUMB_R,
                                         THUMB_R * 2, THUMB_R * 2)
                track_rect = pygame.Rect(SLIDER_X, SLIDER_Y - SLIDER_H,
                                         SLIDER_W, SLIDER_H * 3)
                if thumb_rect.collidepoint(event.pos) or track_rect.collidepoint(event.pos):
                    dragging = True
                    volume = x_to_vol(event.pos[0])
                    if bgm:
                        bgm.setVolume(volume)
                else:
                    for rect, (_, action) in zip(btn_rects, options):
                        if rect.collidepoint(event.pos):
                            return action

            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False

            if event.type == pygame.MOUSEMOTION and dragging:
                volume = x_to_vol(mouse[0])
                if bgm:
                    bgm.setVolume(volume)

        screen.blit(background, (-cam_x, 0))
        ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 160))
        screen.blit(ov, (0, 0))

        panel = pygame.Rect(px, py, panel_w, panel_h)
        pygame.draw.rect(screen, C_PAPER, panel, border_radius=10)
        pygame.draw.rect(screen, C_INK,   panel, 3,  border_radius=10)

        ts = font_h.render("PAUSED", True, C_INK)
        screen.blit(ts, ts.get_rect(center=(SCREEN_W // 2, py + 40)))

        vol_label = font_sm.render(f"Music Volume  —  {int(volume * 100)}%", True, C_INK)
        screen.blit(vol_label, (SLIDER_X, SLIDER_Y - 28))

        fill_w = int(volume * SLIDER_W)
        pygame.draw.rect(screen, (210, 215, 230),
                         (SLIDER_X, SLIDER_Y - SLIDER_H // 2,
                          SLIDER_W, SLIDER_H), border_radius=4)
        if fill_w > 0:
            pygame.draw.rect(screen, C_INK,
                             (SLIDER_X, SLIDER_Y - SLIDER_H // 2,
                              fill_w, SLIDER_H), border_radius=4)

        tx = vol_to_x(volume)
        pygame.draw.circle(screen, C_INK,   (tx, SLIDER_Y), THUMB_R)
        pygame.draw.circle(screen, C_PAPER, (tx, SLIDER_Y), THUMB_R - 3)

        screen.blit(font_sm.render("0",   True, C_FAINT),
                    (SLIDER_X - 8, SLIDER_Y + 14))
        screen.blit(font_sm.render("100", True, C_FAINT),
                    (SLIDER_X + SLIDER_W - 16, SLIDER_Y + 14))

        pygame.draw.line(screen, (*C_INK, 60),
                         (px + 20, py + 150), (px + panel_w - 20, py + 150), 1)

        for rect, (label, _) in zip(btn_rects, options):
            hov  = rect.collidepoint(mouse)
            fill = C_ACCENT if hov else C_PAPER
            pygame.draw.rect(screen, fill,  rect, border_radius=5)
            pygame.draw.rect(screen, C_INK, rect, 2, border_radius=5)
            ls = font_b.render(label, True, C_INK)
            screen.blit(ls, ls.get_rect(center=rect.center))

        pygame.display.flip()
        clock.tick(FPS)

def handle_click(pos, rects, cam, state, warning):
    def hit(name): return sr(rects[name], cam).collidepoint(pos)

    if hit('delete'):
        if state['teapot']:
            state['teapot'] = None
            state['click_count'] += 1
        else:
            warning.show("No teapot to delete!")
        return

    if hit('submit'):
        tp = state['teapot']
        if tp and tp.is_complete:
            acc          = score_accuracy(state['ghost'], tp)
            duration_sec = (pygame.time.get_ticks() - state['ghost_spawn_time']) / 1000.0
            state['ghosts_served_today'] += 1
            state['total_ghost_no']      += 1
            state['day_accuracy_scores'].append(acc)
            state['last_accuracy'] = acc
            log_game_data(
                state['session_id'],
                state['current_day'],
                state['ghosts_served_today'],
                state['total_ghost_no'],
                acc,
                tp.basewater, tp.teabag, tp.topping,
                duration_sec,
                state['click_count'],
            )
            state['anim'].start()
            state['teapot'] = None
        else:
            warning.show("Finish brewing before serving!")
        return

    if hit('kettle'):
        if state['teapot'] is None:
            state['teapot'] = Teapot()
            state['click_count'] += 1
        else:
            warning.show("Teapot already exists!")
        return

    for code in ('h', 's', 'a', 'f'):
        if hit(f'water_{code}'):
            state['click_count'] += 1
            if state['teapot']:
                if not state['teapot'].add_basewater(code):
                    warning.show("Base water already added!")
            else:
                warning.show("Create a teapot first!")
            return

    for code in ('h', 's', 'a', 'f'):
        if hit(f'teabag_{code}'):
            state['click_count'] += 1
            tp = state['teapot']
            if tp:
                if not tp.add_teabag(code):
                    warning.show("Add water before tea bag!" if tp.basewater == 'Not'
                                 else "Tea bag already added!")
            else:
                warning.show("Create a teapot first!")
            return

    for code in ('h', 's', 'a', 'f'):
        if hit(f'topping_{code}'):
            state['click_count'] += 1
            tp = state['teapot']
            if tp:
                if not tp.add_topping(code):
                    warning.show("Add tea bag before topping!" if tp.teabag == 'Not'
                                 else "Topping already added!")
            else:
                warning.show("Create a teapot first!")
            return

    for emotion in ('happiness', 'sadness', 'anger', 'fear'):
        if hit(f'hint_{emotion}'):
            state['click_count'] += 1
            state['hint_card'] = state['ghost_hints'][emotion]
            return

def draw_buttons(screen, rects, cam, teapot, kettle_img, hint_imgs,
                 water_imgs, teabag_imgs, topping_imgs, submit_img, delete_img,
                 waterchose_imgs, teabagchose_imgs, toppingchose_imgs, kettleempty_img):
    for emotion, code in (('happiness','h'),('sadness','s'),
                           ('anger','a'),('fear','f')):
        r   = sr(rects[f'hint_{emotion}'], cam)
        img = hint_imgs.get(emotion)
        if img:
            screen.blit(img, r)
            if r.collidepoint(pygame.mouse.get_pos()):
                glow = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                glow.fill((255, 255, 255, 55))
                screen.blit(glow, r)
        else:
            pygame.draw.rect(screen, EMOTION_COLORS[code], r)

    for code in ('h', 's', 'a', 'f'):
        r   = sr(rects[f'water_{code}'], cam)
        img = water_imgs.get(code)
        if img:
            screen.blit(img, r)
            if r.collidepoint(pygame.mouse.get_pos()):
                glow = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                glow.fill((255, 255, 255, 55))
                screen.blit(glow, r)
        else:
            pygame.draw.rect(screen, EMOTION_COLORS[code], r)

    for code in ('h', 's', 'a', 'f'):
        r   = sr(rects[f'teabag_{code}'], cam)
        img = teabag_imgs.get(code)
        if img:
            screen.blit(img, r)
            if r.collidepoint(pygame.mouse.get_pos()):
                glow = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                glow.fill((255, 255, 255, 55))
                screen.blit(glow, r)
        else:
            pygame.draw.rect(screen, EMOTION_COLORS[code], r)

    for code in ('h','s','a','f'):
        r   = sr(rects[f'topping_{code}'], cam)
        img = topping_imgs.get(code)
        if img:
            screen.blit(img, r)
            if r.collidepoint(pygame.mouse.get_pos()):
                glow = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
                glow.fill((255, 255, 255, 55))
                screen.blit(glow, r)
        else:
            pygame.draw.rect(screen, EMOTION_COLORS[code], r)

    kr  = sr(rects['kettle'], cam)
    screen.blit(kettle_img, kr)
    if kr.collidepoint(pygame.mouse.get_pos()):
        glow = pygame.Surface((kr.w, kr.h), pygame.SRCALPHA)
        glow.fill((255, 255, 255, 55))
        screen.blit(glow, kr)

    sub_r = sr(rects['submit'], cam)
    if submit_img:
        screen.blit(submit_img, sub_r)
        if sub_r.collidepoint(pygame.mouse.get_pos()):
            glow = pygame.Surface((sub_r.w, sub_r.h), pygame.SRCALPHA)
            glow.fill((255, 255, 255, 55))
            screen.blit(glow, sub_r)
    else:
        pygame.draw.rect(screen, (34, 139, 34), sub_r)

    del_r = sr(rects['delete'], cam)
    if delete_img:
        screen.blit(delete_img, del_r)
        if del_r.collidepoint(pygame.mouse.get_pos()):
            glow = pygame.Surface((del_r.w, del_r.h), pygame.SRCALPHA)
            glow.fill((255, 255, 255, 55))
            screen.blit(glow, del_r)
    else:
        pygame.draw.rect(screen, (139, 69, 19), del_r, 3)
    tray_rect = pygame.Rect(550 - cam, 450, 150, 150)
    if teapot and kettleempty_img:
        screen.blit(kettleempty_img, tray_rect)

    IND = 55
    GAP = 10
    gx = 550 - cam
    gy = 450
    gw, gh = 150, 150

    def _draw_indicator(ix, iy, chosen, chose_imgs):
        if chosen == 'Not':
            return
        box = pygame.Rect(ix, iy, IND, IND)
        img = chose_imgs.get(chosen) if chose_imgs else None
        if img:
            screen.blit(img, box)
        else:
            pygame.draw.rect(screen, EMOTION_COLORS[chosen], box, border_radius=8)
            pygame.draw.rect(screen, (62, 75, 130),           box, 2, border_radius=8)

    water_chosen  = teapot.basewater if teapot else 'Not'
    teabag_chosen = teapot.teabag    if teapot else 'Not'
    topping_chosen= teapot.topping   if teapot else 'Not'

    _draw_indicator(gx - IND - GAP,       gy + (gh - IND)//2, water_chosen,   waterchose_imgs)
    _draw_indicator(gx + gw + GAP,        gy + (gh - IND)//2, teabag_chosen,  teabagchose_imgs)
    _draw_indicator(gx + (gw - IND)//2,   gy + gh + GAP,      topping_chosen, toppingchose_imgs)

def run_main_game(screen: pygame.Surface, clock: pygame.time.Clock,
                  save_data: Optional[dict] = None) -> str:

    font_warn = get_font(26, bold=True)
    font_icon = get_font(22, bold=True)

    warning = WarningSystem(font_warn)
    hud     = HUD()
    rects   = build_rects()
    anim    = BrewingAnimation()
    bgm     = SoundManager(bgmVolume=0.5)
    bgm.playMusic("main")
    phantom_anim = GhostToPhantomAnimation()

    background_default = safe_load("Game_png/Background.png", (BG_W, SCREEN_H), (50, 50, 50))

    _kr = rects['kettle']
    _kettle_paths = [
        "KettleTea.PNG",
        "KettleTea.png",
        "Game_png/Kettle/KettleTea.PNG",
        "Game_png/Kettle/KettleTea.png",
        "Game_png/KettleTea.PNG",
    ]
    _kettle_raw = None
    for _p in _kettle_paths:
        try:
            _kettle_raw = pygame.image.load(_p).convert_alpha()
            print(f"[Kettle] Loaded from: {_p}")
            break
        except (pygame.error, FileNotFoundError):
            continue
    if _kettle_raw is None:
        print("[Kettle] WARNING: KettleTea.PNG not found in any expected location.")
        print("         Tried:", _kettle_paths)
        _kettle_raw = pygame.Surface((_kr.width, _kr.height), pygame.SRCALPHA)
        _kettle_raw.fill((255, 0, 255))
    kettle_img = pygame.transform.smoothscale(_kettle_raw, (_kr.width, _kr.height))

    def _load_hint_img(name, w, h):
        for _p in [f"{name}.png", f"{name}.PNG",
                   f"Game_png/{name}.png", f"Game_png/{name}.PNG",
                   f"Game_png/Hint/{name}.png", f"Game_png/Hint/{name}.PNG"]:
            try:
                surf = pygame.image.load(_p).convert_alpha()
                print(f"[Hint] Loaded from: {_p}")
                return pygame.transform.smoothscale(surf, (w, h))
            except (pygame.error, FileNotFoundError):
                continue
        print(f"[Hint] WARNING: {name}.png not found — using colour fallback.")
        return None

    _hw, _hh = BTN_W, BTN_H
    hint_imgs = {
        'happiness': _load_hint_img("hint_happiness", _hw, _hh),
        'sadness':   _load_hint_img("hint_sadness",   _hw, _hh),
        'anger':     _load_hint_img("hint_anger",     _hw, _hh),
        'fear':      _load_hint_img("hint_fear",      _hw, _hh),
    }

    water_imgs = {
        'h': _load_hint_img("water_h", BASE_W, BASE_H),
        's': _load_hint_img("water_s", BASE_W, BASE_H),
        'a': _load_hint_img("water_a", BASE_W, BASE_H),
        'f': _load_hint_img("water_f", BASE_W, BASE_H),
    }

    teabag_imgs = {
        'h': _load_hint_img("teabag_h", TEABAG_W, TEABAG_H),
        's': _load_hint_img("teabag_s", TEABAG_W, TEABAG_H),
        'a': _load_hint_img("teabag_a", TEABAG_W, TEABAG_H),
        'f': _load_hint_img("teabag_f", TEABAG_W, TEABAG_H),
    }

    topping_imgs = {
        'h': _load_hint_img("topping_h", TOPPING_W, TOPPING_H),
        's': _load_hint_img("topping_s", TOPPING_W, TOPPING_H),
        'a': _load_hint_img("topping_a", TOPPING_W, 50),
        'f': _load_hint_img("topping_f", TOPPING_W, 52),
    }

    submit_img = _load_hint_img("submit", SUBMIT_W, SUBMIT_H)
    delete_img = _load_hint_img("delete", DELETE_W, DELETE_H)

    IND = 55
    waterchose_imgs = {
        'h': _load_hint_img("waterchose_h",   IND, IND),
        's': _load_hint_img("waterchose_s",   IND, IND),
        'a': _load_hint_img("waterchose_a",   IND, IND),
        'f': _load_hint_img("waterchose_f",   IND, IND),
    }
    teabagchose_imgs = {
        'h': _load_hint_img("teabagchose_h",  IND, IND),
        's': _load_hint_img("teabagchose_s",  IND, IND),
        'a': _load_hint_img("teabagchose_a",  IND, IND),
        'f': _load_hint_img("teabagchose_f",  IND, IND),
    }
    toppingchose_imgs = {
        'h': _load_hint_img("toppingchose_h", IND, IND),
        's': _load_hint_img("toppingchose_s", IND, IND),
        'a': _load_hint_img("toppingchose_a", IND, IND),
        'f': _load_hint_img("toppingchose_f", IND, IND),
    }
    kettleempty_img = _load_hint_img("kettleempty_", 150, 150)

    assets = {
        'background':   background_default,
        'kettle':       kettle_img,
        'hint':         hint_imgs,
        'water':        water_imgs,
        'teabag':       teabag_imgs,
        'topping':      topping_imgs,
        'submit':       submit_img,
        'delete':       delete_img,
        'waterchose':   waterchose_imgs,
        'teabagchose':  teabagchose_imgs,
        'toppingchose': toppingchose_imgs,
        'kettleempty':  kettleempty_img,
    }

    pause_rect = pygame.Rect(SCREEN_W - ICON_BTN_SIZE - ICON_MARGIN,
                             ICON_MARGIN, ICON_BTN_SIZE, ICON_BTN_SIZE)
    htp_rect   = pygame.Rect(SCREEN_W - ICON_BTN_SIZE * 2 - ICON_MARGIN * 2,
                             ICON_MARGIN, ICON_BTN_SIZE, ICON_BTN_SIZE)
    btn_pause  = IconButton("||", pause_rect, font_icon)
    btn_htp    = IconButton("?",  htp_rect,  font_icon)

    sd = save_data or {}
    _first_ghost = Ghost()
    _session_id  = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    state = {
        'running':             True,
        'current_day':         sd.get('current_day',         1),
        'ghosts_served_today': sd.get('ghosts_served_today', 0),
        'ghost':               _first_ghost,
        'ghost_hints':         _make_ghost_hints(_first_ghost),
        'teapot':              None,
        'hint_card':           None,
        'hint_scroll':         0,
        'day_accuracy_scores': [],
        'all_accuracy_scores': [],
        'pending_day_end':     False,
        'anim':                anim,
        'phantom_anim':        phantom_anim,
        'last_accuracy':       0.0,
        'session_id':          _session_id,
        'total_ghost_no':      sd.get('ghosts_served_today', 0),
        'ghost_spawn_time':    pygame.time.get_ticks(),
        'click_count':         0,
    }
    camera_x = 0

    if save_data is None:
        run_tutorial(screen, clock, assets)

    if state['ghosts_served_today'] == 0:
        background = background_default
        run_daily_letter(screen, clock, state['current_day'], background, camera_x)

    while state['running']:
        background = background_default
        mouse_pos = pygame.mouse.get_pos()

        if state['pending_day_end']:
            state['pending_day_end'] = False

            completed_day = state['current_day']
            scores = state['day_accuracy_scores']
            avg    = (sum(scores) / len(scores)) if scores else 0.0

            state['all_accuracy_scores'].extend(scores)

            state['current_day'] += 1
            state['ghosts_served_today'] = 0
            state['day_accuracy_scores'] = []

            if state['current_day'] > TOTAL_DAYS:
                run_manager_message(screen, clock, completed_day, avg)
                delete_save()
                bgm.stopMusic()
                all_scores = state['all_accuracy_scores']
                overall_avg = (sum(all_scores) / len(all_scores)) if all_scores else 0.0
                run_ending_screen(screen, clock, overall_avg)
                state['running'] = False
                continue

            save_game(state['current_day'], 0)

            run_manager_message(screen, clock, completed_day, avg)

            background = background_default
            run_daily_letter(screen, clock, state['current_day'], background, camera_x)

            state['ghost']       = Ghost()
            state['ghost_hints'] = _make_ghost_hints(state['ghost'])
            state['teapot'] = None
            bgm.playMusic("main")
            _reset_ghost_tracking(state)
            continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(state['current_day'], state['ghosts_served_today'])
                bgm.stopMusic()
                pygame.quit(); sys.exit()

            if anim.is_playing:
                if anim.handle_event(event):
                    anim.skip()
                continue

            if state['phantom_anim'].is_playing:
                continue

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                result = run_pause_menu(screen, clock, background, camera_x, bgm)
                if result == 'title':
                    save_game(state['current_day'], state['ghosts_served_today'])
                    bgm.stopMusic()
                    return 'title'
                elif result == 'exit':
                    save_game(state['current_day'], state['ghosts_served_today'])
                    bgm.stopMusic()
                    pygame.quit(); sys.exit()

            elif event.type == pygame.MOUSEWHEEL and state['hint_card']:
                result = handle_hint_card_event(event, state)
                if result == 'close':
                    state['hint_card']   = None
                    state['hint_scroll'] = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_pause.clicked(event):
                    result = run_pause_menu(screen, clock, background, camera_x, bgm)
                    if result == 'title':
                        save_game(state['current_day'], state['ghosts_served_today'])
                        bgm.stopMusic()
                        return 'title'
                    elif result == 'exit':
                        save_game(state['current_day'], state['ghosts_served_today'])
                        bgm.stopMusic()
                        pygame.quit(); sys.exit()

                elif btn_htp.clicked(event):
                    run_how_to_play(screen, clock)

                elif state['hint_card']:
                    result = handle_hint_card_event(event, state)
                    if result == 'close':
                        state['hint_card']   = None
                        state['hint_scroll'] = 0

                else:
                    handle_click(event.pos, rects, camera_x, state, warning)

        if anim.is_playing:
            anim.update()

        if anim.finished:
            anim.reset()
            _update_bgm(state, bgm)
            if state['last_accuracy'] < 10:
                state['phantom_anim'].start()
            elif state['ghosts_served_today'] >= GHOSTS_PER_DAY:
                state['pending_day_end'] = True
            else:
                save_game(state['current_day'], state['ghosts_served_today'])
                state['ghost'] = Ghost()
                state['ghost_hints'] = _make_ghost_hints(state['ghost'])
                _reset_ghost_tracking(state)

        elif state['phantom_anim'].is_playing:
            state['phantom_anim'].update()

        elif state['phantom_anim'].finished:
            state['phantom_anim'].reset()
            if state['ghosts_served_today'] >= GHOSTS_PER_DAY:
                state['pending_day_end'] = True
            else:
                save_game(state['current_day'], state['ghosts_served_today'])
                state['ghost'] = Ghost()
                state['ghost_hints'] = _make_ghost_hints(state['ghost'])
                _reset_ghost_tracking(state)
        if not anim.is_playing and not state['phantom_anim'].is_playing and not state['hint_card']:
            if mouse_pos[0] > SCREEN_W - EDGE_MARGIN:
                camera_x = min(camera_x + SCROLL_SPEED, MAX_SCROLL)
            elif mouse_pos[0] < EDGE_MARGIN:
                camera_x = max(camera_x - SCROLL_SPEED, 0)

        screen.blit(background, (-camera_x, 0))
        draw_buttons(screen, rects, camera_x, state['teapot'], kettle_img,
                     hint_imgs, water_imgs, teabag_imgs, topping_imgs, submit_img, delete_img,
                     waterchose_imgs, teabagchose_imgs, toppingchose_imgs, kettleempty_img)

        hud.draw(screen, state['current_day'],
                 state['ghosts_served_today'], GHOSTS_PER_DAY)

        btn_htp.draw(screen)
        btn_pause.draw(screen)
        warning.draw(screen)

        if state['hint_card']:
            state['hint_scroll'] = draw_hint_text_card(
                screen, *state['hint_card'], state['hint_scroll'])

        if anim.is_playing:
            anim.draw(screen)

        if state['phantom_anim'].is_playing:
            state['phantom_anim'].draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    bgm.stopMusic()
    return 'title'

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Soul Steep")
    clock = pygame.time.Clock()
    run_main_game(screen, clock)
    pygame.quit()