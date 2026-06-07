import re

def fix_broken_strings(text):
    """
    Fix broken string literals where closing quote was consumed by encoding corruption.
    Pattern: "text..." followed by : or , without closing quote.
    """
    # Fix ternary: "text... : "other  -->  "text..." : "other
    # The pattern: opening quote, content, ..., then space colon space (ternary)
    text = re.sub(r'"([^"\\]*?\.\.\.) : "', r'"\1" : "', text)
    # Fix ternary without space: "text... :"
    text = re.sub(r'"([^"\\]*?\.\.\.) :"', r'"\1" :"', text)
    # Fix array: "text..., "next  -->  "text...", "next
    text = re.sub(r'"([^"\\]*?\.\.\.)(, )"', r'"\1"\2"', text)
    # Fix broken: "text...] --> "text..."]
    text = re.sub(r'"([^"\\]*?\.\.\.)(\])', r'"\1"\2', text)
    # Fix: "text...> --> "text...">
    text = re.sub(r'"([^"\\]*?\.\.\.) >', r'"\1" >', text)
    # Fix ternary where closing brace follows: "text... : n}  -> "text..." : n}  (n = non-string)
    text = re.sub(r'"([^"\\]*?\.\.\.) : ([a-zA-Z0-9_}])', r'"\1" : \2', text)
    # Fix icon: icon: "..., -> icon: "...", (emoji was eaten)
    text = re.sub(r"(icon: )\"(\.\.\.)(\s*,)", r'\1"\2"\3', text)
    return text

import os, glob

pages = glob.glob(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\**\page.tsx', recursive=True)

count = 0
for path in pages:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    orig = text
    text = fix_broken_strings(text)
    if text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        count += 1
        name = os.path.basename(os.path.dirname(path))
        print(f'Fixed: {name}/page.tsx')

print(f'Done. Fixed {count} files.')
