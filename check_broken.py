import os, glob

pages = glob.glob(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\**\page.tsx', recursive=True)

for path in pages:
    with open(path, encoding='utf-8') as f:
        lines = f.readlines()
    name = os.path.basename(os.path.dirname(path))
    found = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        # broken: "text..., "next  or  "text... : "next  etc
        if ('...,' in s and '"' in s) or ('... :' in s and '"' in s) or ('... >' in s):
            if not found:
                print(f'\n=== {name}/page.tsx ===')
                found = True
            print(f'  {i}: {s[:120]}')
