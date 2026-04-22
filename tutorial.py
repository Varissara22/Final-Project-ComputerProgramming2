
import pygame
import sys

from ghost     import Ghost
from teapot    import Teapot
from hint_card import draw_hint_text_card

SCREEN_W, SCREEN_H = 1000, 700
BG_W         = 1420
MAX_SCROLL   = BG_W - SCREEN_W
SCROLL_SPEED = 8
EDGE_MARGIN  = 100
FPS          = 60

BTN_W,    BTN_H    = 53,  52
BASE_W,   BASE_H   = 53, 100
KETTLE_W, KETTLE_H = 175, 100
TEABAG_W, TEABAG_H = 50,  50
TOPPING_W, TOPPING_H = 50, 60
SUBMIT_W, SUBMIT_H = 120, 60
DELETE_W, DELETE_H = 150, 120
IND                = 55

C_INK    = ( 62,  75, 130)
C_PAPER  = (248, 247, 244)
C_ACCENT = (220, 225, 255)
C_ICON   = (240, 240, 255)
C_FAINT  = (150, 155, 180)
C_PASS   = ( 39, 174,  96)
C_FAIL   = (231,  76,  60)

EMOTION_COLORS = {
    'h': (255, 223,   0),
    's': ( 30, 144, 255),
    'a': (255,  69,   0),
    'f': (138,  43, 226),
}

TUT_HAPPINESS = 30
TUT_SADNESS   = 20
TUT_FEAR      = 10
TUT_ANGER     = 5

STEP_INTRO      = 0
STEP_READ_HINT  = 1
STEP_KETTLE     = 2
STEP_WATER      = 3
STEP_TEABAG     = 4
STEP_TOPPING    = 5
STEP_SUBMIT     = 6
STEP_DONE       = 7

ENABLED_KEYS = {
    STEP_READ_HINT: {'hint_happiness', 'hint_sadness', 'hint_anger', 'hint_fear'},
    STEP_KETTLE:    {'kettle'},
    STEP_WATER:     {'water_h', 'water_s', 'water_a', 'water_f'},
    STEP_TEABAG:    {'teabag_h', 'teabag_s', 'teabag_a', 'teabag_f'},
    STEP_TOPPING:   {'topping_h', 'topping_s', 'topping_a', 'topping_f', 'delete'},
    STEP_SUBMIT:    {'submit'},
}

MICHAEL_LINES = {
    STEP_READ_HINT: (
        "Read all 4 of the ghost's hints before we get started — "
        "each one tells you something about what they're feeling. "
        "{remaining}"
    ),
    STEP_KETTLE: (
        "Nice! The hints tell you exactly what they need. "
        "Now grab the kettle on the far left to get started."
    ),
    STEP_WATER: (
        "The Base Water carries the ghost's strongest emotion. "
        "Pick whichever matches their biggest feeling!"
    ),
    STEP_TEABAG: (
        "Good pick! Now choose a Tea Bag — that covers the second emotion."
    ),
    STEP_TOPPING: (
        "Nearly there! Choose a Topping for their third or fourth feeling. "
        "Made a mistake? The trash can at the bottom-left resets everything "
        "so you can start over."
    ),
    STEP_SUBMIT: (
        "All three ingredients chosen — now ring the bell on the right to serve!"
    ),
    STEP_DONE: (
        "Brilliant! You're a natural. Every ghost is different, "
        "so keep reading those hints and you'll do great. "
        "Good luck on your shift — I'll be rooting for you!"
    ),
}

def _font(size, bold=False):
    for name in ("Comic Sans MS", "Bradley Hand ITC", "Segoe Print",
                 "Chalkboard SE", "Arial"):
        try:
            return pygame.font.SysFont(name, size, bold=bold)
        except Exception:
            continue
    return pygame.font.Font(None, size)

def _sr(world_rect, cam):
    return pygame.Rect(world_rect.x - cam, world_rect.y,
                       world_rect.width, world_rect.height)

