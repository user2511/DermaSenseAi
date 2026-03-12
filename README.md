<!-- ============================= -->
<!-- PROJECT TITLE -->
<!-- ============================= -->

# DermaSense AI

**Multimodal Dermatology Assistant using Computer Vision + RAG + LLMs**

DermaSense AI is a multimodal AI system for **skin analysis and skincare question answering**.  
It combines **computer vision, Retrieval Augmented Generation (RAG), memory systems, and large language models** to analyze skin images and generate contextual dermatology responses.

Users can **upload a skin image and ask a question**, and the system uses AI models and knowledge retrieval to generate a relevant answer.

---

<!-- ============================= -->
<!-- LIVE DEMO SECTION -->
<!-- ============================= -->

#  Live Demo

### API Endpoint

https://dermasenseai-4.onrender.com

### Swagger API Documentation

https://dermasenseai-4.onrender.com/docs

You can test the API directly using **Swagger UI**.

---

<!-- ============================= -->
<!-- FEATURES -->
<!-- ============================= -->

#  Key Features

- Skin image analysis  
- Multimodal AI (Image + Text reasoning)  
- Retrieval Augmented Generation (RAG)  
- Vector similarity search  
- Memory system for repeated queries  
- LangGraph agent workflow orchestration  
- Streaming LLM responses  
- Lightweight deployment architecture  

---

```markdown


#  System Architecture

User Uploads Image + Query  
↓  
FastAPI Backend  

FastAPI splits into two services:

Vision Service → Image Analysis  

Query Service  
↓  
Query Dependency Detection  
↓  
Query Builder  

Query Builder triggers parallel retrieval:

Memory Retrieval  
RAG Retrieval  

Memory Retrieval + RAG Retrieval  
↓  
Context Aggregation  
↓  
LLM Generation  
↓  
Generated Response  
↓  
Memory Storage  
↓  
Response Returned to User


---



#  LangGraph Agent Workflow

Vision Node  
↓  
Query Builder Node  
↓  
Parallel Retrieval

Parallel Retrieval splits into:

Memory Retrieval  
RAG Retrieval  

Memory Retrieval + RAG Retrieval  
↓  
Context Merge  
↓  
LLM Generation  
↓  
Response Streaming  
↓  
Memory Storage


---



#  Lightweight Deployment Architecture

User Image + Query  
↓  
Generate Image pHash  
↓  
Compare With Stored Image Hashes  
↓  
Find Closest Image Match  
↓  
Retrieve Precomputed Results  
↓  
Retrieve Conversation History  
↓  
LLM Generates Final Answer  
↓  
Return Response


---


#  Project Evolution

Phase 1 → Basic LLM System  
↓  
Phase 2 → RAG Integration  
↓  
Phase 3 → Multimodal Vision + Text  
↓  
Phase 4 → Query Dependency Detection  
↓  
Phase 5 → Memory System  
↓  
Phase 6 → LangGraph Workflow  
↓  
Phase 7 → Deployment Challenges  
↓  
Phase 8 → Precomputed Pipeline  
↓  
Phase 9 → Lightweight Deployment
```


<!-- ============================= -->
<!-- PROJECT EVOLUTION -->
<!-- ============================= -->

#  Project Evolution

### Phase 1 — Basic LLM System

Initial prototype built with **FastAPI + LLM** to answer skincare questions.

User Query → LLM → Response


---


### Phase 2 — Retrieval Augmented Generation

To improve answer quality, a **skincare dataset from HuggingFace** was embedded into a vector database.

Query → Embedding → Vector Search → LLM


---


### Phase 3 — Multimodal AI

Image understanding was introduced using **vision models**.

#### Vision Models Used

- BLIP  
- CLIP  

Pipeline:

Skin Image → Vision Model → Image Context
Query + Context → RAG → LLM


---

### Phase 4 — Query Dependency Detection

Not all questions depend on the image.

A **Query Service** determines whether the question should include image analysis.

Example:

- **"What skin condition is this?"** → Image dependent  
- **"What moisturizer helps acne?"** → Not image dependent  

Scoring mechanism:

- Keyword heuristics → **40%**  
- LLM scoring → **60%**


---

### Phase 5 — Memory System

The system stores previous interactions to reuse knowledge.

Image + Query + Answer

When a similar query is detected:

- Return stored answer

Otherwise:


Generate new response → store in memory 


---

### Phase 6 — LangGraph Workflow

