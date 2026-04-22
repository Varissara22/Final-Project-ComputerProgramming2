import pygame

SCREEN_W, SCREEN_H = 1000, 700

_EMOTION_COLORS = {
    'h': (255, 223,   0),
    's': ( 30, 144, 255),
    'a': (255,  69,   0),
    'f': (138,  43, 226),
}

_C_INK   = ( 62,  75, 130)
_C_PAPER = (248, 247, 244)

CARD_W = 520
CARD_H = 380
CARD_X = (SCREEN_W - CARD_W) // 2
CARD_Y = (SCREEN_H - CARD_H) // 2

_SB_W       = 8
_SB_MARGIN  = 6
_SB_X       = CARD_X + CARD_W - _SB_W - 10
_THUMB_MIN  = 24
_SCROLL_STEP = 22

def _get_font(size, bold=False):
    for name in ("Comic Sans MS", "Bradley Hand ITC", "Segoe Print",
                 "Chalkboard SE", "Arial"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)

def _wrap(text, font, max_w):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        cur = ""
        for word in words:
            test = (cur + " " + word).strip()
            if font.size(test)[0] <= max_w:
                cur = test
            else:
                if cur:
                    lines.append(cur)
                cur = word
        lines.append(cur)
    return lines

def _content_height(title_line, body_text, font_title, font_body, max_w):
    h = 0
    for _ in _wrap(f'"{title_line}"', font_title, max_w):
        h += font_title.get_height() + 2
    h += 8
    for _ in _wrap(body_text, font_body, max_w):
        h += font_body.get_height() + 2
    return h

def _layout():
    font_label = _get_font(16)
    label_h    = font_label.get_height() + 4 + 10 + 4
    SCROLL_TOP = CARD_Y + 22 + label_h
    FOOTER_H   = 28
    SCROLL_BOT = CARD_Y + CARD_H - FOOTER_H
    VIEWPORT_H = SCROLL_BOT - SCROLL_TOP
    MAX_W      = CARD_W - 56 - _SB_W - _SB_MARGIN
    return SCROLL_TOP, SCROLL_BOT, VIEWPORT_H, MAX_W

def get_hint_card_max_scroll(title_line, body_text):
    font_title = _get_font(22, bold=True)
    font_body  = _get_font(19)
    _, _, VIEWPORT_H, MAX_W = _layout()
    content_h = _content_height(title_line, body_text, font_title, font_body, MAX_W)
    return max(0, content_h - VIEWPORT_H)

def draw_hint_text_card(screen, emotion, emotion_name, title_line, body_text,
                        scroll_y=0):
    stripe_color = _EMOTION_COLORS.get(emotion[0], _C_INK)

    font_label  = _get_font(16)
    font_title  = _get_font(22, bold=True)
    font_body   = _get_font(19)
    font_footer = _get_font(14)

    TEXT_X = CARD_X + 28
    SCROLL_TOP, SCROLL_BOT, VIEWPORT_H, MAX_W = _layout()

    content_h  = _content_height(title_line, body_text, font_title, font_body, MAX_W)
    max_scroll = max(0, content_h - VIEWPORT_H)
    scroll_y   = max(0, min(scroll_y, max_scroll))

    ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 180))
    screen.blit(ov, (0, 0))

    card_rect = pygame.Rect(CARD_X, CARD_Y, CARD_W, CARD_H)
    pygame.draw.rect(screen, _C_PAPER, card_rect, border_radius=10)
    pygame.draw.rect(screen, _C_INK,   card_rect, 2, border_radius=10)

    pygame.draw.rect(screen, stripe_color,
                     pygame.Rect(CARD_X, CARD_Y, CARD_W, 10), border_radius=10)
    pygame.draw.rect(screen, stripe_color,
                     pygame.Rect(CARD_X, CARD_Y + 5, CARD_W, 5))

    label = font_label.render(emotion_name.upper(), True, stripe_color)
    screen.blit(label, (TEXT_X, CARD_Y + 22))
    rule_y = CARD_Y + 22 + label.get_height() + 4
    pygame.draw.line(screen, (*_C_INK, 80),
                     (TEXT_X, rule_y), (CARD_X + CARD_W - 28, rule_y), 1)

    content_surf = pygame.Surface((MAX_W, content_h), pygame.SRCALPHA)
    content_surf.fill((0, 0, 0, 0))
    cy = 0
    for line in _wrap(f'"{title_line}"', font_title, MAX_W):
        s = font_title.render(line, True, _C_INK)
        content_surf.blit(s, (0, cy))
        cy += s.get_height() + 2
    cy += 8
    for line in _wrap(body_text, font_body, MAX_W):
        s = font_body.render(line, True, (80, 85, 110))
        content_surf.blit(s, (0, cy))
        cy += s.get_height() + 2

    screen.blit(content_surf, (TEXT_X, SCROLL_TOP),
                pygame.Rect(0, scroll_y, MAX_W, VIEWPORT_H))

    pygame.draw.rect(screen, _C_PAPER,
                     pygame.Rect(CARD_X + 2, CARD_Y + 2,
                                 CARD_W - 4, SCROLL_TOP - CARD_Y - 2))
    pygame.draw.rect(screen, _C_PAPER,
                     pygame.Rect(CARD_X + 2, SCROLL_BOT,
                                 CARD_W - 4, CARD_Y + CARD_H - SCROLL_BOT - 2))

    pygame.draw.rect(screen, _C_INK, card_rect, 2, border_radius=10)
    pygame.draw.rect(screen, stripe_color,
                     pygame.Rect(CARD_X, CARD_Y, CARD_W, 10), border_radius=10)
    pygame.draw.rect(screen, stripe_color,
                     pygame.Rect(CARD_X, CARD_Y + 5, CARD_W, 5))
    screen.blit(label, (TEXT_X, CARD_Y + 22))
    pygame.draw.line(screen, (*_C_INK, 80),
                     (TEXT_X, rule_y), (CARD_X + CARD_W - 28, rule_y), 1)

    if max_scroll > 0:
        track = pygame.Rect(_SB_X, SCROLL_TOP, _SB_W, VIEWPORT_H)
        pygame.draw.rect(screen, (210, 215, 230), track, border_radius=4)

        thumb_h = max(_THUMB_MIN, int(VIEWPORT_H * VIEWPORT_H / content_h))
        thumb_y = SCROLL_TOP + int((VIEWPORT_H - thumb_h) * scroll_y / max_scroll)
        pygame.draw.rect(screen, _C_INK,
                         pygame.Rect(_SB_X, thumb_y, _SB_W, thumb_h),
                         border_radius=4)

    hint_text = ("scroll to read  ·  click outside to close"
                 if max_scroll > 0 else "click outside to close")
    footer = font_footer.render(f"— {hint_text} —", True, (*_C_INK, 120))
    screen.blit(footer, footer.get_rect(
        centerx=CARD_X + CARD_W // 2, y=CARD_Y + CARD_H - 22))

    return scroll_y

def handle_hint_card_event(event, state):
    card_rect = pygame.Rect(CARD_X, CARD_Y, CARD_W, CARD_H)

    if event.type == pygame.MOUSEWHEEL:
        state['hint_scroll'] = state.get('hint_scroll', 0) - event.y * _SCROLL_STEP
        if state['hint_card']:
            _, _, title_line, body_text = state['hint_card']
            max_s = get_hint_card_max_scroll(title_line, body_text)
            state['hint_scroll'] = max(0, min(state['hint_scroll'], max_s))
        return None

    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
        if not card_rect.collidepoint(event.pos):
            return 'close'

    return None