def operationIndex(list, parantheses_ini, operacao):
    temp = list[parantheses_ini:]
    for i in range(1, len(temp)):
        if temp[i] == operacao:
            return i + parantheses_ini

# separa todos os elementos de uma expressao e distribui em um vetor
def separateString(expression):
    expression = expression.replace('–', '-') # o sinal de subtracao `-` do professor esta diferente: `–`
    list = []
    a = ""
    for i in range(0, len(expression)):
        if expression[i].isdigit():
            a += expression[i]
            if not i == len(expression) - 1:
                if not expression[i + 1].isdigit():
                    list.append(a)
            else:
                list.append(a)
        else:
            if not expression[i] == " ":
                list.append(expression[i])
                a = ""
    return list

# resolve uma expressao definida em um vetor
def solve_expression(expression):
    answer = expression
    toResolve = {}
    if '(' in answer:
        openParentheses = [i for i, item in enumerate(answer) if item == '(']
        closedParentheses = [i for i, item in enumerate(answer) if item == ')']
        x_index = 0
        if len(answer[max(openParentheses)+1:min(closedParentheses)-1]) <= 3:
            x1 = float (answer[max(openParentheses) + 1])
            x2 = float (answer[min(closedParentheses) - 1])
            toResolve['x1'] = x1
            toResolve['x2'] = x2
            toResolve['Op'] = answer[max(openParentheses) + 2]
            toResolve['n'] = operationIndex(answer, max(openParentheses), toResolve['Op']) - 1
            del(answer[min(closedParentheses)])
            del(answer[max(openParentheses)])
        else:
            toResolve = solve_expression(answer[max(openParentheses)+1:min(closedParentheses)])
            toResolve['n'] += max(openParentheses) + 1
    elif '^' in answer:
        x1 = float (answer[answer.index('^') - 1])
        x2 = float (answer[answer.index('^') + 1])
        n = [i for i, item in enumerate(answer) if item == '^']
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '^'
        toResolve['n'] = answer.index(toResolve['Op'])
    elif '*' in answer:
        x1 = float (answer[answer.index('*') - 1])
        x2 = float (answer[answer.index('*') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '*'
        toResolve['n'] = answer.index(toResolve['Op'])
    elif '/' in answer:
        x1 = float (answer[answer.index('/') - 1])
        x2 = float (answer[answer.index('/') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '/'
        toResolve['n'] = answer.index(toResolve['Op'])
    elif '-' in answer:
        x1 = float (answer[answer.index('-') - 1])
        x2 = float (answer[answer.index('-') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '-'
        toResolve['n'] = answer.index(toResolve['Op'])
    elif '+' in answer:
        x1 = float (answer[answer.index('+') - 1])
        x2 = float (answer[answer.index('+') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '+'
        toResolve['n'] = answer.index(toResolve['Op'])

    return toResolve

# problema1 = "23 + 12 - 55 + (2 + 4) - 8 / 2^2"
# problema1_sep = separa_elementos_string(problema1)
# print(problema1_sep)
# print(resolve_expressao(problema1_sep))
