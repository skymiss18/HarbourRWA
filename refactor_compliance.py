#!/usr/bin/env python3
"""Refactor compliance page: left sidebar inbox list + right form+results layout."""
import sys, re

filepath = r'e:\Repos\TheTuringTestHackathon2026\app\src\app\compliance\page.tsx'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# ─── Change 1: Replace pendingSubmission state + useEffect with submissions list ───
old1 = (
    '  // Pending submission from Issuer (persisted via /api/sponsor-inbox)\n'
    '  type PendingSubmission = { id: string; assetName: string; assetType: string; totalSupply: string; unitPrice: string; prospectusText: string; submittedAt: string; reference: string; issuer: string };\n'
    '  const [pendingSubmission, setPendingSubmission] = useState<PendingSubmission | null>(null);\n'
    '\n'
    '  useEffect(() => {\n'
    '    fetch("/api/sponsor-inbox")\n'
    '      .then((r) => r.json() as Promise<{ submissions: PendingSubmission[] }>)\n'
    '      .then(({ submissions }) => { if (submissions.length > 0) setPendingSubmission(submissions[submissions.length - 1]); })\n'
    '      .catch(() => {/* ignore */});\n'
    '  }, []);'
)

new1 = (
    '  // Inbox submissions from Issuer (persisted via /api/sponsor-inbox)\n'
    '  type PendingSubmission = { id: string; assetName: string; assetType: string; totalSupply: string; unitPrice: string; prospectusText: string; submittedAt: string; reference: string; issuer: string };\n'
    '  const [submissions,        setSubmissions]        = useState<PendingSubmission[]>([]);\n'
    '  const [selectedSubmission, setSelectedSubmission] = useState<PendingSubmission | null>(null);\n'
    '\n'
    '  useEffect(() => {\n'
    '    fetch("/api/sponsor-inbox")\n'
    '      .then((r) => r.json() as Promise<{ submissions: PendingSubmission[] }>)\n'
    '      .then(({ submissions }) => setSubmissions(submissions))\n'
    '      .catch(() => {/* ignore */});\n'
    '  }, []);\n'
    '\n'
    '  function handleSelectSubmission(sub: PendingSubmission) {\n'
    '    setSelectedSubmission(sub);\n'
    '    setAssetName(sub.assetName);\n'
    '    setAssetType((sub.assetType as AssetType) || "Bond");\n'
    '    setTotalSupply(sub.totalSupply);\n'
    '    setUnitPrice(sub.unitPrice);\n'
    '    setText(sub.prospectusText);\n'
    '    setResult(null);\n'
    '    setTradeResult(null);\n'
    '    setSfcSubmitted(false);\n'
    '    setError(null);\n'
    '  }\n'
    '\n'
    '  function handleDismissSubmission(sub: PendingSubmission) {\n'
    '    void fetch("/api/sponsor-inbox", { method: "DELETE", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ id: sub.id }) });\n'
    '    setSubmissions((prev) => prev.filter((s) => s.id !== sub.id));\n'
    '    if (selectedSubmission?.id === sub.id) setSelectedSubmission(null);\n'
    '  }'
)

assert old1 in content, "Pattern 1 not found"
content = content.replace(old1, new1, 1)
print("Change 1 (state section): OK")

# ─── Change 2: Replace return() opening through the Header div ───
# Find the return( statement and everything up to (not including) the Form comment
# Strategy: find return( index, find Form comment index, replace that slice

return_idx = content.index('\n  return (\n')
# Find the form comment - use a distinctive string that appears right before the form
form_comment_str = '\n      {/* \u2500\u2500 Form \u2500\u2500 */'
form_idx = content.index(form_comment_str)

# The old section is from return_idx to form_idx
old_section = content[return_idx:form_idx]

# Verify it contains the expected markers
assert 'max-w-[1200px]' in old_section, "max-w-[1200px] not in old section"
assert 'pendingSubmission' in old_section, "pendingSubmission not in old section"
assert 'Header' in old_section, "Header not in old section"

