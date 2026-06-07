import os

root = r'e:\Repos\TheTuringTestHackathon2026'
exts = {'.tsx', '.ts', '.json', '.md', '.txt', '.mjs', '.js', '.sol', '.ps1', '.py'}

replacements = [
    # SFC header / branding
    ('Securities and Futures Commission', 'Securities and Futures Commission'),
    ('SFC', 'SFC'),
    ('SFC-Authorised', 'SFC-Authorised'),
    # Jurisdiction / law
    ('Laws of Singapore', 'Laws of Singapore'),
    ('courts of Singapore', 'courts of Singapore'),
    ('Jurisdiction: Singapore', 'Jurisdiction: Singapore'),
    ('jurisdiction of the courts of Singapore', 'jurisdiction of the courts of Singapore'),
    ('laws of Singapore', 'laws of Singapore'),
    ('registered in Singapore', 'registered in Singapore'),
    ('registered office at', 'registered office at'),  # no-op placeholder
    ('Incorporated in Singapore.', 'Incorporated in Singapore.'),
    # Company names
    ('Asia Property Trust Management Ltd', 'Asia Property Trust Management Ltd'),
    ('Asia Property Trust Management', 'Asia Property Trust Management'),
    ('Bank of China Trustees Limited', 'Bank of China Trustees Limited'),
    ('Standard Chartered Bank Limited', 'Standard Chartered Bank Limited'),
    ('HSBC', 'HSBC'),
    ('HSBC', 'HSBC'),
    ('Clifford Chance LLP', 'Clifford Chance LLP'),
    ('Clifford Chance LLP', 'Clifford Chance LLP'),
    ('Singapore International Arbitration Centre (SIAC)', 'Singapore International Arbitration Centre (SIAC)'),
    ('Singapore Port, Tanjong Pagar', 'Singapore Port, Tanjong Pagar'),
    ('Singapore Port.', 'Singapore Port.'),
    ('Singapore Land Registry and ACRA.', 'Singapore Land Registry and ACRA.'),
    ('Carbon Trust', 'Carbon Trust'),
    # Geography
    ('Marina Bay, Singapore', 'Marina Bay, Singapore'),
    ('Marina Bay, Singapore', 'Marina Bay, Singapore'),
    ('38/F, Two International Finance Centre, 8 Finance Street, Marina Bay, Singapore', '1 Harbourfront Ave, #12-01, Singapore 098632'),
    ('1 Harbourfront Ave,', '1 Harbourfront Ave,'),
    ('Times Square, Marina Bay, Singapore', 'Marina Bay, Singapore'),
    ('Singapore', 'Singapore'),
    ('Singapore real estate', 'Singapore real estate'),
    ('Asia infrastructure sector', 'Asia infrastructure sector'),
    ('Asia logistics infrastructure projects', 'Asia logistics infrastructure projects'),
    ('Asia logistics infrastructure', 'Asia logistics infrastructure'),
    ('Asia logistics', 'Asia logistics'),
    ('Asia infrastructure', 'Asia infrastructure'),
    ('60% allocated to Asia', '60% allocated to Asia'),
    ('Southeast Asia', 'Southeast Asia'),
    ('geographically concentrated in Asia-Pacific', 'geographically concentrated in Asia-Pacific'),
    ('Asia-Pacific exporters', 'Asia-Pacific exporters'),
    ('from Singapore.', 'from Singapore.'),
    ('in Singapore.', 'in Singapore.'),
    ('in Singapore,', 'in Singapore,'),
    ('Singapore,', 'Singapore,'),
    ('Singapore.', 'Singapore.'),
    # Interest rates
    ('SOFR swap arrangements are in place.', 'SOFR swap arrangements are in place.'),
    ('SOFR', 'SOFR'),
    # Generic remaining
    ('professional investors', 'professional investors'),
    ('SFC rules', 'SFC rules'),
    ('market interest rate', 'market interest rate'),
    ('Asia-Pacific', 'Asia-Pacific'),
    # Previously replaced HK shortcuts
    ('Securities and Futures Commission', 'Securities and Futures Commission'),
    ('senior securities lawyer', 'senior securities lawyer'),
    ('SFC REIT Code', 'SFC REIT Code'),
    ('Asia-Pacific commercial real estate', 'Asia-Pacific commercial real estate'),
    ('Asia-Pacific', 'Asia-Pacific'),
    ('between Asia-Pacific', 'between Asia-Pacific'),
    ('Governing law: SFC', 'Governing law: SFC'),
    ('Governing Law: SFC', 'Governing Law: SFC'),
    ("1 Queen's Road Central", "1 Queen's Road Central"),
    ('SFC-Authorised', 'SFC-Authorised'),
    ('60% Asia logistics', '60% Asia logistics'),
    ('en-GB', 'en-GB'),
    ('Valid National Identity Card or international passport', 'Valid National Identity Card or international passport'),
    ('code: "SG", label: "Singapore"', 'code: "SG", label: "Singapore"'),
    ('jurisdiction: "SG"', 'jurisdiction: "SG"'),
    ('"jurisdiction": "SG"', '"jurisdiction": "SG"'),
    # country of origin
    ('Country of Origin: Asia-Pacific', 'Country of Origin: Singapore'),
    ('Port of Loading: Asia-Pacific', 'Port of Loading: Singapore'),
    # address
    ('Singapore\n', 'Singapore\n'),
]

changed_files = []
for dirpath, dirnames, files in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in ('node_modules', '.next', '.git', '__pycache__')]
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
            changed_files.append(fpath)
            print(f'Updated: {fname}')

print(f'\nDone. {len(changed_files)} files updated.')
