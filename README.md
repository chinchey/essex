# Essex Card Game

## Usage
To run a game, import the Game class, instantiate and call the 'play' method.
PYTHONPATH should be to the dir containing the essex package

For example:
`from essex.game import Game
game = Game()
game.play()`

Two players are added to the game. They draw three cards each, then compare
hand values according to the calculation rules. This uses all of the associated
classes, however the important operations can also be called individually.

`from essex.game import Game
from essex.cards import Deck

game = Game()
game.draw_cards()
game.compare_hands()

deck = Deck()
deck.shuffle()
deck.sort()`

## Assumptions

- Assuming Python 3
  - Classes need not inherit from `object`
  - `__ne_`_ automatically delegates to `__eq__` so we don’t need to define it.
- Assuming the game is the scope of the project
  - The card and suit classes contain some information and calculations for
     the game that may not apply to other games. We could move this logic to
     individual game classes if needed, but I have not structured it this way
     now, as this is cleaner design and encapsulation for the given
     requirements.
- Computational efficiency is not prioritized
  - Rationale is that we’re operating on a set of 52 items, which has a very
     small chance of changing in the future. Optimising for efficiency will
     likely have a negligible effect on, e.g., sorting this small set, so
     readability and maintenance are better goals
  - `@total_ordering` is slightly less efficient, but produces smaller code and
     fewer errors expanding the various ordering methods
  - Sorting a deck always resolves to the same configuration of cards in the
     same order. We could statically define this for efficiency, but the gain
     is not high (and this exercise probably works better if we do the work).
- The game is used by other classes and code that understand certain usage
  guidelines
  - Card values could be modified by callers. For example, drawing a card,
     then setting card.value = something_else would be allowed, and mess up
     the deck. The assumption is that users know not to do this. If we did not
     trust the users or wanted extra safety at the cost of memory and
     computation, we could return copies of cards, hide card data from external
     use, etc.
- The game is played automatically
  - Since there’s no choice for the players to make along the way, I just have
     the game playing itself out when called. We could prompt the users for each
     draw, but it doesn’t seem to have any impact.
- The game is only intended for 2 players
  - We could pretty easily extend this to start a game for N players, and
     iterate instead of specifying 2 players always.
- Ties result in no winner
- Some of this is tied into randomness. I see a couple of possibilities for
  testing this. We could try to seed the random number generation with a
  consistent value and strictly validate that. Or, we could allow it to run
  more “realistically”, and test using some statistical confidence. That is to
  say that we would do something enough times that we can be 99.xxx% confident
  that it is correct.
  - The tradeoff is that we get more realistic testing with the latter, but
     there is a small (as small as we wish to make it) chance that, e.g.,
     shuffling the deck will randomly return the same ordering as before.
     Depending on our CI/CD system, this may be acceptable or not. Certain test
     docstrings go into this line of thought a bit more
- The requirements ask for a “game” that can do things like shuffle the deck.
  I interpret this to mean that the code I write should allow this, not
  necessarily that the Game class needs to expose this functionality, which I
  have put into the Deck class (for example).
- Pylint warnings - I silenced a pylint warning that I inspected and felt
  the code was justified, but I want to list it here for transparency
  - The Suit class has too-few-public-methods (0). This is essentially an Enum
     class, but with a couple of extra helpful features. I could not add those
     to a class derived from enum.Enum, but preferred this structure.


`Coverage report:
Name                 Stmts   Miss  Cover   Missing
--------------------------------------------------
cards.py                62      0   100%
game.py                 50      0   100%
test/test_cards.py     182      2    99%   322, 340
test/test_game.py      105      0   100%
--------------------------------------------------
TOTAL                  399      2    99%`

The missing coverage from test_cards are two lines that only execute on test
failure.


`~$ python -m pylint essex/

--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)_`

