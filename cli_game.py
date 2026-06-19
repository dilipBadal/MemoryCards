#!/usr/bin/env python3
import os
import time
import sys
import random

# Import our helper modules
import memory_sound as sound
import memory_logic as logic

# ── ANSI ESCAPE CODES FOR COLOR STYLING ────────────────────────
CLR_RESET   = "\033[0m"
CLR_BOLD    = "\033[1m"
CLR_DIM     = "\033[2m"
CLR_GREEN   = "\033[32m"
CLR_YELLOW  = "\033[33m"
CLR_BLUE    = "\033[34m"
CLR_CYAN    = "\033[36m"
CLR_RED     = "\033[31m"
CLR_GOLD    = "\033[38;5;220m"
CLR_GRAY    = "\033[90m"

# ── RENDER SYSTEM FUNCTIONS ────────────────────────────────────
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def draw_banner():
    print(f"\n  {CLR_GREEN}{CLR_BOLD}=== TERMINAL MEMORY MATCHING GAME ==={CLR_RESET}")

def print_board(sel_a=None, sel_b=None):
    print(f"\n      {CLR_CYAN}COLUMN 1      COLUMN 2      COLUMN 3      COLUMN 4{CLR_RESET}")
    print(f"    +-------------+-------------+-------------+-------------+")
    for r in range(4):
        # Top padding row
        print("    |             |             |             |             |")
        
        # Content cell row
        content_str = "    "
        for c in range(4):
            idx = r * 4 + c
            is_active  = (idx == sel_a or idx == sel_b)
            is_matched = logic.matched[idx]
            
            # Index indicator e.g. "[03]"
            idx_label = f"{CLR_GRAY}[{idx+1:02d}]{CLR_RESET}"
            
            if is_matched:
                val_str = f"{CLR_GREEN}[ {logic.board[idx]} ]{CLR_RESET}"
                cell_content = f"{idx_label} {val_str}"
            elif is_active:
                val_str = f"{CLR_GOLD}[ {logic.board[idx]} ]{CLR_RESET}"
                cell_content = f"{idx_label} {val_str}"
            else:
                val_str = f"{CLR_DIM}[ ? ]{CLR_RESET}"
                cell_content = f"{idx_label} {val_str}"
                
            content_str += f"|  {cell_content}  "
        content_str += "|"
        print(content_str)
        
        # Bottom padding row
        print("    |             |             |             |             |")
        print("    +-------------+-------------+-------------+-------------+")
    print()


