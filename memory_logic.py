import random

# ── GAME STATE VARIABLES ───────────────────────────────────────
board    = []
revealed = []
matched  = []

first_pick  = None
second_pick = None
waiting     = False
wait_timer  = 0

score = 0
moves = 0

# Text / CLI mode variables
text_input    = ""
text_step     = 1
text_a        = None
text_b        = None
text_revealed = []  # Kept for compatibility/fallback
text_waiting  = False
text_timer    = 0
text_score    = 0
text_moves    = 0
message       = "Enter first card (1-16):"
cli_log       = []

# Popup overlay state
show_popup   = False

# Auto-solver (human-like memory)
auto_solving    = False
auto_memory     = {}   # {card_index: card_value} — what solver has seen
auto_step_timer = 0
AUTO_STEP_DELAY = 650  # ms between auto moves

# Mode switcher: "menu", "gui", "text"
mode = "menu"


# ── LOGIC FUNCTIONS ────────────────────────────────────────────
def create_board():
    values = list("AABBCCDDEEFFGGHH")
    random.shuffle(values)
    return values

def cli_log_append(line):
    global cli_log
    cli_log.append(line)
    if len(cli_log) > 6:  # Max visible lines in terminal log view
        cli_log.pop(0)

def reset():
    global board, revealed, matched
    global first_pick, second_pick, waiting, wait_timer, score, moves
    global text_input, text_step, text_a, text_b, text_revealed, text_waiting, text_timer
    global text_score, text_moves, message, cli_log
    global show_popup, auto_solving, auto_memory, auto_step_timer

    board    = create_board()
    revealed = [False] * 16
    matched  = [False] * 16

    first_pick  = None
    second_pick = None
    waiting     = False
    wait_timer  = 0
    score       = 0
    moves       = 0

    text_input    = ""
    text_step     = 1
    text_a        = None
    text_b        = None
    text_revealed = []
    text_waiting  = False
    text_timer    = 0
    text_score    = 0
    text_moves    = 0
    message       = "Enter first card (1-16):"
    
    # Initialize scrolling terminal log with retro OS welcome messages
    cli_log = [
        "antigravity-os v1.0.0 (tty1)",
        "memory-match module initialized...",
        "board layout randomized.",
        "Enter first card (1-16):"
    ]
    
    show_popup      = False
    auto_solving    = False
    auto_memory     = {}
    auto_step_timer = 0


def auto_pick_pair():
    """
    Human-like pick logic:
    1. If we already know a complete unmatched pair in memory -> use it.
    2. Otherwise, pick first card randomly from unseen unmatched cards
       (fall back to any unmatched if all seen).
       Then if we know the partner of first card -> pick it (smart).
       Otherwise pick second card randomly from remaining unmatched.
    """
    unmatched = [i for i in range(16) if not matched[i]]
    if len(unmatched) < 2:
        return None

    # Build known-complete pairs from memory
    val_to_idx = {}
    known_pairs = []
    for idx in unmatched:
        if idx in auto_memory:
            val = auto_memory[idx]
            if val in val_to_idx:
                known_pairs.append((val_to_idx[val], idx))
            else:
                val_to_idx[val] = idx

    # If we know a pair, use it (with slight randomness — sometimes skip)
    if known_pairs and random.random() < 0.85:
        return random.choice(known_pairs)

    # Pick first card: prefer unseen cards so solver "explores"
    unseen = [i for i in unmatched if i not in auto_memory]
    ia = random.choice(unseen) if unseen else random.choice(unmatched)

    # If we've seen ia before and know its partner, pick partner
    if ia in auto_memory:
        partner_val = auto_memory[ia]
        partner = next(
            (i for i in unmatched if i != ia
             and i in auto_memory and auto_memory[i] == partner_val),
            None
        )
        if partner is not None:
            return ia, partner

    # Otherwise pick second card randomly (not same as first)
    remaining = [i for i in unmatched if i != ia]
    ib = random.choice(remaining)
    return ia, ib
