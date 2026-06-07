with open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\compliance\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
problems = []
for i, line in enumerate(lines, 1):
    stripped = line.strip()
    if stripped == '...' or (stripped.startswith('...') and len(stripped) < 10):
        problems.append((i, repr(line[:80])))
print(f'Found {len(problems)} problem lines')
for lnum, content in problems[:20]:
    print(f'  Line {lnum}: {content}')
