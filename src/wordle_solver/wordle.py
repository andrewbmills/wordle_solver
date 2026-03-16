import random
import numpy as np

class PrintColors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'

# Letter match enums
class Match:
    INCORRECT = "k"
    CORRECT_LETTER_WRONG_POSITION = "y"
    CORRECT_LETTER_CORRECT_POSITION = "g"

def select_random_word_from_bank():
    with open("data/wordle-answers-alphabetical.txt") as file:
        words = file.readlines()
        word = random.choice(words)
        return word[:-1] # strip the trailing new line

def load_allowed_guesses():
    allowed_guesses = []
    with open("data/wordle-allowed-guesses.txt") as file:
        words = file.readlines()
        for word in words:
            allowed_guesses.append(word[:-1])
    return allowed_guesses

class Wordle:
    def __init__(self, solution):
        self._solution = solution
        self._num_letters_in_solution = len(solution)
        self._guesses = []
        self._return_keys = []
        self._solved = False
        self._allowed_guesses = load_allowed_guesses()
        return
           
    def run(self):
        print("\n-----\nWORDLE\n-----\n")
        while not self.is_solved():
            guess = input()
            if (len(guess) != self._num_letters_in_solution):
                print("Submissions must be %d letters long." % self._num_letters_in_solution)
                continue
            if not self.is_guess_allowed(guess):
                print("Please submit a valid word.")
                continue
            key = self.submit_guess(guess)
            if (len(self._guesses) == 6):
                print("Too many guesses, the solution was %s!" % self._solution)
                break

    def is_solved(self):
        return self._solved

    def is_guess_allowed(self, guess):
        candidate_match_id = np.searchsorted(self._allowed_guesses, guess, side="right")
        return self._allowed_guesses[candidate_match_id-1] == guess

    def submit_guess(self, guess):
        key = self.generate_return_key(guess)
        self._guesses.append(guess)
        self._return_keys.append(key)
        self.display_return_key(key, guess)
        if (guess == self._solution):
            print("SOLVED!")
            self._solved = True
        return key

    def display_return_key(self, key, guess):
        display_string = ""
        for i in range(self._num_letters_in_solution):
            if key[i] == Match.CORRECT_LETTER_CORRECT_POSITION:
                display_string += (f"{PrintColors.GREEN}%s{PrintColors.END}" % guess[i])
            if key[i] == Match.CORRECT_LETTER_WRONG_POSITION:
                display_string += (f"{PrintColors.YELLOW}%s{PrintColors.END}" % guess[i])
            if key[i] == Match.INCORRECT:
                display_string += guess[i]
        print(display_string)

    def generate_return_key(self, guess):
        if len(guess) != self._num_letters_in_solution:
            return self.get_blank_return_key()
        key = self.check_guess_against_solution(guess)
        return key

    def get_blank_return_key(self):
        return "k"*self._num_letters_in_solution

    def check_guess_against_solution(self, guess):
        key = ""
        for i in range(self._num_letters_in_solution):
            letter = guess[i]
            if (letter == self._solution[i]):
                key += str(Match.CORRECT_LETTER_CORRECT_POSITION)
            elif (letter in self._solution):
                # Make sure the other instance isn't green
                already_green_count = self.count_other_greens_of_the_same_letter(guess, i)
                # Make sure there aren't more duplicate yellow letters in the guess than in the solution
                previous_yellow_count = self.count_previous_yellows_of_the_same_letter(guess, i)
                if (already_green_count >= self._solution.count(letter)) or (previous_yellow_count >= self._solution.count(letter)):
                    key += str(Match.INCORRECT)
                else:
                    key += str(Match.CORRECT_LETTER_WRONG_POSITION)
            else:
                key += str(Match.INCORRECT)
        return key

    def count_other_greens_of_the_same_letter(self, guess, letter_id):
        green_count = 0
        for j in range(self._num_letters_in_solution):
            if (guess[j] == guess[letter_id]) and (j != letter_id) and (guess[j] == self._solution[j]):
                green_count += 1
        return green_count

    def count_previous_yellows_of_the_same_letter(self, guess, letter_id):
        yellow_count = 0
        for j in range(letter_id):
            if (guess[j] == guess[letter_id]) and (guess[j] != self._solution[j]):
                yellow_count += 1
        return yellow_count

def main():
    # Read in word bank
    wordle_puzzle = Wordle(select_random_word_from_bank())
    wordle_puzzle.run()
    return

if __name__ == "__main__":
    main()