import random

ATTEMPTS = 6 #number of attempts given per one round
FILE_NAME = 'wordle_list.txt'
WORD_LENGTH = 5

def main():
    #print out an intro
    print("Guess the Wordle in 6 tries.", "Each guess must be a valid 5-letter word.",
          "The color of the tiles will change to show how close your guess was to the word", sep = '\n')

# creates a list of words from the provided file
    words_list = get_words_from_file()

# get a random word from a list and make it uppercase
    answer = select_word(words_list)
    play_game(words_list, answer)


def play_game(dictionary, answer):
    already_guessed = []    # list to store words user already tried
    rounds_results = []  # list to store all rounds feedback

    print("round 1/6")
    user_guess = ask_user_guess(dictionary, already_guessed).upper()
    already_guessed.append(user_guess)
    user_attempt = 1

    ''' if user's guess is not correct and number of guesses made is less than 6,
    check if there are correctly guessed letters and provides user with feedback
    if user used the last attempt and the guess is wrong - print out that game is over and correct answer
    '''
    while user_guess != answer:
        feedback = give_feedback(answer, user_guess)
        rounds_results.append(feedback)

        print('') #print empty line
        if user_attempt < ATTEMPTS:
            user_attempt += 1
            print(f"round {user_attempt}/6")
            for result in rounds_results:
                print(result)
            user_guess = ask_user_guess(dictionary, already_guessed)
            already_guessed.append(user_guess)

        else:
            print("Game is over.")
            print(f"The wordle is: {answer}")
            break

    # if user guessed correctly print congratulations
    if user_guess == answer:
        for result in rounds_results:
            print(result)
        feedback = give_feedback(answer, user_guess)
        print("YOU WIN")


def ask_user_guess(words_list, user_guesses):
    ''' get user guess as input and compares if such word is in dictionary and consisits of 5 letters
    also check if user already guessed it
    '''
    user_guess = input("Your guess:").upper()

    flag = "false"
    while flag == "false":
        if len(user_guess) != 5: #
            print("The word must be of 5 letters")
            user_guess = input("Your guess:").upper()
            flag = "false"
        elif user_guess not in words_list:
            print("There is no such word in the dictionary")
            user_guess = input("Your guess:").upper()
            flag = "false"
        elif user_guess in user_guesses:
            print("You already guessed this word")
            user_guess = input("Your guess:").upper()
            flag = "false"
        else:
            flag = "true"

    return user_guess

def give_feedback(answer, user_guess):
    #create a list of letters of the word
        wordle_letters = list(answer)
        user_letters = list(user_guess)

        remaining_wordle_letters = wordle_letters.copy() #make copy of wordle characters list to keep track wwhich letters were compared
        feedback = [''] * 5 #list to write checked letters in correct oreder (some googling was done here to find this way)

        # Check for correct position (green) and write them into feedback list using index for correct position
        for i in range(WORD_LENGTH):
            if user_letters[i] == wordle_letters[i]:
                feedback[i] = colored_green(user_letters[i]) #color the guessed letter green
                remaining_wordle_letters[i] = None  # cross out this letter as used

        # Check for correct letter but wrong position (yellow)
        # if such letter exists in the wordle now it's deleted from the list so usedr won't get falsly another such letter marked as in wrong position
        for i in range(WORD_LENGTH):
            if feedback[i] == '':  #check that there's still no correctly guessed letter in given position
                if user_letters[i] in remaining_wordle_letters: #but the letter is present in wordle
                    feedback[i] = colored_yellow(user_letters[i]) #add to feedback colored yellow
                    remaining_wordle_letters[remaining_wordle_letters.index(user_letters[i])] = None
                else:
                    feedback[i] = user_letters[i] #add letter that is not in the wordle but uncolored

        # Print feedback
        feedback = str(''.join(feedback))
        print(''.join(feedback))
        return feedback

def colored_yellow(text):
    return(f"\033[38;2;255;255;0m{text}\033[0m")

def colored_green(text):
    return(f"\033[38;2;0;255;0m{text}\033[0m")


def select_word(lst):
    # function to select a random word from the given list
    max_index = len(lst) - 1 #getting the max index of the list
    index = random.randint(0, max_index)
    word = lst[index]
    return word

# Function to create a list of words retrieved from the file
def get_words_from_file():
    # I honestly copied it from a task
    f = open(FILE_NAME)
    words = []
    for word in f:
        # removes whitespace characters (\n) from the start and end of the line
        word = word.strip()
        # if the line was only whitespace characters, skip it
        if word != "":
            words.append(word)
    return words




if __name__ == "__main__":
    main()