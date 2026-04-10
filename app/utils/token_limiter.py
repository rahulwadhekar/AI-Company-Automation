def limit_tokens(text: str, max_tokens: int = 3000):
    words = text.split()
    return " ".join(words[:max_tokens])