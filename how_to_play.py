import pygame, sys

C_BG       = (248, 247, 244)
C_INK      = ( 62,  75, 130)
C_PANEL    = (255, 255, 255)
C_BORDER   = ( 62,  75, 130)
C_BTN_FILL = (255, 255, 255)
C_BTN_HOV  = (230, 235, 255)
C_FAINT    = (150, 155, 180)

EMOTION_COLORS = {
    'Happiness': (255, 205,  50),
    'Sadness':   ( 80, 140, 220),
    'Anger':     (220,  80,  60),
    'Fear':      (150,  80, 200),
}

SCREEN_W, SCREEN_H = 1000, 700
FPS         = 60
TOTAL_PAGES = 4
MARGIN      = 40
HDR_H       = 56
CONTENT_TOP = HDR_H + 10
NAV_Y       = 630
DOTS_Y      = 682
CONTENT_BOT = NAV_Y - 10

def _get_font(size, bold=False):
    for name in ("Comic Sans MS","Segoe Print","Chalkboard SE","Arial"):
        try: return pygame.font.SysFont(name, size, bold=bold)
        except: continue
    return pygame.font.Font(None, size)

def _wrap(text, font, max_w):
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words: lines.append(""); continue
        cur = ""
        for w in words:
            t = (cur + " " + w).strip()
            if font.size(t)[0] <= max_w: cur = t
            else:
                if cur: lines.append(cur)
                cur = w
        lines.append(cur)
    return lines

