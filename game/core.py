from config import DIFFICULTY_LEVELS, MAX_LIVES


class GameState:
    """
    Holds the current state of a game session.
    """

    def __init__(self, player_name: str, mode: str, difficulty_key: str):
        self.player_name = player_name
        self.mode = mode            # "Number" or "Word"
        self.difficulty_key = difficulty_key
        self.difficulty = DIFFICULTY_LEVELS[difficulty_key]
        self.lives = MAX_LIVES
        self.score = 0

    @property
    def difficulty_name(self) -> str:
        return self.difficulty["name"]


def show_welcome_screen():
    print("=" * 40)
    print("        WELCOME TO GUESSROYALE       ")
    print("=" * 40)
    print("A multi-mode guessing arena with")
    print("lives, difficulty levels, and revival mini-games.")
    print()


def ask_player_name() -> str:
    name = input("Enter your player name: ").strip()
    if not name:
        name = "Anonymous"
    return name


def choose_difficulty() -> str:
    print("\nChoose difficulty:")
    for key, info in DIFFICULTY_LEVELS.items():
        print(f"  {key}. {info['name']}")
    while True:
        choice = input("Enter 1 / 2 / 3: ").strip()
        if choice in DIFFICULTY_LEVELS:
            return choice
        print("Invalid choice. Try again.")
