import numpy as np
import sympy as sp


def generate_SLAE(n_variables=5, n_equations=3, param_symbol="p"):
    param = sp.symbols(param_symbol)

    coef_matrix = np.random.randint(-10, 11, size=(n_equations, n_variables)).tolist()
    free_terms = np.random.randint(-10, 11, size=n_equations).tolist()

    rand_i, rand_j = np.random.randint(n_equations), np.random.randint(n_variables)
    coef_matrix[rand_i][rand_j] = param

    coef_matrix = sp.Matrix(coef_matrix)
    free_terms = sp.Matrix(free_terms)

    return coef_matrix, free_terms


def latex_SLAE(coef_matrix, free_terms):
    n_equations, n_variables = coef_matrix.shape
    variables = sp.symbols("x:%d" % (n_variables))
    equations = [
        sum(coef_matrix[i, j] * variables[j] for j in range(n_variables))
        for i in range(n_equations)
    ]
    latex_equations = "$$\n\\left\\{\\begin{matrix}\n"
    for eq in equations:
        latex_equations += sp.latex(eq) + " \\\\ \n"
    latex_equations += "\\end{matrix}\\right.\n$$"
    return latex_equations


def generate_slae_with_param():
    coef_matrix, free_terms = generate_SLAE()
    return latex_SLAE(coef_matrix, free_terms)
