import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Enforce node consistency for every variable in self.domains (whole crossword)
        for variable in self.domains:

            # Remove values from domain of variable if the value length does not match the variable length
            to_be_removed = set()
            for value in self.domains[variable]:
                if len(value) != variable.length:
                    to_be_removed.add(value)

            for element in to_be_removed:
                self.domains[variable].remove(element)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Initially set revised to False since no changes were made
        revised = False

        # Search for overlaps (if there are any)
        overlap = self.crossword.overlaps[(x, y)]

        # Return False if there are no overlaps, since no changes were made
        if overlap == None:
            return revised
        # Else if there are overlaps, ensure that x is arc consistent with y
        else:
            # Split overlap into the respective x and y positions
            x_overlap, y_overlap = overlap

            # From y's domain, generate set of possible letters that the letter in x can match
            tmpset = set()
            for word_y in self.domains[y]:
                tmpset.add(word_y[y_overlap])

            # Generate set of words in x's domain that prevent x from being arc consistent with y
            # Update revised to True if changes are going to be made to x's domain
            to_be_removed = set()
            for word_x in self.domains[x]:
                if word_x[x_overlap] not in tmpset:
                    to_be_removed.add(word_x)
                    revised = True

            # Eliminate words in variable x's domain, such that x is arc consistent with y
            for word in to_be_removed:
                self.domains[x].remove(word)

        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Start with an initial queue of all the arcs in the problem if arcs == None
        if arcs == None:
            arcs = []
            for variable_x in self.domains:
                for variable_y in self.domains:
                    if variable_x != variable_y:
                        arcs.append((variable_x, variable_y))

        # While queue non-empty
        while len(arcs) != 0:
            # Dequeue a tuple from arcs
            x, y = arcs[0]
            arcs = arcs[1:]

            # Call revise function on (x, y)
            if self.revise(x, y):
                # Return False if size of variable_x domain is 0
                if len(self.domains[x]) == 0:
                    return False
                # For each variable_z in variable_x.neighbors - variable_y, enqueue(z, x)
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arcs.append((z, x))

        # Return True if arc consistency is enforced and no domains are empty
        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """

        # Iterate over each variable in the crossword
        for variable in self.crossword.variables:

            # Return False if any of the crossword variables are still not in the assignment
            if variable not in assignment:
                return False

        # Return True if assignment is complete
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        # Ensure that all values are distinct, and of the correct length
        variable_set = set()
        for variable in assignment:
            variable_set.add(assignment[variable])

            # Ensure that every value is the correct length
            if variable.length != len(assignment[variable]):
                return False

        # If the same word is used for more than one variable (values are not distinct), return False
        if len(variable_set) != len(assignment):
            return False

        # Ensure that there are no conflicts between neighbouring variables
        for varx in assignment:
            for vary in assignment:

                # Skip the check if varx and vary are the same variable
                if varx == vary:
                    continue

                # Search for overlaps (if there are any)
                overlap = self.crossword.overlaps[(varx, vary)]

                # continue with the next (varx, vary) if there are no overlaps, since there would be no conflicts
                if overlap == None:
                    continue

                # Else if there are overlaps, ensure that there are no conflicts
                else:
                    # Split "overlap" into the respective x and y positions
                    x_overlap, y_overlap = overlap

                    if assignment[varx][x_overlap] != assignment[vary][y_overlap]:
                        return False

        # Return True if all conditions are satisfied
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        if len(list(self.domains[var])) == 0:
            return []

        # Obtain list of neighbours
        neighbour_list = list(self.crossword.neighbors(var))

        # Remove neighbour variables that are already in assignment from neighbour_list
        for neighbourr in neighbour_list:
            if neighbourr in assignment:
                neighbour_list.remove(neighbourr)

        # Create unordered list of values in var's domain and their respective number of possible choices eliminated
        domain_values_unordered = []
        for valuee in self.domains[var]:
            domain_values_unordered.append([valuee, 0])

        # Check for possible collisions between each value in var's domain and
        # the possible values in neighbouring variables' domain
        for value in domain_values_unordered:
            for neighbour in neighbour_list:
                overlap_v, overlap_n = self.crossword.overlaps[(var, neighbour)]
                original_letter = value[0][overlap_v]

                for neighbour_value in self.domains[neighbour]:
                    neighbour_letter = neighbour_value[overlap_n]
                    if original_letter != neighbour_letter:
                        value[1] += 1

        # Sort domain values according to the no. of possible choices eliminated (ascending), keeping only the word
        domain_values_sorted = []
        for domain_value in sorted(domain_values_unordered, key=lambda domain_value_list: domain_value_list[1]):
            domain_values_sorted.append(domain_value[0])

        # Return sorted list of values in the domain of var
        return domain_values_sorted

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Find set of unassigned variables not already part of the assignment
        unassigned = set()
        for variable in self.crossword.variables:
            if variable not in assignment:
                unassigned.add(variable)

        # Find set of variable(s) with minimum number of remaining values in its domain
        min_length = 999999999
        min_length_variables = set()

        for unassigned_variable in unassigned:
            # Find number of remaining values in the domain of each unassigned variable
            unassigned_variable_length = len(self.domains[unassigned_variable])

            # If unassigned variable has a lower number of remaining values than the current minimum,
            # Set min_length to be the new lowest number and
            # Empty the set min_length_variables, keeping only the new unassigned variable
            if unassigned_variable_length < min_length:
                min_length = unassigned_variable_length
                min_length_variables = {unassigned_variable}

            # Else if unassigned variable has the same number of remaining values as the current minimum,
            # Add the new unassigned variable to the set min_length_variables
            elif unassigned_variable_length == min_length:
                min_length_variables.add(unassigned_variable)

        # Return variable with minimum number of remaining values in its domain (if there is no tie)
        if len(min_length_variables) == 1:
            return list(min_length_variables)[0]

        # Else if there is a tie, choose the variable with the highest degree
        else:
            highest_degree = -1
            highest_degree_variables = set()

            # Iterate over all the variables
            for var in min_length_variables:

                # Find number of neighbours that each variable has
                neighbour_count = len(self.crossword.neighbors(var))

                if neighbour_count > highest_degree:
                    highest_degree = neighbour_count
                    highest_degree_variables = {var}
                elif neighbour_count == highest_degree:
                    highest_degree_variables.add(var)

            # If there are no ties, return variable with highest degree
            if len(highest_degree_variables) == 1:
                return list(highest_degree_variables)[0]

            # If there are still ties, return any of the tied variables
            else:
                return list(highest_degree_variables)[0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Return assignment if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):

            # add {var = value} to assignment and check if value is consistent with assignment
            assignment[var] = value
            if self.consistent(assignment):
                # Continue with backtracking search if value is consistent with assignment
                result = self.backtrack(assignment)

                # if result != failure, return result
                if result != None:
                    return result

            # remove {var = value} from assignment
            assignment.pop(var)

        # return failure
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
