from wordle import *

def main():
    # Read in word bank
    wordle_puzzle = Wordle(select_random_word_from_bank())
    # Run CLI for wordle
    wordle_puzzle.run()
    return

if __name__ == "__main__":
    main()