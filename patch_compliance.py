
path = r"e:\Repos\TheTuringTestHackathon2026\app\src\app\compliance\page.tsx"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

# 1. After the loading useEffect, insert inbox state + functions
old1 = '  }, [loading]);\r\n\r\n\r\n\r\n  const disabled'
new1 = '  }, [loading]);\r\n\r\n  // \u2500\u2500 Sponsor inbox \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\r\n  const [submissions,        setSubmissions]        = useState<PendingSubmission[]>([]);\r\n  const [selectedSubmission, setSelectedSubmission] = useState<PendingSubmission | null>(null);\r\n\r\n  async function loadSubmissions() {\r\n    try {\r\n      const res = await fetch("/api/sponsor-inbox");\r\n      const data = await res.json();\r\n      setSubmissions(data.submissions ?? []);\r\n    } catch { /* ignore */ }\r\n  }\r\n\r\n  function handleSelectSubmission(sub: PendingSubmission) {\r\n    setSelectedSubmission(sub);\r\n    setAssetName(sub.assetName);\r\n    setAssetType(sub.assetType as AssetType);\r\n    if (sub.assetType === "TradeReceivable") {\r\n      if (sub.invoiceText)  setInvoiceText(sub.invoiceText);\r\n      if (sub.contractText) setContractText(sub.contractText);\r\n    } else {\r\n      if (sub.prospectusText) setText(sub.prospectusText);\r\n    }\r\n    if (sub.totalSupply) setTotalSupply(sub.totalSupply);\r\n    if (sub.unitPrice)   setUnitPrice(sub.unitPrice);\r\n    setResult(null);\r\n    setTradeResult(null);\r\n    setError(null);\r\n  }\r\n\r\n  useEffect(() => { void loadSubmissions(); }, []);\r\n\r\n\r\n\r\n  const disabled'

assert old1 in src, f"Step 1 search not found"
src = src.replace(old1, new1, 1)
assert 'loadSubmissions' in src, "Step 1 failed"
print("Step 1 OK")

# 2. Change outer return div + add sidebar
old2 = '    <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-12">\r\n\r\n      <div className="flex gap-10 items-start">\r\n\r\n        <div className={showRight ? "w-[460px] shrink-0" : "w-full max-w-2xl mx-auto"}>'
new2 = (
    '    <div className="max-w-[1500px] mx-auto px-4 sm:px-6 lg:px-8 py-8">\r\n'
    '      <div className="flex gap-5 items-start">\r\n'
    '\r\n'
    '        {/* \u2500\u2500 Left sidebar: issuer submission queue \u2500\u2500 */}\r\n'
    '        <div className="w-56 shrink-0 sticky top-6">\r\n'
    '          <div className="rounded-xl p-3" style={{ background: "#ffffff", border: "1px solid rgba(0,0,0,0.10)" }}>\r\n'
    '            <div className="flex items-center justify-between pb-2 mb-2" style={{ borderBottom: "1px solid rgba(0,0,0,0.06)" }}>\r\n'
    '              <span className="text-[11px] font-semibold text-slate-700">\U0001f4e5 \u53d1\u884c\u4eba\u63d0\u4ea4\u961f\u5217</span>\r\n'
    '              <span className="text-[10px] text-slate-400">{submissions.length} \u9879</span>\r\n'
    '            </div>\r\n'
    '            {submissions.length === 0 ? (\r\n'
    '              <p className="text-[11px] text-slate-400 text-center py-4">\u6682\u65e0\u5f85\u5ba1\u6838\u63d0\u4ea4</p>\r\n'
    '            ) : (\r\n'
    '              <div className="space-y-1">\r\n'
    '                {submissions.map((sub) => (\r\n'
    '                  <button key={sub.id} type="button" onClick={() => handleSelectSubmission(sub)}\r\n'
    '                    className="w-full text-left rounded-lg px-2.5 py-2 transition-colors"\r\n'
    '                    style={{\r\n'
    '                      background: selectedSubmission?.id === sub.id ? "rgba(26,86,219,0.07)" : "transparent",\r\n'
    '                      border: `1px solid ${selectedSubmission?.id === sub.id ? "rgba(26,86,219,0.3)" : "transparent"}`,\r\n'
    '                    }}>\r\n'
    '                    <div className="text-[11px] font-semibold text-slate-800 truncate">{sub.assetName || "\uff08\u672a\u547d\u540d\uff09"}</div>\r\n'
    '                    <div className="flex items-center justify-between mt-0.5 gap-1">\r\n'
    '                      <span className="text-[10px] text-slate-500">{sub.assetType}</span>\r\n'
    '                      <span className="text-[10px] text-slate-400">{new Date(sub.receivedAt).toLocaleDateString("zh-HK")}</span>\r\n'
    '                    </div>\r\n'
    '                    {sub.issuer && <div className="text-[10px] text-slate-400 truncate mt-0.5">{sub.issuer}</div>}\r\n'
    '                  </button>\r\n'
    '                ))}\r\n'
    '              </div>\r\n'
    '            )}\r\n'
    '            <button type="button" onClick={loadSubmissions}\r\n'
    '              className="w-full mt-2 text-[10px] text-slate-500 hover:text-slate-700 py-1.5 rounded transition-colors"\r\n'
    '              style={{ border: "1px solid rgba(0,0,0,0.08)" }}>\r\n'
    '              \u5237\u65b0\r\n'
    '            </button>\r\n'
    '          </div>\r\n'
    '        </div>\r\n'
    '\r\n'
    '        {/* \u2500\u2500 Main area: form + results \u2500\u2500 */}\r\n'
    '        <div className="flex-1 min-w-0 flex gap-8 items-start">\r\n'
    '        <div className={showRight ? "w-[460px] shrink-0" : "w-full max-w-2xl"}>'
)

assert old2 in src, f"Step 2 search not found"
src = src.replace(old2, new2, 1)
assert 'max-w-[1500px]' in src, "Step 2 failed"
print("Step 2 OK")

# 3. Close the extra wrapper div at the end
old3 = '    </div>\r\n  </div>\r\n  );\r\n}'
new3 = '        </div>{/* \u2500\u2500 end main area \u2500\u2500 */}\r\n    </div>\r\n  </div>\r\n  );\r\n}'

assert old3 in src, f"Step 3 search not found"
src = src.replace(old3, new3, 1)
assert 'end main area' in src, "Step 3 failed"
print("Step 3 OK")

with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("Done.")
