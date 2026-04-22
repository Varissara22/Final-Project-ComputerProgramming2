import math
import pygame
import sys

SCREEN_W, SCREEN_H = 1000, 700
FPS = 60

C_BLACK  = (  0,   0,   0)
C_WHITE  = (255, 255, 255)
C_DIM    = (180, 180, 180)
C_GOLD   = (220, 185,  60)
C_RED    = (180,  60,  60)

PASS_LINES = [
    ("EVALUATION COMPLETE", "title"),
    ("", "gap"),
    ("Final Average Accuracy:  {avg:.1f}%", "stat"),
    ("", "gap"),
    ("...", "pause"),
    ("", "gap"),
    ("A note slides under the door.", "body"),
    ("", "gap"),
    ('"I will admit,"', "body"),
    ('"I did not expect you to make it."', "body"),
    ("", "gap"),
    ('"But the spirits rested."', "body"),
    ('"The clinic is still standing."', "body"),
    ('"And I have not had to order any hay."', "body"),
    ("", "gap"),
    ('"You pass."', "body"),
    ("", "gap"),
    ("Manager Grimoire sets down her pen.", "body"),
    ("For the first time, she almost smiles.", "body"),
    ("", "gap"),
    ("", "gap"),
    ("INTERNSHIP COMPLETE", "subtitle"),
    ("Thank you for playing Soul Steep.", "credit"),
]

FAIL_LINES = [
    ("EVALUATION COMPLETE", "title"),
    ("", "gap"),
    ("Final Average Accuracy:  {avg:.1f}%", "stat"),
    ("", "gap"),
    ("...", "pause"),
    ("", "gap"),
    ("A letter arrives.", "body"),
    ("", "gap"),
    ('"I am not angry."', "body"),
    ('"I am simply... disappointed."', "body"),
    ("", "gap"),
    ('"The spirits were not helped."', "body"),
    ('"The clinic suffered."', "body"),
    ('"And I have paperwork to do because of you."', "body"),
    ("", "gap"),
    ('"I have filed the rebirth request."', "body"),
    ('"The paddock is ready."', "body"),
    ('"I hope you enjoy grass."', "body"),
    ("", "gap"),
    ("Somewhere, a donkey is born.", "body"),
    ("It seems content.", "body"),
    ("", "gap"),
    ("", "gap"),
    ("INTERNSHIP FAILED", "subtitle"),
    ("Thank you for playing Soul Steep.", "credit"),
]

def _get_font(size, bold=False):
    for name in ("Comic Sans MS", "Bradley Hand ITC", "Segoe Print",
                 "Chalkboard SE", "Arial"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)

def run_ending_screen(screen: pygame.Surface,
                      clock:  pygame.time.Clock,
                      overall_avg: float):
    passed = overall_avg >= 70.0
    lines  = PASS_LINES if passed else FAIL_LINES
    accent = C_GOLD if passed else C_RED

    font_title    = _get_font(36, bold=True)
    font_subtitle = _get_font(28, bold=True)
    font_stat     = _get_font(26, bold=True)
    font_body     = _get_font(21)
    font_credit   = _get_font(16)
    font_hint     = _get_font(14)

    rendered = []
    for text, style in lines:
        text = text.replace("{avg:.1f}%", f"{overall_avg:.1f}%")
        if style == "title":
            surf = font_title.render(text, True, accent)
        elif style == "subtitle":
            surf = font_subtitle.render(text, True, accent)
        elif style == "stat":
            surf = font_stat.render(text, True, C_WHITE)
        elif style == "pause":
            surf = font_body.render(text, True, C_DIM)
        elif style == "credit":
            surf = font_credit.render(text, True, C_DIM)
        elif style == "gap":
            surf = None
        else:
            surf = font_body.render(text, True, C_WHITE)
        rendered.append((surf, style))

    LINE_H    = font_body.get_height() + 6
    GAP_H     = LINE_H // 2
    total_h   = sum(GAP_H if s == "gap" else LINE_H for _, s in rendered)
    start_y   = max(30, (SCREEN_H - total_h) // 2)

    REVEAL_DELAY = 55
    revealed      = 0
    tick_counter  = 0
    all_shown     = False

    hint = font_hint.render(
        "— click or press any key to continue —", True, C_DIM)
    hint_rect = hint.get_rect(center=(SCREEN_W // 2, SCREEN_H - 28))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                if all_shown:
                    return
                else:
                    revealed = len(rendered)
                    all_shown = True

        if not all_shown:
            tick_counter += 1
            if tick_counter >= REVEAL_DELAY:
                tick_counter = 0
                if revealed < len(rendered):
                    revealed += 1
                else:
                    all_shown = True

        screen.fill(C_BLACK)

        y = start_y
        for i, (surf, style) in enumerate(rendered[:revealed]):
            if style == "gap" or surf is None:
                y += GAP_H
                continue
            x = SCREEN_W // 2 - surf.get_width() // 2
            screen.blit(surf, (x, y))
            y += LINE_H

        if all_shown:
            alpha = 160 + int(80 * abs(math.sin(
                pygame.time.get_ticks() / 600)))
            hint_s = hint.copy()
            hint_s.set_alpha(alpha)
            screen.blit(hint_s, hint_rect)

        pygame.display.flip()
        clock.tick(FPS)