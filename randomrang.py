import random

num1 = 0
num2 = 1

while num1 != num2


def generateIP():
    # your code below
    import random
    ipads = [""] * 100

    for i in range(100):
        dig1 = random.randint(10, 255)
        dig2 = random.randint(100, 255)
        dig3 = random.randint(0, 255)
        dig4 = random.randint(0, 255)

        ip = str(dig1) + "." + str(dig2) + "." + str(dig3) + "." + str(dig4)
        ipads[i] = ip

    return ipads




