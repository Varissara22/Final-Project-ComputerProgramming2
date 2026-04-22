import pygame
import sys

C_BG     = (248, 247, 244)
C_INK    = ( 62,  75, 130)
C_ACCENT = (220, 225, 255)
C_FAINT  = (150, 155, 180)

SCREEN_W, SCREEN_H = 1000, 700
FPS = 60

DAILY_LETTERS = {
    1: (
        "To the New Employee\n"
        "(hoping to survive beyond this week)",

        "Welcome to my tea shop, a proud subsidiary of the Reincarnation Department.\n"
        "The job isn't complicated: just listen to the pathetic rambling of our emotional\n"
        "spirit clients — I had to beg Michael for those, do you have any idea how much\n"
        "effort that took? — brew the right tea, and help them find peace...\n"
        "or at least stop them from wrecking the place.\n\n"
        "Honestly, I'm not expecting much from you. The previous employee was utterly\n"
        "incompetent, mixing ingredients haphazardly until the spirits lost focus.\n"
        "I got so annoyed that I sent them to be reborn as a 'donkey.'\n"
        "They're probably happily munching on grass somewhere right now.\n\n"
        "The rules are simple: I'll evaluate your performance in 7 days.\n"
        "If your average satisfaction score is over 70%, you pass and get to keep working.\n\n"
        "But if not... I'll print out the previous employee's resume just in case\n"
        "you both get reborn as donkeys in the same litter.\n\n"
        "Don't waste my time.\n\n"
        "— Manager"
    ),

    2: (
        "To the Employee\n"
        "(who somehow survived the first day)",

        "The first day must have been 'tough' for a novice like you, hm?\n"
        "But you made it. Not bad... though it shouldn't have been that difficult\n"
        "in the first place, right?\n\n"
        "However, I'd like to inform you that there's a restless spirit from yesterday\n"
        "still lingering about. I assume the tea you brewed was such a disaster\n"
        "that it didn't even come close to the recipe.\n\n"
        "But never mind, don't strain your tiny brain stressing over it.\n"
        "We have a 'Cleanup Team' to handle these leftovers...\n"
        "and you 'don't need to know' how they do it.\n\n"
        "Focus on the customers in front of you.\n"
        "Get back to work and try to be useful for once.\n\n"
        "May death be with you.\n\n"
        "— Manager"
    ),

    3: (
        "To the Employee\n"
        "(who's still showing their face, which is... impressive, I suppose)",

        "Congratulations on dragging your soul into work for a third day.\n"
        "Honestly, I'm almost annoyed you haven't snapped and vanished yet.\n\n"
        "I saw that gormless look on your face while you were handling the Base Water,\n"
        "the Tea Bags, or those Flower Toppings. Listen closely: don't be nosy.\n"
        "It's better for your puny mental health if you don't go poking around for answers.\n"
        "Don't ask why some teas smell like forgotten memories,\n"
        "and certainly don't ask why the flowers in that jar seem to twitch when you touch them.\n\n"
        "Because if you get too curious, I might have no choice but to turn you into a\n"
        "shriveled little blossom and toss you into the topping jar myself.\n"
        "Just to end the headache.\n\n"
        "...Oh, wipe that look off your face! I'm joking. Who has the energy for that?\n"
        "Besides, you're dead. Everyone here is dead. Even I've been dead so long\n"
        "I've lost count. Death around here is as mundane as a cup of tea.\n\n"
        "And one more thing — don't go blabbering about our 'little jokes' to other departments.\n"
        "Not because it's a secret, but because the whole 'turning-employees-into-flowers' bit\n"
        "is so old it's practically a cliché. If you act traumatized, they'll just think\n"
        "you're some country bumpkin who's lost their mind.\n"
        "I refuse to be embarrassed by a subordinate who can't handle office humor.\n\n"
        "Now, get back to brewing. Don't keep those spirits waiting until they start\n"
        "'rotting' in my shop. It's a nightmare to scrub out the stains.\n\n"
        "— Manager"
    ),

    4: (
        "To the Employee\n"
        "(who's hopefully still in one piece)",

        "Don't even think about making small talk today; I'm buried in work\n"
        "and frankly, I'm in a foul mood. Yesterday, 'Michael' came crawling in\n"
        "to report that some spirits broke loose and caused a complete disaster outside...\n"
        "Ugh, there I go again, blabbering about things you don't need to know. Never mind.\n\n"
        "The point is, Michael says those rampaging spirits are the result of some pathetic\n"
        "'incomplete brewing' or messed-up recipes that clashed with their original identities.\n"
        "Instead of finding peace, they turned into beasts that tear other souls apart...\n"
        "and 'devour' the brewers too!\n\n"
        "Oh, that look on your face — I take it you didn't know souls could eat each other?\n"
        "Spare me the dramatics. That cramped office you're stuck in isn't an open bar\n"
        "like the outside lounge. Stop wondering why I've kept you locked in there alone;\n"
        "it's for the safety of my (precious) ingredients... meaning you.\n\n"
        "Just focus on the tea and don't screw up. I'd hate to waste energy\n"
        "sending the 'Cleanup Team' to scrape your remains off the floor.\n\n"
        "Trust me... 'dying a second time' is a hideous look.\n"
        "And the paperwork is ten times more annoying than the first!\n\n"
        "— Manager"
    ),

    5: (
        "To the Employee\n"
        "(hopefully not brewing up any 'bright ideas' in that empty head of yours)",

        "Following up on my last letter... I'm giving you a fair warning:\n"
        "Don. Even. Try it.\n\n"
        "Just because I said nothing can get into your office doesn't mean\n"
        "you're 100% safe. If you deliberately mess up a recipe just to 'see what happens,'\n"
        "the ones who suffer are the 'Cleanup Team' who have to scrub away your failures.\n"
        "And trust me, those guys aren't nearly as good-natured as I'm trying to be right now.\n\n"
        "Don't let me find out you're having 'thoughts' or trying to test the limits\n"
        "of the tea recipes out of some misplaced curiosity. Even if you aren't devoured\n"
        "by a rampaging soul at your desk, your fate is already written in the registry...\n"
        "In 2 days, if your satisfaction score is an absolute eyesore, you're becoming a 'donkey.'\n"
        "Period.\n\n"
        "Stop wondering, stop experimenting, and just keep your head down and work.\n\n"
        "Try to be worth more... than a pile of hay in a donkey stall, will you?\n\n"
        "— Manager"
    ),

    6: (
        "To the Employee\n"
        "(who needs to just get the job done already!)",

        "Briefly: DO YOUR JOB!\n\n"
        "Do you have any idea how badly I want a new employee — one who actually knows\n"
        "what they're doing for once? But the paperwork for a new hire is an absolute nightmare!\n"
        "You have no clue how revolting it is to deal with the 'Registry of Spirit Labor.'\n"
        "The bureaucracy is so tedious it makes me want to brew those officers into tea\n"
        "and be done with it.\n\n"
        "Then there's the budget for new soul quotas and all those petty administrative fees.\n"
        "It's so mind-numbingly boring that I refuse to do it twice in one month!\n\n"
        "So, if you don't want me to lose my temper and decide to 'cut costs'\n"
        "by disposing of you without the paper trail... just get a passing score.\n"
        "Don't give me more work.\n\n"
        "There are only 24 hours left.\n"
        "Don't make me start drafting a 'Certificate of Secondary Death' for you!\n\n"
        "— Manager"
    ),

    7: (
        "To the Employee\n"
        "(on your final day)",

        "I have no advice, no insults, and no threats left for you today.\n"
        "Quite frankly, I'm exhausted from talking.\n\n"
        "Just get your work done. Brew every cup of tea as if it were your last breath —\n"
        "and judging by your performance so far, that might actually be the case.\n"
        "Don't you dare tarnish the reputation of this clinic on the very last day\n"
        "of your evaluation.\n\n"
        "Finish your shift... and then we'll 'talk' about your future.\n"
        "That is, if you have one left.\n\n"
        "I certainly hope I don't have to waste my time\n"
        "ordering hay for the paddock out back.\n\n"
        "— Manager"
    ),
}

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

