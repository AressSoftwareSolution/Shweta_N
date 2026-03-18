
def Add(a, b):
    """Print the sum of a and b.

    Args:
        a (int): First addend.
        b (int): Second addend.
    """
    return print(f"Addition is:{a+b}")


def Sub(a, b):
    """Print the difference (a - b).

    Args:
        a (int | float): Minuend.
        b (int | float): Subtrahend.
    """
    return print(f"Substraction is:{a-b}")


def Mul(a, b):
    """Print the product of a and b.
    """
    return print(f"Multiplication is:{a*b}")


def Div(a, b):
    """Print the quotient (a / b) if b is not zero.

    Args:
        a (int | float): Dividend.
        b (int | float): Divisor.

    Handles divide-by-zero by printing an error message.
    """
    if b != 0:
        return print(f"Division is:{a/b}")
    else:
        return print("Denominator Should not be Zero")


def calculator():
    """Run a simple CLI loop that asks for two integers and an operation.

    The user is prompted to enter values for A and B, then select an
    operation from the numbered menu. The chosen operation is executed
    and its result printed. If an unknown option is chosen, an
    appropriate message is displayed.
    """
    a = int(input("Enter the value of A"))
    b = int(input("Enter the value of B"))
    c = int(input("Enter 1:Addition\n 2:Substraction\n 3:Multiplication \n 4:Division"))

    match c:
        case 1:
            Add(a, b)
        case 2:
            Sub(a, b)
        case 3:
            Mul(a, b)
        case 4:
            Div(a, b)
        case _:             ## Default Case to handle a invalid input
            print("Operation Not Found")


calculator()