def _build_rects():
    return {
        'hint_happiness': pygame.Rect(520, 160, BTN_W,    BTN_H),
        'hint_sadness':   pygame.Rect(600, 160, BTN_W,    BTN_H),
        'hint_anger':     pygame.Rect(680, 160, BTN_W,    BTN_H),
        'hint_fear':      pygame.Rect(760, 160, BTN_W,    BTN_H),
        'water_h':   pygame.Rect(200, 300, BASE_W,   BASE_H),
        'water_s':   pygame.Rect(260, 300, BASE_W,   BASE_H),
        'water_a':   pygame.Rect(320, 300, BASE_W,   BASE_H),
        'water_f':   pygame.Rect(380, 300, BASE_W,   BASE_H),
        'teabag_h':  pygame.Rect(510, 332, TEABAG_W, TEABAG_H),
        'teabag_s':  pygame.Rect(605, 332, TEABAG_W, TEABAG_H),
        'teabag_a':  pygame.Rect(700, 332, TEABAG_W, TEABAG_H),
        'teabag_f':  pygame.Rect(795, 332, TEABAG_W, TEABAG_H),
        'topping_h': pygame.Rect( 950, 140, TOPPING_W, TOPPING_H),
        'topping_s': pygame.Rect(1100, 220, TOPPING_W, TOPPING_H),
        'topping_a': pygame.Rect(1000, 300, TOPPING_W, 50),
        'topping_f': pygame.Rect(1050, 370, TOPPING_W, 52),
        'kettle':    pygame.Rect(  2, 285, KETTLE_W, KETTLE_H),
        'submit':    pygame.Rect(1250, 300, SUBMIT_W, SUBMIT_H),
        'delete':    pygame.Rect(  20, 550, DELETE_W, DELETE_H),
    }

def _make_ghost_hints(ghost):
    return {
        e: (e,) + ghost.get_hint_clue(e)
        for e in ('happiness', 'sadness', 'anger', 'fear')
    }

def _score_accuracy(ghost, teapot):
    emotions = ('happiness', 'sadness', 'anger', 'fear')
    gv = [getattr(ghost,  e) for e in emotions]
    tv = [getattr(teapot, e) for e in emotions]
    diff = sum(abs(g - t) for g, t in zip(gv, tv))
    return max(0.0, 100.0 - (diff / (sum(gv) or 100) * 100))

def _wrap_text(text, font, max_width):
    words = text.split()
    lines, line = [], []
    for word in words:
        test = ' '.join(line + [word])
        if font.size(test)[0] <= max_width:
            line.append(word)
        else:
            if line:
                lines.append(' '.join(line))
            line = [word]
    if line:
        lines.append(' '.join(line))
    return lines

