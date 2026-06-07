path = r"e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

old = "const upd = (f: keyof FormState, v: string) => setForm((s) => ({ ...s, [f]: v }));\n\n\n\n  async function runCompliance"
new_code = "\n".join([
    "const upd = (f: keyof FormState, v: string) => setForm((s) => ({ ...s, [f]: v }));",
    "",
    "  async function submitToSponsorInbox() {",
    "    try {",
    '      await fetch("/api/sponsor-inbox", {',
    '        method: "POST",',
    '        headers: { "Content-Type": "application/json" },',
    "        body: JSON.stringify({",
    "          assetName:      form.assetName,",
    "          assetType:      form.assetType,",
    "          description:    form.description,",
    "          totalSupply:    form.totalSupply,",
    "          unitPrice:      form.unitPrice,",
    "          prospectusText: form.prospectusText,",
    "          invoiceText:    form.invoiceText,",
    "          contractText:   form.contractText,",
    "        }),",
    "      });",
    "    } catch { /* non-critical */ }",
    "  }",
    "",
    "  async function runCompliance",
])

assert old in src, "not found"
src = src.replace(old, new_code, 1)
with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("Done")
