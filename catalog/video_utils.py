
import re
from urllib.parse import urlparse


def get_youtube_embed_url(value):
    if not value:
        return None

    value = value.strip()

    # Если вставлен полный iframe, извлекаем src
    match = re.search(
        r'<iframe\b[^>]*\bsrc=["\']([^"\']+)["\']',
        value,
        re.IGNORECASE
    )

    if match:
        value = match.group(1)

    parsed = urlparse(value)

    host = parsed.netloc.lower().removeprefix("www.")

    if host not in ("youtube.com", "m.youtube.com"):
        return None

    if not parsed.path.startswith("/embed/"):
        return None

    video_id = parsed.path.split("/")[2]

    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", video_id):
        return None

    return f"https://www.youtube.com/embed/{video_id}"
