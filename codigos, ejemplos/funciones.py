# Ejemplo de función para registrar un participante
def registrar_participante(nombre, dni, email):
    """
    Crea un diccionario con los datos del participante.
    Parámetros: nombre, dni, email (str)
    Retorna: dict con la info del usuario
    """
    participante = {
        "nombre": nombre,
        "dni": dni,
        "email": email,
        "asistencia": False
    }
    return participante