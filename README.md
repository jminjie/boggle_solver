# Boggle solver

## Usage

`python3.7 boggle_solver`

Example 5x5 grid:

`e i h v r in o y a m r l e u r s n s o c p e n i b`

Should also work with other python versions > 3.

(More example boards in the directory.)

## Options
- Change the dictionary by editing the value of DICT.
`20k.txt` is a list of the 20k most common English words (missing many real words).
`words_alpha` is a very comprehensive list of all English words (includes many words
we wouldn't think of as real words).
`scrabble.txt` is the Scrabble dictionary, seems to be the best medium ground.

## TODO
- Take DICT as a flag, set to scrabble by default
