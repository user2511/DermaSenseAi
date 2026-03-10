🧴 DermaSense AI

Multimodal Dermatology Assistant using Computer Vision + RAG + LLMs

DermaSense AI is a multimodal AI system for skin analysis and skincare question answering.
It combines computer vision, Retrieval Augmented Generation (RAG), memory systems, and large language models to analyze skin images and generate contextual dermatology responses.

Users can upload a skin image and ask a question, and the system uses AI models and knowledge retrieval to generate a relevant answer.

🚀 Live Demo
API Endpoint

https://dermasenseai-4.onrender.com

Swagger API Documentation

https://dermasenseai-4.onrender.com/docs

You can test the API directly using Swagger UI.

🧠 Key Features

Skin image analysis

Multimodal AI (Image + Text reasoning)

Retrieval Augmented Generation (RAG)

Vector similarity search

Memory system for repeated queries

LangGraph agent workflow orchestration

Streaming LLM responses

Lightweight deployment architecture

🏗 System Architecture

<img width="1035" height="800" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/c91fc2f4-4365-4151-8b4a-2accfe4fbd8a" />

🔗 LangGraph Agent Workflow

<img width="3563" height="376" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/628021ae-eec2-4511-aa0e-0baeb29b03de" />

  
🚀 Lightweight Deployment Architecture

<img width="516" height="800" alt="mermaid-diagram (2)" src="https://github.com/user-attachments/assets/e409a08a-2134-472c-a847-d2d313e42928" />


🧩 Project Structure

<img width="3563" height="376" alt="mermaid-diagram (3)" src="https://github.com/user-attachments/assets/473bcbf7-12fe-45bf-851d-4b02d654d306" />



📊 Project Evolution

Phase 1 — Basic LLM System

Initial prototype built with FastAPI + LLM to answer skincare questions.

User Query → LLM → Response


Phase 2 — Retrieval Augmented Generation

To improve answer quality, a skincare dataset from HuggingFace was embedded into a vector database.

Query → Embedding → Vector Search → LLM


Phase 3 — Multimodal AI

Image understanding was introduced using vision models.

Vision models used:

BLIP

CLIP

Pipeline:

Skin Image → Vision Model → Image Context
Query + Context → RAG → LLM


Phase 4 — Query Dependency Detection

Not all questions depend on the image.
A Query Service determines whether the question should include image analysis.

Example:

"What skin condition is this?" → Image dependent
"What moisturizer helps acne?" → Not image dependent

Scoring mechanism:

Keyword heuristics → 40%
LLM scoring → 60%


Phase 5 — Memory System

The system stores previous interactions to reuse knowledge.

Image + Query + Answer

When a similar query is detected:

Return stored answer

Otherwise:

Generate new response → store in memory


Phase 6 — LangGraph Workflow

As the system grew complex, the pipeline was redesigned using LangGraph.

Graph nodes include:

Vision node

Query builder

Memory retrieval

RAG retrieval

LLM generation

This enabled parallel retrieval and modular orchestration.


Phase 7 — Deployment Challenges

Deployment on Render free tier failed due to heavy ML libraries:

torch
sentence-transformers
CLIP

These models required more RAM than available.


Phase 8 — Precomputed Pipeline

To solve deployment constraints, a precomputed inference pipeline was introduced.

Script used:

generate_precomputed.py

This script runs the entire AI pipeline offline and stores results.


Phase 9 — Demo Deployment

The deployed version uses pHash image similarity to match user images with stored dermatology examples.

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


⚠ Limitations

Small dermatology dataset

pHash similarity has limited visual accuracy

Demo architecture optimized for deployment constraints


🔮 Future Improvements

Better Image Similarity

Replace pHash with:

CLIP image embeddings

Vector Database for Images

Use:

FAISS

Weaviate

Chroma

Larger Dermatology Knowledge Base

Improve RAG retrieval accuracy.

Full Multimodal Pipeline Deployment

Deploy using scalable infrastructure such as:

GPU servers

Kubernetes

serverless AI APIs

Production UI

Build a frontend using:

React

Next.js


🧑‍💻 Installation
Clone Repository
git clone https://github.com/yourusername/DermaSenseAi.git
cd DermaSenseAi
Create Virtual Environment
python -m venv venv
Activate Environment

Windows

venv\Scripts\activate

Linux / Mac

source venv/bin/activate
Install Dependencies
pip install -r requirements.txt
Run FastAPI Server
uvicorn main:app --reload
📌 Branch Overview
main
Full AI pipeline

precomputed-deploy
Offline inference pipeline

demo-deploy
Lightweight deployed demo
📖 What This Project Demonstrates

This project explores advanced AI engineering concepts:

Multimodal AI systems

Retrieval Augmented Generation

Vector similarity search

Agent workflows with LangGraph

Memory systems for LLM applications

Efficient deployment strategies for ML systems

🤝 Contributions

Contributions and improvements are welcome.

📜 License

MIT License
