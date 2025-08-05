import streamlit as st
from app.core.config import settings
from app.github_fetcher import fetch_repo_code
from app.chunker import split_code_into_chunks
from app.vector_store import add_to_vector_store, search_similar_chunks
from app.qa_engine import build_prompt, get_answer_from_llm


st.set_page_config(page_title="GitHub Q&A", layout="wide")
st.title("🧠 Ask Questions About Any GitHub Repo")

if "repo_loaded" not in st.session_state:
    st.session_state.repo_loaded = False

with st.form("repo_form"):
    repo_url = st.text_input("GitHub Repo URL (e.g. https://github.com/besleagadan/fastapi-project-skeleton)")
    submitted = st.form_submit_button("Load Repo")

    if submitted:
        owner_repo = repo_url.strip().replace("https://github.com/", "").split("/")
        owner, repo = owner_repo[0], owner_repo[1]

        try:
            code_data = fetch_repo_code(owner, repo)

            all_chunks = []
            all_meta = []

            for path, content in code_data.items():
                chunks = split_code_into_chunks(content)
                for i, chunk in enumerate(chunks):
                    all_chunks.append(chunk)
                    all_meta.append({"path": path, "chunk_index": i})

            add_to_vector_store(all_chunks, all_meta)
            st.session_state.repo_loaded = True
            st.success(f"Loaded {len(all_chunks)} code chunks from {repo}")
        except Exception as e:
            st.error(f"Failed to load repo: {e}")

if st.session_state.repo_loaded:
    st.markdown("### Ask a question about the repo")
    question = st.text_input("Your question")

    if question:
        try:
            results = search_similar_chunks(question)
            prompt = build_prompt(results, question)
            answer = get_answer_from_llm(prompt)

            st.markdown("### 💡 Answer")
            st.write(answer)

            with st.expander("🔍 Show Relevant Code Chunks"):
                for chunk, meta in results:
                    st.markdown(f"**File:** {meta['path']} — Chunk {meta['chunk_index']}")
                    st.code(chunk, language="python")

        except Exception as e:
            st.error(f"Error answering question: {e}")
