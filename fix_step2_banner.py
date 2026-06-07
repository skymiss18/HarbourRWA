with open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx', encoding='utf-8') as f:
    content = f.read()

old = 'The designated Intermediary (Type 6 LC\xa0/\xa0Sponsor) has completed AI compliance screening at the <strong className="text-amber-700">Compliance Check</strong> page. The score has been anchored on-chain to ComplianceOracle.sol and will be included in the SFC filing.'
new = 'The designated Intermediary (Type\xa06\xa0LC\xa0/\xa0Sponsor) has completed AI compliance screening at the <strong className="text-amber-700">Compliance Check</strong> page. The score has been anchored on-chain to ComplianceOracle.sol and filed with SFC as part of the issuance application. Confirm the result below before proceeding to check SFC approval status.'

if old in content:
    content = content.replace(old, new, 1)
    with open(r'e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Fixed!')
else:
    print('Not found')
