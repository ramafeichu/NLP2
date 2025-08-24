# Chatbot RAG - Consulta sobre CV

Este proyecto implementa un sistema de generación de texto que combina técnicas de recuperación de información (Retrieval-Augmented Generation, RAG) con generación de lenguaje natural, permitiendo responder preguntas sobre documentos previamente cargados (en este caso, un CV en PDF).

## Objetivos principales

1. **Cargar un CV en formato PDF** y extraer su contenido para construir un índice de recuperación semántica.
2. **Obtener vectores de embedding** a partir del contenido textual utilizando un modelo de Groq o similar.
3. **Almacenar los vectores en Pinecone**, una base de datos vectorial.
4. **Recuperar contexto relevante** para una consulta mediante similitud de coseno.
5. **Construir un chatbot RAG** que combine la consulta del usuario y el contexto recuperado para generar respuestas personalizadas.

---

## Estructura del código

- `Chatbot_CV_PDF.ipynb`: Notebook principal con todos los pasos del pipeline RAG implementado.
- `/cvs`: Directorio que debe ser creado de forma local, para luego incluir dentro el CV (Esta implementación sirve de base para el TP3).
- Uso de `Pinecone` como vector store.

---

## Resultados esperados

- El chatbot responde preguntas específicas sobre el contenido del CV cargado.
- La generación de texto se basa en contexto relevante, mejorando precisión y coherencia.
- Se evaluó el funcionamiento del sistema en ejemplos de prueba en clase.

---

## Autor

Trabajo práctico realizado en el marco de la **Posgrado de Especialización en Inteligencia Artificial (UBA)**.