# Build the new opening section
# Note: Chinese text is preserved as UTF-8 string literals
new_section = (
    '\n'
    '  return (\n'
    '    <div className="max-w-[1400px] mx-auto px-4 sm:px-6 lg:px-8 py-8">\n'
    '\n'
    '      {/* \u2500\u2500 Page Header \u2500\u2500 */}\n'
    '      <div className="mb-6">\n'
    '        <div className="rounded-lg px-3 py-2.5 text-xs mb-4" style={{ background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.2)" }}>\n'
    '          <span className="font-semibold text-amber-700 uppercase tracking-wide text-[10px]">Sponsor (Type 6 LC) \u00b7 \u5408\u89c4\u590d\u6838 &amp; SFC \u53d1\u884c\u7533\u8bf7</span>\n'
    '          <p className="text-slate-600 mt-1">\u7531<strong className="text-amber-700">\u4fdd\u8350\u4eba\uff08Type 6 LC\uff09</strong>\u64cd\u4f5c\u3002\u4fdd\u8350\u4eba\u987b\u5728\u5411 SFC \u9012\u4ea4\u524d\u72ec\u7acb\u5b8c\u6210 AI \u5408\u89c4\u590d\u6838\uff0c\u5e76\u5c06\u5408\u89c4\u62a5\u544a\u548c\u5ba1\u8ba1\u8bc1\u660e\u4e00\u5e76\u63d0\u4ea4\u81f3 SFC\uff0c\u7533\u8bf7\u4ee3\u5e01\u53d1\u884c\u6388\u6743\uff08SFO s.103\uff09\u3002\u5408\u89c4\u7ed3\u679c\u9501\u5b9a\u81f3\u94fe\u4e0a ComplianceOracle.sol\uff0c\u4e0d\u53ef\u7bf9\u6539\u3002</p>\n'
    '        </div>\n'
    '        <h1 className="text-2xl font-bold text-gray-900 mb-1">\u5408\u89c4\u590d\u6838 &amp; \u5411 SFC \u9012\u4ea4\u53d1\u884c\u7533\u8bf7</h1>\n'
    '        <p className="text-sm text-slate-500">\n'
    '          {isTradeReceivable\n'
    '            ? "\u4e0a\u4f20\u53d1\u884c\u4eba\u7684\u5546\u4e1a\u53d1\u7968\u548c\u8d38\u6613\u5408\u540c\u3002AI \u5c06\u9a8c\u8bc1\u6587\u4ef6\u4e00\u81f4\u6027\u3001AML \u98ce\u9669\u53ca SFC \u4ee3\u5e01\u5316\u89c4\u5219\uff0c\u5408\u683c\u540e\u7531 Type 6 LC \u9012\u4ea4 SFC\u3002"\n'
    '            : "\u7c98\u8d34\u53d1\u884c\u4eba\u7684\u62db\u80a1\u8bf4\u660e\u4e66\u6216\u6761\u6b3e\u4e66\u3002AI \u5bf9\u7167 SFC \u516b\u9879\u89c4\u5219\u9010\u6761\u8bc4\u5206\uff0c\u8bc4\u5206\u901a\u8fc7\u540e\u7531 Type 6 LC \u5411 SFC \u9012\u4ea4\u53d1\u884c\u6388\u6743\u7533\u8bf7\u3002"}\n'
    '        </p>\n'
    '      </div>\n'
    '\n'
    '      <div className="flex gap-5 items-start">\n'
    '\n'
    '        {/* \u2500\u2500 Left sidebar: Inbox list \u2500\u2500 */}\n'
    '        <div className="w-64 shrink-0 sticky top-6">\n'
    '          <div className="rounded-lg overflow-hidden" style={{ border: "1px solid rgba(0,0,0,0.10)" }}>\n'
    '            <div className="px-3 py-2.5 flex items-center justify-between" style={{ background: "#f3f1eb", borderBottom: "1px solid rgba(0,0,0,0.08)" }}>\n'
    '              <span className="text-[11px] font-semibold text-slate-700 uppercase tracking-wide">\U0001F4E5 \u53d1\u884c\u4eba\u63d0\u4ea4\u961f\u5217</span>\n'
    '              {submissions.length > 0 && (\n'
    '                <span className="text-[10px] font-bold text-blue-700 rounded-full px-1.5 py-0.5" style={{ background: "rgba(29,78,216,0.1)" }}>{submissions.length}</span>\n'
    '              )}\n'
    '            </div>\n'
    '            {submissions.length === 0 ? (\n'
    '              <div className="px-3 py-8 text-center" style={{ background: "#ffffff" }}>\n'
    '                <p className="text-[11px] text-slate-400">\u6682\u65e0\u5f85\u5ba1\u6838\u63d0\u4ea4</p>\n'
    '                <p className="text-[10px] text-slate-300 mt-1">\u53d1\u884c\u4eba\u4ece /tokenize \u63d0\u4ea4\u540e\u4f1a\u5728\u6b64\u663e\u793a</p>\n'
    '              </div>\n'
    '            ) : (\n'
    '              <div style={{ background: "#ffffff" }}>\n'
    '                {submissions.map((sub) => {\n'
    '                  const isSelected = selectedSubmission?.id === sub.id;\n'
    '                  return (\n'
    '                    <div\n'
    '                      key={sub.id}\n'
    '                      onClick={() => handleSelectSubmission(sub)}\n'
    '                      className="px-3 py-3 cursor-pointer transition-colors relative group"\n'
    '                      style={{\n'
    '                        background: isSelected ? "rgba(29,78,216,0.06)" : "#ffffff",\n'
    '                        borderLeft: isSelected ? "3px solid #1d4ed8" : "3px solid transparent",\n'
    '                        borderBottom: "1px solid rgba(0,0,0,0.06)",\n'
    '                      }}\n'
    '                    >\n'
    '                      <div className="pr-5">\n'
    '                        <p className="text-xs font-semibold text-slate-800 leading-tight">{sub.assetName || "(Unnamed)"}</p>\n'
    '                        <p className="text-[11px] text-slate-500 mt-0.5">\n'
    '                          <span className="inline-block px-1.5 py-0.5 rounded text-[10px] font-medium mr-1"\n'
    '                            style={{ background: "rgba(29,78,216,0.08)", color: "#1d4ed8" }}>{sub.assetType}</span>\n'
    '                          {Number(sub.totalSupply).toLocaleString()} tokens\n'
    '                        </p>\n'
    '                        <p className="text-[10px] text-slate-400 mt-1">\n'
    '                          {new Date(sub.submittedAt).toLocaleString("en-GB", { timeZone: "Asia/Hong_Kong", month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" })} HKT\n'
    '                        </p>\n'
    '                      </div>\n'
    '                      <button\n'
    '                        onClick={(e) => { e.stopPropagation(); handleDismissSubmission(sub); }}\n'
    '                        className="absolute right-2 top-2 w-5 h-5 flex items-center justify-center rounded text-slate-300 hover:text-red-400 transition-colors text-xs opacity-0 group-hover:opacity-100"\n'
    '                        title="Dismiss"\n'
    '                      >\n'
    '                        \u00d7\n'
    '                      </button>\n'
    '                    </div>\n'
    '                  );\n'
    '                })}\n'
    '              </div>\n'
    '            )}\n'
    '          </div>\n'
    '        </div>\n'
    '\n'
    '        {/* \u2500\u2500 Main area: Form + Results \u2500\u2500 */}\n'
    '        <div className="flex-1 min-w-0 flex gap-8 items-start">\n'
    '          <div className={showRight ? "w-[420px] shrink-0" : "w-full max-w-2xl"}>\n'
    '\n'
)