def _draw_game_world(screen, rects, cam, teapot, assets, enabled_keys):
    A = assets
    mouse = pygame.mouse.get_pos()

    def _blit_or_color(img, r, color):
        if img:
            screen.blit(img, r)
        else:
            pygame.draw.rect(screen, color, r)

    def _glow(r):
        if r.collidepoint(mouse):
            glow = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            glow.fill((255, 255, 255, 55))
            screen.blit(glow, r)

    for emotion, code in (('happiness','h'),('sadness','s'),
                           ('anger','a'),('fear','f')):
        key = f'hint_{emotion}'
        if key in enabled_keys:
            r = _sr(rects[key], cam)
            _blit_or_color(A['hint'].get(emotion), r, EMOTION_COLORS[code])
            _glow(r)

    if 'kettle' in enabled_keys:
        kr = _sr(rects['kettle'], cam)
        screen.blit(A['kettle'], kr)
        _glow(kr)

    for code in 'hsaf':
        key = f'water_{code}'
        if key in enabled_keys:
            r = _sr(rects[key], cam)
            _blit_or_color(A['water'].get(code), r, EMOTION_COLORS[code])
            _glow(r)

    for code in 'hsaf':
        key = f'teabag_{code}'
        if key in enabled_keys:
            r = _sr(rects[key], cam)
            _blit_or_color(A['teabag'].get(code), r, EMOTION_COLORS[code])
            _glow(r)

    for code in 'hsaf':
        key = f'topping_{code}'
        if key in enabled_keys:
            r = _sr(rects[key], cam)
            _blit_or_color(A['topping'].get(code), r, EMOTION_COLORS[code])
            _glow(r)

    if 'delete' in enabled_keys:
        del_r = _sr(rects['delete'], cam)
        if A['delete']:
            screen.blit(A['delete'], del_r)
        else:
            pygame.draw.rect(screen, (139, 69, 19), del_r, 3)
        _glow(del_r)

    if 'submit' in enabled_keys:
        sub_r = _sr(rects['submit'], cam)
        if A['submit']:
            screen.blit(A['submit'], sub_r)
        else:
            pygame.draw.rect(screen, (34, 139, 34), sub_r)
        _glow(sub_r)

    if teapot:
        tray_r = pygame.Rect(550 - cam, 450, 150, 150)
        if A.get('kettleempty'):
            screen.blit(A['kettleempty'], tray_r)

        GAP = 10
        gx, gy, gw, gh = 550 - cam, 450, 150, 150

        def _draw_ind(ix, iy, chosen, chose_imgs):
            if chosen == 'Not':
                return
            box = pygame.Rect(ix, iy, IND, IND)
            img = chose_imgs.get(chosen) if chose_imgs else None
            if img:
                screen.blit(img, box)
            else:
                pygame.draw.rect(screen, EMOTION_COLORS[chosen], box, border_radius=8)
                pygame.draw.rect(screen, C_INK, box, 2, border_radius=8)

        _draw_ind(gx - IND - GAP, gy + (gh - IND)//2,
                  teapot.basewater, A.get('waterchose',  {}))
        _draw_ind(gx + gw + GAP,  gy + (gh - IND)//2,
                  teapot.teabag,   A.get('teabagchose', {}))
        _draw_ind(gx + (gw-IND)//2, gy + gh + GAP,
                  teapot.topping,  A.get('toppingchose',{}))

def _draw_michael_strip(screen, message, fonts, step, last_accuracy=None):
    BOX_H = 170
    BOX_Y = SCREEN_H - BOX_H - 8
    BOX_X = 10
    BOX_W = SCREEN_W - 20

    card = pygame.Surface((BOX_W, BOX_H), pygame.SRCALPHA)
    card.fill((*C_PAPER, 245))
    screen.blit(card, (BOX_X, BOX_Y))
    pygame.draw.rect(screen, C_INK,
                     pygame.Rect(BOX_X, BOX_Y, BOX_W, BOX_H), 2, border_radius=8)
    pygame.draw.rect(screen, C_INK,
                     pygame.Rect(BOX_X, BOX_Y, 6, BOX_H), border_radius=4)

    name_surf = fonts['name'].render("Michael", True, C_INK)
    screen.blit(name_surf, (BOX_X + 18, BOX_Y + 10))

    pygame.draw.line(screen, (*C_FAINT, 160),
                     (BOX_X + 14, BOX_Y + 40),
                     (BOX_X + BOX_W - 14, BOX_Y + 40), 1)

    lines = _wrap_text(message, fonts['msg'], BOX_W - 44)
    for i, ln in enumerate(lines[:4]):
        surf = fonts['msg'].render(ln, True, C_INK)
        screen.blit(surf, (BOX_X + 18, BOX_Y + 50 + i * 26))

    if step == STEP_DONE and last_accuracy is not None:
        color = C_PASS if last_accuracy >= 70 else C_FAIL
        acc_surf = fonts['acc'].render(
            f"Brew accuracy: {last_accuracy:.0f}%", True, color)
        screen.blit(acc_surf, (BOX_X + 18, BOX_Y + BOX_H - 44))

    if step == STEP_DONE:
        BW, BH = 210, 40
        bx = BOX_X + BOX_W - BW - 16
        by = BOX_Y + BOX_H - BH - 10
        btn_r = pygame.Rect(bx, by, BW, BH)
        hov   = btn_r.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, C_ACCENT if hov else C_ICON, btn_r, border_radius=7)
        pygame.draw.rect(screen, C_INK,                       btn_r, 2, border_radius=7)
        lbl = fonts['btn'].render("Start my shift", True, C_INK)
        screen.blit(lbl, lbl.get_rect(center=btn_r.center))
        return btn_r

    return None

