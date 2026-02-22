# 🦎 Chameleon AI - Adaptive Neural Search Engine

![React](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-blue)
![Python](https://img.shields.io/badge/Backend-FastAPI%20%2B%20Python-yellow)
![AI](https://img.shields.io/badge/AI-LangGraph%20%2B%20Gemini-orange)
![License](https://img.shields.io/badge/License-MIT-green)

**Chameleon AI** is a full-stack intent-based retrieval system that adapts its personality and domain expertise based on user queries. Unlike generic chatbots, it uses a custom state machine to route questions to specialized "expert" agents (Sports 🏀, Finance 📈, Tech 🤖), preventing hallucinations and providing grounded, context-aware responses.

## 🚀 Features

* **🧠 Adaptive Personality Engine:** Automatically detects user intent (using keyword/semantic logic) and switches the AI's persona to match the topic (e.g., an energetic commentator for sports, a serious analyst for finance).
* **🕸️ State-Based Routing (LangGraph):** Implements a directed cyclic graph (DAG) to orchestrate the flow between classification, retrieval, and generation nodes.
* **⚡ Real-Time RAG Architecture:** Retrieval-Augmented Generation pipeline designed to fetch relevant context before generating answers.
* **🎨 Modern UI:** A responsive, dark-mode chat interface built with **React, TypeScript, and Tailwind CSS**, featuring smooth Framer Motion animations.
* **🚀 High-Performance Backend:** Powered by **FastAPI** for asynchronous request handling and sub-second latency.

## 🛠️ Tech Stack

### **Frontend**
* **Framework:** React 18 + Vite
* **Language:** TypeScript
* **Styling:** Tailwind CSS
* **Animations:** Framer Motion
* **HTTP Client:** Axios

### **Backend & AI**
* **Server:** FastAPI (Python)
* **Orchestration:** LangGraph (StateGraph)
* **Data Processing:** Pandas, NumPy
* **Machine Learning:** Scikit-Learn (TF-IDF, K-Means for topic clustering)
* **LLM Integration:** Google Gemini API (2.5 Flash)

## 📂 Project Structure

```bash
chameleon-ai/
├── frontend/             # React + TypeScript Client
│   ├── src/
│   │   ├── App.tsx       # Main Chat Interface
│   │   └── index.css     # Tailwind Configuration
│   └── package.json
│
├── backend/              # Python FastAPI Server
│   ├── app/
│   │   ├── agent.py      # LangGraph Logic & Gemini Integration
│   │   └── server.py     # API Endpoints
│   ├── data/
│   │   └── clustered_data.pkl # Pre-processed knowledge base
│   └── requirements.txt
```
## ⚡ Getting Started
* Node.js & npm
* Python 3.10+
### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/chameleon-ai.git](https://github.com/yourusername/chameleon-ai.git)
cd chameleon-ai
```
### 2. Backend Setup (The Brain)
### Open a terminal and run:
```bash
cd backend
pip install -r requirements.txt
# Make sure to add your GEMINI_KEY in app/agent.py
python -m app.server
```
### The server will start on http://localhost:8000
### 3. Frontend Setup (The Interface)
### Open a new terminal and run:
```bash
cd frontend
npm install
npm run dev
```
### The app will run on http://localhost:5173

## 🤝 Contributing
#### Contributions are welcome! Please open an issue or submit a pull request for any improvements.

## 📜 License
#### This project is licensed under the MIT License.
