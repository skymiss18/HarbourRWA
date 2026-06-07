import os, glob

pages = glob.glob(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\**\page.tsx', recursive=True)
pages = [p for p in pages if not p.endswith(r'app\src\app\page.tsx')]

replacements = [
    ('"#07111f"', '"#f7f5f0"'),
    ('"#03080f"', '"#f7f5f0"'),
    ('"#061220"', '"#f3f1eb"'),
    ('"#0b1628"', '"#ffffff"'),
    ('"#091525"', '"#ffffff"'),
    ('"#0d1e35"', '"#f3f1eb"'),
    ('"1px solid #1d3a5c"', '"1px solid rgba(0,0,0,0.10)"'),
    ('"1px solid #0e1e2e"', '"1px solid rgba(0,0,0,0.08)"'),
    ('"1px solid #162840"', '"1px solid rgba(0,0,0,0.09)"'),
    ('"#e8f1ff"', '"#111111"'),
    ('"#c8d8e8"', '"#222222"'),
    ('"#b8cfe8"', '"#333333"'),
    ('"#a8c4e0"', '"#444444"'),
    ('"#94b3cc"', '"#555555"'),
    ('"#7594b4"', '"#666666"'),
    ('"#6b8aaa"', '"#555555"'),
    ('"#6a8aaa"', '"#555555"'),
    ('"#4a8abf"', '"#555555"'),
    ('"#7a96b2"', '"#666666"'),
    ('"#3a5a7a"', '"#888888"'),
    ('"#4a6480"', '"#888888"'),
    ('"#2e4a68"', '"#aaaaaa"'),
    ('"#5a7a9a"', '"#666666"'),
    ('"#60a5fa"', '"#1a56db"'),
    ('"#3b82f6"', '"#1a56db"'),
]

count = 0
for path in pages:
    with open(path, 'r', encoding='utf-8') as f:
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
