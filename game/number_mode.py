# game/number_mode.py

import random

from config import DIFFICULTY_LEVELS
from .core import GameState, choose_difficulty
from .revival import revival_minigame


def play_number_game(player_name: str) -> GameState:
    print("\n=== NUMBER GUESSING MODE ===")

    difficulty_key = choose_difficulty()
    diff = DIFFICULTY_LEVELS[difficulty_key]

    state = GameState(player_name, mode="Number", difficulty_key=difficulty_key)

    print(
        f"\nYou chose {state.difficulty_name} mode: "
        f"guess numbers between {diff['min']} and {diff['max']}."
    )
    print(f"You have {state.lives} lives. Good luck!\n")

    while True:
        target = random.randint(diff["min"], diff["max"])
        attempts_left = diff["max_attempts"]
        guessed_correctly = False

        print(f"\nNew round! I picked a number between {diff['min']} and {diff['max']}.")

        while attempts_left > 0:
            guess_str = input(f"Attempts left {attempts_left}. Your guess: ").strip()
            try:
                guess = int(guess_str)
            except ValueError:
                print("Please enter a valid integer.")
                continue

            if guess == target:
                print("✅ Correct! You cracked this round.")
                round_score = attempts_left * 10
                state.score += round_score
                print(f"You earned {round_score} points. Total score: {state.score}")
                guessed_correctly = True
                break
            elif guess < target:
                print("Too low.")
            else:
                print("Too high.")

            attempts_left -= 1

        if not guessed_correctly:
            state.lives -= 1
            if state.lives > 0:
                print(f"\nYou ran out of attempts. Lives left: {state.lives}")
            else:
                print("\nYou are out of lives...")
                revived = revival_minigame()
                if revived:
                    state.lives = 1
                    print(f"Lives restored to {state.lives}. Continue fighting!")
                else:
                    print("\nNumber mode run ended.")
                    break

        # Ask if they want another round if still alive
        if state.lives > 0:
            again = input("\nPlay another round in Number mode? (y/n): ").strip().lower()
            if again != "y":
                break

    print(f"\nFinal score in Number mode: {state.score}")
    return state
