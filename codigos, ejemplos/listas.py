# Lista para almacenar los participantes en memoria
inscriptos = []

# Agregar un nuevo inscripto a la lista
nuevo_inscripto = {"nombre": "Ana Pérez", "dni": "12345678"}
inscriptos.append(nuevo_inscripto)

# Recorrer la lista
for p in inscriptos:
    print(f"Participante: {p['nombre']} - DNI: {p['dni']}")