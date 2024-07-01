"""Modul omogućava parsiranje aritmetičkih izraza."""
import re

__author__ = 'mijicd'

REGEX = r'(?:\d*\.\d+)|(?:\d+)|(?:[()+\-\^/*])'

class ExpressionNotStringError(Exception):
    pass

class UnknownCharacterError(Exception):
    pass

class InvalidMathematicalExpressionError(Exception):
    pass

def tokenize(expression):
    """Funkcija kreira tokene na osnovu zadatog izraza.

    Postupak formiranja liste tokena koristi regularni izraz
    zadat putem REGEX varijable. Omogućeno je pronalaženje
    sledećih tipova tokena:
        - floating-point vrednosti
        - celobrojne vrednosti
        - operatori +, -, *, /, ^
        - zagrade

    Args:
        expression (string): Izraz koji se parsira.

    Returns:
        list: Lista pronađenih tokena.

    Raises:
        AssertionError: Ako izraz nije zadat kao string.
    """
    if not isinstance(expression, str):
        raise ExpressionNotStringError("Izraz treba da bude string.")

    tokens = re.findall(REGEX, expression)

    if expression.replace(" ", "") != "".join(tokens):
        raise UnknownCharacterError("Izraz sadrži karaktere koji nisu podržani.")

    operations = ["+", "-", "*", "/", "^", "(", ")"]
    unary_minus = True
    multiple_exponent = True
    output = []
    for token in tokens:
        if token not in operations:
            unary_minus = False
        if token == "(":
            unary_minus = True
        if token == "-" and unary_minus:
            token = "~"
        output.append(token)
    
    return output