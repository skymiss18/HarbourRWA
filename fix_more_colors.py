import os, glob

pages = glob.glob(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\**\page.tsx', recursive=True)

replacements = [
    # More dark backgrounds missed in first pass
    ('"#060f1c"', '"#ffffff"'),
    ('"#080f1c"', '"#ffffff"'),
    ('"#0a1a2e"', '"#f3f1eb"'),
    ('"#0a1524"', '"#f0ede6"'),
    ('"#0f2035"', '"#e8e4dd"'),
    ('"#0d1a35"', '"#ffffff"'),
    # Borders
    ('"1px solid #0f2035"', '"1px solid rgba(0,0,0,0.08)"'),
    ('"1px solid #2a4a70"', '"1px solid rgba(0,0,0,0.10)"'),
    ('"1px dashed #1d3a5c"', '"1px dashed rgba(0,0,0,0.15)"'),
    ('"1px solid #3b82f6"', '"1px solid #1a56db"'),
    ('"2px solid #16a34a"', '"1px solid #16a34a"'),
    # Input text color on dark bg
    ('"#d6e0ef"', '"#222222"'),
    # Dark green bg (success states) -> light green tint
    ('"#0d2a1a"', '"rgba(22,163,74,0.07)"'),
    ('"#0d6e4e"', '"rgba(22,163,74,0.08)"'),
    # Tailwind hover classes with dark bg
    ('hover:bg-[#0d1e35]', 'hover:bg-gray-100'),
    ('hover:bg-[#0d2035]', 'hover:bg-gray-100'),
]

count = 0
for path in pages:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    orig = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        count += 1
        name = os.path.basename(os.path.dirname(path))
        print(f'Updated: {name}/page.tsx')

print(f'Done. Updated {count} files.')
