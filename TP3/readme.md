# Chatbot - Búsqueda Semántica en CVs PDF

## Descripción

Este proyecto implementa un sistema conversacional que permite realizar preguntas sobre el contenido de currículums en formato PDF. Utiliza embeddings semánticos y un índice vectorial en Pinecone para recuperar fragmentos relevantes del texto, que luego son utilizados como contexto para generar una respuesta.

## Estructura del código

- `upsert.ipynb`: carga e indexa los CVs en Pinecone.
- `retriever.py`: realiza búsquedas semánticas.
- `main.py`: gestiona el flujo del chatbot.
- `pearson_graph.py`: estructura conversacional con LangGraph.
- `helpers.py`: funciones auxiliares (extracción de texto, preprocesamiento, etc.).
- `.env`: contiene configuración (Las API Keys fueron cargadas en el Sistema para ser usadas como Variables de Entorno Global y no dejarlas en el proyecto en claro).
- `requirements.txt`: dependencias del proyecto.


## Notas

- Es necesario tener configurado el archivo `.env` con las claves necesarias antes de ejecutar.
- El sistema asume que los archivos PDF contienen texto extraíble (no imágenes escaneadas sin OCR).
- La calidad de las respuestas depende tanto del modelo de lenguaje como de la relevancia de los chunks recuperados.