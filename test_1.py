from backtracklib import resolver

num_respuestas = 1
max_time = 0			# no importa el tiempo

# ejemplo 9 reinas

def basecase(parcial):
	for num in (num for num in range(10)):
		if num not in parcial:
			return False
	return True

def CalcularPosibles(parcial):
	ret = []
	for num in (num for num in range(10)):
		if num not in parcial:
			ret.append(num)
	return ret

solucion, tiempo, todas = resolver(num_respuestas, max_time, CalcularPosibles, basecase)

def test_1():
	assert basecase(solucion[0])

print(solucion, tiempo, todas)