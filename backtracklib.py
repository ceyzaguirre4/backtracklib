from time import time

def resolver(num_respuestas, max_time, CalcularPosibles, basecase):
    parcial = []
    solucion = []
    t_inicio = time()
    limit = ResolverRecursivo(parcial, solucion, num_respuestas, max_time, t_inicio,  CalcularPosibles, basecase)
    todas = False if (limit and len(solucion) < num_respuestas) else True
    return solucion, time() - t_inicio, todas

def ResolverRecursivo(parcial, solucion, num_respuestas, max_time, t_inicio,  CalcularPosibles, basecase):
    def _agregar(posible):
        parcial.append(posible)
    def _sacar():
        parcial.pop()


    if max_time and time() - t_inicio > max_time:  # si se ha demorado mas de 1 segundo, matar el proceso y devuelve lo que lleve.
        return True
    if basecase(parcial):  # incluir aca restricciones de tiempo
        solucion.append(list(parcial))
        return False if len(solucion) < num_respuestas else True
    else:
        posibles = CalcularPosibles(parcial)
        p = 0
        solucionado = False
        while not solucionado and p < len(posibles):
            posible = posibles[p]
            _agregar(posible)
            solucionado = ResolverRecursivo(parcial, solucion, num_respuestas, max_time, t_inicio,  CalcularPosibles, basecase)
            _sacar()
            p += 1
        return solucionado
