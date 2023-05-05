import numpy as np
from sympy import Eq, symbols, linsolve


def generate_known_solution():
    return np.random.randint(-10, 11, (5, 1))


def generate_system(known_solution):
    A = np.random.randint(-10, 11, (3, 5))
    B = np.dot(A, known_solution)
    return A, B


def solve_system(A, B):
    x1, x2, x3, x4, x5 = symbols("x1 x2 x3 x4 x5")
    equations = [
        Eq(
            A[i, 0] * x1 + A[i, 1] * x2 + A[i, 2] * x3 + A[i, 3] * x4 + A[i, 4] * x5,
            B[i, 0],
        )
        for i in range(3)
    ]
    solution = linsolve(equations, x1, x2, x3, x4, x5)
    return solution


def to_latex(A, B, known_solution):
    latex_equations = "\\begin{align*}\n\\left\\{\\begin{matrix}\n"
    for i in range(3):
        row = [f"{A[i, j]:+d} x_{{{j+1}}}" for j in range(5)]
        row_str = " ".join(row)
        if row_str.startswith("+"):
            row_str = row_str[1:]
        latex_equations += f"{row_str} = " + f"{B[i, 0]:+d} \\\\ \n".replace("+", "")
    latex_equations += "\\end{matrix}\\right."

    latex_solution = "\\qquad X_0=\\left[\\begin{matrix}"
    for el in known_solution:
        latex_solution += f"{el[0]} & "
    latex_solution = latex_solution[:-2] + "\\end{matrix}\\right]"

    latex_equations += latex_solution + "\\end{align*}"
    return latex_equations


def generate_linear_system_latex():
    known_solution = generate_known_solution()
    A, B = generate_system(known_solution)
    latex_output = to_latex(A, B, known_solution)

    return latex_output


# print(generate_linear_system_latex())
