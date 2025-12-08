# game/revival.py

import random
import time
import os


def revival_minigame() -> bool:
    """
    Revival hub.
    Shows a menu of mini-challenges and runs the chosen one.
    Returns True if player revives, False otherwise.
    """
    print("\n=== ⚔ REVIVAL ARENA ⚔ ===")
    print("You have fallen in GuessRoyale...")
    print("Win a challenge to earn a second chance!\n")

    challenges = {
        "1": memory_flash_challenge,
        "2": direction_reflex_challenge,
        "3": fast_typing_challenge,
        "4": quick_math_challenge,
    }

    print("Choose your challenge:")
    print("  1. Memory Flash")
    print("  2. Direction Reflex")
    print("  3. Fast Typing")
    print("  4. Quick Math\n")

    choice = input("Enter 1–4 (blank/invalid = random): ").strip()

    if choice in challenges:
        challenge_func = challenges[choice]
    else:
        challenge_func = random.choice(list(challenges.values()))
        print("\nNo valid choice… The arena chooses for you!")

    print(f"\nChallenge Selected: {challenge_func.__name__.replace('_', ' ').title()}")
    time.sleep(1)
    print("\n--- Challenge Begins ---\n")

    result = challenge_func()

    if result:
        print("\n🔥 Revival successful! One life restored.")
    else:
        print("\n💀 Revival failed. Game Over.")

    return result


# ==============================
# 1. MEMORY FLASH
# ==============================

def memory_flash_challenge() -> bool:
    print("MEMORY FLASH")
    sequence = [str(random.randint(0, 9)) for _ in range(5)]
    print("\nMemorize this sequence:")
    print(" ".join(sequence))

    time.sleep(3)
    clear_screen()

    user_input = input("Enter the sequence exactly as shown: ").strip().replace(" ", "")
    correct = "".join(sequence)

    if user_input == correct:
        print("\nPerfect recall.")
        return True
    else:
        print(f"\nWrong sequence. Correct was: {correct}")
        return False


# ==============================
# 2. DIRECTION REFLEX
# ==============================

def direction_reflex_challenge() -> bool:
    print("DIRECTION REFLEX")
    directions = {"L": "LEFT", "R": "RIGHT", "U": "UP", "D": "DOWN"}

    for _ in range(5):
        correct_key, label = random.choice(list(directions.items()))
        print(f"\nType the first letter of: {label}")

        start = time.time()
        user = input("Your input: ").strip().upper()
        duration = time.time() - start

        if duration > 1.5:
            print("Too slow.")
            return False

        if user != correct_key:
            print("Wrong direction.")
            return False

        print("Correct!")

    print("\nReflexes on point.")
    return True


# ==============================
# 3. FAST TYPING
# ==============================

def fast_typing_challenge() -> bool:
    print("FAST TYPING")
    words = ["royale", "python", "reflex", "memory", "ninja", "system"]
    word = random.choice(words)
    time_limit = 4

    print(f"\nType this word in {time_limit} seconds:")
    print(word)

    start = time.time()
    user_input = input("Your input: ").strip()
    duration = time.time() - start

    if duration > time_limit:
        print(f"Too slow! Time: {duration:.2f}s")
        return False

    if user_input == word:
        print("Typing accurate.")
        return True
    else:
        print("Typing incorrect.")
        return False


# ==============================
# 4. QUICK MATH
# ==============================

def quick_math_challenge() -> bool:
    print("QUICK MATH")
    a = random.randint(5, 15)
    b = random.randint(2, 12)
    op = random.choice(["+", "-", "*"])

    if op == "+":
        correct = a + b
    elif op == "-":
        correct = a - b
    else:
        correct = a * b

    time_limit = 5

    print(f"\nSolve this in {time_limit} seconds:")
    print(f"{a} {op} {b}")

    start = time.time()
    user_input = input("Your answer: ").strip()
    duration = time.time() - start

    if duration > time_limit:
        print(f"Too slow! Time: {duration:.2f}s")
        return False

    try:
        if int(user_input) == correct:
            print("Correct calculation.")
            return True
        else:
            print(f"Wrong. Correct answer was {correct}.")
            return False
    except ValueError:
        print("Invalid number.")
        return False


# ==============================
# Utility
# ==============================

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")
