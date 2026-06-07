import glob, re

files = glob.glob(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\**\page.tsx', recursive=True)

# Colors to replace globally (in all contexts)
replacements = [
    ('#060f1c', '#ffffff'),
    ('#080f1c', '#ffffff'),
    ('#0a1a2e', '#f3f1eb'),
    ('#0d1a35', '#f3f1eb'),
    ('#0d1e35', '#f3f1eb'),
    ('#0d2a1a', 'rgba(22,163,74,0.08)'),
    ('#0d6e4e', 'rgba(22,163,74,0.08)'),
    ('#0e1e2e', '#f3f1eb'),
    ('#0f2035', 'rgba(0,0,0,0.08)'),
    ('#14263d', 'rgba(0,0,0,0.08)'),
    ('#1d3a5c', 'rgba(0,0,0,0.12)'),
    ('#2a4a70', 'rgba(0,0,0,0.12)'),
    ('hover:bg-[#0d1e35]', 'hover:bg-gray-100'),
    ('hover:bg-[#0f2035]', 'hover:bg-gray-100'),
    ('hover:bg-[#080f1c]', 'hover:bg-gray-100'),
    ('hover:bg-[#0e1e2e]', 'hover:bg-gray-100'),
]

total_changes = 0
for fpath in files:
    with open(fpath, encoding='utf-8') as f:
        text = f.read()
    original = text
    for old, new in replacements:
        text = text.replace(old, new)
    if text != original:
        count = sum(original.count(old) for old, _ in replacements)
        total_changes += 1
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(text)
        name = fpath.split('\\')[-2]
        print(f'Updated: {name}/page.tsx')

print(f'\nDone. Updated {total_changes} files.')
