from fast_comparable_primitive import FastComparablePrimitive
from create_population import create_population
import numpy as np



np.random.seed(42)
L = create_population(4, 10)
np.random.seed(42)
R = create_population(4, 10)

for l in L:
	l.print_as_tree()
	print ("|")

print ("if compare works, matrix should be id")

for l in L:
	for r in R:
		if l.equals(r):
			if L.index(l) != R.index(r):
				print ("algo thinks that")
				l.print_as_tree()
				print ("equals to " + "-" * 100)
				r.print_as_tree()
				print ("-------------\n" * 4)
			print ("1", end="")
		else:
			print (".", end="")
	print ()


for l in L:
	for r in R:
		print ("%.2d" % l.get_first_structural_distance(r), end=" ")
	print ()