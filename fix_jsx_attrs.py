import re, os, glob

def fix_jsx_attrs(text):
    """Fix unclosed JSX attribute strings: attr="text... /> or attr="text..."""
    # Fix attribute value not closed: ="text... /> -> ="text..." />
    text = re.sub(r'(=")([^"]*?\.\.\.) />', r'\1\2" />', text)
    # Fix attribute value not closed at line end: ="text...\n -> ="text..."\n
    text = re.sub(r'(=")([^"]*?\.\.\.)(\s*\n)', r'\1\2"\3', text)
    # Fix: ="text...> -> ="text...">  
    text = re.sub(r'(=")([^"]*?\.\.\.)>', r'\1\2">', text)
    # Fix: placeholder="text... followed by next line with />
    return text

pages = glob.glob(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\**\page.tsx', recursive=True)

count = 0
for path in pages:
    with open(path, encoding='utf-8') as f:
        text = f.read()
    orig = text
    text = fix_jsx_attrs(text)
    if text != orig:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        count += 1
        name = os.path.basename(os.path.dirname(path))
        print(f'Fixed JSX attrs: {name}/page.tsx')

print(f'Done. Fixed {count} files.')
