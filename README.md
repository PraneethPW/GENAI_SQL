# GENAI SQL – Natural Language to Postgres

GENAI SQL is a full‑stack web application that lets you ask questions in plain English and get back **both** the generated SQL and live results from a Neon‑hosted PostgreSQL database. It is designed as a transparent, AI‑assisted interface for analysts and developers who want fast data exploration without giving up control over the underlying queries.

---

## Features

- **Natural language → SQL**  
  Type questions like _“Show total sales by month in 2024”_ and receive a runnable `SELECT` query plus a result table.

- **Live Neon Postgres results**  
  All queries run against a real Neon PostgreSQL instance, returning fresh data in real time.

- **Transparent and safe**  
  The generated SQL is always shown, and the backend validates that only read‑only `SELECT` statements are executed.

- **Clean, responsive UI**  
  Two‑panel layout: query input on the left and “SQL & Results” on the right, optimized for desktop and mobile with Tailwind CSS.

- **Schema‑driven prompts**  
  The LLM is guided by a textual description of your tables and columns so queries stay aligned with the actual database schema.

---

## Tech Stack

**Frontend**

- React + TypeScript (Vite)
- Tailwind CSS for styling
- Axios for HTTP requests

**Backend**

- Python + FastAPI
- SQLAlchemy (with PostgreSQL driver) for DB access 
- LLM API for natural‑language → SQL generation

**Database & Infra**

- Neon serverless PostgreSQL
- Railway (or similar) for backend deployment
- Vercel (or similar) for frontend hosting

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/genai-sql.git
cd genai-sql
```
### 2. Environment variables
Create a .env file in the backend directory:

```bash
DATABASE_URL=postgresql://user:password@host:port/dbname
OPENAI_API_KEY=your_api_key_here
```
Create a .env file in the frontend directory:

```bash
VITE_API_BASE_URL=https://your-backend-url.com
```
### 3. Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 4. Frontend setup

```bash
cd frontend
npm install
npm run dev
```
Open the printed localhost URL to access the GENAI SQL UI.

---
### Project Structure

```bash
genai-sql/
  frontend/
    src/
      components/
      App.tsx
  backend/
    app/
      api/
      db/
      core/
      main.py
```

## License

This project is released under the **MIT License**. You are free to use, modify, and distribute the code, provided that the original copyright notice and this permission notice are included in all copies or substantial portions of the software.


