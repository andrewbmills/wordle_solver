from tkinter import *
from wordle import *
from filter import *

root = Tk()
root.geometry("650x400")
root.configure(background='#403f3e')
current_letter_position = (0,0)

def in_alphabet(letter):
    return(letter in "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")

def convert_letter_to_color_string_background(letter):
    if letter == "k":
        return "#403f3e"
    elif letter == "y":
        return "#aeb21f"
    elif letter == "g":
        return "#7eb46a"
    else:
        return "#403f3e"

class WordleGridGui:
    def __init__(self):
        self.cursor = (0,0)
        self.create_letter_grid()
        self.guess = ""

    def create_letter_grid(self):
        self.letter_grid = []
        for row in range(6):
            for col in range(5):
                self.letter_grid.append(self.create_letter_box(row, col))

    def create_letter_box(self, row=0, col=0):
        letter_box = Label(root, text=" ", width=15, borderwidth=1, relief="solid", background='#403f3e',
            font = ('Helvetica', 30, "bold"), foreground = '#FFFFFF')
        letter_box.place(x = 63*col+10, y = 63*row+10, width = 60, height = 60)
        return letter_box

    def display_letter(self, letter):
        if letter.isupper():
            letter = letter.lower()
        if not self.is_cursor_at_line_end():
            self.letter_grid[self.cursor[1]*5 + self.cursor[0]].configure(text=letter.upper())
            self.guess += letter
            self.move_cursor_to_next_letter()

    def is_cursor_at_line_end(self):
        return (self.cursor[0] >= 5)

    def move_cursor_to_next_letter(self):
        self.cursor = (min(self.cursor[0]+1, 5), self.cursor[1])

    def move_cursor_to_next_word(self):
        self.cursor = (0, min(self.cursor[1]+1, 5))
        self.guess = ""

    def backspace(self):
        self.cursor = (max(0, self.cursor[0]-1), self.cursor[1])
        self.letter_grid[self.cursor[1]*5 + self.cursor[0]].configure(text=" ")
        if len(self.guess):
            self.guess = self.guess[:-1]

    def display_color_key(self, key):
        word_id = self.cursor[1]
        for i in range(len(key)):
            self.letter_grid[word_id*5+i].configure(
                background = convert_letter_to_color_string_background(key[i]))

class WordleGuesserGui():
    def __init__(self):
        self.candidates = []
        self.score = []
        self.create_guess_labels()
    
    def create_guess_labels(self):
        self.guess_labels = []
        for i in range(20):
            self.guess_labels.append(self.create_guess_label(row=i))

    def create_guess_label(self, row=0):
        guess_label = Label(root, text="", width=30, background='#403f3e',
            font = ('Helvetica', 12, "bold"), foreground = '#FFFFFF')
        if row < 10:
            guess_label.place(x=340, y=35*row+20, width=100, height=25)
        else:
            guess_label.place(x=450, y=35*(row-10)+20, width=100, height=25)
        return guess_label

    def display_guess_info_pairs(self, info_guess_pairs):
        info_guess_pairs = np.sort(info_guess_pairs, order="information")
        N_guesses = len(info_guess_pairs)
        self.clear_guess_display()
        for i in range(min(len(info_guess_pairs), 20)):
            guess = info_guess_pairs[N_guesses-i-1][0]
            info_gain = info_guess_pairs[N_guesses-i-1][1]
            guess_gain_string = ("%s   %0.2f" % (guess.decode("utf-8"), info_gain))
            self.guess_labels[i].configure(text=guess_gain_string)
            
    def clear_guess_display(self):
        for label in self.guess_labels:
            label.configure(text="")

wordle_gui = WordleGridGui()
wordle_guesser_gui = WordleGuesserGui()
wordle_puzzle = Wordle(select_random_word_from_bank())
wordle_guesser = Filter()

def on_keyboard_event(event):
    if in_alphabet(event.char):
        wordle_gui.display_letter(event.char)
    elif (event.keysym == "BackSpace"):
        wordle_gui.backspace()

def on_return_press(entry):
    guess = wordle_gui.guess
    if (wordle_puzzle.is_guess_allowed(guess)):
        key = wordle_puzzle.submit_guess(guess)
        wordle_gui.display_color_key(key)
        wordle_gui.move_cursor_to_next_word()
        wordle_guesser_gui.display_guess_info_pairs(wordle_guesser.calculate_info_gains(wordle_puzzle._guesses, wordle_puzzle._return_keys))

root.bind("<Key>", on_keyboard_event)
root.bind("<Return>", on_return_press)

def main():
    root.mainloop()
    return

if __name__ == "__main__":
    main()