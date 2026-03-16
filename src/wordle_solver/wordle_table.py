import numpy as np
from tqdm import tqdm
from wordle import Wordle
from wordle import load_allowed_guesses

# Pre-compute all the guess-solution key pairs in a table
# Keys can be saved as an int from 0 to 242 where 0 is all black and 242 is all green

def convert_color_to_digit(color):
    if color == "k": # black
        return 0
    elif color == "y": # yellow
        return 1
    elif color == "g": # green
        return 2
    else:
        assert(False)

def convert_digit_to_color(digit):
    if (digit == 0):
        return "k"
    elif (digit == 1):
        return "y"
    elif (digit == 2):
        return "g"
    else:
        assert(False)

def convert_wordle_key_to_int(wordle_key):
    key_id = 0
    assert(len(wordle_key) == 5)
    for i in range(5):
        key_id += (3**i)*convert_color_to_digit(wordle_key[i])
    return key_id

def convert_wordle_int_to_key(id):
    return_key = ""
    for i in range(5):
        quotient = np.floor(id/(3**(4-i)))
        return_key += convert_digit_to_color(quotient)
        id -= quotient*(3**(4-i))
    return return_key

def main():
    words = load_allowed_guesses()
    N = len(words)
    key_table = np.zeros((N,N))
    for i in tqdm(range(N), desc="Pre-computing wordle match keys..."):
        wordle_problem = Wordle(words[i])
        for j in range(i,N):
            key_table[i,j] = convert_wordle_key_to_int(wordle_problem.generate_return_key(words[j]))
            key_table[j,i] = key_table[i,j]

    # Save wordle_table to file
    with open("data/wordle_table.npy", "wb") as file:
        np.save(file, key_table)

    with open("data/wordle_table.npy", "rb") as file:
        wordle_table = np.load(file)
        assert(wordle_table.shape == key_table.shape)
    return

if __name__ == "__main__":
    main()