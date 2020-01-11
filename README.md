# Pyriodic

Periodic table word thinger. In Python.

This is a toy to display the periodic table of the elements, or information
about a specific element.

## Features

* Display the standard layout (or wide version) of the Periodic Table of the
  Elements, with or without grid markings, in mono or in colour.
* Render a word or phrase using element symbols
* Provide alternate solutions for rendering a word using only element symbols

## Flashy screenies

The table rendered in colour, with grid, produced with `periodic.py -tcg`

![The periodic table of the elements](/images/table-cg.png)

A selection of words, produced with `periodic.py -cp "chocolate bacon counterespionage" --width=100`

![The words "chocolate", "bacon" and "counterespionage" rendered in colourful element symbols](/images/chocolate-bacon-counterespionage.png)

## Help

```
usage: periodic.py [-h] [-i ELEMENT] [-w WORD] [-v | -p PHRASE] [-g] [-t] [-l {standard,standard32}] [-c] [--width WIDTH]

Periodic table word confabulator

optional arguments:
  -h, --help            show this help message and exit
  -i ELEMENT, --info ELEMENT
                        show more info about a particular element
  -w WORD, --word WORD  a word to render
  -v, --variations      display all variations, rather than just the best match.
  -p PHRASE, --phrase PHRASE
                        a phrase to render
  -g, --grid            show the grid
  -t, --table           display the entire periodic table
  -l {standard,standard32}, --layout {standard,standard32}
                        specify the table layout to render
  -c, --color           display each element using its color
  --width WIDTH         number of character columns to display on one line
```

## Installation

```sh
pip install -r requirements.txt
```

## Dependencies

* Python 3
* colored

## Credits

Element name information was cribbed from Wikipedia.
