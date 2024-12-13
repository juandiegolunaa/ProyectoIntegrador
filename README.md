# README - Proyecto Integrador

## Instalación del chatbot

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
1. Acceda a `http://localhost:3000/` desde un navegador web.
2. Cree una cuenta de administrador al ingresar por primera vez.
3. Una vez dentro, puede comenzar a ingresar prompts y seleccionar el modelo de su preferencia para obtener respuestas.

Con esto, el sistema está listo para realizar pruebas de rendimiento y evaluar la experiencia del usuario.

---