As the system grew complex, the pipeline was redesigned using **LangGraph**.

Graph nodes include:

- Vision node  
- Query builder  
- Memory retrieval  
- RAG retrieval  
- LLM generation  

This enabled **parallel retrieval and modular orchestration**.

---

### Phase 7 — Deployment Challenges

Deployment on **Render free tier** failed due to heavy ML libraries:

torch
sentence-transformers
CLIP


These models required **more RAM than available**.

---

### Phase 8 — Precomputed Pipeline

To solve deployment constraints, a **precomputed inference pipeline** was introduced.

Script used:

generate_precomputed.py


This script runs the entire AI pipeline **offline** and stores results.

---

### Phase 9 — Demo Deployment

The deployed version uses **pHash image similarity** to match user images with stored dermatology examples.

User Image
↓
Generate pHash
↓
Compare With Stored Hashes
↓
Find Closest Match
↓
Retrieve Stored Results
↓
LLM Generates Final Response


---


<!-- ============================= -->
<!-- LIMITATIONS -->
<!-- ============================= -->

# ⚠ Limitations

### Demo Deployment Constraints (Memory + Cost)

The current deployed demo uses a **lightweight architecture** due to infrastructure limitations.

Heavy ML libraries such as:

- torch
- sentence-transformers
- CLIP
- BLIP

require **significant RAM**, which exceeds the limits of the **Render free tier environment**.

Running the full multimodal pipeline would require **2–8GB+ memory**, making it impractical for free-tier deployment.

To address this, the system uses a **precomputed inference pipeline** where the heavy AI processing is executed offline and results are stored for retrieval.

---

### Precomputed Pipeline Instead of Real-Time Models

Instead of loading full models during runtime:

- vision models  
- embedding models  
- RAG pipelines  

the system retrieves **precomputed outputs** generated offline using the script:

generate_precomputed.py

This significantly reduces runtime memory usage and enables deployment within constrained environments.

---

### Cost Constraints for Embedding APIs

The system avoids using external embedding APIs such as:

- OpenAI embeddings
- HuggingFace hosted embeddings

because frequent embedding calls for:

- user queries
- image processing
- vector search

can lead to **high operational costs in production**.

For the demo version, lightweight retrieval and precomputed results were used instead.

---

### Image Similarity Using pHash

The deployed system uses **perceptual hashing (pHash)** for image comparison.

Limitations:

- works best for visually similar images
- cannot capture deep semantic features
- less accurate than CLIP-style embeddings

---

### Limited Dermatology Dataset

The RAG knowledge base currently uses a relatively small dermatology dataset.

This limits:

- coverage of rare skin conditions
- medical depth of generated responses

---

### No True Multimodal Inference in Deployment

Although the architecture supports **multimodal reasoning**, the deployed version does not run real-time vision models due to compute constraints.

---

### Lack of Clinical Validation

The system is designed as a **research/demo AI system**, not a medical diagnostic tool.

Responses should not be interpreted as medical advice.

---

### Limited Memory System Scalability

The memory system stores interactions for retrieval, but a production system would require:

- scalable vector storage
- efficient indexing
- conversation management

---

### Single Image Processing

The system currently supports **single-image analysis** and does not yet support:

- multi-image comparison
- skin progression tracking
- temporal analysis of skin conditions



<!-- ============================= -->
<!-- FUTURE IMPROVEMENTS -->
<!-- ============================= -->

# 🔮 Future Improvements

### Full Real-Time Multimodal Pipeline

The current demo uses a **precomputed inference pipeline** due to deployment constraints.

Future versions will run the **complete multimodal AI pipeline in real time**, including:

- vision model inference
- embedding generation
- dynamic RAG retrieval
- LLM reasoning

This would allow the system to analyze **new unseen images dynamically instead of relying on precomputed results**.

---

### GPU-Based Model Deployment

Running full multimodal models requires GPU infrastructure.

Future deployment options include:

- AWS / GCP GPU instances
- Kubernetes GPU clusters
- serverless AI inference platforms

This would enable **real-time execution of vision models and embedding systems**.

---

### Replace pHash With Deep Vision Embeddings

The current demo uses **perceptual hashing (pHash)** for lightweight image similarity.

Future systems can use:

- CLIP image embeddings
- BLIP embeddings
- Vision Transformers (ViT)

This would enable **semantic similarity search for dermatology images instead of simple perceptual comparison**.

---

### Vector Database for Image + Text Retrieval

