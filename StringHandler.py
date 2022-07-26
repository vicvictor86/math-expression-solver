import re


def addition(a, b):
    return a + b
def subtraction(a, b):
    return a - b
def multiplication(a, b):
    return a * b
def division(a, b):
    return a / b

def resolve(operator, match: str):
    operation = addition
    if operator == "-": operation = subtraction
    if operator == "*": operation = multiplication
    if operator == "/": operation = division

    data = match
    while data.find(f"{operator}") > 0:
        result = re.findall(rf'[0-9]+\{operator}[0-9]+', data)
        number1 = int(result[0].split(operator)[0])
        number2 = int(result[0].split(operator)[1])
        data = re.sub(rf'[0-9]+\{operator}[0-9]+', str(operation(number1, number2)), data)
        print(data)

    return data


def handler(data: str):
    print(data, end="\n\n")

    matchesParentheses = re.findall(r'\(.+?\)', data)
    print(matchesParentheses, end="\n\n")

    for match in matchesParentheses:
        match = match.replace("(", "")
        match = match.replace(")", "")

        print(match)

        highPriority = re.findall(r'[0-9]+[\/\*][0-9]+', match)
        print(highPriority)
        if highPriority:
            match = resolve("* /", match)
            print(match)

        additions = re.findall(r'[0-9]+\+[0-9]+', match)
        if additions:
            resolve("+", match)
        subtractions = re.findall(r'[0-9]+\-[0-9]+', match)
        if subtractions:
            resolve("-", match)


# data = str(input("Digite a expressão > "))
data = "23 + 12 – 55 + (2 / 4 * 5) – (8 * 6) / 2^2"

handler(data.replace(" ", ""))


