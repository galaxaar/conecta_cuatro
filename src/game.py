from enum import Enum, auto
from player import Player, HumanPlayer
from match import Match
from board import Board

try:
    import pyfiglet
    _PYFIGLET = True
except ImportError:
    _PYFIGLET = False


class RoundType(Enum):
    COMPUTER_VS_HUMAN = auto()
    COMPUTER_VS_COMPUTER = auto()


class Game():

    def __init__(self):
        self.round_type = None
        self.match = None
        self.board = Board()

    def start(self):
        self._print_logo()
        self._configure_by_user()
        self._run()

    def _print_logo(self):
        if _PYFIGLET:
            logo = pyfiglet.Figlet(font="univers")
            print(logo.renderText("Conecta Cuatro"))
        else:
            print("=" * 40)
            print("       C O N E C T A   C U A T R O")
            print("=" * 40)
        print()

    def _configure_by_user(self):
        self.round_type = self._get_round_type()
        self.match = self._make_match()
        self.board = Board()

    def _get_round_type(self):
        print("  Elige el tipo de partida:")
        print("  1) IA vs IA")
        print("  2) IA vs Humano")
        answer = ""
        while answer not in ("1", "2"):
            answer = input("  Escribe 1 o 2: ").strip()
        return RoundType.COMPUTER_VS_COMPUTER if answer == "1" else RoundType.COMPUTER_VS_HUMAN

    def _make_match(self):
        if self.round_type == RoundType.COMPUTER_VS_COMPUTER:
            p1 = Player("Buzz")
            p2 = Player("Zurg")
        else:
            p1 = HumanPlayer(name=input("  Nombre del jugador humano: ").strip() or "Jugador")
            p2 = Player("HAL 9000")
        return Match(p1, p2)

    def _run(self):
        print("\n  ¡Comienza la partida!\n")
        self._print_board()

        while True:
            player = self.match.next_player
            print(f"  Turno de {player.name} ({player._char.upper()})")

            player.play(self.board)
            self._print_board()

            if self.board.is_victory(player._char):
                print(f"\n  🎉  ¡{player.name} gana!\n")
                break

            if self._is_draw():
                print("\n  🤝  ¡Empate! El tablero está lleno.\n")
                break

        self._ask_rematch()

    def _print_board(self):
        from settings import BOARD_COLUMNS
        # cabecera con números de columna
        header = "  " + "".join(f" {i} " for i in range(BOARD_COLUMNS))
        print(header)
        print("  " + "-" * (BOARD_COLUMNS * 3))
        print(self.board.print_board(self.board._columns))

    def _is_draw(self):
        from settings import BOARD_COLUMNS
        return all(self.board.is_full(c) for c in range(BOARD_COLUMNS))

    def _ask_rematch(self):
        answer = input("  ¿Jugar otra vez? (s/n): ").strip().lower()
        if answer == "s":
            self._configure_by_user()
            self._run()
        else:
            print("\n  ¡Hasta la próxima!\n")
