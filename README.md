# TFG Chatbot RAG

Asistente conversacional institucional para la Universidad CEU San Pablo basado en Retrieval-Augmented Generation (RAG), memoria conversacional híbrida e integración con WhatsApp Cloud API.

## Descripción

Este proyecto desarrolla un chatbot especializado en la Universidad CEU San Pablo capaz de responder preguntas sobre grados, dobles grados, idiomas, campus, prácticas, admisión y otros aspectos académicos.

El sistema combina recuperación de información mediante RAG, memoria conversacional y reformulación contextual de consultas para ofrecer respuestas más naturales y precisas.

Actualmente puede utilizarse a través de:

- Interfaz web
- API REST
- WhatsApp

---

## Arquitectura

```text
Usuario
   │
   ▼
Web / WhatsApp
   │
   ▼
FastAPI
   │
   ├─ Gestión automática de sesiones
   ├─ Memoria conversacional
   ├─ Query Rewriter (OpenAI)
   ├─ Clasificación de preguntas
   │
   ▼
ChromaDB
   │
   ▼
OpenAI
   │
   ▼
Respuesta final
```

---

## Tecnologías utilizadas

- Python 3
- FastAPI
- OpenAI API
- ChromaDB
- SQLite
- Nginx
- Ubuntu Server
- Hetzner Cloud
- WhatsApp Cloud API
- Let's Encrypt

---

## Características principales

### Retrieval-Augmented Generation (RAG)

La información se obtiene a partir de documentación institucional de la Universidad CEU San Pablo.

Durante la ingesta:

- Extracción de texto
- División en chunks
- Generación de embeddings
- Almacenamiento vectorial en ChromaDB

### Memoria conversacional

El sistema incorpora una arquitectura híbrida de memoria basada en:

- Historial por sesión
- Detección de follow-ups
- Reformulación contextual mediante LLM
- Reutilización automática del contexto

Ejemplo:

```text
Usuario: ¿Qué idiomas tiene Medicina?
Usuario: ¿Y el campus?

Consulta reformulada:
¿Dónde se encuentra el campus asociado al grado de Medicina?
```

### Gestión automática de sesiones

Cada conversación dispone de:

- user_identifier
- channel
- session_id

Esto permite mantener conversaciones persistentes tanto desde la web como desde WhatsApp.

### Trazabilidad

El sistema registra:

- Mensaje original
- Mensaje efectivo utilizado para retrieval
- Tipo de pregunta
- Respuesta generada
- Fuentes recuperadas
- Chunks utilizados

---

## Despliegue

El sistema se encuentra desplegado en un servidor VPS utilizando:

- Hetzner Cloud
- Ubuntu Server
- Nginx como proxy inverso
- HTTPS mediante Let's Encrypt
- Dominio propio

---

## Integración con WhatsApp

El chatbot está integrado con WhatsApp Cloud API.

Flujo de funcionamiento:

```text
WhatsApp
   │
   ▼
Meta Cloud API
   │
   ▼
Webhook FastAPI
   │
   ▼
Sistema RAG
   │
   ▼
OpenAI
   │
   ▼
WhatsApp
```

---

## Instalación

### Clonar repositorio

```bash
git clone https://github.com/adolfotblancoa/tfg-chatbot-rag.git
cd tfg-chatbot-rag
```

### Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno virtual

Windows:

```bash
venv\Scripts\activate
```

Linux:

```bash
source venv/bin/activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

Crear un archivo `.env` con las credenciales necesarias.

### Ejecutar la ingesta documental

```bash
python -m ingestion.ingest_to_chroma
```

### Lanzar la aplicación

```bash
uvicorn app.main:app --reload
```

---

## Estado actual

Funcionalidades implementadas:

- Sistema RAG operativo
- ChromaDB
- Memoria conversacional híbrida
- Reformulación contextual mediante LLM
- Frontend web
- Gestión automática de sesiones
- Trazabilidad de consultas
- Despliegue en VPS
- HTTPS
- Integración con WhatsApp Cloud API

---

## Autor

**Adolfo Blanco Araujo**

Trabajo Fin de Grado — Ingeniería Informática  
Universidad CEU San Pablo