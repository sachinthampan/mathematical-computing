from math import isqrt


def continued_fractions(D) -> list[int]:
    a0 = isqrt(D)
    m = 0
    d = 1
    a = a0
    coefficients = [a0]
    seen = set()

    while True:
        m = d * a - m
        d = (D - m * m) // d
        a = (a0 + m) // d

        if (m, d) in seen:
            break

        seen.add((m, d))
        coefficients.append(a)
    return coefficients


def convergents(coefficients):
    p_minus_2 = 0
    p_minus_1 = 1

    q_minus_2 = 1
    q_minus_1 = 0

    result = []

    for a in coefficients:
        # calculate p
        p = a * p_minus_1 + p_minus_2

        # calculate q
        q = a * q_minus_1 + q_minus_2

        # add (p, q) to result
        result.append((p, q))

        # shift previous values

        p_minus_2 = p_minus_1
        p_minus_1 = p

        q_minus_2 = q_minus_1
        q_minus_1 = q

    return result

def pells_solver(D):
    if not isinstance(D, int) or isinstance(D, bool):
        raise TypeError("D must be an integer")
    if D < 2:
        raise ValueError("D must be an integer greater than or equal to 2")
    if isqrt(D) ** 2 == D:
        raise ValueError("D must not be a perfect square")
    coefficients = continued_fractions(D)
    # print("Coefficients : ", coefficients)
    periods = coefficients[1:]

    if len(periods) % 2 != 0:
        periods.extend(periods[:-1])
    else:
        periods = periods[:-1]

    # print("Periods = ", periods)
    pell_coefficients = [coefficients[0]] + periods
    # print("P_coefficients", pell_coefficients)
    results = convergents(pell_coefficients)

    return results[-1]

def find_largest_minimal_x (limit):
    if not isinstance(limit, int) or isinstance(limit, bool):
        raise TypeError("D must be an integer")
    if limit < 2:
        raise ValueError("D must be an integer greater than or equal to 2")
    best_D = 0
    max_x = 0
    best_y = 0

    for index in range(2, limit+1):
        if isqrt(index) ** 2 != index:
            result = pells_solver(index)
            x, y = result

            if x > max_x:
                max_x = x
                best_D = index
                best_y = y
            # print("D , result ", index, result[0])

    #print("D with largest minimal x:", best_D)
    #print("Largest minimal x:", max_x)
    return best_D, max_x, best_y