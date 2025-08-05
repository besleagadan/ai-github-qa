import subprocess
from app.core.config import settings
from openai import OpenAI

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def build_prompt(chunks: list, question: str) -> str:
    context = "\n\n".join(f"# File: {meta['path']}, Chunk {meta['chunk_index']}\n{chunk}" for chunk, meta in chunks)

    prompt = f"""
You are a senior Python developer assistant.
A user is asking a question about a GitHub repo.
Below is relevant code from the repo.

{context}

Now, answer the user's question clearly and professionally.

Question: {question}
Answer:
""".strip()

    return prompt

def get_answer_from_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


# def get_answer_from_llm(prompt: str, model: str = "llama2") -> str:
#     process = subprocess.run(
#         ["ollama", "run", model],
#         input=prompt.encode("utf-8"),
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     if process.returncode != 0:
#         raise RuntimeError(f"Ollama CLI error: {process.stderr.decode()}")

#     output = process.stdout.decode("utf-8").strip()
#     return output
