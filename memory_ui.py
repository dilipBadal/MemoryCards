import pygame
import math
import memory_constants as const
import memory_logic as logic
import memory_sound as sound

# ── RENDER HELPERS ─────────────────────────────────────────────
def draw_text(text, x, y, color=const.WHITE, fnt=None):
    f   = fnt or const.font
    img = f.render(str(text), True, color)
    rect = img.get_rect(center=(x, y))
    const.screen.blit(img, rect)

def draw_small(text, x, y, color=const.WHITE):
    img = const.small_font.render(str(text), True, color)
    const.screen.blit(img, (x, y))

def draw_tiny(text, x, y, color=const.WHITE):
    img = const.tiny_font.render(str(text), True, color)
    const.screen.blit(img, (x, y))

def draw_key_hint(key_text, desc, x, y):
    kw = const.tiny_font.size(key_text)[0] + 16
    kh = 26
    rect = pygame.Rect(x, y, kw, kh)
    pygame.draw.rect(const.screen, (50, 55, 75), rect, border_radius=5)
    pygame.draw.rect(const.screen, (100, 110, 140), rect, 1, border_radius=5)
    draw_text(key_text, rect.centerx, rect.centery, color=const.WHITE, fnt=const.tiny_font)
    draw_small(desc, x + kw + 10, y + 2, color=(160, 170, 190))


# ── BUTTON CLASS ───────────────────────────────────────────────
class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, mouse):
        color = const.BUTTON_HOVER if self.rect.collidepoint(mouse) else const.BUTTON
        pygame.draw.rect(const.screen, color, self.rect, border_radius=10)
        draw_text(self.text, self.rect.centerx, self.rect.centery)

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and self.rect.collidepoint(pygame.mouse.get_pos()))


