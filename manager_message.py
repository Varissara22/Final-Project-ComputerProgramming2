import pygame
import sys

C_BG      = (248, 247, 244)
C_INK     = ( 62,  75, 130)
C_PANEL   = (255, 255, 255)
C_BORDER  = ( 62,  75, 130)
C_ACCENT  = (220, 225, 255)

SCREEN_W, SCREEN_H = 1000, 700
FPS = 60

MANAGER_LINES = {
    (0,  20): (
        "Manager",
        "…Are you even trying?",
        [
            "I watched you brew today and I nearly cried.",
            "The spirits left MORE distressed than when they arrived.",
            "Read the hint cards. Please. They exist for a reason.",
            "Come back tomorrow. We'll pretend this day never happened.",
        ]
    ),
    (20, 30): (
        "Manager",
        "This is… concerning.",
        [
            "I appreciate that you showed up. That is the kindest",
            "thing I can say about today's performance.",
            "Your brews were so mismatched the spirits filed complaints.",
            "Study the ingredient chart tonight. I'm serious.",
        ]
    ),
    (30, 40): (
        "Manager",
        "Room for improvement. A lot of room.",
        [
            "You're getting the steps right — water, tea, topping.",
            "But the emotional matching needs serious work.",
            "Think about what each spirit's hints are telling you.",
            "Tomorrow is a new day. Don't waste it.",
        ]
    ),
    (40, 50): (
        "Manager",
        "Below expectations, but I see some effort.",
        [
            "A few of your brews today were almost passable.",
            "You clearly understand the system, just not the subtlety.",
            "Pay closer attention to the secondary emotion clues.",
            "Keep at it. You're not fired. Yet.",
        ]
    ),
    (50, 60): (
        "Manager",
        "Mediocre. I've seen worse… barely.",
        [
            "Right in the middle — which is not where an intern",
            "should aspire to stay. The spirits deserve better.",
            "You're reading the hints, but are you really thinking?",
            "Push harder tomorrow. I know you have it in you.",
        ]
    ),
    (60, 70): (
        "Manager",
        "Not bad. Not great. Solidly average.",
        [
            "More spirits left at peace today, which is the whole point.",
            "I noticed you're starting to read the emotional layering better.",
            "The toppings are still tripping you up a bit — review them.",
            "A respectable day. Try to do better tomorrow.",
        ]
    ),
    (70, 80): (
        "Manager",
        "Good work today, intern.",
        [
            "The spirits were noticeably calmer when they departed.",
            "You're reading the hint cards with real intent now.",
            "A few brews were off, but the overall picture is positive.",
            "I'm starting to think you might actually make it through the week.",
        ]
    ),
    (80, 90): (
        "Manager",
        "Impressive. I don't say that lightly.",
        [
            "Today was genuinely strong work. The spirits sensed your care.",
            "Your emotional calibration is becoming quite precise.",
            "I caught myself nodding in approval — don't let it go to your head.",
            "Keep this up and your final evaluation will reflect it.",
        ]
    ),
    (90, 100): (
        "Manager",
        "Extraordinary. Truly.",
        [
            "I have mentored many interns over many decades.",
            "Days like today remind me why I still believe in this work.",
            "The spirits you served today will rest in genuine peace.",
            "You have a gift, intern. Don't squander the days that remain.",
        ]
    ),
}

def _get_bucket(avg_accuracy: float) -> tuple:
    for low, high in sorted(MANAGER_LINES):
        if low <= avg_accuracy < high:
            return (low, high)
    return (90, 100)

def _get_font(size: int, bold: bool = False) -> pygame.font.Font:
    for name in ("Comic Sans MS", "Bradley Hand ITC", "Segoe Print",
                 "Chalkboard SE", "Arial"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)

def _wrap(text: str, font: pygame.font.Font, max_w: int) -> list[str]:
    lines = []
    for word_group in text.split("\n"):
        words = word_group.split()
        cur = ""
        for w in words:
            test = (cur + " " + w).strip()
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = w
        if cur:
            lines.append(cur)
    return lines

