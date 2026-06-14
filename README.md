
# Deep Sea Diver

A browser-playable implementation of the Deep Sea Diver board game, built with a focus on algorithmic efficiency using classical data structures from Donald Knuth's *The Art of Computer Programming*.

🎮 **[Play the game](https://shruthi276.github.io/deep-sea-diver/)** 

---

## What is Deep Sea Diver?

Up to 6 players share a submarine and a single air tank. Each turn, players dive deeper to collect treasure chips — but the more treasure you carry, the faster the air depletes. Make it back to the submarine before the air runs out, or lose everything.

---

## Data structures

### Board — doubly linked list

The board is a linear sequence of 26 treasure chips implemented as a doubly linked list. Each node holds:

- A treasure value
- A pointer to the next chip (deeper into the sea)
- A pointer to the previous chip (toward the submarine)
- A reference to whichever player is currently standing on it

```python
class ChipNode:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None
        self.player = None
```

### Player order — circular linked list

Turn order is maintained as a circular doubly linked list of players. The last player's `next` pointer points back to the first, allowing infinite traversal of turns without index management or bounds checking.

```python
class PlayerNode:
    def __init__(self, name):
        self.name = name
        self.treasure = 0
        self.next = None
        self.prev = None
        self.position = None
        self.returned = False
```

### Jump mechanic — Dancing Links

The core algorithmic insight of this implementation is the use of **Dancing Links** (Knuth, 2000) to handle the jump mechanic.

When a player moves and lands on an occupied chip, they must jump over it without counting it as a step. In a naive array implementation, this requires scanning ahead to find the next free space — a cost that scales with board size and player density.

With Dancing Links, an occupied chip is temporarily removed from the board's traversal in O(1) time using two pointer reassignments:

```python
def remove_chip(chip):
    if chip.prev is not None:
        chip.prev.next = chip.next
    if chip.next is not None:
        chip.next.prev = chip.prev
```

The node is invisible to traversal but its own pointers remain untouched. When the player lands, the chip is restored in O(1) time using those saved pointers:

```python
def restore_chip(chip):
    if chip.prev is not None:
        chip.prev.next = chip
    if chip.next is not None:
        chip.next.prev = chip
```

No searching. No shifting. Just four pointer reassignments total.

---

## Complexity proof

**Claim:** every move in this implementation resolves in at most O(18) operations, regardless of game state.

**Proof:**

Let the constants of this game be fixed:
- Maximum players: **6**
- Maximum spaces moved per turn (2 dice, each 1–3): **6**
- Dancing Links operations per occupied chip encountered: **O(1)**

In the worst case, a player moves 6 spaces and encounters an occupied chip on every space. Each jump costs O(1) via Dancing Links remove and restore. This gives:

```
worst case = 6 spaces × 1 jump check per space + up to 6 pointer operations
           = at most 18 constant-time operations per turn
```

Since both the board size and player count are **fixed constants** in this game, the cost per turn never grows as the game progresses. The formal asymptotic complexity is therefore **O(1) per move** — O(18) is simply a tight constant bound.

**Comparison to naive array implementation:**

In an array-based board, jumping over an occupied space requires scanning forward until a free space is found. With N board spaces and P players, the worst-case jump cost is O(N) per step. Since board size and player count are fixed here, the practical difference is bounded — but the Dancing Links approach is structurally cleaner, eliminates all index arithmetic, and makes the jump mechanic a direct expression of the data structure rather than an algorithmic workaround.

---

## Project structure

```
deep-sea-diver/
├── index.html           # browser game (HTML + JS, no dependencies)
└── deep_sea_diver.py    # Python implementation with full game logic
```

---

## Running the Python version

```bash
python deep_sea_diver.py
```

Supports 2–6 players, 3 dives, terminal input/output. No dependencies beyond the Python standard library.

---

## References

- Knuth, D. E. (2000). *Dancing links*. Millennial Perspectives in Computer Science, 187–214.
- Knuth, D. E. *The Art of Computer Programming*, Vol. 4B — Combinatorial Algorithms.
