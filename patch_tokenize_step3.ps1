$f = "e:\Repos\TheTuringTestHackathon2026\app\src\app\tokenize\page.tsx"
$raw = [System.IO.File]::ReadAllText($f, [System.Text.Encoding]::UTF8)

# ── Replacement 1: Insert SFC useEffect before the prospectus useEffect ─────
$old1 = "  // Pre-fill prospectus text if navigated from /prospectus page`n  useEffect(() => {"
$new1 = @'
  // Fetch real SFC approval when entering Step 3
  useEffect(() => {
    if (step !== 3) return;
    setSfcLoading(true);
    setSfcApproval(null);
    fetch("/api/sfc-inbox")
      .then((r) => r.json())
      .then((data: { submissions: Record<string, unknown>[] }) => {
        const name = form.assetName.toLowerCase();
        const found =
          data.submissions.find(
            (s) =>
              s.status === "Approved" &&
              (name === "" || (s.asset as string).toLowerCase().includes(name))
          ) ?? null;
        setSfcApproval(found);
      })
      .catch(() => setSfcApproval(null))
      .finally(() => setSfcLoading(false));
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [step]);

  // Pre-fill prospectus text if navigated from /prospectus page
  useEffect(() => {
'@
$new1 = $new1.Replace("`r`n", "`n")

if ($raw.Contains($old1)) {
    $raw = $raw.Replace($old1, $new1)
    Write-Host "Replacement 1: OK"
} else {
    Write-Host "Replacement 1: NOT FOUND"
}

# ── Replacement 2: Replace hardcoded Step 3 SFC panel with dynamic version ──
$old2 = @'
          {/* SFC Approval panel */}
          <div className="rounded-lg p-4 space-y-3" style={{ background: "rgba(167,139,250,0.06)", border: "1px solid rgba(167,139,250,0.25)" }}>
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-bold text-violet-700 uppercase tracking-wide">SFC Issuance Authorisation</span>
              <span className="text-xs font-bold text-emerald-700">✓ APPROVED</span>
            </div>
            <div className="space-y-2 text-[11px]">
              {[
                ["Filed by",                 "Harbour Capital Markets Corp (Type 6 LC)"],
                ["Reference",               "SFC/RWA/2026/ISS-001"],
                ["Approved by",              "Ms. Wong Mei-Ling, SFC Senior Director"],
                ["Approval Date",            "20 May 2026"],
                ["Asset",                    form.assetName || "HIBT"],
                ["Authorised Total Supply",  `${Number(form.totalSupply).toLocaleString()} tokens`],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between gap-4">
                  <span className="text-slate-600 shrink-0">{k}</span>
                  <span className="font-mono text-violet-700 text-right">{v}</span>
                </div>
              ))}
            </div>
            <p className="text-[10px] text-slate-600 leading-relaxed pt-1" style={{ borderTop: "1px solid rgba(167,139,250,0.1)" }}>
              Authorised under SFO s.103 and the SFC Circular on Tokenisation of SFC-authorised Investment Products (November 2023). Subject to ongoing reporting obligations under SFO Part XII.
            </p>
          </div>
          <p className="text-xs text-slate-500">SFC authorisation received. Proceed to deploy the smart contracts on Mantle Network.</p>
          <div className="flex gap-3">
            <button onClick={() => setStep(2)} className="flex-1 py-2.5 text-sm text-slate-600 hover:text-slate-400 rounded-md transition-colors" style={{ border: "1px solid rgba(0,0,0,0.10)" }}>Back</button>
            <button onClick={() => setStep(4)} className="flex-1 py-2.5 text-sm font-semibold text-white rounded-md transition-opacity hover:opacity-90" style={{ background: "#1d4ed8" }}>
              Proceed to Deployment ...
            </button>
          </div>
'@
$old2 = $old2.Replace("`r`n", "`n")

$new2 = @'
          {/* SFC Approval panel */}
          {sfcLoading && (
            <div className="flex items-center gap-3 py-4">
              <div className="w-4 h-4 border-2 border-violet-500 border-t-transparent rounded-full animate-spin shrink-0" />
              <span className="text-xs text-slate-500">Checking SFC approval status...</span>
            </div>
          )}
          {!sfcLoading && sfcApproval && (
            <div className="rounded-lg p-4 space-y-3" style={{ background: "rgba(167,139,250,0.06)", border: "1px solid rgba(167,139,250,0.25)" }}>
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-violet-700 uppercase tracking-wide">SFC Issuance Authorisation</span>
                <span className="text-xs font-bold text-emerald-700">✓ APPROVED</span>
              </div>
              <div className="space-y-2 text-[11px]">
                {([
                  ["Filed by",               "Harbour Capital Markets Corp (Type 6 LC)"],
                  ["Reference",              sfcApproval.sfcRef as string ?? ""],
                  ["Approved by",            sfcApproval.approvedBy as string ?? ""],
                  ["Approval Date",          sfcApproval.approvedAt as string ?? ""],
                  ["Asset",                  sfcApproval.asset as string ?? form.assetName],
                  ["Authorised Total Supply", `${Number(form.totalSupply).toLocaleString()} tokens`],
                ] as [string, string][]).map(([k, v]) => (
                  <div key={k} className="flex justify-between gap-4">
                    <span className="text-slate-600 shrink-0">{k}</span>
                    <span className="font-mono text-violet-700 text-right">{v}</span>
                  </div>
                ))}
              </div>
              {sfcApproval.approvedTx && (
                <details className="group">
                  <summary className="cursor-pointer text-[10px] text-slate-600 hover:text-slate-400 transition-colors list-none select-none">
                    <span className="group-open:hidden">View on-chain approval record </span>
                    <span className="hidden group-open:inline">Hide </span>
                  </summary>
                  <div className="font-mono text-[10px] text-violet-700 mt-0.5 break-all">{sfcApproval.approvedTx as string}</div>
                </details>
              )}
              <p className="text-[10px] text-slate-600 leading-relaxed pt-1" style={{ borderTop: "1px solid rgba(167,139,250,0.1)" }}>
                Authorised under SFO s.103 and the SFC Circular on Tokenisation of SFC-authorised Investment Products (November 2023). Subject to ongoing reporting obligations under SFO Part XII.
              </p>
            </div>
          )}
          {!sfcLoading && !sfcApproval && (
            <div className="rounded-lg p-4 space-y-2" style={{ background: "rgba(245,158,11,0.06)", border: "1px solid rgba(245,158,11,0.25)" }}>
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-bold text-amber-700 uppercase tracking-wide">SFC Issuance Authorisation</span>
                <span className="text-xs font-bold text-amber-600">⏳ PENDING</span>
              </div>
              <p className="text-[11px] text-slate-600">
                No SFC approval has been issued for this asset yet. The SFC regulator must review and approve the issuance application before you can proceed to deployment.
              </p>
              <p className="text-[10px] text-slate-500">Submit your application via the Compliance &amp; Structuring step, then await SFC review on the regulator portal.</p>
            </div>
          )}
          <div className="flex gap-3">
            <button onClick={() => setStep(2)} className="flex-1 py-2.5 text-sm text-slate-600 hover:text-slate-400 rounded-md transition-colors" style={{ border: "1px solid rgba(0,0,0,0.10)" }}>Back</button>
            <button
              onClick={() => setStep(4)}
              disabled={!sfcApproval}
              className="flex-1 py-2.5 text-sm font-semibold text-white rounded-md transition-opacity hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed"
              style={{ background: "#1d4ed8" }}
            >
              Proceed to Deployment ...
            </button>
          </div>
'@
$new2 = $new2.Replace("`r`n", "`n")

if ($raw.Contains($old2)) {
    $raw = $raw.Replace($old2, $new2)
    Write-Host "Replacement 2: OK"
} else {
    Write-Host "Replacement 2: NOT FOUND - searching for snippet..."
    $snippet = "SFC authorisation received"
    $idx = $raw.IndexOf($snippet)
    if ($idx -ge 0) {
        Write-Host "Found '$snippet' at index $idx"
        $raw.Substring($idx - 50, 150)
    }
}

[System.IO.File]::WriteAllText($f, $raw, (New-Object System.Text.UTF8Encoding $false))
Write-Host "Done. Lines: $((Get-Content $f).Count)"
