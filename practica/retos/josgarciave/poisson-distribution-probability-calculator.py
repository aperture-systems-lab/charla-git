# Link del reto: https://www.deep-ml.com/problems/81

import math

def poisson_probability(k, lam):
    val = (math.exp(-lam) * lam**k) / math.factorial(k)
    return round(val, 5)
