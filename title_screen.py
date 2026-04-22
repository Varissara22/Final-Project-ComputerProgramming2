import pygame
import sys
from typing import Optional
from save_system import has_save
from data_game import run_dashboard, has_data

C_BG        = (248, 247, 244)
C_INK       = ( 62,  75, 130)
C_BTN_FILL  = (255, 255, 255)
C_BTN_HOVER = (230, 235, 255)
C_BTN_LINE  = ( 62,  75, 130)

SCREEN_W, SCREEN_H = 1000, 700
FPS = 60

BTN_X      = 55
BTN_W, BTN_H = 260, 55
BTN_GAP    = 18
BTN_START_Y = 310
BTN_RADIUS  = 4

def _safe_load(path: str, size: Optional[tuple] = None) -> Optional[pygame.Surface]:
    try:
        img = pygame.image.load(path).convert_alpha()
        if size:
            img = pygame.transform.smoothscale(img, size)
        return img
    except (pygame.error, FileNotFoundError):
        return None

class TitleButton:

    def __init__(self, label: str, rect: pygame.Rect, font: pygame.font.Font):
        self.label  = label
        self.rect   = rect
        self.font   = font
        self.hovered = False

    def update(self, mouse_pos: tuple):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface):
        fill = C_BTN_HOVER if self.hovered else C_BTN_FILL
        pygame.draw.rect(surface, fill, self.rect, border_radius=BTN_RADIUS)
        pygame.draw.rect(surface, C_BTN_LINE, self.rect, 2, border_radius=BTN_RADIUS)
        text = self.font.render(self.label, True, C_INK)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))

MUSIC_CREDITS = [
    (
        "Hyperfun",
        "Kevin MacLeod  ·  incompetech.com",
        "License: CC BY 4.0",
        "https://youtu.be/Vugj1cii9Y0",
    ),
    (
        "Source d'Amour",
        "Arthur-Marie Brillouin  ·  soundcloud.com/amariamusique",
        "License: CC BY-NC-SA 3.0",
        "https://youtu.be/BtOc2Uo46hI",
    ),
    (
        "Winter Waltz",
        "Scott Buckley  ·  scottbuckley.com.au",
        "License: CC BY 4.0",
        "https://youtu.be/FdjMtzmVOGI",
    ),
    (
        "SPRINKLE.wav by genel",
        "genel",
        "License: Creative Commons",
        "https://freesound.org/s/611675/",
    ),
]

def run_credits(screen: pygame.Surface, clock: pygame.time.Clock):

    def get_font(size, bold=False):
        for name in ("Comic Sans MS", "Bradley Hand ITC", "Segoe Print",
                     "Chalkboard SE", "Arial"):
            try:
                return pygame.font.SysFont(name, size, bold=bold)
            except Exception:
                continue
        return pygame.font.Font(None, size)

    font_header = get_font(32, bold=True)
    font_title  = get_font(22, bold=True)
    font_body   = get_font(18)
    font_hint   = get_font(14)

    C_PANEL  = (255, 255, 255)
    CARD_W   = 680
    CARD_X   = (SCREEN_W - CARD_W) // 2

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return

        screen.fill(C_BG)

        for row in range(0, SCREEN_H, 30):
            pygame.draw.line(screen, (210, 215, 230), (0, row), (SCREEN_W, row), 1)

        pygame.draw.rect(screen, C_INK, (0, 0, SCREEN_W, 56))
        hs = font_header.render("MUSIC CREDITS", True, C_BG)
        screen.blit(hs, hs.get_rect(center=(SCREEN_W // 2, 28)))

        y = 76
        for track, artist, license_, url in MUSIC_CREDITS:
            card_h = 108
            card = pygame.Rect(CARD_X, y, CARD_W, card_h)
            pygame.draw.rect(screen, C_PANEL, card, border_radius=8)
            pygame.draw.rect(screen, C_INK,   card, 2, border_radius=8)
            pygame.draw.rect(screen, C_INK, (CARD_X, y, 5, card_h), border_radius=4)

            screen.blit(font_title.render(f"♪  {track}", True, C_INK),
                        (CARD_X + 16, y + 10))
            screen.blit(font_body.render(artist,   True, (70, 75, 110)),
                        (CARD_X + 16, y + 38))
            screen.blit(font_body.render(license_, True, (70, 75, 110)),
                        (CARD_X + 16, y + 62))
            screen.blit(font_hint.render(url,      True, (120, 130, 180)),
                        (CARD_X + 16, y + 86))
            y += card_h + 12

        game_s = font_body.render("Please going to support them by the link - From Manager",
                                  True, C_INK)
        screen.blit(game_s, game_s.get_rect(center=(SCREEN_W // 2, y + 20)))

        hint = font_hint.render("— click anywhere or press ESC to return —", True, (150, 155, 180))
        screen.blit(hint, hint.get_rect(center=(SCREEN_W // 2, SCREEN_H - 24)))

        pygame.display.flip()
        clock.tick(FPS)

def run_title_screen(screen: pygame.Surface,
                     clock:  pygame.time.Clock,
                     bg_image_path: str = "Game_png/TitleGameBg.jpg") -> str:
    def get_font(size: int, bold: bool = False) -> pygame.font.Font:
        for name in ("Comic Sans MS", "Bradley Hand ITC", "Segoe Print",
                     "Chalkboard SE", "Arial"):
            try:
                return pygame.font.SysFont(name, size, bold=bold)
            except Exception:
                continue
        return pygame.font.Font(None, size)

    font_title    = get_font(68, bold=True)
    font_subtitle = get_font(26)
    font_btn      = get_font(24)

    bg_surf = _safe_load(bg_image_path, (SCREEN_W, SCREEN_H))

    button_defs = [("NEW GAME",    "new_game"),
                   ("CREDITS",     "credits"),
                   ("EXIT GAME",   "exit")]
    if has_save():
        button_defs.insert(1, ("CONTINUE GAME", "continue"))
    if has_data():
        button_defs.insert(1, ("STATISTIC",   "statistic"))

    buttons: list[tuple[TitleButton, str]] = []
    for i, (label, action) in enumerate(button_defs):
        rect = pygame.Rect(BTN_X,
                           BTN_START_Y + i * (BTN_H + BTN_GAP),
                           BTN_W, BTN_H)
        buttons.append((TitleButton(label, rect, font_btn), action))

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();  sys.exit()

            for btn, action in buttons:
                if btn.is_clicked(event):
                    if action == 'credits':
                        run_credits(screen, clock)
                    elif action == 'statistic':
                        run_dashboard()
                    else:
                        return action

        screen.fill(C_BG)

        if bg_surf:
            screen.blit(bg_surf, (0, 0))
        else:
            screen.fill(C_BG)

        title_panel = pygame.Surface((420, 280), pygame.SRCALPHA)
        title_panel.fill((0, 0, 0, 0))
        screen.blit(title_panel, (30, 20))

        t1 = font_title.render("SOUL",   True, C_INK)
        t2 = font_title.render("STEEP",  True, C_INK)
        t3 = font_subtitle.render("AN INTERN'S TRAIL", True, C_INK)
        screen.blit(t1, (55, 30))
        screen.blit(t2, (55, 105))
        screen.blit(t3, (58, 185))

        for btn, _ in buttons:
            btn.update(mouse_pos)
            btn.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    return "exit"