def run_daily_letter(screen: pygame.Surface,
                     clock:  pygame.time.Clock,
                     day:    int,
                     background: pygame.Surface = None,
                     camera_x:   int = 0):
    font_day  = _get_font(20, bold=True)
    font_to   = _get_font(18, bold=True)
    font_body = _get_font(17)
    font_hint = _get_font(13)

    letter_text = DAILY_LETTERS.get(day, ("", "No letter found for this day."))
    to_line, body_text = letter_text

    CARD_W  = 640
    CARD_H  = SCREEN_H - 80
    CARD_X  = (SCREEN_W - CARD_W) // 2
    CARD_Y  = (SCREEN_H - CARD_H) // 2
    TEXT_X  = 32
    TEXT_MW = CARD_W - 64

    body_lines = _wrap(body_text, font_body, TEXT_MW)
    to_lines   = _wrap(to_line,  font_to,   TEXT_MW)

    LINE_H    = font_body.get_height() + 4
    TO_LINE_H = font_to.get_height()   + 4
    DAY_H     = font_day.get_height()

    HEADER_H = 10 + 14 + DAY_H + 10
    content_h = (len(to_lines)   * TO_LINE_H + 12 +
                 len(body_lines) * LINE_H     + 20)
    TOTAL_H   = HEADER_H + content_h

    SCROLL_AREA_Y = CARD_Y + HEADER_H
    SCROLL_AREA_H = CARD_H - HEADER_H - 28
    scroll_y   = 0
    MAX_SCROLL = max(0, content_h - SCROLL_AREA_H)

    def build_content_surface() -> pygame.Surface:
        surf = pygame.Surface((CARD_W - 4, content_h), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        y = 0
        for tl in to_lines:
            surf.blit(font_to.render(tl, True, C_INK), (TEXT_X, y))
            y += TO_LINE_H
        y += 12
        for bl in body_lines:
            surf.blit(font_body.render(bl, True, (60, 65, 90)), (TEXT_X, y))
            y += LINE_H
        return surf

    content_surf = build_content_surface()

    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))

    card_rect = pygame.Rect(CARD_X, CARD_Y, CARD_W, CARD_H)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not card_rect.collidepoint(event.pos):
                    return

            if event.type == pygame.MOUSEWHEEL:
                scroll_y -= event.y * 24
                scroll_y  = max(0, min(scroll_y, MAX_SCROLL))

        if background:
            screen.blit(background, (-camera_x, 0))
        else:
            screen.fill(C_BG)

        screen.blit(overlay, (0, 0))

        pygame.draw.rect(screen, (255, 255, 255), card_rect, border_radius=8)
        pygame.draw.rect(screen, C_INK,           card_rect, 2, border_radius=8)

        pygame.draw.rect(screen, C_INK,
                         pygame.Rect(CARD_X, CARD_Y, CARD_W, 10), border_radius=8)
        pygame.draw.rect(screen, C_INK,
                         pygame.Rect(CARD_X, CARD_Y + 5, CARD_W, 5))

        day_surf = font_day.render(f"DAY  {day}  — Letter from the Manager",
                                   True, (255, 255, 255))
        screen.blit(day_surf, (CARD_X + TEXT_X, CARD_Y + 14))

        rule_y = CARD_Y + 14 + DAY_H + 6
        pygame.draw.line(screen, (*C_INK, 70),
                         (CARD_X + TEXT_X, rule_y),
                         (CARD_X + CARD_W - 32, rule_y), 1)

        viewport = pygame.Rect(0, scroll_y, CARD_W - 4, SCROLL_AREA_H)
        screen.blit(content_surf, (CARD_X + 2, SCROLL_AREA_Y), viewport)

        pygame.draw.rect(screen, (255,255,255),
                         pygame.Rect(CARD_X, CARD_Y, CARD_W, HEADER_H - 2))
        pygame.draw.rect(screen, (255,255,255),
                         pygame.Rect(CARD_X + 2, CARD_Y + CARD_H - 26, CARD_W - 4, 28))
        pygame.draw.rect(screen, C_INK, card_rect, 2, border_radius=8)

        if MAX_SCROLL > 0:
            BAR_X   = CARD_X + CARD_W - 8
            BAR_TOP = SCROLL_AREA_Y
            BAR_H   = SCROLL_AREA_H
            thumb_h = max(30, int(BAR_H * SCROLL_AREA_H / content_h))
            thumb_y = BAR_TOP + int((BAR_H - thumb_h) * scroll_y / MAX_SCROLL)
            pygame.draw.rect(screen, (210, 215, 230),
                             pygame.Rect(BAR_X, BAR_TOP, 4, BAR_H), border_radius=2)
            pygame.draw.rect(screen, C_INK,
                             pygame.Rect(BAR_X, thumb_y, 4, thumb_h), border_radius=2)

        hint_text = ("scroll to read  ·  click outside to close"
                     if MAX_SCROLL > 0 else "click outside to close")
        hint = font_hint.render(f"— {hint_text} —", True, C_FAINT)
        screen.blit(hint, hint.get_rect(
            centerx=CARD_X + CARD_W // 2,
            y=CARD_Y + CARD_H - 20))

        pygame.display.flip()
        clock.tick(FPS)