# Problem Set 2, hangman.py
# Name: 
# Collaborators:
# Time spent:

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string
from functools import reduce

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''

    return set(secret_word).issubset(set(letters_guessed))


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    return ''.join([letter if letter in letters_guessed else '_ ' for letter in secret_word])


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    return ''.join([letter for letter in string.ascii_lowercase if letter not in letters_guessed])


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guesed = []
    tried_letters = []

    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_remaining} warnings left: ')

    while not is_word_guessed(secret_word, letters_guesed) and guesses_remaining > 0:
      print('-' * 12)
      print(f'You have {guesses_remaining} guesses left.')
      print(f'Available letters: {get_available_letters(letters_guesed)}')
      attempt_letter = input('Please guess a letter: ').lower()

      if not attempt_letter.isalpha():
        warnings_remaining -= 1
        print('Oops! This is not a valid letter. ', end = '')
        if warnings_remaining < 0:
          print('You have no warnings left so you lose one guess: ', end = '')
          guesses_remaining -= 1
        else:
          print(f'You have {warnings_remaining} warnings left: ', end = '')
        print(get_guessed_word(secret_word, letters_guesed))
        continue

      if attempt_letter in tried_letters:
        warnings_remaining -= 1
        print('Oops! You\'ve already guessed that letter. ', end = '')
        if warnings_remaining < 0:
          print('You have no warnings left so you lose one guess: ', end = '')
          guesses_remaining -= 1
        else:
          print(f'You have {warnings_remaining} warnings left: ', end = '')
        print(get_guessed_word(secret_word, letters_guesed))
      elif attempt_letter in secret_word:
        letters_guesed.append(attempt_letter)
        print(f'Good guess: {get_guessed_word(secret_word, letters_guesed)}')
        tried_letters.append(attempt_letter)
      else:
        print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guesed)}')
        if attempt_letter in {'a', 'e', 'i', 'o', 'u'}:
          guesses_remaining -= 2
        else:
          guesses_remaining -= 1
        tried_letters.append(attempt_letter)
    
    print('-' * 12)
    if is_word_guessed(secret_word, letters_guesed):
      print(f'Congratulations, you won! Your total score for this game is: {guesses_remaining * len(set(secret_word))}')
    else:
      print('Sorry, you ran out of guesses. The word was else')

      









# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = ''.join(list(filter(lambda char: char != ' ', my_word)))
    if len(my_word) != len(other_word):
      return False
    i = 0
    is_matching = True
    while i < len(other_word):
      if my_word[i] != other_word[i] and my_word[i] != '_':
        is_matching = False
        break
      i += 1
    return is_matching



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_matches = []
    for word in wordlist:
      if match_with_gaps(my_word, word):
        possible_matches.append(word)
    if possible_matches == []:
      return 'No matches found'
    else:
      return ' '.join(possible_matches)


def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guesed = []
    tried_letters = []

    print('Welcome to the game Hangman!')
    print(f'I am thinking of a word that is {len(secret_word)} letters long.')
    print(f'You have {warnings_remaining} warnings left: ')

    while not is_word_guessed(secret_word, letters_guesed) and guesses_remaining > 0:
      print('-' * 12)
      print(f'You have {guesses_remaining} guesses left.')
      print(f'Available letters: {get_available_letters(letters_guesed)}')
      attempt_letter = input('Please guess a letter: ').lower()

      if attempt_letter == '*':
        print(f'Possible word matches are: {show_possible_matches(get_guessed_word(secret_word, letters_guesed))}')
      elif not attempt_letter.isalpha():
        warnings_remaining -= 1
        print('Oops! This is not a valid letter. ', end = '')
        if warnings_remaining < 0:
          print('You have no warnings left so you lose one guess: ', end = '')
          guesses_remaining -= 1
        else:
          print(f'You have {warnings_remaining} warnings left: ', end = '')
        print(get_guessed_word(secret_word, letters_guesed))
        continue

      if attempt_letter in tried_letters:
        warnings_remaining -= 1
        print('Oops! You\'ve already guessed that letter. ', end = '')
        if warnings_remaining < 0:
          print('You have no warnings left so you lose one guess: ', end = '')
          guesses_remaining -= 1
        else:
          print(f'You have {warnings_remaining} warnings left: ', end = '')
        print(get_guessed_word(secret_word, letters_guesed))
      elif attempt_letter in secret_word:
        letters_guesed.append(attempt_letter)
        print(f'Good guess: {get_guessed_word(secret_word, letters_guesed)}')
        tried_letters.append(attempt_letter)
      elif attempt_letter != '*':
        print(f'Oops! That letter is not in my word: {get_guessed_word(secret_word, letters_guesed)}')
        if attempt_letter in {'a', 'e', 'i', 'o', 'u'}:
          guesses_remaining -= 2
        else:
          guesses_remaining -= 1
        tried_letters.append(attempt_letter)
    
    print('-' * 12)
    if is_word_guessed(secret_word, letters_guesed):
      print(f'Congratulations, you won! Your total score for this game is: {guesses_remaining * len(set(secret_word))}')
    else:
      print('Sorry, you ran out of guesses. The word was else')



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    # pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.
    
    secret_word = choose_word(wordlist)
    hangman(secret_word)

###############
    
    # To test part 3 re-comment out the above lines and 
    # uncomment the following two lines. 
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)