# ── MAIN GAME CONTROLLER ───────────────────────────────────────
def main():
    logic.reset()
    moves = 0
    sound.play(sound.restart_snd)
    
    first_card = None
    
    while True:
        clear_screen()
        draw_banner()
        
        # HUD Status bar
        print(f" {CLR_BOLD}Moves: {moves} | Pairs Matched: {sum(logic.matched)//2}/8{CLR_RESET}\n")
        
        # Draw board grid
        print_board(first_card)
        
        # Dynamic Prompt
        if first_card is None:
            prompt = f" {CLR_CYAN}Select 1st Card (1-16) | [s] Solver | [r] Reset | [q] Quit:{CLR_RESET} "
        else:
            prompt = f" {CLR_CYAN}Select 2nd Card (1-16) | [s] Solver | [r] Reset | [q] Quit:{CLR_RESET} "
            
        choice = input(prompt).strip().lower()
        
        if choice == 'q':
            print("\nGoodbye!")
            break
            
        elif choice == 'r':
            sound.play(sound.restart_snd)
            logic.reset()
            moves = 0
            first_card = None
            print("\nGame reset. Shuffling board...")
            time.sleep(1.0)
            continue
            
        elif choice == 's':
            sound.play(sound.auto_snd)
            if first_card is not None:
                # Helper auto-solver for second selection
                unmatched_other = [i for i in range(16) if not logic.matched[i] and i != first_card]
                if unmatched_other:
                    partner_val = logic.board[first_card]
                    partner = next((i for i in unmatched_other if i in logic.auto_memory and logic.auto_memory[i] == partner_val), None)
                    if partner is None:
                        partner = random.choice(unmatched_other)
                    
                    second_card = partner
                    logic.auto_memory[second_card] = logic.board[second_card]
                    
                    # intermediate show
                    clear_screen()
                    draw_banner()
                    print(f" {CLR_BOLD}Moves: {moves} | Pairs Matched: {sum(logic.matched)//2}/8{CLR_RESET}\n")
                    print(f" {CLR_GOLD}[AUTO] Solver selects Card {second_card+1}{CLR_RESET}")
                    print_board(first_card, second_card)
                    
                    moves += 1
                    time.sleep(1.8)
                    
                    # Match check
                    if logic.board[first_card] == logic.board[second_card]:
                        logic.matched[first_card] = True
                        logic.matched[second_card] = True
                        sound.play(sound.match_snd)
                        print(f" {CLR_GREEN}[SUCCESS] Match! Pair '{logic.board[first_card]}' matched.{CLR_RESET}")
                    else:
                        sound.play(sound.no_match_snd)
                        print(f" {CLR_RED}[FAIL] Card {first_card+1} and Card {second_card+1} mismatched.{CLR_RESET}")
                    
                    first_card = None
                    time.sleep(1.5)
            else:
                # Solver makes full turn
                pick = logic.auto_pick_pair()
                if pick:
                    ia, ib = pick
                    logic.auto_memory[ia] = logic.board[ia]
                    logic.auto_memory[ib] = logic.board[ib]
                    
                    # intermediate first pick show
                    clear_screen()
                    draw_banner()
                    print(f" {CLR_BOLD}Moves: {moves} | Pairs Matched: {sum(logic.matched)//2}/8{CLR_RESET}\n")
                    print(f" {CLR_GOLD}[AUTO] Solver selects Card {ia+1}{CLR_RESET}")
                    print_board(ia)
                    time.sleep(1.0)
                    
                    # intermediate second pick show
                    clear_screen()
                    draw_banner()
                    print(f" {CLR_BOLD}Moves: {moves} | Pairs Matched: {sum(logic.matched)//2}/8{CLR_RESET}\n")
                    print(f" {CLR_GOLD}[AUTO] Solver selects Card {ia+1} and Card {ib+1}{CLR_RESET}")
                    print_board(ia, ib)
                    
                    moves += 1
                    time.sleep(1.8)
                    
                    # Match check
                    if logic.board[ia] == logic.board[ib]:
                        logic.matched[ia] = True
                        logic.matched[ib] = True
                        sound.play(sound.match_snd)
                        print(f" {CLR_GREEN}[SUCCESS] Match! Pair '{logic.board[ia]}' matched.{CLR_RESET}")
                    else:
                        sound.play(sound.no_match_snd)
                        print(f" {CLR_RED}[FAIL] Card {ia+1} and Card {ib+1} mismatched.{CLR_RESET}")
                    
                    time.sleep(1.5)
            continue
            
        else:
            try:
                num = int(choice)
                idx = num - 1
                if idx < 0 or idx > 15:
                    print(f" {CLR_RED}[ERROR] Choose a card from 1 to 16!{CLR_RESET}")
                    time.sleep(1.5)
                    continue
                if logic.matched[idx]:
                    print(f" {CLR_RED}[ERROR] Card {num} is already matched!{CLR_RESET}")
                    time.sleep(1.5)
                    continue
                if first_card is not None and idx == first_card:
                    print(f" {CLR_RED}[ERROR] Card {num} is already selected! Select a different card.{CLR_RESET}")
                    time.sleep(1.5)
                    continue
                
                sound.play(sound.select_snd)
                sound.play(sound.flip_snd)
                logic.auto_memory[idx] = logic.board[idx]
                
                if first_card is None:
                    first_card = idx
                else:
                    second_card = idx
                    
                    # intermediate show both selections
                    clear_screen()
                    draw_banner()
                    print(f" {CLR_BOLD}Moves: {moves} | Pairs Matched: {sum(logic.matched)//2}/8{CLR_RESET}\n")
                    print_board(first_card, second_card)
                    
                    moves += 1
                    time.sleep(1.8)
                    
                    # Match evaluation
                    if logic.board[first_card] == logic.board[second_card]:
                        logic.matched[first_card] = True
                        logic.matched[second_card] = True
                        sound.play(sound.match_snd)
                        print(f" {CLR_GREEN}[SUCCESS] Match! Pair '{logic.board[first_card]}' matched.{CLR_RESET}")
                    else:
                        sound.play(sound.no_match_snd)
                        print(f" {CLR_RED}[FAIL] Card {first_card+1} and Card {second_card+1} mismatched.{CLR_RESET}")
                    
                    first_card = None
                    time.sleep(1.5)
            except ValueError:
                print(f" {CLR_RED}[ERROR] Invalid input. Enter 1-16, 's' for solver, 'r' for reset, or 'q' for quit.{CLR_RESET}")
                time.sleep(1.5)
                continue
                
        # Game win condition
        if all(logic.matched):
            sound.play(sound.game_finish_snd)
            clear_screen()
            draw_banner()
            
            # Fetch roasts from memory_ui.py helper
            from memory_ui import get_sarcastic_message
            headline, subline = get_sarcastic_message(moves)
            
            trophy = f"""
{CLR_GOLD}      ======================================================
                   🏆   CONGRATULATIONS!   🏆
      ======================================================
                 Completed in {moves} moves.
                 
          "{headline}"
          {subline}
{CLR_RESET}
            """
            print(trophy)
            
            choice = input(f" {CLR_CYAN}Play again? [y/n]:{CLR_RESET} ").strip().lower()
            if choice == 'y':
                sound.play(sound.restart_snd)
                logic.reset()
                moves = 0
                first_card = None
            else:
                print("\nGoodbye!")
                break

if __name__ == "__main__":
    main()
