# Agentic AI Chrome Extension

An intelligent browser assistant with multi-step reasoning, upgraded to a production-ready SaaS backend powered by FastAPI, PostgreSQL, Prisma, and Groq LLMs.

## 🚀 Features

-   **SaaS Authentication**: Fully secure JWT Access and Refresh token flows with safe password hashing.
-   **Database Layer**: PostgreSQL integration managed natively by Prisma Client Python for users and extensions.
-   **LLM Upgrade**: Swapped Gemini for the ultra-fast Groq API (default `llama-3.1-8b-instant`).
-   **Usage Tracking & Rate Limiting**: Built-in usage metrics tracking requests and consumed tokens, with automatic rate-limiting on the Free tier.
-   **Multi-Step Reasoning**: Uses advanced Agentic planning to interact with tools like Web Search, Wikipedia, and PDFs.

## 🛠️ Setup

### Prerequisites

-   Python 3.10+
-   Google Chrome
-   PostgreSQL Server (Local or Neon/Supabase)
-   Groq API Key (`GROQ_API_KEY`)

### Backend Setup

1.  Install dependencies:
    ```bash
    pip install -r backend/requirements.txt
    ```
2.  Set up your `.env` configuration file in the root configuration:
    ```env
    DATABASE_URL="postgresql://user:password@localhost:5432/saas_db"
    GROQ_API_KEY="your_groq_api_key"
    JWT_SECRET="your_secure_string_here"
    ```
3.  Initialize and push the Prisma Database schema:
    ```bash
    prisma generate --schema=backend/prisma/schema.prisma
    prisma db push --schema=backend/prisma/schema.prisma
    ```
4.  Start the FastAPI server:
    ```bash
    uvicorn backend.main:app --reload
    ```
    The server API will run at `http://localhost:8000` (Visit `http://localhost:8000/docs` to see Swagger).

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
