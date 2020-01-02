#!/usr/bin/env python3

import argparse
import json
from colored import fg, bg, attr


class PeriodicTableError(Exception):
    """Periodic Table exceptions."""

    pass


class PeriodicTable:
    """Periodic Table."""

    def __init__(self, **kwargs):
        self.color = kwargs["color"] if "color" in kwargs else False
        self.width = kwargs["width"] if "width" in kwargs else None

        with open('data/elements.json') as data_file:
            self.elements = json.load(data_file)

        with open('data/layout.txt') as layout_file:
            self.layout = layout_file.read()

    def colorize_symbol(self, symbol, show_number=False):
        """Get a pretty version of a symbol or number."""

        if symbol == " ":
            return "    "

        symbol = symbol.lower().capitalize()

        text = f" {symbol:2} "

        if show_number:
            number = str(self.elements[symbol]["number"])
            text = f" {number:3}"

        if self.color:
            element_color = self.elements[symbol]["color"]
            contrast_color = "white"

            if element_color == "yellow":
                contrast_color = "yellow_1"

            background_color = bg(element_color)
            text_color = fg(contrast_color) if show_number else fg("black")
            reset = attr("reset")

            text = f"{background_color}{text_color}{text}{reset}"

        return text


    def render_info(self, symbol):
        """Print summary information for a particular element."""

        if symbol not in self.elements:
            raise PeriodicTableError(f"Symbol not found in the periodic table")

        if self.color:
            self.render_symbols([symbol])

        element = self.elements[symbol]

        print(f"Symbol: {symbol}")
        print(f"Name: {element['name']}")

        if "origin" in element:
            print(f"Origin of name: {element['origin']}")

        print(f"Series: {element['series'].capitalize()}")
        print(f"Atomic number: {element['number']}")
        print(f"Period: {element['period']}")

        if "group" in element:
            print(f"Group: {element['group']}")

    def render_table(self, show_grid=False):
        """Print the classic periodic table using current output
        configuration."""

        if show_grid:
            headers = [str(group).ljust(3) for group in range(1, 19)]
            print("    " + " ".join(headers))
            print()

        period = 1

        for line in self.layout.splitlines():
            line = f" {line} "
            is_top_line = period == int(period)
            period += 0.5

            for symbol in self.elements:
                replacement = self.colorize_symbol(symbol, is_top_line)

                line = line.replace(f" {symbol:2} ", replacement)

            if show_grid:
                header = int(period) if period < 8 and is_top_line else ' '
                line = f"{header}  {line}"

            if line.strip()[:2] == "* ":
                print()

            if self.color:
                reset = attr('reset')

                for symbol in self.elements:
                    color = bg(self.elements[symbol]["color"])
                    pattern = f" {symbol:2} "
                    line = line.replace(pattern, f"{color}{pattern}{reset}")

            print(line)

    def render_symbols(self, symbols):
        """Print a list of symbols using current output configuration."""

        columns = int(self.width / 4)
        lines = [symbols[i:i + columns] for i in range(0, len(symbols), columns)]

        for line in lines:
            top = [self.colorize_symbol(symbol, show_number=True) for symbol in line]
            bottom = [self.colorize_symbol(symbol) for symbol in line]

            print("".join(top))
            print("".join(bottom))

    def get_solutions(self, word, recursing=False):
        """Find all permutations that can spell a word."""

        if not recursing:
            self.stack = []
            self.results = []
            word = word.lower()

        for symbol in self.elements:
            symbol = symbol.lower()

            if symbol == word:
                if self.stack not in self.results:
                    self.stack.append(symbol)
                    self.results.append(self.stack)
                    self.stack = self.stack[:-1]

                continue

            if symbol == word[:len(symbol)]:
                self.stack.append(symbol)
                self.get_solutions(word[len(symbol):], recursing=True)

        self.stack = self.stack[:-1]

        return sorted(self.results, key=self.get_solution_ranking)

    def get_solution_ranking(self, solution):
        """Score a solution based on length and number of repeated symbols."""

        return len(solution) + 100 * (len(solution) - len(set(solution)))

    def get_symbol_from_atomic_number(self, number):
        """Translate an atomic number into an element's symbol."""

        number = int(number)
        elements = self.elements
        matches = [e for e in elements if elements[e]["number"] == number]

        return matches[0] if matches else None


def main():
    """Periodic table word confabulator"""

    table_columns = 74
    grid_columns = 4

    parser = argparse.ArgumentParser(description=main.__doc__)

    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "-i", "--info", type=str,
        help="show more info about a particular element", metavar=("ELEMENT")
    )
    parser.add_argument("-w", "--word", type=str, help="a word to render")
    group.add_argument(
        "-v", "--variations", action="store_true",
        help="display all variations, rather than just the best match."
    )
    group.add_argument("-p", "--phrase", type=str, help="a phrase to render")
    parser.add_argument(
        "-g", "--grid", action="store_true",
        help="show the grid"
    )
    parser.add_argument(
        "-t", "--table", action="store_true",
        help="display the traditional layout for the periodic table"
    )
    parser.add_argument(
        "-c", "--color", action="store_true",
        help="display each element using its color"
    )
    parser.add_argument(
        "--width", type=int, default=80,
        help="number of character columns to display on one line"
    )

    args = parser.parse_args()

    if args.grid and args.table and args.width < table_columns + grid_columns:
        print(f"Terminal width must be > {table_columns + grid_columns}.")
        exit(1)

    if args.table and args.width < table_columns:
        print(f"Terminal width must be > {table_columns}.")
        exit(1)

    periodic = PeriodicTable(**vars(args))

    if args.info:
        symbol = args.info.lower().capitalize()

        if symbol.isnumeric():
            symbol = periodic.get_symbol_from_atomic_number(symbol)

        try:
            periodic.render_info(symbol)
        except PeriodicTableError as exception:
            print(exception)
            exit(1)

    if args.word:
        solutions = periodic.get_solutions(args.word)

        if not solutions:
            print(f"No solutions found for '{args.word}'.")
            exit(1)

        if not args.variations:
            solutions = solutions[:1]

        for solution in solutions:
            periodic.render_symbols(solution)

    if args.phrase:
        symbols = []

        for word in args.phrase.split():
            solutions = periodic.get_solutions(word)

            if not solutions:
                print(f"No solution found for .{word}'.")
                exit(1)

            if len(symbols):
                symbols.append(" ")

            symbols += solutions[0]

        periodic.render_symbols(symbols)

    if args.table:
        periodic.render_table(show_grid=args.grid)


if __name__ == "__main__":
    main()


