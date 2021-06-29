import json
import random
import os


def cls():
    os.system('cls' if os.name == 'nt' else 'clear')


def computer_pick_word():
    with open("words.json") as word_data:
        words_dict = json.load(word_data)
    word_list = words_dict['data']
    return random.choice(word_list)


def generate_template_word(guessed_word):
    count = len(guessed_word)
    return "-" * count


def display_prompt(t_word, guesses, already_guessed):
    cls()
    print(f"Computer guessed a word. Guesses left: {7-guesses}\n")
    print(t_word)
    print(f"Already guessed letters: {already_guessed}")
    letter = input("\nGuess a letter? ")
    return letter


def validate(letter, already_guessed):
    return len(letter) == 1 and letter.lower()[0].isalpha() and (letter.lower()[0] not in already_guessed)


def update_template_word(letter, word, t_word):
    template_list = list(t_word)
    for i, c in enumerate(word):
        if c == letter:
            template_list[i] = letter

    return ''.join(template_list)


def game_start():
    guesses = 0
    already_guessed = []
    word = computer_pick_word()
    template_word = generate_template_word(word)

    while True:
        guessed_letter = display_prompt(template_word, guesses, already_guessed)
        if validate(guessed_letter, already_guessed):
            already_guessed.append(guessed_letter)

            if guessed_letter in word:
                template_word = update_template_word(guessed_letter, word, template_word)
                if template_word == word:
                    print("You've won!!!")
                    break
            else:
                guesses += 1
                if guesses == 7:
                    print("Game Over!")
                    print(f"Word was {word}")
                    os.system("pause")
                    break
        else:
            print("Wrong input!")
            os.system("pause")


cls()
while True:
    game_start()
    cls()
