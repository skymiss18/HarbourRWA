path = r"e:\Repos\TheTuringTestHackathon2026\app\src\app\compliance\page.tsx"
with open(path, "r", encoding="utf-8") as f:
    src = f.read()

# Step 1: Add inbox state + functions after loading useEffect
old1 = "  }, [loading]);\n\n\n\n  const disabled"
new1 = "\n".join([
    "  }, [loading]);",
    "",
    "  // -- Sponsor inbox --",
    "  const [submissions,        setSubmissions]        = useState<PendingSubmission[]>([]);",
    "  const [selectedSubmission, setSelectedSubmission] = useState<PendingSubmission | null>(null);",
    "",
    "  async function loadSubmissions() {",
    "    try {",
    '      const res = await fetch("/api/sponsor-inbox");',
    "      const data = await res.json();",
    "      setSubmissions(data.submissions ?? []);",
    "    } catch { /* ignore */ }",
    "  }",
    "",
    "  function handleSelectSubmission(sub: PendingSubmission) {",
    "    setSelectedSubmission(sub);",
    "    setAssetName(sub.assetName);",
    "    setAssetType(sub.assetType as AssetType);",
    '    if (sub.assetType === "TradeReceivable") {',
    "      if (sub.invoiceText)  setInvoiceText(sub.invoiceText);",
    "      if (sub.contractText) setContractText(sub.contractText);",
    "    } else {",
    "      if (sub.prospectusText) setText(sub.prospectusText);",
    "    }",
    "    if (sub.totalSupply) setTotalSupply(sub.totalSupply);",
    "    if (sub.unitPrice)   setUnitPrice(sub.unitPrice);",
    "    setResult(null);",
    "    setTradeResult(null);",
    "    setError(null);",
    "  }",
    "",
    "  // eslint-disable-next-line react-hooks/exhaustive-deps",
    "  useEffect(() => { void loadSubmissions(); }, []);",
    "",
    "",
    "",
    "  const disabled",
])
assert old1 in src, "Step 1 not found"
src = src.replace(old1, new1, 1)
print("Step 1 OK")

# Step 2: Change layout + add sidebar
old2 = '    <div className="max-w-[1200px] mx-auto px-4 sm:px-6 lg:px-8 py-12">\n\n      <div className="flex gap-10 items-start">\n\n        <div className={showRight ? "w-[460px] shrink-0" : "w-full max-w-2xl mx-auto"}>'

sidebar = "\n".join([
    '    <div className="max-w-[1500px] mx-auto px-4 sm:px-6 lg:px-8 py-8">',
    '      <div className="flex gap-5 items-start">',
    "",
    "        {/* Left sidebar: issuer submission queue */}",
    '        <div className="w-56 shrink-0 sticky top-6">',
    '          <div className="rounded-xl p-3" style={{ background: "#ffffff", border: "1px solid rgba(0,0,0,0.10)" }}>',
    '            <div className="flex items-center justify-between pb-2 mb-2" style={{ borderBottom: "1px solid rgba(0,0,0,0.06)" }}>',
    '              <span className="text-[11px] font-semibold text-slate-700">\U0001f4e5 \u53d1\u884c\u4eba\u63d0\u4ea4\u961f\u5217</span>',
    '              <span className="text-[10px] text-slate-400">{submissions.length} \u9879</span>',
    "            </div>",
    "            {submissions.length === 0 ? (",
    '              <p className="text-[11px] text-slate-400 text-center py-4">\u6682\u65e0\u5f85\u5ba1\u6838\u63d0\u4ea4</p>',
    "            ) : (",
    '              <div className="space-y-1">',
    "                {submissions.map((sub) => (",
    '                  <button key={sub.id} type="button" onClick={() => handleSelectSubmission(sub)}',
    '                    className="w-full text-left rounded-lg px-2.5 py-2 transition-colors"',
    "                    style={{",
    '                      background: selectedSubmission?.id === sub.id ? "rgba(26,86,219,0.07)" : "transparent",',
    "                      border: `1px solid ${selectedSubmission?.id === sub.id ? \"rgba(26,86,219,0.3)\" : \"transparent\"}`,",
    "                    }}>",
    '                    <div className="text-[11px] font-semibold text-slate-800 truncate">{sub.assetName || "\u672a\u547d\u540d"}</div>',
    '                    <div className="flex items-center justify-between mt-0.5 gap-1">',
    '                      <span className="text-[10px] text-slate-500">{sub.assetType}</span>',
    '                      <span className="text-[10px] text-slate-400">{new Date(sub.receivedAt).toLocaleDateString("zh-HK")}</span>',
    "                    </div>",
    '                    {sub.issuer && <div className="text-[10px] text-slate-400 truncate mt-0.5">{sub.issuer}</div>}',
    "                  </button>",
    "                ))}",
    "              </div>",
    "            )}",
    '            <button type="button" onClick={loadSubmissions}',
    '              className="w-full mt-2 text-[10px] text-slate-500 hover:text-slate-700 py-1.5 rounded transition-colors"',
    '              style={{ border: "1px solid rgba(0,0,0,0.08)" }}>',
    "              \u5237\u65b0",
    "            </button>",
    "          </div>",
    "        </div>",
    "",
    "        {/* Main area: form + results */}",
    '        <div className="flex-1 min-w-0 flex gap-8 items-start">',
    '        <div className={showRight ? "w-[460px] shrink-0" : "w-full max-w-2xl"}>',
])

assert old2 in src, "Step 2 not found"
src = src.replace(old2, sidebar, 1)
print("Step 2 OK")

# Step 3: Close the wrapper div before end
old3 = "      </div>\n\n    </div>\n\n  );\n\n}\n"
new3 = "        </div>{/* end main area */}\n      </div>\n\n    </div>\n\n  );\n\n}\n"
assert old3 in src, "Step 3 not found"
src = src.replace(old3, new3, 1)
print("Step 3 OK")

with open(path, "w", encoding="utf-8") as f:
    f.write(src)
print("All done.")
