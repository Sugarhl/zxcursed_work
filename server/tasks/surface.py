import numpy as np


def generate_points():
    A = np.random.randint(-10, 10, 3)
    B = np.random.randint(-10, 10, 3)
    C = np.random.randint(-10, 10, 3)
    return A, B, C


def create_md_description(A, B, C):
    md = (
        "Даны три точки в пространстве A("
        + ", ".join(map(str, A))
        + "), B("
        + ", ".join(map(str, B))
        + "), C("
        + ", ".join(map(str, C))
        + "). "
    )
    md += "Составить уравнение плоскости ABC,"
    md += "систему параметрических уравнений прямой AB и прямой AM, перпендикулярной плоскости ABC."
    return md


def generate_surface_dots():
    A, B, C = generate_points()
    latex_description = create_md_description(A, B, C)
    return latex_description