def _header(screen, fh, title):
    pygame.draw.rect(screen, C_INK, (0, 0, SCREEN_W, HDR_H))
    s = fh.render(title, True, C_BG)
    screen.blit(s, s.get_rect(center=(SCREEN_W//2, HDR_H//2)))

def _card(screen, x, y, w, h, title, body, fh, fb,
          left_stripe=False, title_col=None):
    pygame.draw.rect(screen, C_PANEL,  (x, y, w, h), border_radius=8)
    pygame.draw.rect(screen, C_BORDER, (x, y, w, h), 2, border_radius=8)
    if left_stripe:
        pygame.draw.rect(screen, C_INK, (x, y, 5, h), border_radius=4)
    tc  = title_col or C_INK
    tx  = x + (13 if left_stripe else 10)
    ts  = fh.render(title, True, tc)
    screen.blit(ts, (tx, y + 7))
    ty  = y + 7 + ts.get_height() + 4
    max_ty = y + h - 6
    for line in _wrap(body, fb, w - tx + x - 8):
        if ty + fb.get_height() > max_ty: break
        screen.blit(fb.render(line, True, (65, 70, 100)), (tx, ty))
        ty += fb.get_height() + 3
    return y + h

def _section_label(screen, fh, text, y):
    s = fh.render(text, True, C_INK)
    screen.blit(s, (MARGIN, y))
    return y + s.get_height() + 6

def _page1(screen, fh, fb, fs):
    _header(screen, fh, "INTERN'S FIELD MANUAL  —  Overview  (1/4)")
    W = SCREEN_W - 2*MARGIN

    _card(screen, MARGIN, 66, W, 95, "Your Goal",
          "A restless spirit arrives. Read their emotional hints, brew the right tea "
          "to match their feelings, and help them find peace.\n"
          "Serve 5 spirits per day for 7 days — keep your average Accuracy above 70% to pass!",
          fh, fb)

    y = _section_label(screen, fh, "The Four Emotions — Colour Key", 171)

    bw = (W - 30) // 4
    descs = [
        ("Happiness","Warmth, joy, contentment.\nCalms joyful spirits."),
        ("Sadness",  "Grief, longing, melancholy.\nSoothes sorrowful spirits."),
        ("Anger",    "Fury, frustration, resentment.\nSettles angry spirits."),
        ("Fear",     "Dread, anxiety, terror.\nEases fearful spirits."),
    ]
    SWATCH_H = 40
    DESC_H   = 90
    for i,(emo,desc) in enumerate(descs):
        bx  = MARGIN + i*(bw+10)
        col = EMOTION_COLORS[emo]
        pygame.draw.rect(screen, col,    (bx, y, bw, SWATCH_H), border_radius=8)
        pygame.draw.rect(screen, C_BORDER,(bx,y, bw, SWATCH_H), 2, border_radius=8)
        es = fh.render(emo, True, (255,255,255))
        screen.blit(es, es.get_rect(center=(bx+bw//2, y+SWATCH_H//2)))
        dy2 = y + SWATCH_H + 4
        pygame.draw.rect(screen, C_PANEL,  (bx, dy2, bw, DESC_H), border_radius=6)
        pygame.draw.rect(screen, C_BORDER, (bx, dy2, bw, DESC_H), 1, border_radius=6)
        ty2 = dy2 + 7
        for line in _wrap(desc, fs, bw-12):
            if ty2 + fs.get_height() > dy2+DESC_H-4: break
            screen.blit(fs.render(line,True,(65,70,100)),(bx+6,ty2))
            ty2 += fs.get_height()+3

    levels_y = y + SWATCH_H + 4 + DESC_H + 12
    _card(screen, MARGIN, levels_y, W, 100, "Emotion Levels",
          "Each ghost has all four emotions set to one of four hidden levels:\n"
          "5 (trace)  ·  10 (mild)  ·  20 (strong)  ·  30 (overwhelming)\n"
          "No two emotions share the same level — your job is to figure out which is which!",
          fh, fb)

    strat_y = levels_y + 100 + 10
    _card(screen, MARGIN, strat_y, W, 100, "Your Strategy",
          "Click each of the four coloured hint buttons to read the ghost's diary fragments.\n"
          "Judge the emotional intensity of each letter, rank the emotions strongest to weakest,\n"
          "then brew a tea that targets the highest-ranked emotions.",
          fh, fb)

def _page2(screen, fh, fb, fs):
    _header(screen, fh, "INTERN'S FIELD MANUAL  —  Reading the Hints  (2/4)")
    W = SCREEN_W - 2*MARGIN

    _card(screen, MARGIN, 66, W, 100, "Step 1 — Click the Hint Buttons",
          "Four coloured buttons sit at the top of the screen, one per emotion.\n"
          "Click each one to read a short diary fragment written by the ghost.\n"
          "The letter describes how strongly they feel that emotion — without naming a number.",
          fh, fb)

    y = _section_label(screen, fh, "How to Read the Intensity Level", 176)

    strength = [
        ("Level 5  — Trace",        (200,210,228), False,
         "Dismissive and brief.\n'It was barely there.\nBut I felt it. Briefly.'"),
        ("Level 10  — Mild",        (160,190,235), False,
         "Acknowledged, controlled.\n'There were good moments.\nI kept them close.'"),
        ("Level 20  — Strong",      (100,145,210), True,
         "Clear emotional weight.\n'The tears came more\noften than I'd admit.'"),
        ("Level 30  — Overwhelming",( 62, 75,130), True,
         "Intense, raw, consuming.\n'The rage consumed me.\nI could not let it go.'"),
    ]
    STRIP_H = 26
    BODY_H  = 105
    cw      = (W - 30) // 4
    for i,(title,col,white_text,body) in enumerate(strength):
        cx = MARGIN + i*(cw+10)
        pygame.draw.rect(screen, col,     (cx, y, cw, STRIP_H), border_radius=6)
        pygame.draw.rect(screen, C_BORDER,(cx, y, cw, STRIP_H), 1, border_radius=6)
        tc = (255,255,255) if white_text else (30,30,50)
        ts = fs.render(title, True, tc)
        screen.blit(ts, ts.get_rect(center=(cx+cw//2, y+STRIP_H//2)))
        by = y + STRIP_H
        pygame.draw.rect(screen, C_PANEL,  (cx, by, cw, BODY_H), border_radius=6)
        pygame.draw.rect(screen, C_BORDER, (cx, by, cw, BODY_H), 1, border_radius=6)
        ty2 = by + 7
        for line in _wrap(body, fs, cw-12):
            if ty2 + fs.get_height() > by+BODY_H-4: break
            screen.blit(fs.render(line,True,(65,70,100)),(cx+6,ty2))
            ty2 += fs.get_height()+3

    rank_y = y + STRIP_H + BODY_H + 12
    _card(screen, MARGIN, rank_y, W, 105, "How to Rank the Emotions",
          "After reading all four hints, mentally rank them from strongest to weakest feeling:\n"
          "Most intense, dramatic, all-consuming language  =  Level 30\n"
          "Most dismissive, brief, detached language       =  Level 5\n"
          "Assign 20 and 10 to the remaining two emotions.",
          fh, fb)

    tip_y = rank_y + 105 + 10
    _card(screen, MARGIN, tip_y, W, 90, "Quick Tip",
          "You don't need to read every single word.\n"
          "Skim for overall emotional weight:\n"
          "Short + detached = low.   Dramatic + consuming = high.",
          fh, fb)

def _page3(screen, fh, fb, fs):
    _header(screen, fh, "INTERN'S FIELD MANUAL  —  Brewing the Tea  (3/4)")
    W = SCREEN_W - 2*MARGIN

    _card(screen, MARGIN, 66, W, 90, "Brewing Order — Must Follow This Sequence",
          "1. Click the Kettle on the tray  2. Choose a Base Water  3. Choose a Tea Bag\n"
          "4. Choose a Topping  5. Click SERVE\n"
          "You cannot skip steps. Each ingredient only becomes available after the previous one.",
          fh, fb)

    y = _section_label(screen, fh, "What Each Ingredient Adds to Your Brew", 166)

    col_ws  = [205, 345, 120]
    headers = ["Ingredient", "Emotions Affected", "Points"]
    rows = [
        ["Base Water",    "Your chosen emotion only",          "+30"],
        ["Tea Bag",       "Your chosen emotion only",          "+20"],
        ["Topping  H","Happiness +10  ·  Fear +5",         "+15 total"],
        ["Topping  S","Sadness +10  ·  Happiness +5",      "+15 total"],
        ["Topping  A","Anger +10  ·  Sadness +5",          "+15 total"],
        ["Topping  F","Fear +10  ·  Anger +5",             "+15 total"],
    ]
    tw = sum(col_ws)+4
    hh = 28; rh = 26

    pygame.draw.rect(screen, C_INK, (MARGIN, y, tw, hh), border_radius=6)
    hx = MARGIN+8
    for cw,ht in zip(col_ws,headers):
        screen.blit(fs.render(ht,True,(255,255,255)),(hx, y+7)); hx+=cw
    y += hh
    for ri,row in enumerate(rows):
        fill = (230,234,252) if ri%2==0 else C_PANEL
        pygame.draw.rect(screen, fill,    (MARGIN, y, tw, rh))
        pygame.draw.rect(screen, C_BORDER,(MARGIN, y, tw, rh), 1)
        rx = MARGIN+8
        for cw,cell in zip(col_ws,row):
            screen.blit(fs.render(cell,True,(60,65,100)),(rx, y+6)); rx+=cw
        y += rh

    eg_y = y + 10
    _card(screen, MARGIN, eg_y, W, 100, "Worked Example",
          "Ghost stats: Happiness=30  ·  Sadness=20  ·  Fear=10  ·  Anger=5\n"
          "Best brew: Base Water Happiness (+30)  ·  Tea Bag Sadness (+20)  ·  Topping F (+10 Fear, +5 Anger)\n"
          "Result: Happiness=30, Sadness=20, Fear=10, Anger=5. Dominant emotion matched — this gives a perfect Accuracy score!",
          fh, fb)

    rem_y = eg_y + 100 + 10
    _card(screen, MARGIN, rem_y, W, 90, "Remember",
          "The three small coloured boxes that appear around the kettle show what you have chosen:\n"
          "LEFT box = Base Water colour  ·  RIGHT box = Tea Bag colour  ·  BELOW box = Topping colour\n"
          "Check them before you click SERVE to confirm your selections!",
          fh, fb)

def _page4(screen, fh, fb, fs):
    _header(screen, fh, "INTERN'S FIELD MANUAL  —  Tips & Scoring  (4/4)")

    tips = [
        ("Skim for Intensity",
         "You don't need to read every word.\n"
         "Short + dismissive = low level.\n"
         "Dramatic + consuming = Level 30."),
        ("Target the Dominant Emotion",
         "Put Base Water AND Tea Bag on the Level 30 emotion.\n"
         "That's +50 points on your most important emotion instantly —\n"
         "your biggest single accuracy gain."),
        ("Pick Toppings Carefully",
         "Every topping adds to TWO emotions.\n"
         "Pick the one that boosts your dominant emotion\n"
         "AND whose side-effect helps a secondary need."),
        ("Watch the Colour Indicators",
         "Three small boxes appear around the kettle as you brew:\n"
         "Left = Water colour  ·  Right = Tea Bag colour  ·  Below = Topping colour.\n"
         "Use them to double-check your choices before serving."),
        ("Accuracy Score Explained",
         "Score = how closely your brew matches the ghost's hidden values.\n"
         "100% = perfect match. You don't need perfection —\n"
         "aim for 70%+ each day to pass the evaluation."),
        ("Delete & Retry",
         "Made a mistake? Click DELETE to scrap the teapot and start fresh.\n"
         "You can only delete BEFORE clicking SERVE.\n"
         "Once served, the result is final."),
    ]

    cw     = (SCREEN_W - 2*MARGIN - 10) // 2
    CARD_H = 100
    GAP    = 10

    for i,(title,body) in enumerate(tips):
        col = i % 2
        row = i // 2
        cx  = MARGIN + col*(cw+10)
        cy  = CONTENT_TOP + row*(CARD_H+GAP)
        pygame.draw.rect(screen, C_PANEL,  (cx,cy,cw,CARD_H), border_radius=8)
        pygame.draw.rect(screen, C_BORDER, (cx,cy,cw,CARD_H), 2, border_radius=8)
        pygame.draw.rect(screen, C_INK,    (cx,cy,5,CARD_H),  border_radius=4)
        ts = fh.render(title, True, C_INK)
        screen.blit(ts, (cx+13, cy+7))
        ty = cy+7+ts.get_height()+4
        for line in _wrap(body, fs, cw-20):
            if ty+fs.get_height() > cy+CARD_H-4: break
            screen.blit(fs.render(line,True,(65,70,100)),(cx+13,ty))
            ty += fs.get_height()+3

    bar_y = CONTENT_TOP + 3*(CARD_H+GAP) + 8
    bl = fh.render("Accuracy Colour Guide:", True, C_INK)
    screen.blit(bl, (MARGIN, bar_y))
    bx = MARGIN + bl.get_width() + 14
    for label,col in [("<40%",(200,60,60)),("40–60%",(210,150,40)),
                       ("60–80%",(100,180,80)),("80–100%",(50,160,120))]:
        pygame.draw.rect(screen, col, (bx, bar_y+2, 20, 20), border_radius=4)
        ls = fs.render(f"  {label}", True, (65,70,100))
        screen.blit(ls, (bx+22, bar_y+2))
        bx += 22 + ls.get_width() + 14

def run_how_to_play(screen: pygame.Surface, clock: pygame.time.Clock):
    fh = _get_font(18, bold=True)
    fb = _get_font(15)
    fs = _get_font(13)

    page = 0
    PAGE_FNS = [_page1, _page2, _page3, _page4]

    BTN_W, BTN_H = 120, 40
    prev_rect = pygame.Rect(MARGIN, NAV_Y, BTN_W, BTN_H)
    next_rect = pygame.Rect(SCREEN_W-MARGIN-BTN_W, NAV_Y, BTN_W, BTN_H)
    back_rect = pygame.Rect(SCREEN_W//2-65, NAV_Y, 130, BTN_H)

    while True:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return
                if event.key == pygame.K_RIGHT and page < TOTAL_PAGES-1: page+=1
                if event.key == pygame.K_LEFT  and page > 0:             page-=1
            if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
                if next_rect.collidepoint(event.pos) and page<TOTAL_PAGES-1: page+=1
                elif prev_rect.collidepoint(event.pos) and page>0:           page-=1
                elif back_rect.collidepoint(event.pos) and page==TOTAL_PAGES-1: return

        screen.fill(C_BG)
        PAGE_FNS[page](screen, fh, fb, fs)

        def _btn(rect, label, active):
            if not active: return
            hov = rect.collidepoint(mouse)
            pygame.draw.rect(screen, C_BTN_HOV if hov else C_BTN_FILL, rect, border_radius=6)
            pygame.draw.rect(screen, C_BORDER, rect, 2, border_radius=6)
            screen.blit(fh.render(label,True,C_INK),
                        fh.render(label,True,C_INK).get_rect(center=rect.center))

        _btn(prev_rect, "Prev",  page > 0)
        _btn(next_rect, "Next",  page < TOTAL_PAGES-1)
        _btn(back_rect, "X Close", page == TOTAL_PAGES-1)

        for i in range(TOTAL_PAGES):
            pygame.draw.circle(screen, C_INK if i==page else C_FAINT,
                               (SCREEN_W//2-(TOTAL_PAGES-1)*10+i*20, DOTS_Y), 5)

        pygame.display.flip()
        clock.tick(FPS)