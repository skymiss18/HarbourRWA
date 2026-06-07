import os

root = r'e:\Repos\TheTuringTestHackathon2026'
exts = {'.tsx', '.ts', '.json', '.md', '.txt', '.mjs', '.js', '.sol', '.py'}

replacements = [
    # Jurisdiction code defaults
    ('?? "SG"', '?? "SG"'),
    ('|| "SG"', '|| "SG"'),
    ('["SG"]', '["SG"]'),
    ('"taxResidency": "SG"', '"taxResidency": "SG"'),
    ('taxResidency: "SG"', 'taxResidency: "SG"'),
    # UI labels
    ('PI-qualified', 'PI-qualified'),
    ('Asia Grade-A office REIT', 'Asia Grade-A office REIT'),
    ('SFC-Regulated', 'SFC-Regulated'),
    ('SFC compliance analyst', 'SFC compliance analyst'),
    ('SFC-certified AML', 'SFC-certified AML'),
    ('SFC-certified legal', 'SFC-certified legal'),
    ('SFC tokenisation expert', 'SFC tokenisation expert'),
    ('Asia REITs', 'Asia REITs'),
    ('Asia REIT', 'Asia REIT'),
    ('Asia infrastructure bond', 'Asia infrastructure bond'),
    ('Asia infrastructure', 'Asia infrastructure'),
    ('institutional RWA', 'institutional RWA'),
    ('legally qualified counsel', 'legally qualified counsel'),
    ('applicable law', 'applicable law'),
    ('Singapore courts', 'Singapore courts'),
    ('regulatory authority lists', 'regulatory authority lists'),
    ('SIAC arbitration', 'SIAC arbitration'),
    ('SIAC', 'SIAC'),
    ('SGS Limited', 'SGS Limited'),
    ('SGS-SG-', 'SGS-SG-'),
    ('Prudential Asia', 'Prudential Asia'),
    # Jurisdiction field values
    ('Jurisdiction: `SG`', 'Jurisdiction: `SG`'),
    ('Jurisdiction: `SG`', 'Jurisdiction: `SG`'),
    ('Jurisdiction: SG', 'Jurisdiction: SG'),
    ('Incorporated in Singapore', 'Incorporated in Singapore'),
    ("| `SG` |", "| `SG` |"),
    ("`SG`", "`SG`"),
    # JargonTooltip
    ("primary legislation", "primary legislation"),
    ("independent statutory body", "independent statutory body"),
    ('law requiring', 'law requiring'),
    # Chinese text
    ('亚太合规壁垒', '亚太合规壁垒'),
    ('上传 Asia REIT', '上传 Asia REIT'),
    ('Asia REITs（房地产投资信托）', 'Asia REITs（房地产投资信托）'),
    ('**Asia REITs', '**Asia REITs'),
    ('What asset? Asia infrastructure', 'What asset? Asia infrastructure'),
    # Embedded prospectus text in JSON files still referencing HK
    ('SFC-Authorised', 'SFC-Authorised'),
    ('Incorporated in Singapore', 'Incorporated in Singapore'),
    # layout.tsx / page.tsx
    ('for professional investors', 'for professional investors'),
    ('professional investors', 'professional investors'),
    # compliance.ts / trade-docs.ts
    ('SG or other recognised jurisdiction', 'SG or other recognised jurisdiction'),
    ('SIAC preferred', 'SIAC preferred'),
    # doc files
    ('institutional', 'institutional'),
    ('an Asia infrastructure', 'an Asia infrastructure'),
]

changed_files = []
for dirpath, dirnames, files in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ('node_modules', '.next', '.git', '__pycache__', 'typechain-types', 'artifacts')]
    for fname in files:
        if os.path.splitext(fname)[1] not in exts:
            continue
        fpath = os.path.join(dirpath, fname)
        try:
            with open(fpath, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception:
            continue
        new_content = content
        for src, dst in replacements:
            new_content = new_content.replace(src, dst)
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            changed_files.append(fname)
            print(f'Updated: {fname}')

print(f'\nDone. {len(changed_files)} files updated.')
