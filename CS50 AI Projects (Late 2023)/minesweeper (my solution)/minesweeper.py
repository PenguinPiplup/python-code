import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        confirmed_mines = set()
        for cella in self.cells:
            if cella in MinesweeperAI.mines:
                confirmed_mines.add(cella)
        return confirmed_mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        confirmed_safes = set()
        for cella in self.cells:
            if cella in MinesweeperAI.safes:
                confirmed_safes.add(cella)
        return confirmed_safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # If cell in sentence
        if cell in self.cells:
            # Remove mine from sentence
            self.cells.remove(cell)
            # Update count
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # If cell in sentence
        if cell in self.cells:
            # Remove safe cell from sentence
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) Mark cell as move that has been made
        self.moves_made.add(cell)

        # 2) Mark cell as safe
        self.mark_safe(cell)

        # 3) Add new sentence to AI's knowledge base
        # Obtain set of neighbouring cells
        cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Skip the cell that we took as input
                if (i, j) == cell:
                    continue

                # Skip cell if it is already known to be safe
                elif (i, j) in self.safes:
                    continue

                # Skip cell and minus one from count if it is already known to be a mine
                elif (i, j) in self.mines:
                    count -= 1
                    continue

                # Add cell to the set if cell lies within the game's boundaries
                if 0 <= i < self.height and 0 <= j < self.width:
                    cells.add((i, j))

        new_sentence = Sentence(cells, count)
        self.knowledge.append(new_sentence)

        # Run steps 4 and 5 until no additional knowledge can be added
        while self.add_additional_knowledge():
            continue

        return

    def add_additional_knowledge(self):

        counter = 0
        additional_safes = set()
        additional_mines = set()

        # 4) Mark additional cells as safe or mines
        for sentence in self.knowledge:
            # Mark all cells in sentence as safe if mine-count of sentence is 0
            if sentence.count == 0:
                for cella in sentence.cells:
                    if cella not in self.safes:
                        additional_safes.add(cella)
                        counter += 1

            # Mark all cells in sentence as mines if mine-count of sentence matches the number of cells in sentence
            elif sentence.count == len(sentence.cells):
                for cella in sentence.cells:
                    if cella not in self.mines:
                        additional_mines.add(cella)
                        counter += 1

        if len(additional_safes) > 0:
            for cella in additional_safes:
                self.mark_safe(cella)

        if len(additional_mines) > 0:
            for cella in additional_mines:
                self.mark_mine(cella)

        # 5) Add new sentences to AI's knowledge base if they can be inferred
        inferred_sentences = []
        for sentence_a in self.knowledge:
            for sentence_b in self.knowledge:
                # If sentence_a is a subset of sentence_b and sentence_a is not an empty sentence
                if sentence_a.cells < sentence_b.cells and len(sentence_a.cells) > 0:
                    cell_difference = sentence_b.cells - sentence_a.cells
                    count_difference = sentence_b.count - sentence_a.count
                    sentence_c = Sentence(cell_difference, count_difference)
                    inferred_sentences.append(sentence_c)

        for sentenc in inferred_sentences:
            self.knowledge.append(sentenc)
            counter += 1

        # Loop this function again if additional knowledge was added
        if counter > 0:
            return True
        else:
            return False

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Generate set of cells that have not been chosen and are not known to be mines
        not_chosen = set()
        for i in range(self.height):
            for j in range(self.width):
                if (i, j) not in self.moves_made and (i, j) not in self.mines:
                    not_chosen.add((i, j))

        # Calculate number of cells that have not been chosen and are not known to be mines
        set_length = len(not_chosen)
        if set_length == 0:
            return None

        # Choose a random cell in not_chosen
        not_chosen_list = list(not_chosen)
        return not_chosen_list[random.randint(0, set_length - 1)]
