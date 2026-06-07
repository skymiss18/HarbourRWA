const fs = require('fs');
const file = 'e:/Repos/TheTuringTestHackathon2026/app/src/app/tokenize/page.tsx';
let c = fs.readFileSync(file, 'utf8');

// Add prospectus textarea after the TradeReceivable unit price block (before the submit button)
// Insert before: {!submittedToIntermediary ? (
const target = `          {!submittedToIntermediary ? (\n            <button onClick={() => { if (form.assetName && form.description) { void submitToSponsorInbox(); setSubmittedToIntermediary(true); } }}`; // exact match with \n (not \r\n)

const newTextarea = `          <div>\r\n\r\n            <label className="block text-xs font-medium text-slate-600 mb-2">Prospectus / Term Sheet <span className="text-slate-400 font-normal">(optional — for Intermediary compliance review)</span></label>\r\n\r\n            <textarea className={\`\${IC} resize-none\`} style={{ ...IS, height: "140px", fontFamily: "monospace", fontSize: "11px" }}\r\n\r\n              placeholder="Paste draft prospectus or term sheet text here. The Intermediary (Type 6 LC) will use this for AI compliance screening before submitting to SFC..."\r\n\r\n              value={form.prospectusText} onChange={(e) => upd("prospectusText", e.target.value)}\r\n\r\n              onFocus={(e) => (e.currentTarget.style.borderColor = "#1a56db")}\r\n\r\n              onBlur={(e)  => (e.currentTarget.style.borderColor = "rgba(0,0,0,0.12)")} />\r\n\r\n          </div>\r\n\r\n          {!submittedToIntermediary ? (\r\n            <button onClick={() => { if (form.assetName && form.description) { void submitToSponsorInbox(); setSubmittedToIntermediary(true); } }}`;

if (c.includes(target)) {
  c = c.replace(target, newTextarea);
  console.log('Prospectus textarea added to Step 1');
} else {
  console.log('ERROR: target not found');
  // Try to debug
  const idx = c.indexOf('!submittedToIntermediary');
  console.log('submittedToIntermediary found at:', idx);
}

fs.writeFileSync(file, c, 'utf8');
console.log('Done');
