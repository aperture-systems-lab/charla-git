# Link del reto: https://www.deep-ml.com/problems/1
import numpy as np

def matrix_dot_vector(a: list[list[int|float]], b: list[int|float]) -> list[int|float]:
	# Return a list where each element is the dot product of a row of 'a' with 'b'.
	# If the number of columns in 'a' does not match the length of 'b', return -1.
	if len(a) == len(b):
		return np.array(a) @ np.array(b) 
	else:
		return -1