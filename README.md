# AI GitHub Q&A

A simple AI-powered tool to ask natural language questions about any public GitHub repository.

It fetches Python source files, chunks them, embeds them into a vector DB, and answers your questions using OpenAI’s GPT-3.5.

---

## What It Does

- Fetches all `.py` files from any public GitHub repo
- Splits the code into token-based chunks
- Stores them in a vector database using OpenAI embeddings
- Lets you ask: “What does X file do?” or “How does login work?”
- Finds matching code blocks and asks GPT-3.5 to explain them

This shows real-world use of RAG (Retrieval-Augmented Generation) for working with unstructured code data.

---

## How to Run It

1. **Install requirements**

2. **Set your OpenAI API key**

    ```ini
    OPENAI_API_KEY=your-key-here
    ```

3. **Run the Streamlit app**

    ```bash
    streamlit run ui/app.py
    ```

4. **Try it out**

- Paste any public GitHub repo URL (e.g. `https://github.com/tiangolo/fastapi`)
- Ask a question like:
    - What does the main.py file do?
    - How does user authentication work?

---

## Tech Stack

- `Python`
- `GitHub REST API`
- `ChromaDB` – local vector DB (DuckDB + Parquet)
- `OpenAI API` – embeddings + answers
- `tiktoken` – token-level chunking
- `Streamlit` – simple UI

---

## Screenshot

<p align="center">
    <img src="https://github.com/besleagadan/ai-github-qa/blob/main/src/imgs/Screenshot%202025-08-06%20at%2011.36.46.png" alt="Screenshot">
</p>

---

## Setup Details (Phases)

### Phase 1 — Project Setup

- Structured the app into `/app` and `/ui` folders
- Installed all needed libraries: `openai`, `chromadb`, `requests`, `streamlit`, `tiktoken`
- Created a `requirements.txt` for clean install

### Phase 2 — Fetch GitHub Repo Code

- Used the GitHub API to list all `.py` files
- Downloaded raw code content
- Built a dict: `{file_path: source_code}`

### Phase 3 — Chunk the Code

- Split code using `tiktoken` into 300-token chunks
- Overlap: 50 tokens
- Prepped for LLM-friendly processing

### Phase 4 — Embed and Store in Vector DB

- Used OpenAI's `text-embedding-3-small` to embed chunks
- Stored in ChromaDB with metadata (path, index)
- Enabled persistent local storage

### Phase 5 — Ask a Question + Retrieve Chunks

- Embedded user's question
- Retrieved top 5 similar chunks from Chroma
- Passed them to the LLM

### Phase 6 — Generate Answer with LLM

- Combined code + question into a system prompt
- Sent to GPT-3.5-turbo
- Returned a natural-language explanation

### Phase 7 — Build the UI with Streamlit

- Input field for GitHub repo
- Load, process, and embed code automatically
- Input box for questions
- Answers + code chunks displayed

---

## Future Ideas

- Add GitHub auth to access private repos
- Support other languages (JS, Go, etc.)
- Add conversation history
- Switch to LangChain / LlamaIndex (optional)
