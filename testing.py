import time


# progessbar = ["#"]
# count = 0
# while count < 101:
#     print(*progessbar, end="".ljust((100 - count) + 3), sep="")
#     print(count, end="%")
#     time.sleep(0.1)
#     print("", end="\r")
#     count += 1
#     progessbar.append("#")
#
# print("Done!")
#
# dots = [""]
# while True:
#     print("Loading", end="")
#     print(*dots, end="", sep="")
#     time.sleep(1)
#     print("", end="\r")
#     dots.append(".")
#     if len(dots) > 4:
#         dots = [""]

# print("HI", end="")
# time.sleep(2)
# print("", end="\r")
# print("Bye")

# def delete_letter(c, string):
#     if c == "a":
#         return string[1:]
#     elif string == "z":
#         return string[:-1]
#
#     for i in range(len(string)):
#         if string[i] == c:
#             return string[:i] + string[i+1:]

alphabets = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

output = []
counter = 0

for char1 in alphabets:
    for char2 in alphabets:
        for char3 in alphabets:
            for char4 in alphabets:
                for char5 in alphabets:
                    counter += 1
                    output.append(f"{char1}{char2}{char3}{char4}{char5}")

print(counter)
print(output)