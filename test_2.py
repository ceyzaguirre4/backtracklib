from backtracklib import resolver

num_respuestas = 1
max_time = 0			# no importa el tiempo

# example 8 queens w/o optimizations

def basecase(parcial):
	if len(parcial) == 8:
		return True

def CalcularPosibles(parcial):
	ret = []
	for x in range(8):
		for y in range(8):
			is_in = False
			for i in range(8):
				if (x,i) in parcial or (i, y) in parcial or (x-i, y-i) in parcial or (x+i, y+i) in parcial:
					is_in = True
			if not is_in: 
				ret.append((x,y))
	return ret

solucion, tiempo, todas = resolver(num_respuestas, max_time, CalcularPosibles, basecase)

def test_1():
	assert basecase(solucion[0])

print(solucion, tiempo, todas)