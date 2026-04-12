from tqdm import tqdm

def delete_letter(c, string):
    if c == "a":
        return string[1:]
    elif string == "z":
        return string[:-1]

    for i in range(len(string)):
        if string[i] == c:
            return string[:i] + string[i+1:]

    return string


def combinations():
    output = {}
    total = 1

    for spc in space:
        total *= len(spc)
    bar_format = ("{desc}: {percentage:3.0f}% |{bar}| {n:,}/{total:,} "
                  "words [{elapsed} elapsed, {remaining} left]")
    progress = tqdm(total=total, desc="Searching words...", dynamic_ncols=False, bar_format=bar_format)
    for char1 in space[0]:
        for char2 in space[1]:
            for char3 in space[2]:
                for char4 in space[3]:
                    for char5 in space[4]:
                        progress.update(1)
                        word = f"{char1}{char2}{char3}{char4}{char5}"
                        if not all(letter in word for letter in found):  # 
                            continue
                        if word in dictionary:
                            output[word] = 0
    progress.close()

    return output


def next_guess(words):  # words = {"word": 0}
    alphabets = {}  # dictionary of each alphabet and its frequency in all the guesses
    best_word = [-1, ""]  # to compare to and find the best word

    for word in words:  # get frequency of each alphabet
        for letter in word:
            if letter not in found:
                if letter in alphabets:
                    alphabets[letter] += 1
                else:
                    alphabets[letter] = 1

    print(alphabets)

    for word in words:
        letters = []  # to check if a letter comes more than once
        for letter in word:
            if letter not in found:
                if letter not in letters:
                    words[word] += alphabets[letter]
                    letters.append(letter)

        if words[word] > best_word[0]:  # to check if its better than the last max
            best_word[0] = words[word]
            best_word[1] = word

    print(words)

    return best_word[1]


def not_valid_guess(word):
    if word == "aabha":
        print("omg who mentioned this goddess. what a sexy woman. anyway give me a guess")
        return True
    if not word.isalpha():
        print("Invalid input. Please enter only alphabets.")
        return True
    if len(word) != 5:
        print("Invalid input. Guess needs to be 5 characters only")
        return True
    if word not in dictionary:
        print("Word in not word list")
        return True
    return False


def not_valid_result(word):
    if word == "FOUND":
        return False

    allowed = "XYG"
    if word == "aabha":
        print("omg who mentioned this goddess. what a sexy woman. anyway give me a guess")
        return True
    if not word.isalpha():
        print("Invalid input. Please enter only alphabets.")
        return True
    if len(word) != 5:
        print("Invalid input. Guess needs to be 5 characters only")
        return True
    if not all(letter in allowed for letter in word):
        print("Please only enter 'X' or 'Y' or 'G'")
        return True
    return False

with open("guesses.txt", 'r') as f:
    dictionary = [line.strip() for line in f.readlines()]

print("Welcome to the Worlde Bot!")
print("I will guess the word in less than 6 tries.")
print("Enter the result of each guess in a five letter string.")
print("Y - Yellow. G - Green. X - Not in word. E.g. XXYXG")
print("If the word is found, enter \"found\"")

space = ["abcdefghijklmnopqrstuvwxyz"] * 5
found = ""

guess = input("You will guess the first try. Enter the first guess: ").lower()
while not_valid_guess(guess):
    guess = input("You will guess the first try. Enter the first guess: ").lower()

for i in range(6): # 6 guesses
    found_word = False

    result = input("Enter result: ").upper()  # output of a guess
    while not_valid_result(result):
        result = input("Enter result: ").upper()

    if result == "FOUND":
        found_word = True
        break

    for j in range(5):  # iterate through the result "XXGXY"
        if result[j] == "X":
            for k in range(len(space)):
                space[k] = delete_letter(guess[j], space[k])
        if result[j] == "Y":
            found += guess[j]
            space[j] = delete_letter(guess[j], space[j])
        if result[j] == "G":
            found += guess[j]
            space[j] = guess[j]

    # add progress bar for for loop
    print("Searching for appropriate words...")
    word_dict = combinations()

    guess = next_guess(word_dict)
    if not guess:
        print("No words left to guess.")
        break
    print(f"Guess this word - {guess.upper()}")

if found_word:
    print(f"The word was {guess.upper()}! Found in {i+1} guesses!")
else:
    print("Word was not found :(")