def _draw_intro_screen(screen, background, fonts):
    screen.blit(background, (0, 0))

    ov = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    ov.fill((0, 0, 0, 155))
    screen.blit(ov, (0, 0))

    CW, CH = 660, 350
    CX = (SCREEN_W - CW) // 2
    CY = (SCREEN_H - CH) // 2

    pygame.draw.rect(screen, C_PAPER, pygame.Rect(CX, CY, CW, CH), border_radius=12)
    pygame.draw.rect(screen, C_INK,   pygame.Rect(CX, CY, CW, CH), 3, border_radius=12)
    pygame.draw.rect(screen, C_INK,   pygame.Rect(CX, CY, CW, 8),  border_radius=6)

    screen.blit(fonts['title'].render("Michael", True, C_INK),
                (CX + 24, CY + 20))

    pygame.draw.line(screen, (*C_FAINT, 160),
                     (CX + 18, CY + 58), (CX + CW - 18, CY + 58), 1)

    greeting = [
        "Hey! I'm Michael — the manager asked me to",
        "show you the ropes before your first ghost arrives.",
        "",
        "Want a quick walkthrough, or have you",
        "brewed here before?",
    ]
    for i, ln in enumerate(greeting):
        surf = fonts['msg'].render(ln, True, C_INK)
        screen.blit(surf, (CX + 24, CY + 70 + i * 30))

    BTN_Y = CY + CH - 70
    tour_r = pygame.Rect(CX + 24,        BTN_Y, 272, 48)
    skip_r = pygame.Rect(CX + CW - 296,  BTN_Y, 272, 48)
    mouse  = pygame.mouse.get_pos()

    for r, label, primary in ((tour_r, "Take the Tour",        True ),
                               (skip_r, "Skip — I know this",  False)):
        hov  = r.collidepoint(mouse)
        fill = C_INK   if primary        else (C_ACCENT if hov else C_ICON)
        fg   = C_PAPER if primary        else C_INK
        pygame.draw.rect(screen, fill, r, border_radius=8)
        pygame.draw.rect(screen, C_INK, r, 2, border_radius=8)
        s = fonts['btn'].render(label, True, fg)
        screen.blit(s, s.get_rect(center=r.center))

    return tour_r, skip_r

def _handle_click(pos, rects, cam, state):
    step    = state['step']
    enabled = ENABLED_KEYS.get(step, set())

    def hit(key):
        return key in enabled and _sr(rects[key], cam).collidepoint(pos)

    for emotion in ('happiness', 'sadness', 'anger', 'fear'):
        if hit(f'hint_{emotion}'):
            state['hint_card']         = state['ghost_hints'][emotion]
            state['pending_hint']      = emotion
            return

    if hit('kettle'):
        state['teapot'] = Teapot()
        state['step']   = STEP_WATER
        return

    for code in 'hsaf':
        if hit(f'water_{code}'):
            if state['teapot']:
                state['teapot'].add_basewater(code)
                state['step'] = STEP_TEABAG
            return

    for code in 'hsaf':
        if hit(f'teabag_{code}'):
            if state['teapot']:
                state['teapot'].add_teabag(code)
                state['step'] = STEP_TOPPING
            return

    for code in 'hsaf':
        if hit(f'topping_{code}'):
            if state['teapot']:
                state['teapot'].add_topping(code)
                state['step'] = STEP_SUBMIT
            return

    if hit('delete'):
        state['teapot'] = None
        state['step']   = STEP_KETTLE
        return

    if hit('submit'):
        tp = state['teapot']
        if tp and tp.is_complete:
            state['last_accuracy'] = _score_accuracy(state['ghost'], tp)
            state['teapot']        = None
            state['step']          = STEP_DONE
        return