Introduce scalable vector databases to store both **text and image embeddings**.

Possible technologies:

- FAISS
- Weaviate
- Pinecone
- Chroma

This would allow **large-scale dermatology image and knowledge retrieval**.

---

### Self-Hosted Embedding Infrastructure

To avoid high API costs from external services such as OpenAI embeddings, future systems can deploy **local embedding models**.

Examples:

- sentence-transformers
- Instructor embeddings
- BGE embeddings

This reduces **long-term operational cost for large-scale systems**.

---

### Larger Dermatology Knowledge Base

The RAG system can be expanded using:

- dermatology research papers
- clinical dermatology datasets
- skincare product databases
- medical treatment guidelines

This will significantly improve **knowledge coverage and response quality**.

---

### Fine-Tuned Dermatology LLM

Future systems can include **domain-adapted language models** trained on dermatology data.

Possible models:

- Llama
- Mistral
- domain-specific medical LLMs

This will improve **medical reasoning and dermatology-specific understanding**.

---

### Real-Time Skin Condition Detection

Vision models could be trained to automatically detect conditions such as:

- acne
- eczema
- rosacea
- pigmentation
- skin lesions

This would transform the system from **question answering to automated skin analysis**.

---

### Multi-Image Skin Tracking

Support for analyzing **multiple images over time**.

Possible use cases:

- tracking acne improvement
- monitoring pigmentation treatment
- analyzing skin recovery progress

This enables **AI-assisted dermatology monitoring**.

---

### Personalized Skincare Recommendations

Introduce a personalization layer based on:

- skin type
- climate
- allergies
- skincare routines
- previous skin conditions

This would enable **custom skincare guidance instead of generic responses**.

---

### Conversational Dermatology Assistant

Extend the system into a **long-term conversational skincare assistant** with:

- session memory
- contextual follow-up questions
- personalized recommendations

---

### Multi-Agent AI Architecture

Future versions could use **specialized AI agents** such as:

- Vision Agent (image analysis)
- Knowledge Agent (RAG retrieval)
- Medical Reasoning Agent
- Recommendation Agent

This would improve **modularity and decision quality**.

---

### Dermatology Dataset Creation

A curated dermatology dataset could be built containing:

- labeled skin condition images
- treatment suggestions
- dermatology annotations

This would enable **better training of vision models**.

---



### Explainable AI for Dermatology

Introduce explainability features such as:

- visual heatmaps for skin regions
- explanation of AI reasoning
- confidence scores for predictions

This helps users **trust and understand AI recommendations**.

---



### Production Web Interface

Build a full frontend interface using:

- React
- Next.js
- Tailwind CSS

to create a **user-friendly dermatology assistant platform**.

---

### Secure Medical Data Infrastructure

Future production systems should include:

- user authentication
- encrypted data storage
- secure API communication
- compliance with medical privacy standards

---

### Continuous Learning Feedback Loop

Introduce feedback mechanisms where users rate responses.

This data can be used to:

- improve retrieval quality
- refine prompts
- update dermatology knowledge bases.

---

### Integration with Dermatology Services

Future versions could integrate with:

- tele-dermatology platforms
- appointment booking systems
- dermatologist consultation services

to provide **real-world healthcare support**.



---

<!-- ============================= -->
<!-- INSTALLATION -->
<!-- ============================= -->

#  Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/DermaSenseAi.git
cd DermaSenseAi
```


### Create Virtaul Environemnt


```bash
python -m venv venv
```
### Activate Environment

#### Windows
```bash
venv\Scripts\activate
```
#### Linux / Mac
```bash
source venv/bin/activate
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run FastAPI Server
```bash
uvicorn main:app --reload
```

---

<!-- ============================= -->
<!-- BRANCHES -->
<!-- ============================= -->
## Branch Overview

### main

Full AI pipeline

precomputed-deploy

Offline inference pipeline

demo-deploy

Lightweight deployed demo

<!-- ============================= --> <!-- WHAT THIS PROJECT SHOWS --> <!-- ============================= -->
## What This Project Demonstrates

This project explores advanced AI engineering concepts:

Multimodal AI systems

Retrieval Augmented Generation

Vector similarity search

Agent workflows with LangGraph

Memory systems for LLM applications

Efficient deployment strategies for ML systems

<!-- ============================= --> <!-- CONTRIBUTIONS --> <!-- ============================= -->
## Contributions

Contributions and improvements are welcome.



