# separa todos os elementos de uma expressao e distribui em um vetor
def separa_elementos_string(expressao):
    expressao = expressao.replace('–', '-') # o sinal de subtracao `-` do professor esta diferente: `–`
    vetor = []
    a = ""
    for i in range(0, len(expressao)):
        if expressao[i].isdigit():
            a += expressao[i]
            if not i == len(expressao) - 1:
                if not expressao[i + 1].isdigit():
                    vetor.append(a)
            else:
                vetor.append(a)
        else:
            if not expressao[i] == " ":
                vetor.append(expressao[i])
                a = ""
    return vetor

# resolve uma expressao definida em um vetor
def resolve_expressao(expressao):
    # solucao = separa_elementos_string(expressao)
    solucao = expressao
    toResolve = {}
    if '(' in solucao:
        prioridade = solucao[solucao.index('(') + 1:solucao.index(')')]
        prioridade = resolve_expressao(prioridade)
        del(solucao[solucao.index('('):solucao.index(')')])
        solucao[solucao.index(')')] = str (prioridade[0])
    elif '^' in solucao:
        x1 = float (solucao[solucao.index('^') - 1])
        x2 = float (solucao[solucao.index('^') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '^'
    elif '*' in solucao:
        x1 = float (solucao[solucao.index('*') - 1])
        x2 = float (solucao[solucao.index('*') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '*'
    elif '/' in solucao:
        x1 = float (solucao[solucao.index('/') - 1])
        x2 = float (solucao[solucao.index('/') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '/'
    elif '-' in solucao:
        x1 = float (solucao[solucao.index('-') - 1])
        x2 = float (solucao[solucao.index('-') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '-'
    elif '+' in solucao:
        x1 = float (solucao[solucao.index('+') - 1])
        x2 = float (solucao[solucao.index('+') + 1])
        toResolve['x1'] = x1
        toResolve['x2'] = x2
        toResolve['Op'] = '+'

        # print(f"Por enquanto ta assim: {solucao}")
    return toResolve



# problema1 = "23 + 12 - 55 + (2 + 4) - 8 / 2^2"
# problema1_sep = separa_elementos_string(problema1)
# print(problema1_sep)
# print(resolve_expressao(problema1_sep))