def run_manager_message(screen: pygame.Surface,
                        clock:  pygame.time.Clock,
                        completed_day: int,
                        avg_accuracy: float):
    font_head  = _get_font(30, bold=True)
    font_title = _get_font(26, bold=True)
    font_body  = _get_font(22)
    font_stat  = _get_font(20)
    font_btn   = _get_font(24)

    bucket = _get_bucket(avg_accuracy)
    manager_name, title_line, body_lines = MANAGER_LINES[bucket]

    def acc_color(v):
        if v < 40:  return (200,  60,  60)
        if v < 60:  return (210, 150,  40)
        if v < 80:  return (100, 180,  80)
        return             ( 50, 160, 120)

    bar_color = acc_color(avg_accuracy)

    btn_w, btn_h = 220, 52
    btn_rect = pygame.Rect((SCREEN_W - btn_w) // 2,
                           SCREEN_H - 80, btn_w, btn_h)

    panel_w = 680
    panel_h = 420
    px = (SCREEN_W - panel_w) // 2
    py = (SCREEN_H - panel_h) // 2

    running = True
    while running:
        mouse = pygame.mouse.get_pos()
        btn_hov = btn_rect.collidepoint(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_hov:
                    return

        screen.fill(C_BG)

        for row in range(0, SCREEN_H, 32):
            pygame.draw.line(screen, (210, 215, 230), (0, row), (SCREEN_W, row), 1)

        panel = pygame.Rect(px, py, panel_w, panel_h)
        pygame.draw.rect(screen, C_PANEL,  panel, border_radius=10)
        pygame.draw.rect(screen, C_BORDER, panel, 3, border_radius=10)

        hdr = pygame.Rect(px, py, panel_w, 54)
        pygame.draw.rect(screen, C_INK, hdr,
                         border_radius=10)
        pygame.draw.rect(screen, C_INK,
                         pygame.Rect(px, py + 30, panel_w, 24))

        day_txt = font_head.render(f"DAY {completed_day} COMPLETE", True, C_BG)
        screen.blit(day_txt, day_txt.get_rect(center=(SCREEN_W // 2, py + 27)))

        name_surf = font_stat.render(f"— {manager_name}", True, C_INK)
        screen.blit(name_surf, (px + 24, py + 68))

        acc_label = font_stat.render(
            f"Average Accuracy:  {avg_accuracy:.1f}%", True, C_INK)
        screen.blit(acc_label, (px + 24, py + 96))

        bar_bg  = pygame.Rect(px + 24, py + 122, panel_w - 48, 14)
        bar_fill = pygame.Rect(px + 24, py + 122,
                               int((panel_w - 48) * avg_accuracy / 100), 14)
        pygame.draw.rect(screen, (210, 215, 225), bar_bg,  border_radius=7)
        pygame.draw.rect(screen, bar_color,       bar_fill, border_radius=7)
        pygame.draw.rect(screen, C_BORDER,        bar_bg,  2, border_radius=7)

        pygame.draw.line(screen, C_BORDER,
                         (px + 20, py + 148), (px + panel_w - 20, py + 148), 1)

        title_surf = font_title.render(f'"{title_line}"', True, C_INK)
        screen.blit(title_surf, title_surf.get_rect(
            centerx=SCREEN_W // 2, y=py + 158))

        y_text = py + 200
        for line in body_lines:
            wrapped = _wrap(line, font_body, panel_w - 48)
            for wl in wrapped:
                ls = font_body.render(wl, True, (80, 85, 110))
                screen.blit(ls, (px + 24, y_text))
                y_text += 28

        fill = C_ACCENT if btn_hov else C_PANEL
        pygame.draw.rect(screen, fill,     btn_rect, border_radius=6)
        pygame.draw.rect(screen, C_BORDER, btn_rect, 2, border_radius=6)
        btn_surf = font_btn.render("NEXT DAY", True, C_INK)
        screen.blit(btn_surf, btn_surf.get_rect(center=btn_rect.center))

        pygame.display.flip()
        clock.tick(FPS)