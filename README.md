# README - Proyecto de Tesis

## Metodología

Este proyecto está basado en la implementación de un chatbot utilizando la técnica **Retrieval-Augmented Generation (RAG)**. Para ello, se aprovecharon APIs preexistentes como **Ollama** y **OpenWebUI**. Además, se realizaron pruebas con diversos modelos de lenguaje dependiendo del objetivo.

### Instalación de Ollama

El primer paso fue instalar Ollama en el servidor. Este entorno permite al chatbot funcionar de manera aislada, asegurando estabilidad durante las pruebas y la implementación. **Nota:** Todos los comandos deben ejecutarse desde una terminal de Linux.

#### Pasos para la instalación:
1. Ejecutar el siguiente comando para instalar Ollama desde su web oficial:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Una vez instalado, Ollama estará funcionando en el puerto **11434** de la máquina.
3. Para verificar que la instalación fue exitosa, abra un navegador y acceda a `http://host:11434`. Debería aparecer el mensaje: **“Ollama is running”**.

### Instalación de Modelos de Lenguaje

Con Ollama instalado, se procedió a instalar los modelos de lenguaje necesarios para el proyecto. Esto se realiza mediante el siguiente comando:
```bash
ollama pull modelName
```

#### Modelos instalados:

| Nombre del Modelo     | Versión  | Parámetros         |
|-----------------------|-----------|---------------------|
| llama3.2             | 3b        | 3.2 mil millones    |
| phi3.5               | latest    | 3.8 mil millones    |
| llama2-uncensored    | latest    | 7 mil millones      |
| llama3.1             | latest    | 8 mil millones      |
| codegemma            | latest    | 9 mil millones      |
| gemma                | latest    | 9 mil millones      |
| gemma2               | latest    | 9.2 mil millones    |
| deepseek-coder-v2    | 16b       | 15.7 mil millones   |
| llava                | 34b       | 34 mil millones     |
| mixtral              | latest    | 47 mil millones     |
| llama3.1             | 70b       | 70.6 mil millones   |

### Prueba de los Modelos de Lenguaje

Una vez instalados los modelos, es posible probar su funcionalidad desde el servidor, sin necesidad de una interfaz gráfica, utilizando el siguiente comando:
```bash
ollama run modelName
```
Esto permite interactuar con los modelos seleccionados, realizar preguntas y verificar sus respuestas para confirmar que se instalaron correctamente.

### Instalación de la Interfaz Gráfica con OpenWebUI

Lo más importante ahora es la interacción de los usuarios, particularmente en el caso de la comunidad USFQ, con el sistema. Para ello, se implementó una interfaz gráfica utilizando OpenWebUI, disponible en su página oficial.

El servidor de la Universidad cuenta con GPU Nvidia, por lo que la interfaz OpenWebUI se ejecuta mediante un contenedor Docker con el siguiente comando:
```bash
docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda
```

#### Verificación de la Instalación:
1. Acceda a `http://172.21.230.10:3000/` desde un navegador web.
2. Cree una cuenta de administrador al ingresar por primera vez.
3. Una vez dentro, puede comenzar a ingresar prompts y seleccionar el modelo de su preferencia para obtener respuestas.

Con esto, el sistema está listo para realizar pruebas de rendimiento y evaluar la experiencia del usuario.

### Evaluación de Modelos

Para garantizar el correcto funcionamiento de los modelos de lenguaje instalados en el servidor Ollama, y evaluar su rendimiento en términos de velocidad y eficiencia, se desarrolló un script en Python. El código tiene como objetivo medir métricas clave de desempeño, como el tiempo de respuesta, el número de tokens generados y la velocidad en tokens por segundo para cada modelo instalado. Se usó la biblioteca `requests` para realizar solicitudes HTTP a la API de Ollama directamente. Para manejar las respuestas y almacenar los resultados se usaron archivos JSON. 

La API de Ollama permitió realizar pruebas automatizadas con prompts predefinidos, mientras que su documentación oficial sirvió como referencia para la correcta configuración de las solicitudes. Este enfoque permitió identificar los modelos más rápidos y eficientes.

#### Prompt de Prueba

Para las pruebas de rendimiento se usó la pregunta: **“¿Por qué el cielo es azul?”**. Esta pregunta evalúa conocimientos científicos básicos, razonamiento lógico y la capacidad del modelo de generar texto coherente. Es una referencia estándar y fácil de validar, lo que permite que sea usada en la comparación de modelos.

#### Resultados de las Pruebas

| Nombre del modelo     | Parámetros (MM) | Tiempo de respuesta promedio (s) | Número promedio de tokens generados | Promedio de tokens por segundo (tokens/s) |
|-----------------------|-----------------|-----------------------------------|-------------------------------------|--------------------------------------------|
| llama3.2             | 3.2             | 2.76                              | 348.00                              | 134.85                                     |
| phi3.5               | 3.8             | 4.78                              | 760.60                              | 159.15                                     |
| llama2-uncensored    | 7               | 1.08                              | 114.55                              | 113.79                                     |
| llama3.1             | 8               | 3.49                              | 370.30                              | 109.19                                     |
| codegemma            | 9               | 2.31                              | 231.10                              | 103.16                                     |
| gemma                | 9               | 2.11                              | 217.55                              | 106.80                                     |
| gemma2               | 9.2             | 3.28                              | 207.15                              | 66.67                                      |
| deepseek-coder-v2    | 15.7            | 5.06                              | 314.10                              | 64.48                                      |
| llava                | 34              | 4.35                              | 157.60                              | 39.72                                      |
| mixtral              | 47              | 3.69                              | 201.75                              | 64.14                                      |
| llama3.1             | 70.6            | 14.81                             | 345.10                              | 23.99                                      |

#### Visualización de Resultados

Para visualizar y comparar de mejor manera los resultados, se realizaron las siguientes gráficas:

1. **Gráfica 1:** Tokens promedio procesados por modelo.
2. **Gráfica 2:** Tiempo de respuesta promedio de los modelos.
3. **Gráfica 3:** Tokens por segundo promedio de cada modelo.

La gráfica de tokens por segundo utiliza como referencia los 35.68 tokens/segundo generados por el modelo GPT-4 Turbo, según su documentación oficial.

#### Observaciones

Los modelos más pequeños en términos de parámetros, como `llama3.2` y `phi3.5:latest`, procesan más tokens por segundo, lo que refuerza su eficiencia en comparación a modelos más grandes. Sin embargo, esto no implica necesariamente mayor calidad en las respuestas, sino un mejor rendimiento computacional.

#### Requisitos para las Pruebas

- Ejecutar el archivo Python `Tiempos de respuesta.py` para medir el rendimiento.
- Ejecutar el archivo Python `Graficar tiempos de respuesta.py` para generar las gráficas correspondientes.