def run_tutorial(screen: pygame.Surface,
                 clock:  pygame.time.Clock,
                 assets: dict) -> str:
    fonts = {
        'title': _font(28, bold=True),
        'name':  _font(20, bold=True),
        'msg':   _font(18),
        'btn':   _font(17, bold=True),
        'acc':   _font(17, bold=True),
    }

    rects = _build_rects()
    cam   = 0

    ghost             = Ghost()
    ghost.happiness   = TUT_HAPPINESS
    ghost.sadness     = TUT_SADNESS
    ghost.fear        = TUT_FEAR
    ghost.anger       = TUT_ANGER
    ghost_hints       = _make_ghost_hints(ghost)

    background = assets['background']

    state = {
        'step':          STEP_INTRO,
        'teapot':        None,
        'hint_card':     None,
        'hint_scroll':   0,
        'ghost':         ghost,
        'ghost_hints':   ghost_hints,
        'last_accuracy': None,
        'hints_seen':    set(),
        'pending_hint':  None,
    }

    while True:
        step = state['step']

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEWHEEL and state['hint_card'] is not None:
                from hint_card import handle_hint_card_event as _hce
                _hce(event, state)
                continue

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos

                if state['step'] == STEP_INTRO:
                    CW, CY_offset = 660, (SCREEN_H - 350) // 2
                    CX = (SCREEN_W - CW) // 2
                    BTN_Y = CY_offset + 350 - 70
                    tour_r = pygame.Rect(CX + 24,       BTN_Y, 272, 48)
                    skip_r = pygame.Rect(CX + CW - 296, BTN_Y, 272, 48)
                    if tour_r.collidepoint(pos):
                        state['step'] = STEP_READ_HINT
                    elif skip_r.collidepoint(pos):
                        return 'skipped'

                elif state['hint_card'] is not None:
                    from hint_card import handle_hint_card_event as _hce
                    result = _hce(event, state)
                    if result == 'close':
                        state['hint_card']   = None
                        state['hint_scroll'] = 0
                        if 'pending_hint' in state:
                            state['hints_seen'].add(state.pop('pending_hint'))
                        if state['step'] == STEP_READ_HINT:
                            if len(state['hints_seen']) >= 4:
                                state['step'] = STEP_KETTLE

                elif state['step'] == STEP_DONE:
                    BOX_H = 170
                    BOX_Y = SCREEN_H - BOX_H - 8
                    BOX_X = 10
                    BOX_W = SCREEN_W - 20
                    BW, BH = 210, 40
                    done_btn = pygame.Rect(
                        BOX_X + BOX_W - BW - 16,
                        BOX_Y + BOX_H - BH - 10,
                        BW, BH
                    )
                    if done_btn.collidepoint(pos):
                        return 'completed'

                else:
                    _handle_click(pos, rects, cam, state)

        if step not in (STEP_INTRO, STEP_DONE) and not state['hint_card']:
            mx = pygame.mouse.get_pos()[0]
            if mx > SCREEN_W - EDGE_MARGIN:
                cam = min(cam + SCROLL_SPEED, MAX_SCROLL)
            elif mx < EDGE_MARGIN:
                cam = max(cam - SCROLL_SPEED, 0)

        if step == STEP_INTRO:
            _draw_intro_screen(screen, background, fonts)

        else:
            screen.blit(background, (-cam, 0))

            enabled = ENABLED_KEYS.get(step, set())
            _draw_game_world(screen, rects, cam,
                             state['teapot'], assets, enabled)

            if step == STEP_READ_HINT:
                seen  = len(state['hints_seen'])
                left  = 4 - seen
                if seen == 0:
                    hint_msg = ("Read all 4 of the ghost's hints before we start — "
                                "each button tells you something about their feelings!")
                elif left == 1:
                    hint_msg = "Almost there — just 1 more hint to read!"
                else:
                    hint_msg = f"Good! {left} hints left to read."
                michael_msg = hint_msg
            else:
                michael_msg = MICHAEL_LINES.get(step, "")

            if state['hint_card']:
                state['hint_scroll'] = draw_hint_text_card(
                    screen, *state['hint_card'], state['hint_scroll'])
            else:
                _draw_michael_strip(screen, michael_msg,
                                    fonts, step,
                                    state['last_accuracy'])

        pygame.display.flip()
        clock.tick(FPS)