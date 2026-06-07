with open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

marker = 'authorisation.</p>\n\n          <DocumentUploadField label="Commercial Invoice"'
replacement = 'authorisation.</p>\n\n          </div>\n\n          <DocumentUploadField label="Commercial Invoice"'

if marker in content:
    content = content.replace(marker, replacement, 1)
    with open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed!')
else:
    print('Not found - dumping area:')
    idx = content.find('authorisation.</p>')
    print(repr(content[idx:idx+200]))
