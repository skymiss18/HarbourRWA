import glob

files = glob.glob(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\**\page.tsx', recursive=True)
for f in files:
    with open(f, encoding='utf-8') as fh:
        lines = fh.readlines()
    name = f.split('\\')[-2]
    for i, line in enumerate(lines, 1):
        stripped = line.rstrip()
        # Skip comments, imports, and empty lines
        s = stripped.strip()
        if not s or s.startswith('//') or s.startswith('*') or s.startswith('import'):
            continue
        # Count unescaped double quotes
        count = 0
        j = 0
        while j < len(stripped):
            if stripped[j] == '\\':
                j += 2
                continue
            if stripped[j] == '"':
                count += 1
            j += 1
        if count % 2 == 1:
            print(f'{name}:{i}: {stripped[-70:]}')
