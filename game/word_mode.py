# game/word_mode.py

import random

from config import WORD_LISTS, DIFFICULTY_LEVELS
from .core import GameState, choose_difficulty
from .revival import revival_minigame


def play_word_game(player_name: str) -> GameState:
    print("\n=== WORD GUESSING MODE ===")

    difficulty_key = choose_difficulty()
    diff = DIFFICULTY_LEVELS[difficulty_key]
    words = WORD_LISTS[difficulty_key]

    state = GameState(player_name, mode="Word", difficulty_key=difficulty_key)

    print(
        f"\nYou chose {state.difficulty_name} mode: "
        f"guess words of moderate difficulty."
    )
    print(f"You have {state.lives} lives. Each round, guess the full word.\n")

    while True:
        secret = random.choice(words).lower()
        attempts_left = diff["max_attempts"]
        guessed_correctly = False

        print("\nNew round! I picked a secret word.")
        print(f"Hint: word length = {len(secret)}")
        print(f"First letter: {secret[0]}")
        print(f"Last letter:  {secret[-1]}")

        while attempts_left > 0:
            guess = input(f"\nAttempts left {attempts_left}. Your word guess: ").strip().lower()

            if not guess:
                print("Please enter a non-empty guess.")
                continue

            if guess == secret:
                print("✅ Correct! You guessed the word.")
                round_score = attempts_left * 15
                state.score += round_score
                print(f"You earned {round_score} points. Total score: {state.score}")
                guessed_correctly = True
                break
            else:
                # simple hint: show how many letters match in position
                matches = sum(1 for g, s in zip(guess, secret) if g == s)
                print(f"Wrong word. {matches} letter(s) are correct and in the right position.")
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
                    print("\nWord mode run ended.")
                    break

        if state.lives > 0:
            again = input("\nPlay another round in Word mode? (y/n): ").strip().lower()
            if again != "y":
                break

    print(f"\nFinal score in Word mode: {state.score}")
    return state
