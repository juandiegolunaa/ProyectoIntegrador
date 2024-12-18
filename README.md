# Proyecto de Tesis

Este repositorio contiene todo lo necesario para replicar el desarrollo de un chatbot basado en la técnica **Retrieval-Augmented Generation (RAG)**, utilizando **Ollama** y **OpenWebUI**.

## Contenido

- [Descripción General](#descripción-general)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
  - [Instalación de Ollama](#1-instalación-de-ollama)
  - [Instalación de OpenWebUI](#2-instalación-de-openwebui)
  - [Instalación de Modelos de Lenguaje](#3-instalación-de-modelos-de-lenguaje)
- [Configuración del Sistema](#configuración-del-sistema)
- [Evaluación de Modelos](#evaluación-de-modelos)
- [Evaluación de Respuestas](#evaluación-de-respuestas)
  - [Cargar Preguntas](#1-cargar-preguntas)
  - [Ejecutar Evaluación](#2-ejecutar-evaluación)
- [Generación de Gráficas](#generación-de-gráficas)
- [Creación de un Modelo Personalizado "Asistente"](#creación-de-un-modelo-personalizado-asistente)
- [Contacto](#contacto)

## Descripción General

Este proyecto busca evaluar el desempeño de diferentes modelos de lenguaje en la tarea de responder preguntas utilizando documentos cargados como base de conocimiento. La metodología incluye:

1. Configuración de un entorno de pruebas con **Ollama** y **OpenWebUI**.
2. Instalación de modelos de lenguaje.
3. Pruebas con múltiples usuarios simulados.
4. Análisis de resultados utilizando métricas de evaluación como Similaridad del Coseno, BERTscore y Rouge-L.

## Requisitos Previos

- **Sistema Operativo:** Linux.
- **Recursos de Hardware:**
  - GPU Nvidia compatible con Docker.
  - Al menos 16 GB de RAM.
- **Software:**
  - Docker
  - Python 3.x
  - Selenium
  - Bibliotecas: `numpy`, `matplotlib`, `scikit-learn`, `sentence-transformers`, `rouge`, `bert-score`

## Instalación

### 1. Instalación de Ollama
Ejecuta el siguiente comando para instalar Ollama:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. Instalación de OpenWebUI
Ejecuta este comando para iniciar un contenedor Docker con OpenWebUI:
```bash
docker run -d -p 3000:8080 --gpus all --add-host=host.docker.internal:host-gateway -v open-webui:/app/backend/data --name open-webui --restart always ghcr.io/open-webui/open-webui:cuda
```
Accede a OpenWebUI en `http://<tu-ip>:3000/` para configurar la interfaz gráfica.

### 3. Instalación de Modelos de Lenguaje
Para instalar un modelo de lenguaje, usa el siguiente comando:
```bash
ollama pull <modelName>
```
Modelos recomendados:
- llama3.2
- phi3.5
- llama2-uncensored
- codegemma

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

## Creación de un Modelo Personalizado "Asistente"

La interfaz de OpenWebUI permite crear modelos derivados personalizados. En este caso, el modelo **"Asistente"** se configura como sigue:

1. **Base del Modelo:** Se selecciona `gemma2:latest` como modelo base.
2. **Descripción del Modelo:** Se establece la siguiente descripción para presentación al usuario:
   > "¡Soy tu asistente para resolver tus dudas sobre la USFQ! No dudes en consultarme cualquier tema de la Universidad. Información sobre el manual de estudiantes, el código de honor y convivencia de la USFQ, etc. ¡Estoy aquí para servirte!"
3. **Prompt del Modelo:** Para mejorar la interacción, se configura un prompt que define el tono y rol del modelo:
   > "Eres una asistente administrativa altamente eficiente y amigable, diseñada para responder preguntas de estudiantes sobre documentos universitarios y procesos académicos. Responde siempre en Español."
4. **Documentación:** Se seleccionan los documentos previamente subidos en la sección de RAG como referencia para que el modelo pueda generar respuestas basadas en ellos.
5. **Guardar Configuración:** Finalmente, se guarda la configuración y el modelo está listo para ser usado.

## Contacto
Si tienes preguntas o comentarios, abre un issue en este repositorio.

