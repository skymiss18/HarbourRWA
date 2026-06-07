with open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\regulator\page.tsx', encoding='utf-8') as f:
    text = f.read()

# Replace icon: "..." sequentially with appropriate icons
icons = [
    '\U0001f4b0',  # 💰 money bag - Tokens Issued
    '\U0001f464',  # 👤 person - KYC Applications
    '\u2713',      # ✓ checkmark - Compliance Pass Rate
    '\U0001f4d1',  # 📑 notepad - On-Chain Audit Records
    '\U0001f464',  # 👤 person - KYC Review
    '\u2705',      # ✅ check mark button - Verify Compliance
    '\U0001f4cb',  # 📋 clipboard - Contract Audit
]

count = 0
for icon in icons:
    old = 'icon: "...",'
    new = f'icon: "{icon}",'
    if old in text:
        text = text.replace(old, new, 1)
        count += 1

with open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\regulator\page.tsx', 'w', encoding='utf-8') as f:
    f.write(text)
print(f'Fixed {count} icons.')
