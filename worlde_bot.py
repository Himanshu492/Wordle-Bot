# def delete_letter(c, string):
#     if c == "a":
#         return string[1:]
#     elif string == "z":
#         return string[:-1]
#
#     for i in range(len(string)):
#         if string[i] == c:
#             return string[:i] + string[i+1:]

def append_at(word, letter, index):
    if index == 0:
        return letter + word
    if index == len(word):
        return word + letter

    return word[:index] + letter + word[index:]


def add_words(output, word):
    flag = False
    for i in range(len(conditions)):
        word = append_at(word, conditions[i], i)

    print(word)
    for char in found:
        if char in word:
            flag = True
        else:
            flag = False

    if word in dictionary and flag:
        output.append(word)

    return output


def combinations(sample, not_found):
    output = []
    if not_found == 5:
        for char1 in sample:
            for char2 in sample:
                for char3 in sample:
                    for char4 in sample:
                        for char5 in sample:
                            word = f"{char1}{char2}{char3}{char4}{char5}"
                            if word in dictionary:
                                output.append(word)

    if not_found == 4:
        for char1 in sample:
            for char2 in sample:
                for char3 in sample:
                    for char4 in sample:
                        word = f"{char1}{char2}{char3}{char4}"
                        output = add_words(output, word)

    if not_found == 3:
        for char1 in sample:
            for char2 in sample:
                for char3 in sample:
                    word = f"{char1}{char2}{char3}"
                    output = add_words(output, word)

    if not_found == 2:
        for char1 in sample:
            for char2 in sample:
                    word = f"{char1}{char2}"
                    output = add_words(output, word)

    if not_found == 1:
        for char1 in sample:
            word = f"{char1}"
            output = add_words(output, word)

    return output


with open("guesses.txt", 'r') as f:
    dictionary = [line.strip() for line in f.readlines()]

print("Welcome to the Worlde Bot!")
print("I will guess the word in less than 6 tries.")
print("Enter the result of each guess in a five letter string.")
print("Y - Yellow. G - Green. X - Not in word. E.g. XXYXG")

guess = input("You will guess the first try. Enter the first guess: ").lower()
found = ""
conditions = [""] * 5
space = "abcdefghijklmnopqrstuvwxyz"

for i in range(5):
    print(f"Guessed word is {guess.upper()}")
    result = input("Enter result: ").upper()
    # print(result)

    for j in range(5):
        if result[j] == "X":
            space = delete_letter(guess[j], space)
        else:
            found += guess[j]
            if result[j] == "G":
                conditions[j] = guess[j]

    word_list = combinations(space, 5-len(found))
    print(word_list)




