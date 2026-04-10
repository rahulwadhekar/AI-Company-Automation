def remove_duplicates(chunks):
    seen = set()
    unique = []

    for chunk in chunks:
        chunk = chunk.strip()
        if chunk and chunk not in seen:
            unique.append(chunk)
            seen.add(chunk)

    return unique