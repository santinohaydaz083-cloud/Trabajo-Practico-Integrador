# Guardado básico en archivo de texto
def guardar_datos(lista_inscriptos):
    with open("inscriptos.csv", "w") as archivo:
        archivo.write("nombre,dni\n")
        for p in lista_inscriptos:
            archivo.write(f"{p['nombre']},{p['dni']}\n")