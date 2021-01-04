class WarGames:
    def __init__(self, p1_deck, p2_deck):
        self.p1_deck = p1_deck
        self.p2_deck = p2_deck
        self.winner = None
        self.score = 0

    def play_round(self):
        temp_1, temp_2 = self.p1_deck[0], self.p2_deck[0]
        self.p1_deck.pop(0)
        self.p2_deck.pop(0)
        if temp_1 > temp_2:
            self.p1_deck = self.p1_deck + [temp_1, temp_2]
        else:
            self.p2_deck = self.p2_deck + [temp_2, temp_1]  # no draws

        if len(self.p1_deck) == 0:
            self.winner = "P2"
        if len(self.p2_deck) == 0:
            self.winner = "P1"

    def score_game(self):
        if self.winner is None:
            raise ValueError("no winner is declared yet. game not ready to score")
        win_deck = self.p1_deck if self.winner == "P1" else self.p2_deck
        cards_and_pts = zip(win_deck, reversed(range(1, len(win_deck) + 1)))
        self.score = sum([a * b for a, b in cards_and_pts])
        return self.score

    def play_game(self):
        while self.winner is None:
            self.play_round()
        self.score_game()
        return self.score


def parse(in_file):
    decks = in_file.read().split("\n\n")
    decks = [[int(x) for x in deck.split("\n")[1:]] for deck in decks]
    return decks[0], decks[1]


def p1(war_game):
    return war_game.play_game()


if __name__ == "__main__":
    with open("input.txt") as my_file:
        p1_deck, p2_deck = parse(my_file)

    war_game = WarGames(p1_deck, p2_deck)

    print(f"P1 Answer: {p1(war_game)}")
