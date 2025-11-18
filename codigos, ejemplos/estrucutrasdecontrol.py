# Ejemplo de validación de datos con while e if
edad = 0
while True:
    entrada = input("Ingrese la edad del participante: ")
    if entrada.isdigit():
        edad = int(entrada)
        if edad >= 18:
            print("Edad válida.")
            break
        else:
            print("El evento es solo para mayores de edad.")
    else:
        print("Por favor, ingrese un número válido.")