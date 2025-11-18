# Ejemplo de Búsqueda Secuencial
def buscar_por_dni(lista, dni_buscado):
    for persona in lista:
        if persona['dni'] == dni_buscado:
            return persona
    return None

# Ejemplo de Ordenamiento Burbuja (por DNI)
def ordenar_por_dni(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n-i-1):
            if lista[j]['dni'] > lista[j+1]['dni']:
                lista[j], lista[j+1] = lista[j+1], lista[j]