content = content[:return_idx] + new_section + content[form_idx:]
print("Change 2 (layout opening): OK")

# ─── Change 3: Fix the end-of-left-column comment ───
# The old "end left column" div is now the "end form column"
old3 = '        </div>{/* \u2500\u2500 end left column \u2500\u2500 */}'
new3 = '          </div>{/* \u2500\u2500 end form column \u2500\u2500 */}'

assert old3 in content, f"Pattern 3 not found"
content = content.replace(old3, new3, 1)
print("Change 3 (column comment): OK")

# ─── Change 4: Fix indentation of right column ───
# The right column "showRight &&" section needs to stay as-is in indentation
# But its parent is now the "main area" flex div, not the outer flex
# The existing indentation (8 spaces for showRight) is fine since we're
# inside the main area flex (which is also at 8 spaces indentation)

# ─── Change 5: Fix closing tags - add missing close for main area ───
# Current end:
#   "      </div>\n\n    </div>\n\n  );\n\n}"
# New end:
#   "          </div>{/* end main area */}\n\n      </div>\n\n    </div>\n\n  );\n\n}"

old5 = '      </div>\n\n    </div>\n\n  );\n\n}'
new5 = (
    '          </div>{/* \u2500\u2500 end main area \u2500\u2500 */}\n'
    '\n'
    '      </div>{/* \u2500\u2500 end outer flex \u2500\u2500 */}\n'
    '\n'
    '    </div>\n'
    '\n'
    '  );\n'
    '\n'
    '}'
)

count5 = content.count(old5)
assert count5 == 1, f"Pattern 5 count: {count5} (expected 1)"
content = content.replace(old5, new5, 1)
print("Change 5 (closing tags): OK")

# Write back
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("\nDone! File written successfully.")
print(f"New line count: {content.count(chr(10))}")
