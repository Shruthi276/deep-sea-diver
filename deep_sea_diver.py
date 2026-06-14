import random

class ChipNode:
    def __init__(self, value):
        self.value = value      # treasure value on this board space
        self.next = None        # next chip/node in the board
        self.prev = None        # previous chip/node in the board
        self.player = None      # player currently occupying this space


class PlayerNode:
    def __init__(self, name):
        self.name = name            # player's name
        self.treasure = 0           # treasure currently being carried
        self.next = None            # next player in turn order
        self.prev = None            # previous player in turn order
        self.position = None        # ChipNode the player is standing on
        self.returned = False


def build_board(num_chips):
    if num_chips <= 0:
        return None
    head = ChipNode(random.randint(1, 5))  # fixed: min 1 so chips always have value
    current = head
    for _ in range(num_chips - 1):
        new_chip = ChipNode(random.randint(1, 5))
        current.next = new_chip
        new_chip.prev = current
        current = new_chip
    return head


def build_players(names):
    if not names:
        return None
    head = PlayerNode(names[0])
    current = head
    for name in names[1:]:
        new_player = PlayerNode(name)
        current.next = new_player
        new_player.prev = current
        current = new_player
    # Close the circle
    current.next = head
    head.prev = current
    return head


def remove_chip(chip):
    if chip.prev is not None:
        chip.prev.next = chip.next
    if chip.next is not None:
        chip.next.prev = chip.prev


def restore_chip(chip):
    if chip.prev is not None:
        chip.prev.next = chip
    if chip.next is not None:
        chip.next.prev = chip


def move_player(player, board, steps):
    current = player.position
    if current is None:
        current = board
    else:
        current.player = None

    for _ in range(steps):
        if current.next is None:
            break
        next_chip = current.next
        while next_chip is not None and next_chip.player is not None:
            if next_chip.next is None:  # occupied last chip, stop here
                break
            remove_chip(next_chip)
            jumped = next_chip
            current = next_chip.next
            restore_chip(jumped)
            next_chip = current
        if next_chip is None:
            break
        current = next_chip

    player.position = current
    current.player = player


def roll_dice():
    return random.randint(1, 3) + random.randint(1, 3)


def take_turn(player, board, air):
    steps = roll_dice()
    move_player(player, board, steps)

    current_chip = player.position
    choice = input(
        f"{player.name}: (p)ick up {current_chip.value} or (d)rop {player.treasure}? "
    )

    if choice.lower() == 'p':
        player.treasure += current_chip.value
        current_chip.value = 0

    elif choice.lower() == 'd':
        current_chip.value += player.treasure
        player.treasure = 0

    return air


def return_to_sub(player):
    if player.position is not None:
        player.position.player = None
    score = player.treasure
    player.position = None
    player.treasure = 0
    player.returned = True
    return score


def air_runs_out(players):
    # FIX 2: players still on board lose all treasure when air runs out
    current = players
    while True:
        if not current.returned and current.position is not None:
            print(f"{current.name} ran out of air! Lost {current.treasure} treasure.")
            current.position.value += current.treasure  # treasure stays on board
            current.treasure = 0
            current.position.player = None
            current.position = None
            current.returned = True
        current = current.next
        if current == players:
            break


def play_dive(players, board, scores, air=25):
    current_player = players

    active_players = 1
    node = players.next
    while node != players:
        active_players += 1
        node = node.next

    while air > 0 and active_players > 0:

        if not current_player.returned:
            air = take_turn(current_player, board, air)

            choice = input(
                f"{current_player.name}, return to submarine? (y/n): "
            )

            if choice.lower() == 'y':
                score = return_to_sub(current_player)
                scores[current_player.name] += score

                print(
                    f"{current_player.name} returned with "
                    f"{score} treasure."
                )

                active_players -= 1

        current_player = current_player.next

        # completed a full round of turns
        if current_player == players:

            total_carried = 0
            node = players

            while True:
                if not node.returned:
                    total_carried += node.treasure

                node = node.next

                if node == players:
                    break

            air -= total_carried

            print(
                f"Air decreases by {total_carried}. "
                f"Air remaining: {air}"
            )

            if air <= 0:
                air_runs_out(players)
                break

def play_game(names):
    players = build_players(names)
    board = build_board(26)
    scores = {name: 0 for name in names}

    for dive in range(1, 4):
        print(f"\n--- Dive {dive} ---")
        # reset all players for new dive
        current = players
        while True:
            current.returned = False
            current.position = None
            current.treasure = 0
            current = current.next
            if current == players:
                break
        play_dive(players, board, scores)
        print("\nStandings after dive:")
        for name, score in scores.items():
            print(f"{name}: {score}")

    print("\n--- Final Scores ---")
    for name, score in scores.items():
        print(f"{name}: {score}")


if __name__ == "__main__":
    play_game(["Alice", "Bob", "Carlos"])