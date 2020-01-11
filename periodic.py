#!/usr/bin/env python3

import argparse
from periodic.table import PeriodicTable, PeriodicTableError
from periodic.layouts import layouts


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
        help="display the entire periodic table"
    )
    parser.add_argument(
        "-l", "--layout", type=str,
        help="specify the table layout to render",
        choices=[layout for layout in layouts],
        default="standard"
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
                print(f"No solution found for '{word}'.")
                exit(1)

            if len(symbols):
                symbols.append(" ")

            symbols += solutions[0]

        periodic.render_symbols(symbols)

    if args.table:
        periodic.render_table(show_grid=args.grid, layout=args.layout)


if __name__ == "__main__":
    main()
