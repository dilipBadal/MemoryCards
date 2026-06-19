import pygame
import sys
import random
import memory_constants as const
import memory_sound as sound
import memory_logic as logic
import memory_ui as ui

# ── INITIALIZE GAME ────────────────────────────────────────────
logic.reset()
clock = pygame.time.Clock()

# ── MAIN LOOP ──────────────────────────────────────────────────
while True:
    dt    = clock.tick(60)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # ── STATE: MENU ────────────────────────────────────────
        if logic.mode == "menu":
            if ui.btn_gui.clicked(event):
                logic.reset()
                logic.mode = "gui"
            elif ui.btn_text.clicked(event):
                logic.reset()
                logic.mode = "text"
            elif ui.btn_quit.clicked(event):
                pygame.quit()
                sys.exit()

        # ── STATE: CLASSIC GUI MODE ────────────────────────────
        elif logic.mode == "gui":
            if logic.show_popup:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ui.btn_popup_again.clicked(event):
                        sound.play(sound.restart_snd)
                        logic.reset()
                    elif ui.btn_popup_menu.clicked(event):
                        logic.reset()
                        logic.mode = "menu"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        sound.play(sound.restart_snd)
                        logic.reset()
                    elif event.key == pygame.K_ESCAPE:
                        logic.reset()
                        logic.mode = "menu"
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        logic.mode = "menu"
                    elif event.key == pygame.K_r:
                        sound.play(sound.restart_snd)
                        logic.reset()
                    elif event.key == pygame.K_s:
                        if logic.auto_solving:
                            logic.auto_solving = False
                            logic.auto_memory  = {}
                        else:
                            sound.play(sound.auto_snd)
                            logic.auto_solving    = True
                            logic.auto_memory     = {}
                            logic.auto_step_timer = 0
                            logic.revealed        = [False] * 16
                            logic.first_pick      = None
                            logic.second_pick     = None
                            logic.waiting         = False

                elif not logic.auto_solving and event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = mouse
                    for i in range(16):
                        row = i // 4
                        col = i % 4
                        x   = const.start_x + col * (const.CARD_SIZE + const.GAP)
                        y   = const.start_y + row * (const.CARD_SIZE + const.GAP)
                        rect = pygame.Rect(x, y, const.CARD_SIZE, const.CARD_SIZE)
                        if rect.collidepoint(mx, my) and not logic.matched[i] and not logic.revealed[i]:
                            sound.play(sound.select_snd)
                            logic.auto_memory[i] = logic.board[i]
                            if logic.first_pick is None:
                                logic.first_pick = i
                                ui.start_flip(i)
                            elif logic.second_pick is None and i != logic.first_pick:
                                logic.second_pick = i
                                ui.start_flip(i)
                                logic.moves += 1
                                logic.waiting = True
                                logic.wait_timer = 0

        # ── STATE: TEXT CLI MODE ───────────────────────────────
        elif logic.mode == "text":
            if logic.show_popup:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ui.btn_popup_again.clicked(event):
                        sound.play(sound.restart_snd)
                        logic.reset()
                    elif ui.btn_popup_menu.clicked(event):
                        logic.reset()
                        logic.mode = "menu"
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        sound.play(sound.restart_snd)
                        logic.reset()
                    elif event.key == pygame.K_ESCAPE:
                        logic.reset()
                        logic.mode = "menu"
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        logic.mode = "menu"
                    elif event.key == pygame.K_r:
                        sound.play(sound.restart_snd)
                        logic.reset()
                    elif event.key == pygame.K_s and not logic.text_waiting:
                        sound.play(sound.auto_snd)
                        logic.cli_log_append("user@mem:~$ auto-solve --next-turn")
                        if logic.text_step == 2 and logic.text_a is not None:
                            unmatched_other = [i for i in range(16) if not logic.matched[i] and i != logic.text_a]
                            if unmatched_other:
                                partner_val = logic.board[logic.text_a]
                                partner = next((i for i in unmatched_other if i in logic.auto_memory and logic.auto_memory[i] == partner_val), None)
                                if partner is None:
                                    partner = random.choice(unmatched_other)
                                logic.text_b = partner
                                logic.auto_memory[partner] = logic.board[partner]
                                logic.text_step = 1
                                logic.text_moves += 1
                                logic.text_waiting = True
                                logic.text_timer = 0
                                logic.message = f"Auto-solve: {logic.text_a+1} & {logic.text_b+1}"
                                logic.cli_log_append(f"[AUTO] Selected Card {partner+1} ('{logic.board[partner]}')")
                        else:
                            pick = logic.auto_pick_pair()
                            if pick:
                                ia, ib = pick
                                logic.auto_memory[ia] = logic.board[ia]
                                logic.auto_memory[ib] = logic.board[ib]
                                logic.text_a = ia
                                logic.text_b = ib
                                logic.text_step = 1
                                logic.text_moves += 1
                                logic.text_waiting = True
                                logic.text_timer = 0
                                logic.message = f"Auto-solve: {ia+1} & {ib+1}"
                                logic.cli_log_append(f"[AUTO] Flipped Card {ia+1} ('{logic.board[ia]}') & Card {ib+1} ('{logic.board[ib]}')")

                    elif event.key == pygame.K_BACKSPACE:
                        logic.text_input = logic.text_input[:-1]
                    elif event.key == pygame.K_RETURN:
                        if not logic.text_waiting:
                            try:
                                num = int(logic.text_input.strip())
                                idx = num - 1
                                if idx < 0 or idx > 15:
                                    logic.message = "Enter a card from 1 to 16!"
                                elif logic.matched[idx]:
                                    logic.message = f"Card {num} is already matched!"
                                elif logic.text_step == 2 and idx == logic.text_a:
                                    logic.message = "Select a different card!"
                                else:
                                    sound.play(sound.select_snd)
                                    sound.play(sound.flip_snd)
                                    logic.auto_memory[idx] = logic.board[idx]
                                    
                                    if logic.text_step == 1:
                                        logic.text_a = idx
                                        logic.text_step = 2
                                        logic.message = f"Selected Card {num}. Enter 2nd card:"
                                        logic.cli_log_append(f"user@mem:~$ select --card {num}")
                                        logic.cli_log_append(f"Card {num} revealed: '{logic.board[idx]}'")
                                    elif logic.text_step == 2:
                                        logic.text_b = idx
                                        logic.text_step = 1
                                        logic.text_moves += 1
                                        logic.text_waiting = True
                                        logic.text_timer = 0
                                        logic.message = "Checking match..."
                                        logic.cli_log_append(f"user@mem:~$ select --card {num}")
                                        logic.cli_log_append(f"Card {num} revealed: '{logic.board[idx]}'")
                            except ValueError:
                                logic.message = "Enter a number (1-16)"
                            logic.text_input = ""
                    elif event.unicode.isdigit():
                        if len(logic.text_input) < 2:
                            logic.text_input += event.unicode

    # ── TICK: AUTO SOLVER (GUI ONLY) ───────────────────────────
    if logic.mode == "gui" and logic.auto_solving and not logic.waiting:
        logic.auto_step_timer += dt
        if logic.auto_step_timer >= logic.AUTO_STEP_DELAY:
            logic.auto_step_timer = 0
            pick = logic.auto_pick_pair()
            if pick is None:
                logic.auto_solving = False
            else:
                ia, ib = pick
                logic.auto_memory[ia] = logic.board[ia]
                logic.auto_memory[ib] = logic.board[ib]
                logic.first_pick   = ia
                logic.second_pick  = ib
                logic.revealed[ia] = True
                logic.revealed[ib] = True
                sound.play(sound.flip_snd)
                logic.moves += 1
                logic.waiting    = True
                logic.wait_timer = 0

    # ── TICK: GUI MATCH CHECKER ────────────────────────────────
    if logic.mode == "gui" and logic.waiting:
        logic.wait_timer += dt
        if logic.wait_timer > 700:
            a, b = logic.first_pick, logic.second_pick
            if logic.board[a] == logic.board[b]:
                logic.matched[a] = True
                logic.matched[b] = True
                logic.score += 1
                if all(logic.matched):
                    sound.play(sound.game_finish_snd)
                    logic.show_popup   = True
                    logic.auto_solving = False
                else:
                    sound.play(sound.match_snd)
            else:
                logic.revealed[a] = False
                logic.revealed[b] = False
                sound.play(sound.no_match_snd)
            logic.first_pick  = None
            logic.second_pick = None
            logic.waiting     = False

    # ── TICK: TEXT MATCH CHECKER ───────────────────────────────
    if logic.mode == "text" and logic.text_waiting:
        logic.text_timer += dt
        if logic.text_timer > 800:
            a, b = logic.text_a, logic.text_b
            if logic.board[a] == logic.board[b]:
                logic.matched[a] = True
                logic.matched[b] = True
                logic.cli_log_append(f"[SUCCESS] Match! Pair '{logic.board[a]}' matched.")
                if all(logic.matched):
                    sound.play(sound.game_finish_snd)
                    logic.show_popup = True
                    logic.message    = ""
                else:
                    sound.play(sound.match_snd)
                    logic.message = f"Match! ({sum(logic.matched)//2}/8 pairs) - Enter 1st card:"
            else:
                logic.message = "No match! - Enter 1st card (1-16):"
                logic.cli_log_append(f"[FAIL] Mismatch! Card {a+1} and {b+1} did not match.")
                sound.play(sound.no_match_snd)
            logic.text_a       = None
            logic.text_b       = None
            logic.text_waiting = False
            logic.text_step    = 1

    # ── RENDER WINDOW ──────────────────────────────────────────
    const.screen.fill(const.BG)

    if logic.mode == "menu":
        ui.draw_menu(mouse)

    elif logic.mode == "gui":
        ui.draw_board()
        ui.draw_hud()
        ui.update_flip()
        if logic.show_popup:
            ui.draw_win_popup(logic.moves, mouse)

    elif logic.mode == "text":
        ui.draw_cli_board()
        ui.draw_text_panel()
        if logic.show_popup:
            ui.draw_win_popup(logic.text_moves, mouse)

    pygame.display.flip()