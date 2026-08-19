from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import json, re, shutil, time, urllib.parse, urllib.request

ROOT = Path(__file__).parent
SOURCE, TARGET = ROOT / "en", ROOT / "fr"
cache = {}
protected_re = re.compile(
    r"(`[^`]*`|https?://[^\s)\]]+|/[\w$.-]+(?:/[\w$.-]+)*|"
    r"\b(?:NomadBill|Stripe|Plaid|Nylas|Resend|pdfme|Supabase|CSV|JSON|PDF|REST|"
    r"API|VAT|IBAN|HMAC-SHA256|OCR|SaaS|PostgreSQL|Realtime)\b)"
)
visible_attr_re = re.compile(r'\b(title|description|cta)="([^"]*)"')


def request_translation(text):
    if not text.strip() or not re.search(r"[A-Za-z]", text):
        return text
    if text in cache:
        return cache[text]
    query = urllib.parse.urlencode(
        {"client": "gtx", "sl": "en", "tl": "fr", "dt": "t", "q": text}
    )
    url = "https://translate.googleapis.com/translate_a/single?" + query
    for attempt in range(6):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                payload = json.loads(response.read().decode())
            result = "".join(part[0] for part in payload[0] if part[0])
            cache[text] = result
            return result
        except Exception:
            if attempt == 5:
                raise
            time.sleep(1 + attempt)


def translate_text(text):
    if not text.strip():
        return text
    leading = text[: len(text) - len(text.lstrip())]
    trailing = text[len(text.rstrip()) :]
    values = []

    def hide(match):
        values.append(match.group())
        return f"ZXQ{len(values)-1}QXZ"

    result = request_translation(protected_re.sub(hide, text.strip()))
    for index, value in enumerate(values):
        result = result.replace(f"ZXQ{index}QXZ", value)
    return leading + result + trailing


def translate_attrs(line):
    return visible_attr_re.sub(
        lambda match: f'{match.group(1)}="{translate_text(match.group(2))}"', line
    )


def translate_line(line):
    newline = "\n" if line.endswith("\n") else ""
    raw = line[:-1] if newline else line
    if not raw.strip() or raw.strip() == "---":
        return line
    if raw.lstrip().startswith("<"):
        changed = translate_attrs(raw)
        if re.fullmatch(r"\s*</?\w+[^>]*>\s*", raw):
            return changed + newline
        raw = changed
    frontmatter = re.match(r"^(\s*(?:title|description):\s*)(.+)$", raw)
    if frontmatter and frontmatter.group(2) not in {">-", "|"}:
        return frontmatter.group(1) + translate_text(frontmatter.group(2)) + newline
    heading = re.match(r"^(\s*#{1,6}\s+)(.+)$", raw)
    if heading:
        return heading.group(1) + translate_text(heading.group(2)) + newline
    if re.fullmatch(r"\s*\|?(?:\s*:?-+:?\s*\|)+\s*", raw):
        return line
    if raw.strip().startswith("|"):
        return "|".join(translate_text(cell) for cell in raw.split("|")) + newline
    if re.fullmatch(r"\s*[-*]\s+`[^`]+`\s*", raw):
        return line.replace("/en/", "/fr/")
    return translate_text(raw).replace("/en/", "/fr/") + newline


def translate_file(source):
    target = TARGET / source.relative_to(SOURCE)
    if source.suffix == ".mdx":
        target.write_text(
            "".join(translate_line(line) for line in source.read_text().splitlines(True))
        )
    elif source.name == "openapi.yaml":
        output = []
        prose = re.compile(r"^(\s*(?:summary|description):\s*)(.+?)(\n?)$")
        for line in source.read_text().splitlines(True):
            match = prose.match(line)
            output.append(
                match.group(1) + translate_text(match.group(2)) + match.group(3)
                if match
                else line
            )
        target.write_text("".join(output))


if __name__ == "__main__":
    if TARGET.exists():
        shutil.rmtree(TARGET)
    shutil.copytree(SOURCE, TARGET)
    files = [path for path in SOURCE.rglob("*") if path.is_file()]
    with ThreadPoolExecutor(max_workers=8) as executor:
        list(executor.map(translate_file, files))
    print(f"Translated {len(files)} files")
