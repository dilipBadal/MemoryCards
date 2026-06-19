import pygame

pygame.init()

# ── DISPLAY CONSTANTS ──────────────────────────────────────────
WIDTH, HEIGHT = 900, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Matching Game - Dual Mode")

# ── COLOR PALETTE ──────────────────────────────────────────────
BG          = (20, 22, 28)       # Deep slate black
CARD_BACK   = (60, 70, 95)       # Muted navy blue
CARD_FRONT  = (240, 180, 60)     # Vibrant gold
GREEN       = (70, 200, 140)     # Mint green
RED         = (220, 80, 80)      # Sarcastic alert red
WHITE       = (235, 235, 235)    # Clean off-white
PANEL       = (30, 32, 40)       # Dark side panel
BUTTON      = (50, 55, 75)       # Slate buttons
BUTTON_HOVER= (90, 100, 140)     # Highlighted slate

# ── LAYOUT CONSTANTS ───────────────────────────────────────────
ROWS, COLS  = 4, 4
CARD_SIZE   = 120
GAP         = 20
start_x     = (WIDTH - (COLS * CARD_SIZE + (COLS - 1) * GAP)) // 2
start_y     = 120

# ── FONT LOADING ───────────────────────────────────────────────
font       = pygame.font.SysFont("arial", 36)
small_font = pygame.font.SysFont("arial", 22)
tiny_font  = pygame.font.SysFont("arial", 17)

def get_monospace_font(size, bold=False):
    for name in ["courier new", "consolas", "monaco", "lucida console", "dejavu sans mono", "monospace"]:
        try:
            f = pygame.font.SysFont(name, size, bold=bold)
            if f:
                return f
        except:
            pass
    return pygame.font.Font(None, size)

cli_font      = get_monospace_font(18, bold=True)
cli_font_big  = get_monospace_font(22, bold=True)
cli_font_tiny = get_monospace_font(14, bold=False)
