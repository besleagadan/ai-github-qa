import tiktoken

def split_code_into_chunks(text: str, max_tokens: int = 300, overlap: int = 50) -> list:
    encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
    tokens = encoding.encode(text)

    chunks = []
    start = 0
    end = max_tokens

    while start < len(tokens):
        chunk_tokens = tokens[start:end]
        chunk_text = encoding.decode(chunk_tokens)
        chunks.append(chunk_text)
        start = end - overlap
        end = start + max_tokens

    return chunks
