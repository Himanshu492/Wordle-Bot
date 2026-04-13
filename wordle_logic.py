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

    for char1 in space[0]:
        for char2 in space[1]:
            for char3 in space[2]:
                for char4 in space[3]:
                    for char5 in space[4]:
                        word = f"{char1}{char2}{char3}{char4}{char5}"
                        if not all(letter in word for letter in found):
                            continue
                        if word in dictionary:
                            output[word] = 0

    return output


def next_guess(words, found):
    alphabets = {}
    best_word = [-1, ""]

    for word in words:
        for letter in word:
            if letter not in found:
                if letter in alphabets:
                    alphabets[letter] += 1
                else:
                    alphabets[letter] = 1

    for word in words:
        letters = []
        for letter in word:
            if letter not in found:
                if letter not in letters:
                    words[word] += alphabets[letter]
                    letters.append(letter)

        if words[word] > best_word[0]:
            best_word[0] = words[word]
            best_word[1] = word

    return best_word[1]


def not_valid_guess(word, dictionary):
    if not word.isalpha():
        print("Invalid input. Please enter only alphabets.")
        return True
    if len(word) != 5:
        print("Invalid input. Guess needs to be 5 characters only")
        return True
    if word not in dictionary:
        print("Word is not in the word list")
        return True
    return False


def not_valid_result(word):
    if word == "FOUND":
        return False

    allowed = "XYG"
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


def update_game_state(result, guess, space, found):
    # iterating through the result e.g. XXYXG
    for j in range(5):
        if result[j] == "X":
            # means we need to delete the letter from all spaces
            for k in range(len(space)):
                space[k] = delete_letter(guess[j], space[k])

        if result[j] == "Y":
            found += guess[j]
            space[j] = delete_letter(guess[j], space[j])

        if result[j] == "G":
            found += guess[j]
            space[j] = guess[j]

    return space, found


def get_next_guess(result, guess, space, found, dictionary):
    space, found = update_game_state(result, guess, space, found)
    word_dict = combinations(space, found, dictionary)
    guess = next_guess(word_dict, found)
    return guess, space, found
