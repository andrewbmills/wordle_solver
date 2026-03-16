import numpy as np
from wordle import load_allowed_guesses
from wordle_table import convert_wordle_key_to_int, convert_wordle_int_to_key
from tqdm import tqdm

def load_wordle_table_from_file():
    with open("data/wordle_table.npy", "rb") as file:
        wordle_table = np.load(file)
    return wordle_table

class Filter:
    def __init__(self):
        self._wordle_table = load_wordle_table_from_file()
        self._words = np.array(load_allowed_guesses())
        self.n_words = len(self._words)

    def filter_word_list_with_guess_key_pairs(self, guesses, return_keys):
        filter_mask = np.ones(self.n_words)
        for (guess, key) in zip(guesses, return_keys):
            filter_mask = np.multiply(filter_mask, self.compute_guess_word_mask(guess, key))
        return self._words[np.nonzero(filter_mask)], filter_mask

    def compute_guess_word_mask(self, guess, return_key):
        key_int = convert_wordle_key_to_int(return_key)
        guess_id = self.get_guess_id(guess)
        valid_word_mask = (self._wordle_table[:, guess_id] == key_int)
        return valid_word_mask # binary mask of valid words

    def get_guess_id(self, guess):
        guess_id = np.searchsorted(self._words, guess, side="right") - 1
        if (self._words[guess_id] == guess):
            return guess_id
        else:
            return -1

    def calculate_info_gains(self, guesses, keys):
        words_remaining, filter_mask = self.filter_word_list_with_guess_key_pairs(guesses, keys)
        info_gains = []
        for i in tqdm(range(len(words_remaining)), desc="Computing info gains for guesses remaining..."):
        # for i in tqdm(range(20), desc="Computing info gains for guesses remaining..."):
            candidate_guess = words_remaining[i]
            information_expected_value = self.calculate_expected_information_from_guess(filter_mask, candidate_guess)
            info_gains.append(information_expected_value)
        guess_information_dictionary = []
        for (guess, information_gain) in zip(words_remaining, info_gains):
            guess_information_dictionary.append((guess, information_gain))
        return np.array(guess_information_dictionary, dtype=[('name', 'S10'), ('information', float)])
    
    def calculate_expected_information_from_guess(self, words_remaining_mask, guess):
        num_words_remaining = np.sum(words_remaining_mask)
        num_words_remaining_by_key = []
        for i in range(243):
            return_key = convert_wordle_int_to_key(i)
            guess_words_remaining_mask = self.compute_guess_word_mask(guess, return_key)
            num_words_after_guess_and_key = np.sum(np.multiply(guess_words_remaining_mask, words_remaining_mask))
            if num_words_after_guess_and_key:
                num_words_remaining_by_key.append(num_words_after_guess_and_key)
        return self.calculate_information(num_words_remaining, num_words_remaining_by_key)

    def calculate_information(self, n_words_before, n_words_after_each_key):
        information_expected_value = 0
        for n_words_remaining in n_words_after_each_key:
            probability_of_key = n_words_remaining/n_words_before
            information = -np.log2(probability_of_key) # in bits of information
            information_expected_value += information*probability_of_key
        return information_expected_value

def main():
    guesses = []
    return_keys = []
    guesses = ["amuse", "lassy", "floss", "fleet", "boast", "flier", "spilt", "stilt"]
    return_keys = ["kykkk", "kkkkk", "kkkkk", "kkkkg", "kkkkg", "kkykk", "kkykg", "kkykg"]
    wordle_filter = Filter()
    information_gains = np.sort(wordle_filter.calculate_info_gains(guesses, return_keys), order='information')
    N_guesses = len(information_gains)
    for i in range(len(information_gains)):
        guess = information_gains[N_guesses-i-1][0]
        info_gain = information_gains[N_guesses-i-1][1]
        print("Guess: %s, information: %0.2f bits" % (guess.decode("utf-8"), info_gain))
        if (i == 20):
            break
    return

if __name__ == "__main__":
    main()