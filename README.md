# Agentic AI Chrome Extension

An intelligent browser assistant with multi-step reasoning, powered by LangGraph, FastAPI, and Google Gemini.

## 🚀 Features

-   **Multi-Step Reasoning**: Uses LangGraph to plan, execute tools, and reflect on results.
-   **Agent Modes**: Research Assistant, Job Analyzer, Content Simplifier, Learning Mode, Autonomous Planner.
-   **Streaming Responses**: Real-time token streaming via Server-Sent Events (SSE).
-   **Tools**: Web Search, Wikipedia, PDF Reader, YouTube Transcript, Vector Memory.
-   **Memory**: Short-term conversation history and long-term vector storage (FAISS).

## 🛠️ Setup

### Prerequisites

-   Python 3.10+
-   Google Chrome
-   Google Gemini API Key
-   (Optional) Tavily API Key for search

### Backend Setup

1.  Navigate to the backend directory:
    ```bash
    cd backend
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Create a `.env` file in `backend/` and add your keys:
    ```env
    GOOGLE_API_KEY=your_gemini_key
    TAVILY_API_KEY=your_tavily_key # Optional
    ```
4.  Start the server:
    ```bash
    uvicorn main:app --reload
    ```
    The server will run at `http://localhost:8000`.

### Extension Setup

1.  Open Chrome and navigate to `chrome://extensions/`.
2.  Enable **Developer mode** (toggle in the top right).
3.  Click **Load unpacked**.
4.  Select the `extension/` folder in this project.
5.  Pin the extension to your toolbar.

## 📦 Deployment

### Backend (Render/Railway)

1.  Push the code to a GitHub repository.
2.  Link the repository to Render/Railway.
3.  Set the **Root Directory** to `backend`.
4.  Set the **Build Command** to `pip install -r requirements.txt`.
5.  Set the **Start Command** to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
6.  Add environment variables (`GOOGLE_API_KEY`, etc.) in the dashboard.

### Extension

1.  Update `host_permissions` in `manifest.json` to point to your deployed backend URL.
2.  Update `popup.js` to fetch from the deployed URL instead of `localhost`.
3.  Pack the extension via Chrome Developer Dashboard or distribute locally.

## 🧪 Testing

1.  Open any webpage.
2.  Click the extension icon.
3.  Select a mode (e.g., "Research Assistant").
4.  Ask a question: "Summarize this page" or "Find related articles".
5.  Watch the agent plan, search, and answer in real-time!
