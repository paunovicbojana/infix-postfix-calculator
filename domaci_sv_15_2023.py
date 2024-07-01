# OVE TRI METODE ĆE BITI POZIVANE KROZ AUTOMATSKE TESTOVE. NEMOJTE MENJATI NAZIV, PARAMETRE I POVRATNU VREDNOST.
# Dozvoljeno je implementirati dodatne, pomoćne metode, ali isključivo u okviru ovog modula.
from stack import *
from tokenizer import *

__author__ = 'sv15/2023_paunovic_bojana'

class MissingCharacterError(Exception):
    pass


class MissingOperandError(Exception):
    pass


class MissingOperationError(Exception):
    pass


class DivisionWithZeroError(Exception):
    pass


class ComplexSolutionError(Exception):
    pass


def infix_to_postfix(expression):
    """Funkcija konvertuje izraz iz infiksne u postfiksnu notaciju

    Args:
        expression (string): Izraz koji se parsira. Izraz može da sadrži cifre, zagrade, znakove računskih operacija.
        U slučaju da postoji problem sa formatom ili sadržajem izraza, potrebno je baciti odgovarajući izuzetak.

    Returns:
        list: Lista tokena koji predstavljaju izraz expression zapisan u postfiksnoj notaciji.
    Primer:
        ulaz '6.11 - 74 * 2' se pretvara u izlaz [6.11, 74, 2, '*', '-']
    """
    tokens = tokenize(expression)
    output = []
    stack = Stack()
    operations = ["+", "-", "*", "/", "^", "(", ")", "~"]
    brackets = 0
    no_operations = True
    no_digits = True
    for token in tokens:
        if token not in operations:
            output.append(token)
            no_digits = False
            if len(output) >= 2 and stack.is_empty():
                raise InvalidMathematicalExpressionError("Nevalidan matematički izraz.")
        elif token == "(":
            stack.push(token)
            brackets += 1
        elif token == ")":
            brackets -= 1
            if brackets < 0: raise MissingCharacterError('Niste uneli "(".')
            top = stack.top()
            while top != "(":
                output.append(stack.pop())
                top = stack.top()
            stack.pop()
        else:
            if stack.is_empty():
                stack.push(token)
                no_operations = False
            else:
                next_operation = check_priority(token)
                while not stack.is_empty():
                    top = stack.top()
                    if check_priority(top) >= next_operation and top != "(":
                        output.append(stack.pop())
                    else:
                        break
                stack.push(token)
                no_operations = False
        
    if brackets != 0: raise MissingCharacterError('Niste uneli ")".')
    
    for i in range(len(tokens)):
        if tokens[i] == "(" and tokens[i+1] == ")":
            raise InvalidMathematicalExpressionError('"()" je nevalidan matematički izraz.')
    
    if no_digits: raise MissingOperandError("Izraz ne sadrži brojeve.")
    if no_operations and no_digits: raise MissingOperationError("Izraz ne sadrži matematičke operacije.")
    
    while not stack.is_empty():
        output.append(stack.pop())
    return output

def calculate_postfix(token_list):
    """Funkcija izračunava vrednost izraza zapisanog u postfiksnoj notaciji
    Args:
        token_list (list): Lista tokena koja reprezentuje izraz koji se izračunava. Izraz može da sadrži cifre, zagrade,
         znakove računskih operacija.
        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.
    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz [6.11, 74, 2, '*', '-'] se pretvara u izlaz -141.89
    """
    stack = Stack()
    operations = ["+", "-", "*", "/", "^", "~"]
    for token in token_list:
        if token not in operations:
            stack.push(token)
        else:
            if token == "~":
                if stack.is_empty():
                    raise MissingOperandError("Nedovoljan broj operanada.")
                element = stack.pop();
                if "." in element: element = -float(element)
                else: element = -int(element)
                if int(element) == float(element): stack.push(str(int(element)))
                else: stack.push(str(element))
            else:
                if stack.is_empty():
                    raise MissingOperandError("Nedovoljan broj operanada.")
                else:   
                    second_elem = stack.pop()
                    if stack.is_empty():
                        raise MissingOperandError("Nedovoljan broj operanada.")
                    else:
                        first_elem = stack.pop()
                        gotten = determine_operation(first_elem, second_elem, token)
                        stack.push(gotten)
    if len(stack) > 1:
        raise MissingOperationError("Nedovoljan broj operacija.")
    result = stack.pop()     
    return result

def calculate_infix(expression):
    """Funkcija izračunava vrednost izraza zapisanog u infiksnoj notaciji
    Args:
        expression (string): Izraz koji se parsira. Izraz može da sadrži cifre, zagrade, znakove računskih operacija.
        U slučaju da postoji problem sa formatom ili sadržajem izraza, potrebno je baciti odgovarajući izuzetak.
        U slučaju da postoji problem sa brojem parametara, potrebno je baciti odgovarajući izuzetak.
    Returns:
        result: Broj koji reprezentuje konačnu vrednost izraza

    Primer:
        Ulaz '6.11 - 74 * 2' se pretvara u izlaz -141.89
    """
    return calculate_postfix(infix_to_postfix(expression))

def check_priority(operation):
    dict_operations = {
        "+": 1,
        "-": 1,
        "*": 2,
        "/": 2,
        "~": 3,
        "^": 4,
        "(": 0,
    }
    return dict_operations[operation]

def determine_operation(first, second, operation):
    if "." in first:
        first = float(first)
    else: first = int(first)

    if "." in second:
        second = float(second)
    else: second = int(second)
    
    if operation == "+":
        answer = first + second
    elif operation == "-":
        answer = first - second
    elif operation == "*":
        answer = first * second
    elif operation == "/":
        if second == 0:
            raise DivisionWithZeroError("Zabranjeno je deljenje nulom.")
        else: answer = first / second
    else:
        if first < 0 and isinstance(second, float): raise ComplexSolutionError("U Python-u, zbog aproksimacije, negativan broj na racionalan stepen uvek daje kompleksan broj.")
        elif first == 0 and second < 0: raise DivisionWithZeroError("Zabranjeno je deljenje nulom.")
        else: answer = first ** second
    
    if float(answer) == int(answer): return str(int(answer))
    else: return str(answer)


if __name__ == '__main__':
    try:
        input1 = input("Unesi izraz: ")
        input2 = infix_to_postfix(input1)
        print(input2)
        print(calculate_postfix(input2))
        print(calculate_infix(input1))
    except Exception as e : print(e)