# ── MENU BUTTONS ───────────────────────────────────────────────
btn_gui   = Button(const.WIDTH//2 - 150, 260, 300, 60, "Classic Mode")
btn_text  = Button(const.WIDTH//2 - 150, 350, 300, 60, "Input Mode")
btn_quit  = Button(const.WIDTH//2 - 150, 440, 300, 60, "Quit")

# ── POPUP BUTTONS ──────────────────────────────────────────────
btn_popup_again = Button(const.WIDTH//2 - 170, const.HEIGHT//2 + 70, 150, 50, "Play Again")
btn_popup_menu  = Button(const.WIDTH//2 + 20,  const.HEIGHT//2 + 70, 150, 50, "Menu")


# ── SARCASTIC WIN MESSAGES ─────────────────────────────────────
def get_sarcastic_message(move_count):
    if move_count <= 9:
        return (
            "Oh Mr. Genius is HERE!",
            "Slow down Einstein, some of us have lives."
        )
    elif move_count <= 12:
        return (
            "Okay okay, calm down Sherlock.",
            "Nobody likes a show-off. ...Nice job though."
        )
    elif move_count <= 16:
        return (
            "Pretty good. For a human.",
            "Your goldfish is slightly less impressed."
        )
    elif move_count <= 20:
        return (
            "Average. Painfully, beautifully average.",
            "Right in the middle of the bell curve. Cozy."
        )
    elif move_count <= 25:
        return (
            "Were you guessing? You were guessing.",
            "A blindfolded raccoon might've done better."
        )
    elif move_count <= 32:
        return (
            "Your goldfish has better memory than this.",
            f"{move_count} moves. The cards are filing a complaint."
        )
    elif move_count <= 42:
        return (
            "Did you take a nap mid-game?",
            f"{move_count} moves. I've seen glaciers move faster."
        )
    else:
        return (
            "Bless. Your. Heart.",
            f"{move_count} moves! Even the board feels sorry for you."
        )


# ── POPUP WINDOW ───────────────────────────────────────────────
def draw_win_popup(move_count, mouse):
    overlay = pygame.Surface((const.WIDTH, const.HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    const.screen.blit(overlay, (0, 0))

    bw, bh = 580, 340
    bx     = const.WIDTH  // 2 - bw // 2
    by     = const.HEIGHT // 2 - bh // 2

    panel = pygame.Surface((bw, bh), pygame.SRCALPHA)
    panel.fill((18, 22, 42, 235))
    const.screen.blit(panel, (bx, by))

    pulse = int(160 + 90 * math.sin(pygame.time.get_ticks() / 300))
    pygame.draw.rect(const.screen, (80, pulse, 255), (bx, by, bw, bh), 3, border_radius=20)

    t = pygame.time.get_ticks() / 800
    confetti_cols = [(255,180,50), (100,220,160), (130,160,255), (255,100,130),
                     (255,220,80), (80,230,200)]
    for i in range(16):
        angle = (i / 16) * math.pi * 2 + t
        rx    = const.WIDTH  // 2 + int(math.cos(angle) * (bw // 2 + 28))
        ry    = const.HEIGHT // 2 + int(math.sin(angle) * (bh // 2 + 28))
        col   = confetti_cols[i % len(confetti_cols)]
        sz    = 5 + int(2 * math.sin(t * 3 + i))
        pygame.draw.circle(const.screen, col, (rx, ry), sz)

    draw_text("🏆", const.WIDTH // 2, by + 55)
    draw_text("YOU  WIN!", const.WIDTH // 2, by + 110, color=(255, 210, 50))
    draw_text(f"{move_count} moves", const.WIDTH // 2, by + 155, color=(140, 150, 200), fnt=const.small_font)

    headline, subline = get_sarcastic_message(move_count)
    draw_text(headline, const.WIDTH // 2, by + 195, color=(230, 230, 255), fnt=const.small_font)
    draw_text(subline,  const.WIDTH // 2, by + 222, color=(110, 118, 160), fnt=const.tiny_font)

    btn_popup_again.draw(mouse)
    btn_popup_menu.draw(mouse)

    draw_tiny("R = play again   |   ESC = menu", const.WIDTH // 2 - 110, by + bh - 26, color=(70, 78, 110))


# ── DRAW: MENU ─────────────────────────────────────────────────
def draw_menu(mouse):
    const.screen.fill(const.BG)
    draw_text("Memory Matching Game", const.WIDTH // 2, 120)
    btn_gui.draw(mouse)
    btn_text.draw(mouse)
    btn_quit.draw(mouse)


# ── DRAW: CLASSIC BOARD ────────────────────────────────────────
flip_anim = []

def start_flip(i):
    flip_anim.append([i, 0])
    sound.play(sound.flip_snd)

def update_flip():
    for f in flip_anim[:]:
        f[1] += 0.12
        if f[1] >= 1:
            logic.revealed[f[0]] = True
            flip_anim.remove(f)

def draw_board():
    for i in range(16):
        row = i // 4
        col = i % 4
        x   = const.start_x + col * (const.CARD_SIZE + const.GAP)
        y   = const.start_y + row * (const.CARD_SIZE + const.GAP)
        rect = pygame.Rect(x, y, const.CARD_SIZE, const.CARD_SIZE)

        color = const.CARD_BACK
        if logic.matched[i]:
            color = const.GREEN
        elif logic.revealed[i]:
            color = const.CARD_FRONT

        pygame.draw.rect(const.screen, color, rect, border_radius=12)
        if logic.revealed[i] or logic.matched[i]:
            draw_text(logic.board[i], rect.centerx, rect.centery)

        # Card index label
        num_img = const.tiny_font.render(str(i + 1), True, (80, 88, 110))
        const.screen.blit(num_img, (x + 5, y + const.CARD_SIZE - 20))


def draw_hud():
    draw_small(f"Moves: {logic.moves}", 30, 20)
    hint = "S = auto-solve  |  R = reset  |  ESC = menu"
    if logic.auto_solving:
        hint = "Auto-solving...  (S to stop)"
    draw_small(hint, const.WIDTH // 2 - 160, const.HEIGHT - 30, color=(100, 110, 140))


# ── DRAW: RETRO TERMINAL & ASCII BOARD ────────────────────────
def draw_cli_board():
    # Drop shadow
    pygame.draw.rect(const.screen, (10, 11, 14), pygame.Rect(34, 44, 540, 620), border_radius=15)
    
    # Terminal body
    term_rect = pygame.Rect(30, 40, 540, 620)
    pygame.draw.rect(const.screen, (12, 14, 18), term_rect, border_radius=15)
    pygame.draw.rect(const.screen, (60, 65, 80), term_rect, 2, border_radius=15)
    
    # Window Header Bar
    title_rect = pygame.Rect(30, 40, 540, 35)
    pygame.draw.rect(const.screen, (32, 35, 45), title_rect, border_top_left_radius=15, border_top_right_radius=15)
    pygame.draw.line(const.screen, (50, 55, 70), (30, 75), (570, 75), 2)
    
    # Header Dots (macOS styled)
    pygame.draw.circle(const.screen, (255, 95, 87), (52, 58), 6)
    pygame.draw.circle(const.screen, (255, 189, 46), (70, 58), 6)
    pygame.draw.circle(const.screen, (39, 201, 63), (88, 58), 6)
    
    draw_text("Memory Cards", 300, 58, color=(140, 160, 180), fnt=const.cli_font_tiny)
    
    # Draw ASCII Card Cells
    for i in range(16):
        row = i // 4
        col = i % 4
        x   = 80 + col * 115
        y   = 110 + row * 95
        cell_rect = pygame.Rect(x, y, 90, 75)
        
        is_active = (i == logic.text_a or i == logic.text_b)
        is_matched = logic.matched[i]
        
        if is_matched:
            bg_color     = (18, 38, 28)
            border_color = const.GREEN
            text_color   = const.GREEN
            val_text     = f"[ {logic.board[i]} ]"
            border_width = 2
        elif is_active:
            bg_color     = (35, 30, 20)
            border_color = const.CARD_FRONT
            text_color   = const.CARD_FRONT
            val_text     = f"[ {logic.board[i]} ]"
            border_width = 2
        else:
            bg_color     = (15, 17, 22)
            border_color = (60, 85, 75)
            text_color   = (120, 140, 130)
            val_text     = "[ ? ]"
            border_width = 1
            
        pygame.draw.rect(const.screen, bg_color, cell_rect, border_radius=8)
        pygame.draw.rect(const.screen, border_color, cell_rect, border_width, border_radius=8)
        
        # Draw Index e.g. "[03]"
        num_img = const.cli_font_tiny.render(f"[{i+1:02d}]", True, (80, 105, 95))
        const.screen.blit(num_img, (x + 8, y + 8))
        
        # Center Value
        val_img = const.cli_font_big.render(val_text, True, text_color)
        val_rect = val_img.get_rect(center=(cell_rect.centerx, cell_rect.centery + 10))
        const.screen.blit(val_img, val_rect)

    # Terminal log partition line
    pygame.draw.line(const.screen, (40, 45, 55), (30, 495), (570, 495), 2)
    
    # Render scrolling terminal lines
    log_y = 510
    for line in logic.cli_log:
        if line.startswith("user@mem"):
            col = (100, 255, 120)
        elif line.startswith("[SUCCESS]"):
            col = const.GREEN
        elif line.startswith("[FAIL]") or line.startswith("[ERROR]"):
            col = const.RED
        else:
            col = (160, 180, 170)
            
        line_img = const.cli_font.render(line, True, col)
        const.screen.blit(line_img, (50, log_y))
        log_y += 24


# ── DRAW: INTERACTIVE SIDEBAR PANEL ─────────────────────────────
def draw_text_panel():
    pygame.draw.rect(const.screen, const.PANEL, (600, 0, 300, const.HEIGHT))
    draw_text("INPUT MODE", 750, 45)
    draw_small(f"Moves: {logic.text_moves}", 630, 95, const.GREEN)
    pygame.draw.line(const.screen, (50, 52, 65), (620, 130), (880, 130), 2)
    
    # 1. Card Selection Slots
    c1_rect = pygame.Rect(625, 150, 100, 110)
    if logic.text_a is not None:
        pygame.draw.rect(const.screen, const.CARD_FRONT, c1_rect, border_radius=12)
        draw_text(f"#{logic.text_a+1}", c1_rect.centerx, c1_rect.top + 25, color=(30, 32, 40), fnt=const.tiny_font)
        draw_text(logic.board[logic.text_a], c1_rect.centerx, c1_rect.centery + 15, color=(30, 32, 40), fnt=const.font)
    else:
        pygame.draw.rect(const.screen, (35, 38, 48), c1_rect, border_radius=12)
        pygame.draw.rect(const.screen, (70, 75, 95), c1_rect, 2, border_radius=12)
        draw_text("1st Card", c1_rect.centerx, c1_rect.top + 25, color=(100, 110, 130), fnt=const.tiny_font)
        draw_text("?", c1_rect.centerx, c1_rect.centery + 15, color=(80, 88, 105), fnt=const.font)

    c2_rect = pygame.Rect(765, 150, 100, 110)
    if logic.text_b is not None:
        pygame.draw.rect(const.screen, const.CARD_FRONT, c2_rect, border_radius=12)
        draw_text(f"#{logic.text_b+1}", c2_rect.centerx, c2_rect.top + 25, color=(30, 32, 40), fnt=const.tiny_font)
        draw_text(logic.board[logic.text_b], c2_rect.centerx, c2_rect.centery + 15, color=(30, 32, 40), fnt=const.font)
    else:
        pygame.draw.rect(const.screen, (35, 38, 48), c2_rect, border_radius=12)
        pygame.draw.rect(const.screen, (70, 75, 95), c2_rect, 2, border_radius=12)
        draw_text("2nd Card", c2_rect.centerx, c2_rect.top + 25, color=(100, 110, 130), fnt=const.tiny_font)
        draw_text("?", c2_rect.centerx, c2_rect.centery + 15, color=(80, 88, 105), fnt=const.font)

    pygame.draw.line(const.screen, (50, 52, 65), (620, 280), (880, 280), 2)

    # 2. Glowing Input Box
    if "No match" in logic.message or "Please" in logic.message or "different" in logic.message or "already" in logic.message or "Enter a card" in logic.message or "range" in logic.message:
        border_color = const.RED
    elif "Match" in logic.message or "won" in logic.message:
        border_color = const.GREEN
    elif logic.text_step == 2:
        border_color = (60, 130, 240)
    else:
        border_color = (130, 140, 170)

    input_rect = pygame.Rect(620, 305, 260, 50)
    pygame.draw.rect(const.screen, (15, 17, 22), input_rect, border_radius=10)
    pygame.draw.rect(const.screen, border_color, input_rect, 2, border_radius=10)

    if not logic.text_input:
        ph_text = "Type card (1-16)..."
        ph_img = const.small_font.render(ph_text, True, (75, 80, 100))
        const.screen.blit(ph_img, (635, 318))
    else:
        text_img = const.small_font.render(logic.text_input, True, const.WHITE)
        const.screen.blit(text_img, (635, 318))
    
    # Cursor
    t = pygame.time.get_ticks()
    if (t // 450) % 2 == 0:
        cursor_x = 635 + const.small_font.size(logic.text_input)[0]
        pygame.draw.line(const.screen, const.WHITE, (cursor_x, 318), (cursor_x, 342), 2)

    # Status Message
    msg_col = border_color
    if border_color == (130, 140, 170):
        msg_col = (140, 160, 210)
    draw_small(logic.message, 625, 375, msg_col)

    pygame.draw.line(const.screen, (50, 52, 65), (620, 420), (880, 420), 2)

    # 3. Keycaps Shortcuts Legend
    draw_key_hint("ENTER", "Select Card", 620, 440)
    draw_key_hint("S",     "Auto-solve Turn", 620, 485)
    draw_key_hint("R",     "Reset Game", 620, 530)
    draw_key_hint("ESC",   "Main Menu", 620, 575)
