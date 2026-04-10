import re


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = remove_unicode(text)
    text = normalize_spaces(text)
    text = remove_duplicate_lines(text)
    text = fix_broken_sentences(text)
    text = remove_noise(text)

    return text.strip()


def remove_unicode(text: str) -> str:
    return text.encode("ascii", "ignore").decode()


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text)


def remove_duplicate_lines(text: str) -> str:
    lines = text.split("\n")
    seen = set()
    clean_lines = []

    for line in lines:
        line = line.strip()
        if line and line not in seen:
            clean_lines.append(line)
            seen.add(line)

    return "\n".join(clean_lines)


def fix_broken_sentences(text: str) -> str:
    return re.sub(r"\n(?=[a-z])", " ", text)


def remove_noise(text: str) -> str:
    text = re.sub(r"[•●■►]", "", text)
    text = re.sub(r"-{2,}", "-", text)
    text = re.sub(r"[!?.]{2,}", ".", text)
    return text