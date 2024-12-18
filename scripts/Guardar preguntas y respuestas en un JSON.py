import json

# Define el nombre del archivo de entrada y salida
input_file = r"C:\Users\Juan Diego\Desktop\Noveno Semestre\Proyecto Integrador\Cuestionario .txt"
output_file = "preguntas_respuestas.json"

# Función para procesar el archivo .txt y convertirlo en una lista de diccionarios
def procesar_preguntas_respuestas(input_file):
    preguntas_respuestas = []
    with open(input_file, "r", encoding="utf-8") as file:
        contenido = file.read()
        bloques = contenido.strip().split("\n\n")  # Divide las preguntas y respuestas por bloques

        for i, bloque in enumerate(bloques):
            lineas = bloque.split("\n")
            pregunta = lineas[0].strip()
            respuesta = " ".join(linea.strip() for linea in lineas[1:])
            
            preguntas_respuestas.append({
                "id": i + 1,
                "pregunta": pregunta,
                "respuesta": respuesta
            })
    return preguntas_respuestas

# Procesar el archivo de entrada y generar el JSON
def guardar_json(preguntas_respuestas, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(preguntas_respuestas, file, ensure_ascii=False, indent=4)

# Llama a las funciones principales
if __name__ == "__main__":
    preguntas_respuestas = procesar_preguntas_respuestas(input_file)
    guardar_json(preguntas_respuestas, output_file)
    print(f"Las preguntas y respuestas han sido guardadas en {output_file}")