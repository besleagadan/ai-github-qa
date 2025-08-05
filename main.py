from app.github_fetcher import fetch_repo_code
from app.chunker import split_code_into_chunks
from app.embedder import embed_text
from app.vector_store import add_to_vector_store, search_similar_chunks
from app.qa_engine import build_prompt, get_answer_from_llm

# if __name__ == "__main__":
#     branch = "main"

#     code_data = fetch_repo_code(branch)
#     all_chunks = []
#     all_meta = []

#     for path, content in code_data.items():
#         chunks = split_code_into_chunks(content)
#         for i, chunk in enumerate(chunks):
#             all_chunks.append(chunk)
#             all_meta.append({
#                 "path": path,
#                 "chunk_index": i
#             })

#     add_to_vector_store(all_chunks, all_meta)
#     print(f"Stored {len(all_chunks)} chunks in vector DB.")


# if __name__ == "__main__":
#     question = "What does the main.py file do?"
#     results = search_similar_chunks(question)

#     print(f"\nTop results for: '{question}'\n")
#     for i, (chunk, meta) in enumerate(results, 1):
#         print(f"\n--- Result {i} ---")
#         print(f"File: {meta['path']}, Chunk #{meta['chunk_index']}")
#         print(chunk[:300] + "...")


if __name__ == "__main__":
    question = "What is the purpose of the main.py file?"

    chunks = search_similar_chunks(question)
    prompt = build_prompt(chunks, question)
    answer = get_answer_from_llm(prompt)

    print(f"\nQ: {question}\n")
    print(f"A:\n{answer}")
