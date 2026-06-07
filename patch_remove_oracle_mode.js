const fs = require('fs');
const file = 'e:/Repos/TheTuringTestHackathon2026/app/src/app/compliance/page.tsx';
let c = fs.readFileSync(file, 'utf8');

// 1. Remove mode state declaration
const modeState = `  const [mode,             setMode]             = useState<"check" | "submit">("check");\r\n`;
if (c.includes(modeState)) {
  c = c.replace(modeState, '');
  console.log('mode state removed');
} else {
  // Try without trailing newline
  const alt = `  const [mode,             setMode]             = useState<"check" | "submit">("check");`;
  const idx = c.indexOf(alt);
  if (idx >= 0) {
    // Remove the line including surrounding blank lines
    const before = c.lastIndexOf('\n', idx);
    const after = c.indexOf('\n', idx + alt.length);
    const afterEnd = c.indexOf('\n', after + 1); // skip next blank line
    c = c.slice(0, before + 1) + c.slice(afterEnd + 1);
    console.log('mode state removed (alt)');
  } else {
    console.log('WARNING: mode state not found');
  }
}

// 2. Always use check endpoint (remove mode-dependent endpoint selection)
const endpointLine = `        const endpoint = mode === "submit" ? "/api/compliance/submit" : "/api/compliance/check";\r\n`;
if (c.includes(endpointLine)) {
  c = c.replace(endpointLine, `        const endpoint = "/api/compliance/check";\r\n`);
  console.log('endpoint fixed');
} else {
  const alt2 = `        const endpoint = mode === "submit" ? "/api/compliance/submit" : "/api/compliance/check";`;
  if (c.includes(alt2)) {
    c = c.replace(alt2, `        const endpoint = "/api/compliance/check";`);
    console.log('endpoint fixed (alt)');
  } else {
    console.log('WARNING: endpoint line not found');
  }
}

// 3. Remove the entire Mode toggle UI block (from label "Mode" through closing </div>)
const modeBlock = `            <div>\r\n\r\n              <label className="block text-xs font-medium text-slate-600 mb-2">Mode</label>\r\n\r\n              <div className="flex rounded overflow-hidden" style={{ width: "fit-content", border: "1px solid rgba(0,0,0,0.10)" }}>\r\n\r\n                {[\r\n\r\n                  { v: "check",  l: "AI 合规复核（仅分析）"          },\r\n\r\n                  { v: "submit", l: "复核 + 写入 ComplianceOracle.sol" },\r\n\r\n                ].map((m, i) => (\r\n\r\n                  <button key={m.v} type="button" onClick={() => setMode(m.v as "check" | "submit")}\r\n\r\n                    className="px-4 py-2 text-xs transition-colors"\r\n\r\n                    style={{\r\n\r\n                      background: mode === m.v ? "#1d4ed8" : "#f3f1eb",\r\n\r\n                      color: mode === m.v ? "white" : "#6b8499",\r\n\r\n                      borderRight: i === 0 ? "1px solid rgba(0,0,0,0.10)" : "none",\r\n\r\n                    }}>\r\n\r\n                    {m.l}\r\n\r\n                  </button>\r\n\r\n                ))}\r\n\r\n              </div>\r\n\r\n            </div>`;

if (c.includes(modeBlock)) {
  c = c.replace(modeBlock, '');
  console.log('mode toggle UI removed');
} else {
  console.log('WARNING: mode toggle block not found as-is, trying indexOf...');
  const idx = c.indexOf('复核 + 写入 ComplianceOracle.sol');
  if (idx >= 0) console.log('Submit option still present at char', idx);
  else console.log('Submit option already gone');
}

// 4. Simplify button label - remove the mode-conditional part
const btnLabel = `            : mode === "submit" ? "运行 AI 合规复核 + 写入链上" : "运行 AI 合规复核"}`;
if (c.includes(btnLabel)) {
  c = c.replace(btnLabel, `            : "运行 AI 合规复核"}`);
  console.log('button label simplified');
} else {
  // Try with \r
  const btnLabelCRLF = `            : mode === "submit" ? "运行 AI 合规复核 + 写入链上" : "运行 AI 合规复核"}\r`;
  if (c.includes(btnLabelCRLF)) {
    c = c.replace(btnLabelCRLF, `            : "运行 AI 合规复核"}\r`);
    console.log('button label simplified (CRLF)');
  } else {
    console.log('WARNING: button label pattern not found');
    const idx = c.indexOf('写入链上');
    if (idx >= 0) {
      const lines = c.split('\n');
      let char = 0;
      for (let i = 0; i < lines.length; i++) {
        char += lines[i].length + 1;
        if (char > idx) { console.log('found at line', i+1, ':', JSON.stringify(lines[i])); break; }
      }
    }
  }
}

fs.writeFileSync(file, c, 'utf8');
console.log('Done');
