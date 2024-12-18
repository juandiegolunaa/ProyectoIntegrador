# Proyecto Integrador

Este repositorio contiene todo lo necesario para replicar y entender el desarrollo de un chatbot basado en la técnica **Retrieval-Augmented Generation (RAG)**, utilizando **Ollama** y **OpenWebUI**.

## Contenido

- [Metodología](#metodología)
- [Instalación de Ollama](#instalación-de-ollama)
- [Instalación de Modelos de Lenguaje](#instalación-de-modelos-de-lenguaje)
- [Instalación de la Interfaz Gráfica con OpenWebUI](#instalación-de-la-interfaz-gráfica-con-openwebui)
- [Evaluación de Modelos](#evaluación-de-modelos)
- [Requisitos para las Pruebas](#requisitos-para-las-pruebas)
- [Creación de un Modelo Personalizado "Asistente"](#creación-de-un-modelo-personalizado-asistente)

## Metodología

Este proyecto está basado en la implementación de un chatbot utilizando la técnica **Retrieval-Augmented Generation (RAG)**. Para ello, se aprovecharon APIs preexistentes como **Ollama** y **OpenWebUI**. Además, se realizaron pruebas con diversos modelos de lenguaje dependiendo del objetivo.

## Instalación de Ollama

El primer paso fue instalar Ollama en el servidor. Este entorno permite al chatbot funcionar de manera aislada, asegurando estabilidad durante las pruebas y la implementación. **Nota:** Todos los comandos deben ejecutarse desde una terminal de Linux.

#### Pasos para la instalación:
1. Ejecutar el siguiente comando para instalar Ollama desde su web oficial:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ```
2. Una vez instalado, Ollama estará funcionando en el puerto **11434** de la máquina.
3. Para verificar que la instalación fue exitosa, abra un navegador y acceda a `http://host:11434`. Debería aparecer el mensaje: **“Ollama is running”**.

## Instalación de Modelos de Lenguaje

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

## Instalación de la Interfaz Gráfica con OpenWebUI

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

## Evaluación de Modelos

Para garantizar el correcto funcionamiento de los modelos de lenguaje instalados en el servidor Ollama, y evaluar su rendimiento en términos de velocidad y eficiencia, se desarrolló un script en Python. El código tiene como objetivo medir métricas clave de desempeño, como el tiempo de respuesta, el número de tokens generados y la velocidad en tokens por segundo para cada modelo instalado. Se usó la biblioteca `requests` para realizar solicitudes HTTP a la API de Ollama directamente. Para manejar las respuestas y almacenar los resultados se usaron archivos JSON. 

La API de Ollama permitió realizar pruebas automatizadas con prompts predefinidos, mientras que su documentación oficial sirvió como referencia para la correcta configuración de las solicitudes. Este enfoque permitió identificar los modelos más rápidos y eficientes.

#### Prompt de Prueba

Para las pruebas de rendimiento se usó la pregunta: **“¿Por qué el cielo es azul?”**. Esta pregunta evalúa conocimientos científicos básicos, razonamiento lógico y la capacidad del modelo de generar texto coherente. Es una referencia estándar y fácil de validar, lo que permite que sea usada en la comparación de modelos.

#### Visualización de Resultados

Para visualizar y comparar de mejor manera los resultados, se realizaron las siguientes gráficas:

1. **Gráfica 1:** Tokens promedio procesados por modelo.
2. **Gráfica 2:** Tiempo de respuesta promedio de los modelos.
3. **Gráfica 3:** Tokens por segundo promedio de cada modelo.

La gráfica de tokens por segundo utiliza como referencia los 35.68 tokens/segundo generados por el modelo GPT-4 Turbo, según su documentación oficial.

#### Observaciones

Los modelos más pequeños en términos de parámetros, como `llama3.2` y `phi3.5:latest`, procesan más tokens por segundo, lo que refuerza su eficiencia en comparación a modelos más grandes. Sin embargo, esto no implica necesariamente mayor calidad en las respuestas, sino un mejor rendimiento computacional.

## Requisitos para las Pruebas

- Ejecutar el archivo Python `Tiempos de respuesta.py` para medir el rendimiento.
- Ejecutar el archivo Python `Graficar tiempos de respuesta.py` para generar las gráficas correspondientes.


## Configuración del Sistema

### 1. Cargar Documentos
En OpenWebUI, carga los documentos que usarás como base de conocimiento desde la sección de configuración de documentos.

### 2. Configurar Parámetros
En OpenWebUI:
- **Modelo de Embedding:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **Tamaño de Fragmentos:** 1024 tokens
- **Superposición de Fragmentos:** 100 tokens
- **Top K:** 10 documentos

## Evaluación de Modelos

Usa el script `Guardar Respuestas Generadas En JSON.py` para realizar las evaluaciones:
1. Define los modelos a evaluar.
2. Simula múltiples usuarios enviando preguntas desde un archivo JSON.
3. Guarda las respuestas generadas en un archivo `responses.json`.

## Evaluación de Respuestas

### 1. Cargar Preguntas
Usa el script `Guardar Preguntas y Respuestas en JSON.py` para cargar las preguntas desde un archivo `.txt` y convertirlas en un archivo JSON.

### 2. Ejecutar Evaluación
Ejecuta el script de evaluación para comparar las respuestas generadas por los modelos con las respuestas de referencia.

## Generación de Gráficas

Ejecuta el script `Generar Gráficas Métricas.py` para generar gráficas de las métricas obtenidas:
1. Coloca todos los archivos JSON en la carpeta de respuestas.
2. Ejecuta el script para generar gráficos de Similaridad del Coseno, BERTscore y Rouge-L.
3. Las gráficas se guardarán en la carpeta de salida especificada en el script.

## Contacto
Si tienes preguntas o comentarios, abre un issue en este repositorio.



## Creación de un Modelo Personalizado "Asistente"

La interfaz de OpenWebUI permite crear modelos derivados personalizados. En este caso, el modelo **"Asistente"** se configura como sigue:

1. **Base del Modelo:** Se selecciona `gemma2:latest` como modelo base.
2. **Descripción del Modelo:** Se establece la siguiente descripción para presentación al usuario:
   > "¡Soy tu asistente para resolver tus dudas sobre la USFQ! No dudes en consultarme cualquier tema de la Universidad. Información sobre el manual de estudiantes, el código de honor y convivencia de la USFQ, etc. ¡Estoy aquí para servirte!"
3. **Prompt del Modelo:** Para mejorar la interacción, se configura un prompt que define el tono y rol del modelo:
   > "Eres una asistente administrativa altamente eficiente y amigable, diseñada para responder preguntas de estudiantes sobre documentos universitarios y procesos académicos. Responde siempre en Español."
4. **Documentación:** Se seleccionan los documentos previamente subidos en la sección de RAG como referencia para que el modelo pueda generar respuestas basadas en ellos.
5. **Guardar Configuración:** Finalmente, se guarda la configuración y el modelo está listo para ser usado.

Para cualquier duda o problema, consulta la documentación de OpenWebUI y Ollama.

