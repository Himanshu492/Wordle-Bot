"""
This file generates guess_db.csv which has the best guess for each of the 243 possible results of a guess. 
for example "XYGXY" means the first letter is not in the word, the second letter is in the word but in a different position, 
the third letter is in the correct position, the fourth letter is not in the word and the fifth letter
is in the word but in a different position. The best guess for this result is "LEARY". 
This means that if we get this result for our first guess "SLATE", then our next guess should be "LEARY".
This is used in wordle_bot2.py to make the bot faster. It takes around 5 minutes to run.

"""


from tqdm import tqdm


def load_dictionary():
    with open("guesses.txt", "r") as file:
        dictionary = set(word.strip().upper() for word in file)
    return dictionary


def delete_letter(c, string):
    if c == "a":
        return string[1:]
    elif string == "z":
        return string[:-1]

    for i in range(len(string)):
        if string[i] == c:
            return string[:i] + string[i+1:]

    return string


def combinations(space, found, dictionary):
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


def next_guess(words, found):  # words = {"word": 0}
    alphabets = {}  # dictionary of each alphabet and its frequency in all the guesses
    best_word = [-1, ""]  # to compare to and find the best word

    for word in words:  # get frequency of each alphabet
        for letter in word:
            if letter not in found:
                if letter in alphabets:
                    alphabets[letter] += 1
                else:
                    alphabets[letter] = 1

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

    return best_word[1]


def generate_results():
    return_set = set()
    letters = "XYG"
    for a in letters:
        for b in letters:
            for c in letters:
                for d in letters:
                    for e in letters:
                        string = f"{a}{b}{c}{d}{e}"
                        return_set.add(string)

    return list(return_set)


def create_db():
    guess = "SLATE"
    dictionary = load_dictionary()
    all_results = generate_results()

    for result in all_results:
        space = ["ABCDEFGHIJKLMNOPQRSTUVWXYZ"] * 5
        found = ""

        for i in range(len(result)):
            if result[i] == 'X':
                for j in range(len(space)):
                    space[j] = delete_letter(guess[i], space[j])
            elif result[i] == 'G':
                found += guess[i]
                space[i] = guess[i]
            elif result[i] == 'Y':
                found += guess[i]
                space[i] = delete_letter(guess[i], space[i])

        print("Calculating best guess for result:", result) 
        words = combinations(space, found, dictionary)
        best_guess = next_guess(words, found)
        print(f"Result: {result}, Best Guess: {best_guess}")

        with open("guess_db.csv", "a") as file:
            file.write(f"{result},{best_guess}\n")


create_db()







