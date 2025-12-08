# main.py

from game.core import show_welcome_screen, ask_player_name
from game.number_mode import play_number_game
from game.word_mode import play_word_game
from game.leaderboard import show_leaderboard, add_score


def main():
    show_welcome_screen()

    while True:
        print("=== MAIN MENU ===")
        print("1. Play Number Guessing")
        print("2. Play Word Guessing")
        print("3. View Leaderboard")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            player_name = ask_player_name()
            state = play_number_game(player_name)
            if state.score >= 0:
                save = input("Save this score to leaderboard? (y/n): ").strip().lower()
                if save == "y":
                    add_score(state)

        elif choice == "2":
            player_name = ask_player_name()
            state = play_word_game(player_name)
            if state.score >= 0:
                save = input("Save this score to leaderboard? (y/n): ").strip().lower()
                if save == "y":
                    add_score(state)

        elif choice == "3":
            show_leaderboard()

        elif choice == "4":
            print("\nThanks for playing GuessRoyale!")
            break

        else:
            print("Invalid choice. Try again.")

        print()  # blank line after each loop

if __name__ == "__main__":
    main()
